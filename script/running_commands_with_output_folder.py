from jnpr.junos import Device
from jnpr.junos.exception import ConnectError, RpcError
import yaml
import os

# Load devices
with open("/home/deb/juniper-lab-automation/inventory/devices.yaml", "r") as file:
    devices = yaml.safe_load(file)['devices']
    print(f"Devices loaded : {devices}")

# Load commands
with open("/home/deb/juniper-lab-automation/inventory/commands.yaml", "r") as file: 
    commands = yaml.safe_load(file)['commands']
    print(f"Commands to run: {commands}") 

# Loop through devices
for device in devices: 
    print(f"\n🔌 Connecting to device {device['host']}")
    try:
        with Device(**device) as dev:
            out_dir = "/home/deb/juniper-lab-automation/configs/healthcheck"
            os.makedirs(out_dir, exist_ok=True)
            output_file = f"{out_dir}/{dev.facts['hostname']}_healthcheck.txt"

            with open(output_file, "w") as outfile:
                for command in commands:
                    try:
                        rsp = dev.cli(command, warning=False)
                        outfile.write(f"\n--- {command} ---\n{rsp}\n")
                        print(f"✅ {command} ran successfully")
                    except RpcError as rpc_err:
                        outfile.write(f"\n--- {command} ---\n⚠️ Failed: {rpc_err}\n")
                        print(f"⚠️ {command} failed: {rpc_err}")

            print(f"📄 Output saved to {output_file}")

    except ConnectError as err:
        print(f"❌ Cannot connect to {device['host']}: {err}")

        
            