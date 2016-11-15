# AAISP to MQTT Service #

A script to publish [Andrews & Arnold / AAISP](http://aa.net.uk) broadband quota and sync rates to [MQTT](http://mqtt.org/).

It uses version 2 of AAISPs [CHAOS](https://support.aa.net.uk/CHAOS) API.

Useful for integrating and displaying AAISP line properties in home automation applications, such as [Home Assistant](https://home-assistant.io/) or [openHAB](http://www.openhab.org/).

![Workflow](https://raw.github.com/natm/aaisp-to-mqtt/master/docs/workflow.png)

## Usage ##

Create a config file, for example in /etc/aaisp-mqtt.conf, minimal viable with no MQTT authentication:

```
[aaisp]
username = aa@1
password = LongAccountPassword

[mqtt]
broker = 127.0.0.1
port = 1883
topic_prefix = aaisp
```

You can also optionally specify MQTT username and password:

```
[aaisp]
username = aa@1
password = LongAccountPassword

[mqtt]
broker = 127.0.0.1
port = 1883
username = aaisp-service
password = AnotherLongPassword
topic_prefix = aaisp
```

Run the service:

```
$ aaisp-to-mqtt.py /etc/aaisp-mqtt.conf
```

## Topics ##

Single account:

```
aaisp/$accounts                          gb12@a
aaisp/$lines                             32891
aaisp/$version                           0.1
aaisp/account/gb12@a/quota/remaining     3333889
aaisp/account/gb12@a/quota/monthly       10000000
aaisp/account/gb12@a/syncrate/down       7800000
aaisp/account/gb12@a/syncrate/up         1900000
aaisp/line/32891/quota/remaining         3333889
aaisp/line/32891/quota/monthly           10000000
aaisp/line/32891/syncrate/down           7800000
aaisp/line/32891/syncrate/up             1900000
```

For multiple accounts:

```
aaisp/$accounts                          el6@a.1,el6@a.2,gb12@a
aaisp/$lines                             37835,37964,32891
aaisp/$version                           0.1
aaisp/account/gb12@a/quota/remaining     3333889
aaisp/account/gb12@a/quota/monthly       10000000
aaisp/account/gb12@a/syncrate/down       7800000
aaisp/account/gb12@a/syncrate/up         1900000
aaisp/account/el6@a.1/quota/remaining    3333889
aaisp/account/el6@a.1/quota/monthly      10000000
aaisp/account/el6@a.1/syncrate/down      7400000
aaisp/account/el6@a.1/syncrate/up        1700000
aaisp/account/el6@a.2/quota/remaining    3333889
aaisp/account/el6@a.2/quota/monthly      10000000
aaisp/account/el6@a.2/syncrate/down      7300000
aaisp/account/el6@a.2/syncrate/up        1600000
aaisp/line/32891/quota/remaining         3333889
aaisp/line/32891/quota/monthly           10000000
aaisp/line/32891/syncrate/down           7800000
aaisp/line/32891/syncrate/up             1900000
aaisp/line/37835/quota/remaining         3333889
aaisp/line/37835/quota/monthly           10000000
aaisp/line/37835/syncrate/down           7300000
aaisp/line/37835/syncrate/up             1600000
aaisp/line/37964/quota/remaining         3333889
aaisp/line/37964/quota/monthly           10000000
aaisp/line/37964/syncrate/down           7400000
aaisp/line/37964/syncrate/up             1700000
```

## Setup ##

TODO
