import paramiko
import os
import socket

def fetch_syslog_remote(remote_host, remote_user, remote_private_key_path, local_destination_path):
    try:
        # Connect to the remote machine
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Use private key for authentication
        expanded_private_key_path = os.path.expanduser(remote_private_key_path)
        private_key = paramiko.RSAKey(filename=expanded_private_key_path)

        # Connect to the remote machine
        ssh.connect(remote_host, username=remote_user, pkey=private_key)

        # Fetch syslog file from remote machine
        sftp = ssh.open_sftp()
        remote_syslog_path = '/var/log/syslog'  # Adjust the path as needed
        local_syslog_path = os.path.join(local_destination_path, f'end-syslog_{remote_host}')
        sftp.get(remote_syslog_path, local_syslog_path)

        # Close the connection
        sftp.close()
        ssh.close()

    except socket.gaierror as e:
        print(f"Error resolving hostname: {e}")

if __name__ == "__main__":
    host = '192.168.1.59'
    remote_user = 'combo'
    remote_private_key_path = '/home/combo/.ssh/id_rsa'  # Adjust the path to your private key
    local_destination_path = '/home/combo/Documents/MAIN/SYSLOG/END DEVICE/'

    # Fetch syslog from the remote machine
    fetch_syslog_remote(host, remote_user, remote_private_key_path, local_destination_path)
