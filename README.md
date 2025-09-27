1. Installation & Setup
Python & Libraries
sudo apt update
sudo apt install python3 python3-pip -y
pip install junos-eznc ncclient pyyaml


junos-eznc → Juniper PyEZ library (for automation).

ncclient → NETCONF client library (used internally by PyEZ).

pyyaml → YAML parsing library.

Git Setup
git --version
git config --global user.name "dj0203"
git config --global user.email "debjyotipaul68@gmail.com"


Confirms Git installed and sets username/email for commits.

VS Code Extensions

Python → for writing scripts.

YAML → for editing YAML inventories.

(Optional) GitHub Copilot / Chat → for AI help in editor.

2. Repository Structure
juniper-lab-automation/
├── configs/         # generated outputs (health check results)
├── inventory/       # devices.yaml, commands.yaml
├── script/          # Python scripts
├── templates/       # Jinja templates (future use)
└── docs/            # Documentation

3. Inventory Files

inventory/devices.yaml

devices:
  - host: 192.168.0.101
    user: deb
    password: Juniper
  - host: 192.168.0.102
    user: deb
    password: Juniper


inventory/commands.yaml

commands:
  - show version
  - show interfaces terse
  - show chassis fpc
  - show system uptime
  - show route
  - show isis adjacency
  - show bgp summary

4. Script – Health Check (Explained)
Full Script
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError, RpcError
import yaml
import os

# Load devices
with open("/home/deb/juniper-lab-automation/inventory/devices.yaml", "r") as file:
    devices = yaml.safe_load(file)['devices']

# Load commands
with open("/home/deb/juniper-lab-automation/inventory/commands.yaml", "r") as file: 
    commands = yaml.safe_load(file)['commands']

# Loop through devices
for device in devices: 
    print(f"\n🔌 Connecting to device {device['host']}")
    try:
        with Device(**device) as dev:   # open NETCONF session
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

Line-by-Line Explanation

Imports

Device → opens Junos connection.

ConnectError → connection failure handler.

RpcError → command failure handler.

yaml → parse YAML.

os → manage folders/files.

Loading devices

Reads devices.yaml.

Creates a Python list of dicts (each dict = one device).

Loading commands

Reads commands.yaml.

Creates a Python list of commands (strings).

Outer loop (devices)

For each device: connect, run commands, save outputs.

Device connection

with Device(**device) as dev:

Expands dict → Device(host="192.168.0.101", user="deb", password="Juniper").

Auto-closes session when finished.

Output handling

os.makedirs(..., exist_ok=True) → ensures folder exists.

output_file = ... → builds filename using hostname.

Inner loop (commands)

Runs each command.

If success → writes output to file, ✅ printed.

If failure → writes error, ⚠️ printed.

Error handling

ConnectError → cannot reach device.

RpcError → command issue.

5. Errors Encountered & Fixes

ModuleNotFoundError: jnpr.junos
→ Installed PyEZ via pip install junos-eznc.

KeyError: 'uptime'
→ Corrected to dev.facts['up_time'] or used cli("show system uptime").

RpcError: syntax error, expecting <command>
→ Switched from dev.rpc.cli() to dev.cli() for raw commands.

File writing bug
→ Mistakenly used output_file(...) instead of outfile.write(...). Fixed.

6. Functions Glossary

yaml.safe_load(file) → parse YAML safely into Python dict/list.

Device(**device) → open NETCONF session using host/user/password from dict.

dev.facts → returns metadata (hostname, model, version, serial).

dev.cli(command) → runs raw CLI, returns text.

os.makedirs(path, exist_ok=True) → create folder if missing.

open(file, "w") → open file for writing (overwrites if exists).

outfile.write("text") → write string into file.

try/except → structured error handling.

7. Git Workflow Explained
Commands Used
git add script/running_commands.py


Staging → tells Git “I want to track this file in the next commit.”

git commit -m "Added health check script with YAML-driven commands"


Commit → snapshot of staged changes, with a message.

git push origin main


Push → sends local commits to GitHub repo (origin is remote name, main is branch).

git pull origin main


Pull → fetch + merge changes from GitHub to your local repo.

git log --oneline
