FROM alpine:3.12

COPY . /

RUN ls -R

ENTRYPOINT ["run.sh"]
