#!/usr/bin/env python3
import argparse
import sys
import json
import logging
import paho.mqtt.client as mqtt
from mppsolar import mppUtils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def publish_to_mqtt(broker, username, password, prefix, payload):
    """Publish inverter metrics to MQTT."""
    client = mqtt.Client()
    if username:
        client.username_pw_set(username, password)
    try:
        client.connect(broker)
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker {broker}: {e}")
        return

    for key, value in payload.items():
        topic = f"{prefix}/{key}"
        client.publish(topic, value, retain=True)
        logging.info(f"MQTT publish: {topic} = {value}")

    client.disconnect()

def get_inverter_data(port, protocol):
    """Fetch data from inverter using mppsolar library."""
    try:
        mpp = mppUtils()
        mpp.set_port(port)
        mpp.set_protocol(protocol)
        result = mpp.run_command("QPIGS")  # General status command
        return result.get("raw_response", {})
    except Exception as e:
        logging.error(f"Error reading inverter data: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="MPP Solar / Voltronic to MQTT bridge")
    parser.add_argument("--port", required=True, help="Inverter USB port (e.g., /dev/hidraw0)")
    parser.add_argument("--protocol", required=True, help="MPP Solar protocol (e.g., PI41)")
    parser.add_argument("--mqtt-broker", required=True, help="MQTT broker address")
    parser.add_argument("--mqtt-user", default="", help="MQTT username")
    parser.add_argument("--mqtt-pass", default="", help="MQTT password")
    parser.add_argument("--mqtt-prefix", default="inverter", help="MQTT topic prefix")
    args = parser.parse_args()

    data = get_inverter_data(args.port, args.protocol)

    if not data:
        logging.warning("No data retrieved from inverter.")
        sys.exit(1)

    # Try to convert raw response to JSON metrics if possible
    if isinstance(data, dict):
        payload = data
    else:
        try:
            payload = json.loads(data)
        except Exception:
            payload = {"raw": str(data)}

    publish_to_mqtt(
        args.mqtt_broker,
        args.mqtt_user,
        args.mqtt_pass,
        args.mqtt_prefix,
        payload
    )

if __name__ == "__main__":
    main()
