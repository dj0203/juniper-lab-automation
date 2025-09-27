from jnpr.junos import Device
from jnpr.junos.exception import ConnectError, RpcError
import yaml
import os  

with open("/home/deb/juniper-lab-automation/inventory/devices.yaml", "r") as file:
    data = yaml.safe_load(file)
    devices = data["devices"]
    print(devices)
with open("/home/deb/juniper-lab-automation/inventory/commands.yaml", "r") as file:
    cmd_data= yaml.safe_load(file)
    commands = cmd_data["commands"] 

#Loop through devices
for device in devices: 
    print(f"Connecting to device {device['host']}")
    try:
        with Device(**device) as dev : 
            for command in commands : 
                rsp= dev.cli(command , warning = False)
                print(f"\n--- {command} ---\n{rsp}")

    except RpcError as rpc_err:
        print(f"⚠️ Command failed: {command} -> {rpc_err}")
