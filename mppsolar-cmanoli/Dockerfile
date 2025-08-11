FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mpp-solar paho-mqtt

COPY run.sh /run.sh
COPY voltronic_entry.py /voltronic_entry.py
RUN chmod +x /run.sh

VOLUME ["/data"]

CMD ["/run.sh"]
