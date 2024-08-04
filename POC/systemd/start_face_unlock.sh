#!/bin/bash

# Log everything to the log file
exec >> /home/luky/playground/face_recognition_unlock/POC/systemd/logs/face_unlock.log 2>&1

echo "Starting face unlock service..."

# Wait for gnome-session to start
while true; do
    PID=$(pgrep -u $LOGNAME gnome-session | head -n 1)
    if [ -n "$PID" ]; then
        break
    fi
    echo "gnome-session not found for user $LOGNAME"
    sleep 5
done

echo "Found gnome-session PID: $PID"

# Extract the DBUS_SESSION_BUS_ADDRESS
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ | tr -d '\0' | cut -d= -f2-)
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    echo "Failed to get DBUS_SESSION_BUS_ADDRESS from PID $PID"
    exit 1
fi

echo "DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS"

# Activate the virtual environment and run the Python script
source /home/luky/playground/face_recognition_unlock/venv/bin/activate
python3 /home/luky/playground/face_recognition_unlock/POC/main.py
