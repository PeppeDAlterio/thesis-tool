FROM ubuntu:18.04

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
    
RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sh get-docker.sh
    
RUN pip3 install requests-html
RUN pip3 install wheel

ENTRYPOINT ["/run.sh"]
