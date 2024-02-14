import paramiko
import socket
import ipaddress
import subprocess

def scan_ssh_devices(network_prefix, start_range, end_range, ssh_port=22, timeout=1):
    for i in range(start_range, end_range + 1):
        target_ip = f"{network_prefix}.{i}"
        target_address = (target_ip, ssh_port)

        # Check if the host is reachable
        try:
            socket.create_connection(target_address, timeout=timeout)
        except (socket.timeout, ConnectionRefusedError):
            continue  # Move to the next IP if the host is not reachable or SSH port is closed

        # Attempt to establish an SSH connection
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(target_ip, port=ssh_port, timeout=timeout)
            print(f"SSH is open on {target_ip}")
            # Add additional actions if needed
        except (paramiko.AuthenticationException, paramiko.SSHException, socket.error):
            pass  # SSH connection failed or not allowed

        finally:
            ssh_client.close()

def show_current_ssh_connections():
    try:
        result = subprocess.run(['w'], stdout=subprocess.PIPE, text=True)
        print("Currently connected users:")
        print(result.stdout)
    except Exception as e:
        print(f"Error while fetching current SSH connections: {e}")

if __name__ == "__main__":
    # Define your network details
    network_prefix = "192.168.1"  # Change this to your network's prefix
    start_range = 1
    end_range = 254  # Adjust the range based on your network size

    scan_ssh_devices(network_prefix, start_range, end_range)
    show_current_ssh_connections()
