FROM alpine:3.8
EXPOSE 80 8080 443
ENV LISTEN_ADDR 0.0.0.0:8080
RUN apk --no-cache add ca-certificates tzdata
ADD miniflux /usr/local/bin/miniflux
USER nobody
CMD ["/usr/local/bin/miniflux"]