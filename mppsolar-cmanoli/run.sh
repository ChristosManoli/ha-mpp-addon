#!/usr/bin/env bash
set -e

# Wait for options file from Supervisor (max ~5s)
for i in {1..10}; do
  if [ -f /data/options.json ]; then break; fi
  sleep 0.5
done

exec python3 /voltronic_entry.py
