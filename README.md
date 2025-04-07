# Winter 2025 Assignment 2

## Group Information

Hi, this is **Group 7**, with three members:
    -Manik Shrestha
    -Samir Shrestha
    -Tanuj Gupta

# Title: Network Configuration and Subnetting

This is a Python-based project which focuses on configuring and analyzing network settings, validating subnets, and assisting with IP allocation on a Linux Machine. It is designed for use in virtual environments where users may want to inspect, modify, or back up networking settings through a script.

## Objectives

The script will:
- Display the current network configuration
- Allow the user to apply changes like setting a static IP address
- Validate the given IP address
- Back up configuration files or system folders
- Ensure the Python script initiates backup automatically before making any changes

---

## Input Collection

Inputs will be collected through command-line arguments using `argparse`.  
The expected inputs include:
- `--show` → View current network configuration
- `--ip` → Provide a new static IP address
- `--subnet` → Provide a subnet mask (optional)
- `--backup` → Create a backup before any change

---

##  Features Based on Project Discussion

As outlined in our meeting with the professor, here are the prioritized features:

1.  Show us the current config  
2.  Allow the user to change config (e.g., set static IP)  
3.  Validate the IP address that they give    
4.  Make sure to back up the virtual machine  
5.  Make sure your Python script creates the backup  

---

##  Output and Functionality

The script will:
- Display details in terminal
- Create `.tar.gz` backup archives in a `/backups` folder
- Log actions (optional)
- Safely apply IP changes via command-line networking tools (like `ip` or `nmcli`)

---

##  Testing & Compatibility

This script is built to run on:
- Matrix Server
- MyVMLab
- Personal Linux VM (Ubuntu/Debian-based)

It does **not** rely on third-party modules. Only standard Python libraries such as:
- `argparse`
- `subprocess`
- `os`
- `datetime`
- `shutil`

---

## Root Privileges Required
This script requires superuser (root) privileges to execute properly. It performs system-level operations such as reading and modifying network configurations, validating IP settings, and backing up system files.

To ensure these operations succeed without permission issues, the script must be run with sudo.

If the script is not executed with the required privileges, it will display an error and exit.
# example usage:
     sudo python3 ./assignment2.py

##  Git Usage & Collaboration

- All members contribute through personal branches (`manik`, `samir`, `tgupta25`)
- Merges into `main` are only allowed via Pull Requests
- Git commits use each member’s `myseneca.ca` email for grading

---
