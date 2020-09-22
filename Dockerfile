FROM docker:19.03

COPY . /

RUN chmod +x /run.sh

RUN apk add --update --no-cache \
    build-base \
    python3-dev \
    python3 \
    py3-pip \
    py3-setuptools \
    curl \
    gcc \
    libpq \
    py3-wheel
    
RUN pip3 install requests-html
RUN pip3 install wheel

ENTRYPOINT ["/run.sh"]
