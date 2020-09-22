FROM docker:19.03

COPY . /

RUN chmod +x /run.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    curl \
    gcc \
    libpq-dev \
    python3-dev \
    python3-wheel \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install requests-html
RUN pip3 install wheel

ENTRYPOINT ["/run.sh"]
