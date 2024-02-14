import subprocess
import re

def scan_devices():
    try:
        
        result = subprocess.run(["sudo", "nmap", '-sP', '192.168.1.0/24'], capture_output=True, text=True, check=True)

        
        pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
        devices = pattern.findall(result.stdout)

        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

def main():
    connected_devices = scan_devices()

    if connected_devices:
        print("Running devices:")
        for device in connected_devices:
            print(device)
    else:
        print("No running devices found.")

if __name__ == "__main__":
    main()
