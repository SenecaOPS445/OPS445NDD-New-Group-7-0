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


def changing_ip():
    '''work here for the function that helps in changing the ip configuration'''

'''Creating a simple backup of /etc as a tar.gz file'''

import os
import shutil
import time

def backup_config():

    '''creating a timestamp for backup file.'''
    backup_name = f"backup_{time.strftime('%Y%m%d_%H%M%S')}.tar.gz" 

    '''Making sure the backups/ folder do exist'''
    if not os.path.exists ("backups"):
        os.mkdir("backups")
    
    '''Creating the backup inside backups/ folder'''
    try:
        shutil.make_archive(f"backups/{backup_name.replace('.tar.gz','')}", 'gztar','/etc')
        print(f"Backup created in backups/{backup_name}")
    except Exception as e:
        print(f"Backup failed {e}")

import argparse

if __name__ == "__main__":

    root_check()

    '''Creatin an ArgumentParser object to handle command-line options like --show and --backup'''
    parser = argparse.ArgumentParser(description="Network configuration and Backup tool")

    '''Adding --show option: If it is used, it will trigger the function to display network config'''
    parser.add_argument('--show', action='store_true', help="Show current network configuration")

    '''Adding --backup option: If it is used, it will trigger the function to back up /etc'''
    parser.add_argument('--backup', action='store_true', help="Create a backup of the system config")

    '''Adding --ip and --subnet: If it is used it will trigger the function to change ip and subnet'''
    parser.add_argument('--ip', type=str, help="Provide a new static IP address")
    parser.add_argument('--subnet', type=str, help="Provide a subnet mask (optional)")


    '''Parsing the arguments provided when the script is to be ran'''
    args = parser.parse_args()

    '''Callin network config function'''
    if args.show:
        get_network_config()

    '''Calling the backup function'''
    if args.backup:
        backup_config()

    '''If changing the ip, back up first'''
    if args.ip or args.subnet:
        backup_config()
        
        # Placeholder — add static IP logic here later

