FROM djdefi/rpi-alpine

RUN apk update && \
apk upgrade && \
apk add build-base py-pip python-dev openssl-dev swig libusb && \
rm -rf /var/cache/apk/*

COPY requirements.txt /

RUN pip install -r /requirements.txt 

RUN pip install firetv[firetv-server]

VOLUME /config

CMD ["firetv-server", "-c", "config/devices.yaml"]