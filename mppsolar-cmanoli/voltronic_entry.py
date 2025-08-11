#!/usr/bin/env python3
import json, os, sys, shlex

opts_path = '/data/options.json'
if not os.path.exists(opts_path):
    print('ERROR: /data/options.json not found. Exiting.', file=sys.stderr)
    sys.exit(1)

with open(opts_path) as f:
    opts = json.load(f)

port = opts.get('port', '/dev/hidraw0')
protocol = opts.get('protocol', 'PI41')
broker = opts.get('mqtt_broker', '127.0.0.1')
user = opts.get('mqtt_user', '')
passwd = opts.get('mqtt_pass', '')
prefix = opts.get('mqtt_prefix', 'inverter')
interval = str(opts.get('interval', 30))

# Build MQTT URI
if user:
    mqtt_uri = f"mqtt://{user}:{passwd}@{broker}:1883"
else:
    mqtt_uri = f"mqtt://{broker}:1883"

cmd = [
    'mpp-solar',
    '-p', port,
    '-P', protocol,
    '-o', 'mqtt',
    '-q', mqtt_uri,
    '--prefix', prefix,
    '-i', interval
]

print('Running:', ' '.join(shlex.quote(c) for c in cmd))
os.execvp('mpp-solar', cmd)
