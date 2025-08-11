# Build argument for Home Assistant base image (multi-arch support)
ARG BUILD_FROM=ghcr.io/hassio-addons/base:14.2.1
FROM ${BUILD_FROM}

# Set environment to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apk add --no-cache \
        build-base \
        libusb \
        libusb-dev \
        python3 \
        py3-pip

# Install Python dependencies
RUN pip3 install --no-cache-dir \
        mpp-solar \
        paho-mqtt

# Copy add-on files
COPY run.sh /run.sh
COPY voltronic_entry.py /voltronic_entry.py

# Ensure scripts are executable
RUN chmod a+x /run.sh /voltronic_entry.py

# Map /data for HA add-on options
VOLUME ["/data"]

# s6-overlay handles the startup, so no CMD override is needed
