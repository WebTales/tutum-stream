FROM gliderlabs/alpine:3.1

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    apt-get install -y --no-install-recommends python-pip && \
    apt-get clean && \
    pip install python-tutum==0.16.21 && \
    rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app

CMD ["/usr/bin/python", "client.py"]
