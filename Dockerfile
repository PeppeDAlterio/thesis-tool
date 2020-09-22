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
    py3-wheel \
    libxml2 \
    libxml2-dev \
    py3-libxml2 \
    libxslt \
    libxslt-dev
    
RUN pip3 install libxml2-python3
RUN pip3 install requests-html
RUN pip3 install wheel

ENTRYPOINT ["/run.sh"]
