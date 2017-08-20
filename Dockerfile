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
    && apk del .build-deps \
    && addgroup -g 1000 aaisp \
    && adduser -u 1000 -G aaisp -s /bin/sh -D aaisp \
    && chown aaisp:aaisp -R /app

EXPOSE 8080/tcp
USER aaisp
CMD ["python", "aaisp-to-mqtt.py", "config.cfg"]
