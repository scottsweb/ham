FROM resin/rpi-raspbian:jessie
MAINTAINER Resilio Inc. <support@resilio.com>
LABEL com.resilio.version="2.5.5"

ADD https://download-cdn.resilio.com/stable/linux-armhf/resilio-sync_armhf.tar.gz /tmp/sync.tgz
RUN tar -xf /tmp/sync.tgz -C /usr/bin rslsync && rm -f /tmp/sync.tgz

COPY sync.conf.default /etc/
COPY run_sync /usr/bin/

EXPOSE 8888
EXPOSE 55555

VOLUME /mnt/sync

ENTRYPOINT ["run_sync"]
CMD ["--config", "/mnt/sync/sync.conf"]
