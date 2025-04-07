#!/usr/bin/env python3
<<<<<<< HEAD

import subprocess
import sys

def get_network_config():
    """ Display the current network configuration."""
    try:
        result = subprocess.run(['ip', 'a'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()

        print("Current Network Configuration:")
        interface = None
        displayed_interfaces = set()

        for line in lines:
            if line.startswith(' '): #IP address lines
                if 'inet ' in line:
                    ip = line.split()[1].split('/')[0]
                    print(f"Interface: {interface}, IP Address: {ip}")
                    displayed_interfaces.add(interface)
            else:
                interface = line.split()[1].strip(':')
                if interface not in displayed_interfaces:
                    print(f"Interface: {interface}, IP Address: None") #shows interfaces with no IP


    except subprocess.CalledProcessError:
        print(f"Error fetching network configuration")
        sys.exit(1)

import os
import shutil
from datetime import datetime


if __name__ == "__main__":
    get_network_config()
=======
>>>>>>> main
