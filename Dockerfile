FROM ubuntu:18.04

COPY . /

RUN chmod +x /run.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    curl \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN curl -fsSL https://get.docker.com -o get-docker.sh
RUN sh get-docker.sh
    
RUN pip3 install requests-html

ENTRYPOINT ["/run.sh"]
