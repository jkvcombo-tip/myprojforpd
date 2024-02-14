import subprocess
import re
import sys

def scan_devices(local_ip):
    try:
        
        result = subprocess.run(["sudo", "nmap", '-sP', local_ip + "/24"], capture_output=True, text=True, check=True)

        
        pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
        devices = pattern.findall(result.stdout)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 your_script.py <local_ip>")
        sys.exit(1)

    local_ip = sys.argv[1]
    connected_devices = scan_devices(local_ip)

    if connected_devices:
        print("Connected devices:")
        for device in connected_devices:
            print(device)
    else:
        print("No connected devices found.")

if __name__ == "__main__":
    main()
