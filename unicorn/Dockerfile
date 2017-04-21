FROM resin/rpi-raspbian:jessie
MAINTAINER Scott Evans <docker@scott.ee>

LABEL unicorn_version="0.0.2" architecture="ARMv7"

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


WORKDIR /root/
RUN git clone https://github.com/pimoroni/unicorn-hat
WORKDIR /root/unicorn-hat/library/rpi-ws281x
RUN python setup.py install
WORKDIR /root/unicorn-hat/library/UnicornHat
RUN python setup.py install

RUN pip install rpi.gpio
RUN pip install paho-mqtt
#RUN pip install rpi-ws281x
#RUN pip install unicornhat
RUN pip install simplejson
RUN pip install numpy
RUN pip install bitarray

# Define working directory
WORKDIR /data

CMD ["python"]
