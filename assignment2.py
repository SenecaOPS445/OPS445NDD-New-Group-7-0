#!/usr/bin/env python3

import subprocess
import sys

def get_network_config():
    """ Display the current network configuration."""
    try:
        result = subprocess.run(['ip', 'a'], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("Error fetching network config.")
        sys.exit(1)



if __name__ == "__main__":
    get_network_config()
