#!/bin/bash

# Script to install htop on Amazon Linux
# Create log file
LOG_FILE="/var/log/htop_installation.log"
touch $LOG_FILE

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_message "Error: This script must be run as root"
    exit 1
fi

# Check if htop is already installed
if command -v htop >/dev/null 2>&1; then
    log_message "htop is already installed"
    exit 0
fi

# Install htop
log_message "Starting htop installation..."

if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$VERSION_ID" == "2" ]]; then
        # Amazon Linux 2
        yum update -y
        yum install -y htop
    else
        # Amazon Linux 2023
        dnf update -y
        dnf install -y htop
    fi
fi

# Verify installation
if command -v htop >/dev/null 2>&1; then
    log_message "htop installed successfully"
    htop --version | tee -a $LOG_FILE
else
    log_message "Error: htop installation failed"
    exit 1
fi