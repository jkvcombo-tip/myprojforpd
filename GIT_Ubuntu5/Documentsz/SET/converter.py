import subprocess
import csv
import os
from configparser import ConfigParser

def get_ssh_username_and_ip(host_entry):
    # Split the host entry into key-value pairs
    host_info = dict(kv.split('=') for kv in host_entry.split(','))
    
    # Extract the ansible_host value
    ansible_host = host_info.get('ansible_host', '').strip()

    # Use the IP address as the username for simplicity
    username = ansible_host.split('.')[-1]

    return username, ansible_host

def ssh_and_get_syslog(username, ip_address, command):
    try:
        # Use subprocess to execute ssh command and capture output
        ssh_command = f"ssh {username}@{ip_address} {command}"
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True, check=True)

        # Return the stdout (syslog content)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving syslog from {ip_address}: {e}")
        return None

def save_syslog_to_csv(ip_address, syslog_content, output_folder):
    try:
        # Create the CSV file with the IP address as the filename
        csv_filename = os.path.join(output_folder, f"{ip_address}.csv")
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the syslog content to the CSV file
            writer.writerow(["Syslog Content"])
            writer.writerow([syslog_content])
        print(f"Syslog from {ip_address} saved to {csv_filename}")
    except Exception as e:
        print(f"Error saving syslog to CSV for {ip_address}: {e}")

if __name__ == "__main__":
    # Load inventory file
    inventory_file = 'inventory.ini'
    config = ConfigParser()
    config.read(inventory_file)

    # Define SSH command to retrieve syslog
    command = 'cat /var/log/syslog'

    # Define output folder
    output_folder = './SYSLOG/END DEVICE'

    # Iterate through each host in the inventory
    for host in config['hosts']:
        username, ip_address = get_ssh_username_and_ip(config['hosts'][host])
        syslog_content = ssh_and_get_syslog(username, ip_address, command)

        if syslog_content:
            save_syslog_to_csv(ip_address, syslog_content, output_folder)
