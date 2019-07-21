FROM balenalib/rpi-raspbian:buster
MAINTAINER Scott Evans <docker@scott.ee>

LABEL blinkt_version="0.0.1" architecture="ARMv7"

# Data directory
RUN mkdir /data

# Install dependencies
RUN apt-get update && apt-get install -y \
	git-core \
	build-essential \
	gcc \
	python \
	python-dev \
	python-pip \
	python-virtualenv \
	python-setuptools \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

RUN pip install rpi.gpio
RUN pip install paho-mqtt
RUN pip install simplejson
RUN pip install numpy
RUN pip install bitarray
RUN pip install blinkt

# Define working directory
WORKDIR /data

CMD ["python"]
