import subprocess

def scan_devices():
    try:
        # Run arp-scan command to discover devices on the local network
        result = subprocess.run(["sudo", "arp-scan", "-l"], capture_output=True, text=True, check=True)

        # Extract the list of devices from the output
        devices = result.stdout.strip().split('\n')[2:]

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
