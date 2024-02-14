import subprocess
import re

def scan_devices(local_ip):
    try:
        # Run nmap command to discover devices on the local network
        result = subprocess.run(["sudo", "nmap", '-Pn', local_ip + "/24"], capture_output=True, text=True, check=True)

        # Extract the list of devices from the output using regular expression
        pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
        devices = pattern.findall(result.stdout)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def main():
    local_ip = "192.168.1.50"  # Adjust this to a valid local IP in your network

    connected_devices = scan_devices(local_ip)

    if connected_devices:
        print("Connected devices:")
        for device in connected_devices:
            print(device)
    else:
        print("No connected devices found.")

if __name__ == "__main__":
    main()
