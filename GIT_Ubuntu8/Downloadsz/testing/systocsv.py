import paramiko
import os
import csv
import configparser
import platform

def convert_syslog_to_csv(syslog_data, csv_file_path):
    # Replace this parsing logic with the actual structure of your syslog entries
    # The example assumes a simple syslog format with timestamp and message
    parsed_syslog_entries = [(entry.split(' ', 1)[0], entry.split(' ', 1)[1]) for entry in syslog_data.splitlines()]

    # Write the parsed syslog entries to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Timestamp', 'Message'])  # CSV header

        for timestamp, message in parsed_syslog_entries:
            csv_writer.writerow([timestamp, message])

def copy_and_convert_syslog(host, user, private_key_path, local_destination_path):
    if host.lower() == 'localhost':
        # If the host is localhost, read the local syslog file
        local_syslog_path = '/var/log/syslog'  # Adjust the path as needed

        print(f"Local Syslog Path: {local_syslog_path}")

        with open(local_syslog_path, 'r') as f:
            syslog_data = f.read()

        # Convert syslog to CSV
        csv_file_path = os.path.join(local_destination_path, f'converted_syslog_{host}.csv')
        print(f"CSV File Path: {csv_file_path}")
        convert_syslog_to_csv(syslog_data, csv_file_path)

        print(f"Local Syslog converted to CSV: {csv_file_path}")

    else:
        # For remote hosts, use SSH to fetch syslog file
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Use private key for authentication
            expanded_private_key_path = os.path.expanduser(private_key_path)
            private_key = paramiko.RSAKey(filename=expanded_private_key_path)

            # Connect to the machine
            ssh.connect(host, username=user, pkey=private_key)

            # Fetch syslog file
            sftp = ssh.open_sftp()
            remote_syslog_path = '/var/log/syslog'  # Adjust the path as needed

            # Local path for the converted syslog file in the specified directory
            local_syslog_path = os.path.join(local_destination_path, f'converted_syslog_{host}.txt')

            # Copy the syslog file from remote to local
            sftp.get(remote_syslog_path, local_syslog_path)

            # Close the connection
            sftp.close()
            ssh.close()

            print(f"Local Syslog Path: {local_syslog_path}")

            # Process the syslog file
            with open(local_syslog_path, 'r') as f:
                syslog_data = f.read()

            # Convert syslog to CSV
            csv_file_path = os.path.join(local_destination_path, f'converted_syslog_{host}.csv')
            print(f"CSV File Path: {csv_file_path}")
            convert_syslog_to_csv(syslog_data, csv_file_path)

            print(f"Remote Syslog converted to CSV: {csv_file_path}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Read IP addresses from inventory.ini
    config = configparser.ConfigParser()
    config.read('inventory.ini')

    for host, host_info in config['hosts'].items():
        if 'ansible_host' in host_info:
            ip_address = host_info.split('=')[1]
            copy_and_convert_syslog(ip_address, 'combo', '~/.ssh/id_rsa', './SYSLOG/END DEVICE/')
