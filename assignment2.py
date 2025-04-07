#!/usr/bin/env python3

import subprocess
import sys
import os

def root_check():
    """asks user to be a root to run the script"""
    if os.geteuid() != 0: #Checks if the script is run as a root.
        print("The script must be run only with superuser previligiess. Use 'sudo' to run it.")
        sys.exit(1)


def get_network_config():
    """ Display the current network configuration."""
    try: 
        #runs 'ip a' command to get network interface details 
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
        #Incase of 'ip a' command fails
        print(f"Error fetching network configuration")
        sys.exit(1)


import shutil
from datetime import datetime


if __name__ == "__main__":
    root_check()
    get_network_config()
