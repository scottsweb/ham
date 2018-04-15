FROM nodered/node-red-docker:rpi
MAINTAINER Scott Evans <docker@scott.ee>

LABEL nodered_version="0.18.4" description="Node-RED with Bluetooth"

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
	bluetooth \
	bluez \
	libbluetooth-dev \
	libudev-dev \
	libpcap-dev \
	build-essential bluez-tools \
	bc

RUN usermod -a -G bluetooth node-red && \
	setcap cap_net_raw+eip /usr/local/bin/node

RUN npm install --quiet \
	noble \
	node-red-contrib-bean \
	node-red-contrib-kodi \
	node-red-contrib-plex \
	node-red-contrib-moment \
	node-red-contrib-particle \
	node-red-contrib-home-assistant \
	node-red-node-emoncms \
	node-red-node-pushbullet \
	node-red-contrib-ifttt \
	node-red-contrib-botmaster \
	node-red-contrib-throttle \
	node-red-node-irc \
	node-red-contrib-gzip \
	Neonox31/node-red-contrib-amazondash#improvements

ADD textcleaner /usr/local/bin
RUN chmod +x /usr/local/bin/textcleaner

EXPOSE 1880
