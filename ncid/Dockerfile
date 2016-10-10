FROM resin/rpi-raspbian:jessie-20160831
MAINTAINER Scott Evans <docker@scott.ee>

LABEL ncid_version="1.4.1" architecture="ARMv7"

# Data directory
# RUN mkdir /data

# Install dependencies
RUN apt-get update && sudo apt-get upgrade -y && apt-get install -y \
	libpcap0.8\* \
	wget \
	socat \
	retext \
	libconfig-simple-perl \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

RUN	wget http://downloads.sourceforge.net/project/ncid/ncid/1.4/ncid_1.4-1_armhf.deb
RUN dpkg -i ncid_1.4-1_armhf.deb

# Define working directory
#WORKDIR /data

#ENTRYPOINT ["/usr/sbin/"]
#CMD ["/bin/ncidd"]
# Avoid ERROR: invoke-rc.d: policy-rc.d denied execution of start.
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d

#ENTRYPOINT ["/usr/sbin/invoke-rc.d", "ncidd"]
#CMD ["start"]

CMD invoke-rc.d ncidd start && tail -f /dev/null
#tail -f /var/log/ncidd.log
