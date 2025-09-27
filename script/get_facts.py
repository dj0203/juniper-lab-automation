from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import yaml

with open("/home/deb/juniper-lab-automation/inventory/devices.yaml", "r") as file:
    data = yaml.safe_load(file)
    print(data)
    devices= data['devices']
#Loop through each device in the devices list

for device in devices: 
    print(f"Connecting to device : {device['host']}")
    try:
        with Device(**device) as dev:
            print(f"Connected to {dev.facts['hostname']}")
            print(f"Model: {dev.facts['model']}")
            print(f"Serial Number: {dev.facts['serialnumber']}")
            print(f"OS Version: {dev.facts['version']}")
            uptime = dev.rpc.get_system_uptime_information()
            print(f"Uptime: {uptime.findtext('.//up-time')}")

    except ConnectError as err:
        print(f"Cannot connect to device: {err}")