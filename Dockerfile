FROM alpine:3.12

COPY . /

ENTRYPOINT ["/run.sh"]
