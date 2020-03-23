# Based on https://github.com/MycroftAI/docker-mycroft
FROM arm32v7/ubuntu:eoan

ENV VERSION 19.2.14
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
ENV IS_TRAVIS true

# Install Server Dependencies for Mycroft
RUN set -x \
	&& sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get -y install git python3 python3-pip locales espeak sudo alsa-base alsa-utils pulseaudio pulseaudio-utils nano libasound2-plugins ca-certificates \
	&& pip3 install --upgrade setuptools \
	&& pip3 install future msm \
	&& pip3 install pulsemixer

# Checkout Mycroft
RUN git clone https://github.com/MycroftAI/mycroft-core.git /opt/mycroft \
	&& cd /opt/mycroft \
	&& git fetch && git checkout master \
	&& mkdir /opt/mycroft/skills \
	&& CI=true /opt/mycroft/./dev_setup.sh --allow-root -sm

# Manually install mimic as we skip it in dev_setup due to IS_TRAVIS
RUN cd /opt/mycroft && scripts/./install-mimic.sh 1 --allow-root

RUN mkdir /opt/mycroft/scripts/logs \
	&& touch /opt/mycroft/scripts/logs/mycroft-bus.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-voice.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-skills.log \
	&& touch /opt/mycroft/scripts/logs/mycroft-audio.log \
	&& apt-get -y remove pulseaudio \
	&& apt-get -y autoremove \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /opt/mycroft
COPY startup.sh /opt/mycroft

# Ensure output goes to pulseaudio
COPY asoundrc /root/.asoundrc

ENV PYTHONPATH $PYTHONPATH:/mycroft/ai

RUN /bin/bash -c "source /opt/mycroft/.venv/bin/activate" \
	chmod +x /opt/mycroft/start-mycroft.sh \
	&& chmod +x /opt/mycroft/startup.sh \
	&& /bin/bash /opt/mycroft/start-mycroft.sh all

EXPOSE 8181

ENTRYPOINT ["/bin/bash", "-c", "rm /.dockerenv; exec /opt/mycroft/startup.sh"]
