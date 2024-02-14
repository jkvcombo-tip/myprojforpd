import paramiko
import os
import csv

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
    try:
        # Connect to the machine (local or remote)
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

        # Process the syslog file
        with open(local_syslog_path, 'r') as f:
            syslog_data = f.read()

        # Convert syslog to CSV
        csv_file_path = os.path.join(local_destination_path, f'converted_syslog_{host}.csv')
        convert_syslog_to_csv(syslog_data, csv_file_path)

        print(f"Syslog converted to CSV: {csv_file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Local machine
    local_host = 'localhost'
    local_user = 'combo'
    local_private_key_path = '~/.ssh/id_rsa'  # Use tilde notation for the home directory

    # Remote machine
    remote_host = '192.168.1.59'
    remote_user = 'combo'
    remote_private_key_path = '~/.ssh/id_rsa'  # Use tilde notation for the home directory

    # Local destination path
    local_destination_path = './SYSLOG/END DEVICE/'  # Specify the desired path

    # Create the directory if it doesn't exist
    os.makedirs(local_destination_path, exist_ok=True)

    # Collect syslog from the local machine and convert to CSV
    copy_and_convert_syslog(local_host, local_user, local_private_key_path, local_destination_path)

    # Collect syslog from the remote machine and convert to CSV
    copy_and_convert_syslog(remote_host, remote_user, remote_private_key_path, local_destination_path)
