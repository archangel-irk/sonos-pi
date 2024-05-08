#!/bin/bash

# Check if the number of arguments provided is not equal to 1
if [ $# -ne 1 ]; then
    echo "Usage: $0 <task>"
    exit 1
fi

# Store the argument in a variable named task
action="$1"

# sudo systemctl start sonosd
# sudo systemctl stop sonosd
# sudo systemctl restart sonosd
# sudo systemctl status sonosd

# Run the systemctl command with sudo and the provided action
sudo systemctl "$action" sonosd

