import subprocess
import re

def scan_devices():
    try:
        # Run nmap command to discover devices on the local network
        result = subprocess.run(["sudo", "nmap", "-sn", "192.168.1.0/24"], capture_output=True, text=True, check=True)

        # Extract the list of devices from the output using regular expression
        pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
        devices = pattern.findall(result.stdout)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def main():
    connected_devices = scan_devices()

    if connected_devices:
        print("Connected devices:")
        for device in connected_devices:
            print(device)
    else:
        print("No devices found.")

if __name__ == "__main__":
    main()
