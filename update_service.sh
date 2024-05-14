#!/bin/bash

# sudo systemctl stop sonosd
# sudo systemctl restart sonosd
# sudo systemctl status sonosd

# journalctl -xe
# journalctl -u sonosd.service -e
# journalctl -u sonosd.service -f
# tail -f /var/log/bird_watching.log

# Define variables
SERVICE="sonosd"
SERVICE_FILE="sonosd.service"
SERVICE_PATH="/etc/systemd/system"

# Check if the service file exists
if [ -e "$SERVICE_FILE" ]; then
  sudo systemctl stop "$SERVICE"
  echo "Systemd daemon stopped"
  sudo systemctl disable "$SERVICE"
  echo "Service disabled to start on boot"

  # Copy the service file to the systemd directory, overwriting if it already exists
  sudo cp -f "$SERVICE_FILE" "$SERVICE_PATH/"
  echo "Service file overwritten successfully in $SERVICE_PATH"

  sudo systemctl daemon-reload
  echo "Systemd daemon reloaded"
  sudo systemctl enable "$SERVICE"
  echo "Service enabled to start on boot"
  sudo systemctl start "$SERVICE"
  echo "Systemd daemon started"
else
  echo "Service file '$SERVICE_FILE' not found in the current directory."
  exit 1
fi
