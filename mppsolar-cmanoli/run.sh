#!/usr/bin/with-contenv bashio
# =====================================================================
# MPP Solar / Voltronic to MQTT bridge startup script
# Reads HA add-on config and runs voltronic_entry.py
# =====================================================================

# Read options from Home Assistant
PORT=$(bashio::config 'port')
PROTOCOL=$(bashio::config 'protocol')
MQTT_BROKER=$(bashio::config 'mqtt_broker')
MQTT_USER=$(bashio::config 'mqtt_user')
MQTT_PASS=$(bashio::config 'mqtt_pass')
MQTT_PREFIX=$(bashio::config 'mqtt_prefix')
INTERVAL=$(bashio::config 'interval')

bashio::log.info "Starting MPP Solar / Voltronic to MQTT bridge..."
bashio::log.info "Using device: ${PORT} (protocol ${PROTOCOL})"
bashio::log.info "MQTT broker: ${MQTT_BROKER} (prefix: ${MQTT_PREFIX})"
bashio::log.info "Polling interval: ${INTERVAL}s"

# Main loop
while true; do
    python3 /voltronic_entry.py \
        --port "${PORT}" \
        --protocol "${PROTOCOL}" \
        --mqtt-broker "${MQTT_BROKER}" \
        --mqtt-user "${MQTT_USER}" \
        --mqtt-pass "${MQTT_PASS}" \
        --mqtt-prefix "${MQTT_PREFIX}"

    sleep "${INTERVAL}"
done
