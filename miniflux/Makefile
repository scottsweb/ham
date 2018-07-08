.PHONY: image push all

image:
	@ docker build -t miniflux/miniflux:${version} .

push:
	@ docker push miniflux/miniflux:${version}

all:
	image push
