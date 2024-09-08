import sys
import re
import os
import shutil
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import netifaces
import netifaces as ni
import io
import ipaddress


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def logo():
    logo_path = "/etc/logo2.sh"
    try:
        subprocess.run(["bash", "-c", logo_path], check=True)
    except subprocess.CalledProcessError as e:
        return e

    return None

def remote_extraction(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        match_ipv4 = re.search(
            r"remote\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", content
        )
        match_ipv6 = re.search(r"remote\s+([0-9a-fA-F:]+)", content)
        if match_ipv4:
            return match_ipv4.group(1)
        elif match_ipv6:
            return match_ipv6.group(1)
    return None


def remote_extraction_sit(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        match = re.search(r"remote\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", content)
        if match:
            return match.group(1)
    return None


def remote_endpoint(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        match = re.search(r"\[Peer\][\s\S]*?Endpoint\s*=\s*([\d\.]+)", content)
        if match:
            return match.group(1)
    return None


def parse_wireguard_config(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    endpoint = re.search(r"Endpoint\s*=\s*(\S+)", content)
    mtu = re.search(r"MTU\s*=\s*(\d+)", content)
    port = re.search(r"ListenPort\s*=\s*(\d+)", content)
    return {
        "endpoint": endpoint.group(1) if endpoint else None,
        "mtu": mtu.group(1) if mtu else None,
        "port": port.group(1) if port else None,
    }


def interface_ex(interface):
    output = subprocess.run(
        ["ip", "a", "show", interface], capture_output=True, text=True
    )
    return output.returncode == 0


def interface_check(interface):
    output = subprocess.run(
        ["ip", "a", "show", interface], capture_output=True, text=True
    )
    if output.returncode == 0:
        if re.search(r"state (UP|UNKNOWN)", output.stdout):
            return "online"
    return "offline"

def wireguard_status():
    os.system("clear")
    logo()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mWireguard Status Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭─────────────────────────────────────────────────╮\033[0m")
    print("\033[93mYou are viewing the status of your current tunnels:\033[0m")

    interfaces = [
        "wireserver5",
        "azumig65",
        "wireserver4",
        "azumig64",
        "wireserver3",
        "azumig63",
        "wireserver2",
        "azumig62",
        "wireserver1",
        "azumig61",
        "wireclient",
        "azumi5",
        "azumi4",
        "azumi3",
        "azumi2",
        "azumi1",
    ]

    active_int = {}
    for interface in interfaces:
        if interface_ex(interface):
            status = interface_check(interface)
            if status == "online":
                active_int[interface] = True

    if not active_int:
        print(" No Interfaces available.")
        return

    config_pairs = [
        (
            "wireserver5",
            "azumig65",
            "/etc/gre65.sh",
            "/etc/wireguard/wireserver5.conf",
            "Server Config [5]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireserver4",
            "azumig64",
            "/etc/gre64.sh",
            "/etc/wireguard/wireserver4.conf",
            "Server Config [4]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireserver3",
            "azumig63",
            "/etc/gre63.sh",
            "/etc/wireguard/wireserver3.conf",
            "Server Config [3]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireserver2",
            "azumig62",
            "/etc/gre62.sh",
            "/etc/wireguard/wireserver2.conf",
            "Server Config [2]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireserver1",
            "azumig61",
            "/etc/gre61.sh",
            "/etc/wireguard/wireserver1.conf",
            "Server Config [1]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireclient",
            "azumig65",
            "/etc/gre65.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [5]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireclient",
            "azumig64",
            "/etc/gre64.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [4]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireclient",
            "azumig63",
            "/etc/gre63.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [3]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireclient",
            "azumig62",
            "/etc/gre62.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [2]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireclient",
            "azumig61",
            "/etc/gre61.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [1]",
            "Native GRE6TAP + WireGuard",
            "WireGuard + GRE6TAP",
        ),
        (
            "wireserver5",
            "azumi5",
            "/etc/private5.sh",
            "/etc/wireguard/wireserver5.conf",
            "Server Config [5]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireserver4",
            "azumi4",
            "/etc/private4.sh",
            "/etc/wireguard/wireserver4.conf",
            "Server Config [4]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireserver3",
            "azumi3",
            "/etc/private3.sh",
            "/etc/wireguard/wireserver3.conf",
            "Server Config [3]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireserver2",
            "azumi2",
            "/etc/private2.sh",
            "/etc/wireguard/wireserver2.conf",
            "Server Config [2]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireserver1",
            "azumi1",
            "/etc/private1.sh",
            "/etc/wireguard/wireserver1.conf",
            "Server Config [1]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireclient",
            "azumi5",
            "/etc/private5.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [5]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireclient",
            "azumi4",
            "/etc/private4.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [4]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireclient",
            "azumi3",
            "/etc/private3.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [3]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireclient",
            "azumi2",
            "/etc/private2.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [2]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
        (
            "wireclient",
            "azumi1",
            "/etc/private1.sh",
            "/etc/wireguard/wireclient.conf",
            "Client [1]",
            "Sit + Wireguard",
            "Sit + Wireguard",
        ),
    ]

    displayed_servers = set()

    for (
        int_a,
        int_b,
        gre_file,
        wg_file,
        config_label,
        tunnel_type_ipv6,
        tunnel_type_ipv4,
    ) in config_pairs:
        if active_int.get(int_a) and active_int.get(int_b):
            remote_ip = (
                remote_extraction(gre_file)
                if "private" not in gre_file
                else remote_extraction_sit(gre_file)
            )
            wg_config = parse_wireguard_config(wg_file)

            if remote_ip:
                if config_label not in displayed_servers:
                    if ":" in remote_ip:  # IPv6
                        print(
                            "\033[93m─────────────────────────────────────────────────\033[0m"
                        )
                        print(f" \033[93mThis is \033[92m{config_label}\033[0m")
                        print(
                            f" \033[97mTunnel Type: \033[92m{tunnel_type_ipv6}\033[0m"
                        )
                        print(
                            f" \033[93mRemote \033[92m[Client]\033[93m IP Address : \033[97m{remote_ip}\033[0m"
                        )
                    else:  # IPv4
                        print(
                            "\033[93m─────────────────────────────────────────────────\033[0m"
                        )
                        print(f" \033[93mThis is \033[92m{config_label}\033[0m")
                        print(
                            f" \033[97mTunnel Type: \033[92m{tunnel_type_ipv4}\033[0m"
                        )
                        if wg_config["endpoint"]:
                            print(
                                f" \033[93mRemote \033[92m[Client]\033[93m IP Address : \033[97m{wg_config['endpoint'].split(':')[0]}\033[0m"
                            )

                    print(f" \033[93mPort: \033[97m{wg_config['port']}\033[0m")
                    print(f" \033[93mMTU: \033[97m{wg_config['mtu']}\033[0m")

                    displayed_servers.add(config_label)

    additional_servers = [
        (
            "wireserver5",
            "Server Config [5]",
            "/etc/wireguard/wireserver5.conf",
        ),
        (
            "wireserver4",
            "Server Config [4]",
            "/etc/wireguard/wireserver4.conf",
        ),
        (
            "wireserver3",
            "Server Config [3]",
            "/etc/wireguard/wireserver3.conf",
        ),
        (
            "wireserver2",
            "Server Config [2]",
            "/etc/wireguard/wireserver2.conf",
        ),
        (
            "wireserver1",
            "Server Config [1]",
            "/etc/wireguard/wireserver1.conf",
        ),
        ("wireclient", "Client", "/etc/wireguard/wireclient.conf"),
    ]

    for interface, label, config_path in additional_servers:
        if active_int.get(interface) and label not in displayed_servers:
            remote_ip = remote_endpoint(config_path)
            wg_config = parse_wireguard_config(config_path)

            if remote_ip:
                print(
                    "\033[93m─────────────────────────────────────────────────\033[0m"
                )
                print(f" \033[93mThis is \033[92m{label}\033[0m")
                print(f" \033[97mTunnel Type: \033[92mWireGuard UDP\033[0m")
                print(
                    f" \033[93mRemote \033[92mClient\033[93m IP Address  \033[96m[{interface[-1]}]: \033[97m{remote_ip}\033[0m"
                )
                print(f" \033[93mPort: \033[97m{wg_config['port']}\033[0m")
                print(f" \033[93mMTU: \033[97m{wg_config['mtu']}\033[0m")
                print(
                    "\033[93m─────────────────────────────────────────────────\033[0m"
                )
    print("\033[93m─────────────────────────────────────────────────\033[0m")
    print("0.\033[97mback to the main script\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "0":
            os.system("clear")
            os._exit(0)
            break
        else:
            print("Invalid choice.")

wireguard_status()
