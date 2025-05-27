
import paramiko
import os

# Define device inventory
device_inventory = {
    "Dallas": [
        {"type": "cisco", "ip": "192.168.1.1", "username": "admin", "password": "password"},
        {"type": "fortigate", "ip": "192.168.1.2", "username": "admin", "password": "password"},
        {"type": "steelhead", "ip": "192.168.1.3", "username": "admin", "password": "password"}
    ],
    "London": [
        {"type": "cisco", "ip": "192.168.2.1", "username": "admin", "password": "password"},
        {"type": "fortigate", "ip": "192.168.2.2", "username": "admin", "password": "password"},
        {"type": "steelhead", "ip": "192.168.2.3", "username": "admin", "password": "password"}
    ],
    # Add more locations as needed
}

# Define backup commands for each device type
backup_commands = {
    "cisco": "show running-config",
    "fortigate": "execute backup config flash",
    "steelhead": "show config"
}

# Function to backup a single device
def backup_device_config(device):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(device["ip"], username=device["username"], password=device["password"])
        print(f"Connected to {device['type']} at {device['ip']}")

        stdin, stdout, stderr = ssh.exec_command(backup_commands[device["type"]])
        config_data = stdout.read().decode()

        # Save to file
        filename = f"{device['type']}_{device['ip'].replace('.', '-')}_backup.txt"
        with open(filename, "w") as f:
            f.write(config_data)

        print(f"Backup saved to {filename}")

    except Exception as e:
        print(f"Error backing up {device['type']} at {device['ip']}: {e}")

    finally:
        ssh.close()

# Function to backup all devices in a location
def backup_location(location):
    print(f"\n🔄 Backing up devices in {location}...")
    for device in device_inventory.get(location, []):
        backup_device_config(device)

# Run backups for all locations
for location in device_inventory:
    backup_location(location)
