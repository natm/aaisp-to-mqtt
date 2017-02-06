FROM phusion/baseimage:0.9.19
MAINTAINER Nat Morris "nat@nuqe.net"

COPY aaisp-to-mqtt.py /usr/local/bin/aaisp-to-mqtt.py

RUN apt-get update
RUN apt-get install -y python-pip python-dev libffi-dev libssl-dev
ADD requirements.txt /tmp
RUN pip install --upgrade -r /tmp/requirements.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
