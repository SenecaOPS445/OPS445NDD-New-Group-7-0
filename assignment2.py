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
        
def get_default_interface():
    """Finds and returns the first active network interface ."""
    try:
        # Runs the 'ip link show' to get list of interfaces
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines() #splits the output into individual lines
        #looping through each line one by one
        for line in lines:
            line = line.strip()
            if line and ':' in line:
                #here it splits the line by colon':' to extract the interface name 
                parts = line.split(':')
                if len(parts) >= 2:
                    interface = parts[1].strip()
                    #skipping the interface 'lo'
                    if interface != "lo":
                        return interface
    except subprocess.CalledProcessError: #if any error detects prints the error message and exits.
        print("Could not detect a valid network interface.")
        sys.exit(1)
        
def validate_ip(ip_address):
    """Validate the format of the provided IP address."""
    ip_address = ip_address.strip() #removes any extra whitespace
    parts = ip_address.split(".")
    #checks if there are exactly 4 parts
    if len(parts) != 4:
        return False

    for part in parts:
        #checks if the part is empty or contains non-numeric characters
        if not part or any(char not in '0123456789' for char in part):
            return False
        #checks if the number is between 0 and 255
        if int(part) < 0 or int(part) > 255:
            return False
    return True #returns true when IP is valid

def validate_interface(interface):
    """Check if the provided network interface exists and is valid."""
    try:
        #runs the 'ip link show' command to check the interface's status
        result = subprocess.run(['ip', 'link', 'show', interface], capture_output=True, text=True)
        
        #checks if the word 'state' appears in the result (indicating interface status)
        if 'state' in result.stdout:
            return True  # Interface exists and is valid
    except subprocess.CalledProcessError:
        # If there's an error (interface doesn't exist), return False
        return False
    return False
        
def changing_ip(ip_address, subnet_mask="24", interface=None):
    """Apply a new static IP address configuration"""
        
    #use the default interface if not provided
    if interface is None:
        interface = get_default_interface()
        
    # Combine IP and subnet
    cidr = f"{ip_address}/{subnet_mask}"

    try:
        # Remove current IP address from interface (optional, depending on use case)
        subprocess.run(['ip', 'addr', 'flush', 'dev', interface], check=True)

        # Assign new IP address
        subprocess.run(['ip', 'addr', 'add', cidr, 'dev', interface], check=True)

        # Bring the interface up
        subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)

        print(f"Successfully changed IP of {interface} to {cidr}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to apply static IP: {e}")
        sys.exit(1)
        
'''Creating a simple backup of /etc as a tar.gz file'''

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

    '''Creating an ArgumentParser object to handle command-line options like --show and --backup'''
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
        changing_ip(args.ip, args.subnet if args.subnet else "24")
        
    #In case of no args, it asks user if they want to change the IP to static
    if not any(vars(args).values()):
        change_ip = input("Do you want to change the IP to static? (yes/no): ").strip().lower()
        
        if change_ip == 'yes':
            #before asking for interface name it shows the current network configuration 
            get_network_config()
            
            #Ask for interface name and also validates the interface
            interface = input("Enterthe interface name (e.g. ens33, ens160): ").strip()
            if not validate_interface(interface):
                print(f"Invalid interface name: {interface}. Please provide a valid network interface.")
                sys.exit(1)
        
            #Asks for IP address and subnet also validate ip format 
            ip_address = input("Enter the new static IP address: ").strip()
            if not validate_ip(ip_address):
                print("Invalid IP address format. Please provide a valid IP address.")
                sys.exit(1)
            
            subnet_mask = input("Enter the subnet mask (default is 24): ").strip() or "24"
        
            #Backup before making changes
            backup_config()
        
            #Apply the provided static IP
            changing_ip(ip_address, subnet_mask, interface)
        
        else:
            print("No changes were made.")
        
       

