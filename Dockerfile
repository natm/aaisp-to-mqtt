FROM alpine:3.6
MAINTAINER Nat Morris <nat@nuqe.net>

COPY requirements.txt /app/
COPY aaisp-to-mqtt.py /app/
WORKDIR /app

RUN apk add --no-cache \
        python \
        ca-certificates \
    && apk add --no-cache --virtual .build-deps \
        py-pip \
    && pip install -r requirements.txt \
    && apk del --no-cache .build-deps \
    && addgroup -g 1000 aaisp \
    && adduser -u 1000 -G aaisp -s /bin/sh -D aaisp \
    && chown aaisp:aaisp -R /app \
    && echo "0 * * * * /usr/bin/python /app/aaisp-to-mqtt.py /app/config.cfg" | crontab -u aaisp -

EXPOSE 8080/tcp
CMD ["/usr/sbin/crond", "-f", "-d", "8"]
