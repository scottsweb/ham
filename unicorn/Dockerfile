FROM resin/rpi-raspbian:jessie
MAINTAINER Scott Evans <docker@scott.ee>

LABEL unicorn_version="0.0.1" architecture="ARMv7"

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
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

RUN pip install paho-mqtt
RUN pip install unicornhat
RUN pip install simplejson
RUN pip install numpy
RUN pip install bitarray

# Define working directory
WORKDIR /data

CMD ["python"]