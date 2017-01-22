FROM nodered/node-red-docker:rpi
MAINTAINER Scott Evans <docker@scott.ee>

LABEL nodered_version="0.16.1" description="Node-RED with Bluetooth"

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
	bluetooth \
	bluez \
	libbluetooth-dev \
	libudev-dev \
	build-essential bluez-tools

RUN usermod -a -G bluetooth node-red && \
	setcap cap_net_raw+eip /usr/local/bin/node

USER node-red

RUN npm install --quiet \
	noble \
	node-red-contrib-bean \
	node-red-contrib-bean \
	node-red-contrib-kodi \
	node-red-contrib-moment \
	node-red-contrib-particle \
	node-red-node-emoncms \
	node-red-node-pushbullet \
	node-red-contrib-ifttt

EXPOSE 1880
