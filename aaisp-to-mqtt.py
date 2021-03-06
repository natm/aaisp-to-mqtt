#!/usr/bin/env python

import sys
import logging
import json
import urllib
import time
import configparser
import paho.mqtt.client as mqtt
import humanfriendly

LOG = logging.getLogger(__name__)
VERSION = 0.1


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)8s [%(asctime)s] %(message)s')

    if len(sys.argv) != 2:
        LOG.fatal("Config file not supplied")
        sys.exit(1)
    cfgfile = sys.argv[1]
    # load the config
    config = configparser.ConfigParser()
    config.read(cfgfile)

    # check it has the correct sections
    for section in ["aaisp", "mqtt"]:
        if section not in config.sections():
            LOG.fatal("%s section not found in config file %s", section, cfgfile)

    aaisp_username = config.get("aaisp", "username")
    aaisp_password = config.get("aaisp", "password")

    # attempt to get details from aaisp
    LOG.info("Connecting to AAISP CHAOSv2 endpoint")
    post_params = "control_login=%s&control_password=%s" % (aaisp_username, aaisp_password)
    url = "https://chaos2.aa.net.uk/broadband/info"
    response = urllib.urlopen(url, data=post_params)
    data = json.loads(response.read())
    if "info" not in data:
        LOG.fatal("info section not found in AAISP CHAOSv2 response")
        sys.exit(1)
    circuits = data["info"]
    LOG.info("Got %s circuits", len(circuits))
    if len(circuits) == 0:
        LOG.fatal("No circuits returned from AAISP CHAOSv2")

    # work out unique line IDs and logins
    logins = []
    lines = []
    for circuit in circuits:
        if circuit["login"] not in logins:
            logins.append(circuit["login"])
        if circuit["ID"] not in lines:
            lines.append(circuit["ID"])
    LOG.info("* Lines: %s", ', '.join(lines))
    LOG.info("* Logins: %s", ', '.join(logins))


    # get MQTT config
    mqtt_broker = config.get("mqtt", "broker")
    mqtt_port = int(config.get("mqtt", "port"))
    mqtt_username = config.get("mqtt", "username")
    mqtt_password = config.get("mqtt", "password")
    mqtt_topic_prefix = config.get("mqtt", "topic_prefix")
    # connect to the broker
    LOG.info("Connecting to MQTT broker %s:%s", mqtt_broker, mqtt_port)
    client = mqtt.Client()
    # do auth?
    if mqtt_username is not None and mqtt_password is not None:
        client.username_pw_set(mqtt_username, mqtt_password)
    client.max_inflight_messages_set(100)
    client.connect(mqtt_broker, mqtt_port, 60)
    LOG.info("Connected OK to MQTT")

    # version and indexes
    publish(client=client, topic="%s/$version" % (mqtt_topic_prefix), payload=VERSION)
    publish(client=client, topic="%s/$lines" % (mqtt_topic_prefix), payload=','.join(lines))
    publish(client=client, topic="%s/$logins" % (mqtt_topic_prefix), payload=','.join(logins))
    LOG.info("Published version and index messages")

    # publish per circuit
    for circuit in circuits:
        publish_per_circuit(client=client, circuit=circuit, mqtt_topic_prefix=mqtt_topic_prefix)
    LOG.info("Published details for %s circuits", len(circuits))
    # disconnect
    LOG.info("Disconnecting from MQTT")
    client.disconnect()


    sys.exit(0)

def publish_per_circuit(client, circuit, mqtt_topic_prefix):
    quota_remaining = int(circuit["quota_remaining"])
    quota_remaining_gb = quota_remaining / 1000000000
    quota_monthly = int(circuit["quota_monthly"])
    quota_monthly_gb = quota_monthly / 1000000000
    up = float(circuit["rx_rate"])
    up_mb = round(up / 1000000, 2)
    down = float(circuit["tx_rate"])
    down_mb = round(down / 1000000, 2)

    # line_prefix = "%s/line/%s" % (mqtt_topic_prefix, circuit["ID"])
    login_prefix = "%s/login/%s" % (mqtt_topic_prefix, circuit["login"])
    for prefix in [login_prefix]:  # , line_prefix]:
        for metric in [
            ("quota/remaining", quota_remaining),
            ("quota/remaining/gb", quota_remaining_gb),
            ("quota/remaining/human", humanfriendly.format_size(quota_remaining)),
            ("quota/monthly", quota_monthly),
            ("quota/monthly/gb", quota_monthly_gb),
            ("quota/monthly/human", humanfriendly.format_size(quota_monthly)),
            ("syncrate/up", up),
            ("syncrate/up/mb", up_mb),
            ("syncrate/up/human", humanfriendly.format_size(up)),
            ("syncrate/down", down),
            ("syncrate/down/mb", down_mb),
            ("syncrate/down/human", humanfriendly.format_size(down)),
            ("postcode", str(circuit["postcode"].strip()))
        ]:
            topic = "%s/%s" % (prefix, metric[0])
            publish(client=client, topic=topic, payload=metric[1])
    return

def publish(client, topic, payload):
    time.sleep(0.1)
    result = client.publish(topic=topic, payload=payload, qos=1)
    if result[0] != 0:
        LOG.fail("MQTT publish failure: %s %s" , topic, payload)

if __name__ == "__main__":
    main()
