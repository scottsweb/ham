FROM resin/rpi-raspbian:jessie
MAINTAINER Scott Evans <docker@scott.ee>

LABEL caddy_version="0.9.4" architecture="ARMv7"

ARG plugins=git,ipfilter,ratelimit,cloudflare,digitalocean

# install deps
RUN apt-get update && \
	apt-get install -y curl git-core libpcap-dev && \
	rm -rf /var/lib/apt/lists/*

# download caddy
RUN curl --silent --show-error --fail --location \
		--header "Accept: application/tar+gzip, application/x-gzip, application/octet-stream" -o - \
		"https://caddyserver.com/download/build?os=linux&arch=arm&features=${plugins}" \
		| tar --no-same-owner -C /usr/bin/ -xz caddy \
	&& chmod 0755 /usr/bin/caddy \
	&& setcap cap_net_bind_service=+ep /usr/bin/caddy \
	&& /usr/bin/caddy -version

EXPOSE 80 443

WORKDIR /srv

CMD caddy

ENTRYPOINT ["/usr/bin/caddy"]
CMD ["--conf", "/etc/Caddyfile"]