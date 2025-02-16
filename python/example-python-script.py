#!/usr/bin/env python3

import subprocess
import os
import sys
import logging
from datetime import datetime
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/nginx_installation.log'),
        logging.StreamHandler()
    ]
)

def run_command(command):
    """Execute shell command and return output"""
    try:
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_root():
    """Check if script is running as root"""
    if os.geteuid() != 0:
        logging.error("This script must be run as root")
        sys.exit(1)

def check_nginx_installed():
    """Check if nginx is already installed"""
    success, output = run_command("which nginx")
    return success

def get_amazon_linux_version():
    """Detect Amazon Linux version"""
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('VERSION_ID='):
                    version = line.split('=')[1].strip('"').strip()
                    return version
    except FileNotFoundError:
        logging.error("Could not determine Amazon Linux version")
        sys.exit(1)

def install_nginx():
    """Install Nginx based on Amazon Linux version"""
    version = get_amazon_linux_version()
    
    if version == "2":
        # Amazon Linux 2
        commands = [
            "amazon-linux-extras enable nginx1",
            "yum clean metadata",
            "yum -y install nginx"
        ]
    else:
        # Amazon Linux 2023
        commands = [
            "dnf update -y",
            "dnf install nginx -y"
        ]
    
    for command in commands:
        success, output = run_command(command)
        if not success:
            logging.error(f"Failed to execute: {command}")
            logging.error(output)
            sys.exit(1)
        logging.info(f"Successfully executed: {command}")

def configure_nginx():
    """Configure and start Nginx service"""
    commands = [
        "systemctl start nginx",
        "systemctl enable nginx",
        "systemctl status nginx"
    ]
    
    for command in commands:
        success, output = run_command(command)
        if not success:
            logging.error(f"Failed to execute: {command}")
            logging.error(output)
            sys.exit(1)
        logging.info(f"Successfully executed: {command}")

def main():
    """Main installation process"""
    logging.info("Starting Nginx installation script")
    
    # Check if running as root
    check_root()
    
    # Check if nginx is already installed
    if check_nginx_installed():
        logging.info("Nginx is already installed")
        sys.exit(0)
    
    # Install nginx
    logging.info("Installing Nginx...")
    install_nginx()
    
    # Configure and start nginx
    logging.info("Configuring Nginx...")
    configure_nginx()
    
    # Verify installation
    success, nginx_version = run_command("nginx -v")
    if success:
        logging.info("Nginx installation completed successfully")
        logging.info(f"Nginx version: {nginx_version}")
    else:
        logging.error("Failed to verify Nginx installation")
        sys.exit(1)

if __name__ == "__main__":
    main()