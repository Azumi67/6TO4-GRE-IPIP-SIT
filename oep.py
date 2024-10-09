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
import threading
import itertools


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

def eoip_status():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEoIP Status Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mYou are viewing the status of your EoIP tunnels:\033[0m")

    eoip_interfaces = {
        "eoipkh1": "eoip kharej config 1",
        "eoipkh2": "eoip kharej config 2",
        "eoipkh3": "eoip kharej config 3",
        "eoipkh4": "eoip kharej config 4",
        "eoipkh5": "eoip kharej config 5",
        "eoipir1": "eoip iran config 1",
        "eoipir2": "eoip iran config 2",
        "eoipir3": "eoip iran config 3",
        "eoipir4": "eoip iran config 4",
        "eoipir5": "eoip iran config 5",
    }

    active_int = []
    for interface, label in eoip_interfaces.items():
        status = interface_check(interface)
        if status == "online":
            active_int.append(interface)

    if not active_int:
        print(" No Interfaces available.")
    else:
        for interface in active_int:
            if interface.startswith("eoipkh"):
                index = interface[-1]
                service_file = f"/etc/systemd/system/eoip_kharej_{index}.service"
                additional_file = f"/etc/systemd/system/eoip_additional_kharej_{index}.service"
                print(f" \033[93mStatus: \033[92mOnline\033[97m | \033[93mInterface name:\033[96m {interface} ({eoip_interfaces[interface]})\033[0m")
                print(" \033[93mTunnel Method: \033[97mEoIP\033[0m")
                if os.path.exists(service_file):
                    remote_ip = remote_extraction(service_file)
                    if remote_ip:
                        print(f" \033[93mRemote IP: \033[97m{remote_ip}\033[0m")
                        print("\033[93m───────────────────────────────────────\033[0m")
                elif os.path.exists(additional_file):
                    remote_ip = remote_extraction(additional_file)
                    if remote_ip:
                        print(f" \033[93mRemote IP (Additional): \033[97m{remote_ip}\033[0m")
            elif interface.startswith("eoipir"):
                index = interface[-1]
                service_file = f"/etc/systemd/system/eoip_iran_{index}.service"
                additional_file = f"/etc/systemd/system/additional_irancmd_{index}.service"
                print(f" \033[93mStatus: \033[92mOnline\033[97m | \033[93mInterface name:\033[96m {interface} ({eoip_interfaces[interface]})\033[0m")
                print(" \033[93mTunnel Method: \033[97mEoIP\033[0m")
                if os.path.exists(service_file):
                    remote_ip = remote_extraction(service_file)
                    if remote_ip:
                        print(f" \033[93mRemote IP: \033[97m{remote_ip}\033[0m")
                        print("\033[93m───────────────────────────────────────\033[0m")
                elif os.path.exists(additional_file):
                    remote_ip = remote_extraction(additional_file)
                    if remote_ip:
                        print(f" \033[93mRemote IP (Additional): \033[97m{remote_ip}\033[0m")
                
                

    secret_key = ipsec_secret()
    if secret_key != "Not found":
        print(" \033[93mIPsec Secret Key:\033[96m", secret_key, "\033[0m")

    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "0":
            os.system("clear")
            eoip_menu()
            break
        else:
            print("Invalid choice.")

def interface_check(interface):
    output = subprocess.run(
        ["ip", "a", "show", interface], capture_output=True, text=True
    )
    if output.returncode == 0:
        if re.search(r"state (UP|UNKNOWN)", output.stdout):
            return "online"
    return "offline"

def remote_extraction(service_file):
    try:
        with open(service_file, "r") as file:
            for line in file:
                if "ExecStart" in line:
                    match = re.search(r"remote\s+((?:[0-9]{1,3}\.){3}[0-9]{1,3}|(?:[a-fA-F0-9:]+))", line)
                    if match:
                        return match.group(1)
    except FileNotFoundError:
        pass
    return None

def ipsec_secret():
    try:
        with open("/etc/ipsec.secrets", "r") as file:
            lines = file.readlines()
            for line in lines:
                if "PSK" in line:
                    secret_key = line.split('"')[1]
                    return secret_key.strip()
    except FileNotFoundError:
        pass
    return "Not found"

def spinnerboy():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_spinner:
            break
        sys.stdout.write(f'\r{c} Loading... ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!          \n')

def runcommand(cmd, desc=""):
    global stop_spinner
    stop_spinner = False
    spinner_thread = threading.Thread(target=spinnerboy)
    spinner_thread.start()
    
    try:
        print(f"{desc}...")
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == b"":
                break
            if output:
                sys.stdout.write(output.decode())
                sys.stdout.flush()
        
        process.communicate()  
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)
            
    except subprocess.CalledProcessError as e:
        stop_spinner = True
        spinner_thread.join()
        print(f"\033[91merror: {desc}: {e}\033[0m")
        raise e

    stop_spinner = True
    spinner_thread.join()
    time.sleep(0.5)

def dependencies():
    commands = [
        ("sudo apt install -y make", "Installing make"),
        ("sudo apt install -y git", "Installing git")
    ]
    for cmd, desc in commands:
        try:
            runcommand(cmd, desc)
        except subprocess.CalledProcessError:
            return

def clone_eoip():
    target_dir = "/usr/local/bin/eoip"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"\033[93mCreated eoip\033[0m")
    
    if os.path.exists(os.path.join(target_dir, ".git")):
        print("\033[93meoip already exists.\033[0m")
    else:
        try:
            runcommand(f"git clone https://github.com/miyugundam/eoip.git {target_dir}", "Cloning eoip repo")
        except subprocess.CalledProcessError:
            print("\033[91mclone failed..\033[0m")
            return

    try:
        os.chdir(target_dir)
        runcommand("make", "Building eoip")
        runcommand("sudo make install", "Installing eoip")
        os.chdir("..")
    except subprocess.CalledProcessError:
        print("\033[91mbuild was unsuccessful.\033[0m")
        return

def create_serviceeoip(service_name, service_exec):
    service_content = f"""[Unit]
Description={service_name}
After=network.target

[Service]
ExecStart=/usr/local/bin/eoip/{service_exec}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
    
    service_file_path = f"/etc/systemd/system/{service_name}.service"
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=True)
    subprocess.run(f"sudo systemctl enable {service_name}.service", shell=True, check=True)
    subprocess.run(f"sudo systemctl restart {service_name}.service", shell=True, check=True)


def create_serviceeoip_additional(service_name, service_exec):
    service_content = f"""[Unit]
Description={service_name}
After=network.target

[Service]
ExecStart={service_exec}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
    
    service_file_path = f"/etc/systemd/system/{service_name}.service"
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(f"sudo systemctl daemon-reload", shell=True, check=True)
    subprocess.run(f"sudo systemctl enable {service_name}.service", shell=True, check=True)
    subprocess.run(f"sudo systemctl restart {service_name}.service", shell=True, check=True)

def cmd(command):
    subprocess.run(command, shell=True, check=True)

def animate(message):
    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.05)
    print()


def anime():
    animation = [
        "[=     ]",
        "[==    ]",
        "[===   ]",
        "[====  ]",
        "[===== ]",
        "[======]",
        "[===== ]",
        "[====  ]",
        "[===   ]",
        "[==    ]",
        "[=     ]",
    ]
    for i in range(20):
        time.sleep(0.1)
        sys.stdout.write(f"\r{animation[i % len(animation)]}")
        sys.stdout.flush()
    sys.stdout.write("\r")
    sys.stdout.flush()


def hide(command):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
    )
    while process.poll() is None:
        anime()
    _, stderr = process.communicate()
    if process.returncode != 0:
        print(f"\033[91merror: {stderr.decode()}\033[0m")

def service_exists(service_name):
    result = subprocess.run(
        ["systemctl", "list-units", "--full", "--all", service_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return service_name in result.stdout.decode()


def set_mtu(private_ip):
    print("\033[93m────────────────────────────────────────\033[0m")
    set_mtu = input(f"\033[93mDo you want to set the \033[92mMTU size\033[93m for \033[96m{private_ip}\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m").lower()
    
    if set_mtu in ["yes", "y"]:
        mtu = input(f"\033[93mEnter the \033[92mMTU size\033[93m for \033[96m{private_ip}\033[93m: \033[0m")
        return mtu
    return None

def additional_commands(server_num, private_ip, dev, ipv4=True):
    subnet = "24" if ipv4 else "64"
    
    script_dir = "/usr/local/bin/cmd/"
    script_path = f"{script_dir}eoip_additional_commands_{server_num}.sh"
    
    os.makedirs(script_dir, exist_ok=True)
    
    additional_commands_script = f"""#!/bin/bash
ip addr add {private_ip}/{subnet} dev {dev}
ip link set {dev} up
"""

    with open(script_path, 'w') as script_file:
        script_file.write(additional_commands_script)
    
    os.chmod(script_path, 0o755)

    return private_ip, subnet, script_path

def nextip(ip, ipv4=True):
    ip_obj = ipaddress.ip_address(ip)
    next_ip = ip_obj + 1
    return str(next_ip)

def oppositeip(ip, ipv4=True):
    try:
        if ipv4:
            octets = ip.split(".")
            if octets[-1] == '1':
                octets[-1] = '2'
            elif octets[-1] == '2':
                octets[-1] = '1'
            return ".".join(octets)
        else:
            ip_obj = ipaddress.IPv6Address(ip)
            if ip_obj.packed[-1] == 1:  
                return str(ip_obj + 1)
            elif ip_obj.packed[-1] == 2:  
                return str(ip_obj - 1)
            else:
                raise ValueError(f"Unsupported IPv6 address: {ip}")
    except ipaddress.AddressValueError:
        raise ValueError(f"IP address format is weird: {ip}")

def config_client_eoip1(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipir1"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip2(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipir2"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip3(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipir3"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip4(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipir4"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip5(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipir5"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

#kharej eoip 
def config_client_eoip_kh1(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipkh1"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip_kh2(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipkh2"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip_kh3(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipkh3"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip_kh4(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipkh4"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_client_eoip_kh5(psk, private_ip, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    dev_name = f"eoipkh5"

    private_ip, subnet, _ = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    opposite_ip = oppositeip(private_ip, ipv4=ipv4)

    ipsec_conf += f"""conn eoip_{dev_name}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={opposite_ip}
  rightsubnet={opposite_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

    with open("/etc/ipsec.secrets", "a") as f:
        f.write(f'{opposite_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def config_server_eoip(psk, num_servers, private_ips, ipv4=True):
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    animate("\033[93mInstalling IPSEC..\033[0m")
    hide("sudo apt install strongswan -y")
    animate("\033[92mIPSEC Installation is completed!\033[0m")

    if service_exists("strongswan-starter.service"):
        cmd("sudo systemctl disable strongswan-starter")
        cmd("sudo systemctl stop strongswan-starter")

    if service_exists("strongswan.service"):
        cmd("sudo systemctl disable strongswan")
        cmd("sudo systemctl stop strongswan")

    cmd("sudo rm -f /etc/ipsec1.conf /etc/ipsec.secrets")

    ipsec_conf = """config setup
  charondebug=all
  uniqueids=no
##azumiisinyourarea

""" 

    for i in range(1, num_servers + 1):
        dev_name = f"eoipkh{i}"
        private_ip = private_ips[i - 1]
        private_ip, subnet, _ = additional_commands(i, private_ip, dev=dev_name, ipv4=ipv4)

        server_ip = oppositeip(private_ip, ipv4=ipv4)

        ipsec_conf += f"""conn eoip_{i}
  left=%defaultroute
  leftsubnet={private_ip}/{subnet}
  leftid={private_ip}
  right={server_ip}
  rightsubnet={server_ip}/{subnet}
  ike=aes256gcm16-sha512-ecp384!
  esp=aes256gcm16-sha512-ecp384!
  keyexchange=ikev2
  auto=start
  authby=secret
  keyingtries=%forever
  dpdaction=restart
  dpddelay=30s
  dpdtimeout=120s
  rekeymargin=3m
  rekeyfuzz=100%
  reauth=no

"""

        with open("/etc/ipsec.secrets", "a") as f:
            f.write(f'{server_ip} {private_ip} : PSK "{psk}"\n')

    with open("/etc/ipsec1.conf", "w") as f:
        f.write(ipsec_conf)

    service_content = """[Unit]
Description=strongazumi IPsec IKEv1/IKEv2 daemon using ipsec.conf
After=network-online.target

[Service]
ExecStart=/usr/sbin/ipsec start --nofork --conf /etc/ipsec1.conf
ExecReload=/usr/sbin/ipsec reload
Restart=always
RestartSec=5
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
"""

    with open("/etc/systemd/system/strong-azumi1.service", "w") as f:
        f.write(service_content)

    cmd("sudo systemctl daemon-reload")
    cmd("sudo systemctl enable strong-azumi1")
    cmd("sudo systemctl restart strong-azumi1")

def kharejserver_eoip():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V4\033[93m Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
    print("\033[93m───────────────────────────────────────\033[0m")
    
    num_servers = int(input("\033[93mHow many \033[92mIran servers\033[93m do you have? \033[0m"))
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    iran_public_ips = [input(f"\033[93mEnter \033[92mIran \033[96m{i+1}\033[93m Public IPv4: \033[0m") for i in range(num_servers)]
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    private_ips = [input(f"\033[93mEnter \033[92mPrivate IP \033[93mfor Iran server {i+1}: \033[0m") for i in range(num_servers)]
    
    for i, iran_public_ip in enumerate(iran_public_ips, start=1):
        print("\033[93m───────────────────────────────────────\033[0m")
        mtu_value = input(f"\033[93mEnter \033[92mMTU value \033[93mfor \033[97mconfig \033[96m{i}: \033[0m")
        dev_name = f"eoipkh{i}"
        eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id {100 + i} mtu {mtu_value}"
        
        create_serviceeoip(f"eoip_kharej_{i}", eoip_command)
        
        private_ip, subnet, script_path = additional_commands(i, private_ips[i - 1], dev=dev_name, ipv4=ipv4)
        
        display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")
        
        create_serviceeoip_additional(f"eoip_additional_kharej_{i}", script_path)
        
        opposite_ip = calculate_oppose_ip(private_ips[i - 1], ipv4)
        
        script_eoip(opposite_ip, i)  
        ping_eoip_service(i)
        
    print("\033[93m────────────────────────────────────────\033[0m")
    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_server_eoip(psk, num_servers, private_ips, ipv4=ipv4) 
        enable_reset_ipsec()


def calculate_oppose_ip(ip, is_ipv4):
    """Calculates the opposite IP for either IPv4 or IPv6."""
    if is_ipv4:
        ip_parts = ip.split('.')
        if ip_parts[-1] == '1':
            ip_parts[-1] = '2'
        else:
            ip_parts[-1] = '1'
        return '.'.join(ip_parts)
    else:
        if ip.endswith('::1'):
            return ip.replace('::1', '::2')
        elif ip.endswith('::2'):
            return ip.replace('::2', '::1')
        else:
            return ip  


def script_eoip(oppositeip, server_index):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = f"/etc/ping_eoip_{server_index}.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoip_service(server_index):
    service_content = f"""[Unit]
Description=keepalive for EOIP server {server_index}
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_{server_index}.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = f"/etc/systemd/system/ping_eoip_{server_index}.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", f"ping_eoip_{server_index}"])
    subprocess.run(["systemctl", "start", f"ping_eoip_{server_index}"])
    sleep(1)
    subprocess.run(["systemctl", "restart", f"ping_eoip_{server_index}"])

def kharejserver_eoip6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
    print("\033[93m───────────────────────────────────────\033[0m")
    
    num_servers = int(input("\033[93mHow many \033[92mIran servers\033[93m do you have? \033[0m"))
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    iran_public_ips = [input(f"\033[93mEnter \033[92mIran \033[96m{i+1}\033[93m Public IPv6: \033[0m") for i in range(num_servers)]
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    private_ips = [input(f"\033[93mEnter \033[92mPrivate IP \033[93mfor Iran server {i+1}: \033[0m") for i in range(num_servers)]
    
    for i, iran_public_ip in enumerate(iran_public_ips, start=1):
        print("\033[93m───────────────────────────────────────\033[0m")
        mtu_value = input(f"\033[93mEnter \033[92mMTU value \033[93mfor \033[97mconfig \033[96m{i}: \033[0m")
        dev_name = f"eoipkh{i}"
        eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id {100 + i} mtu {mtu_value}"
        
        create_serviceeoip(f"eoip_kharej_{i}", eoip_command)
        
        private_ip, subnet, script_path = additional_commands(i, private_ips[i - 1], dev=dev_name, ipv4=ipv4)
        
        display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")
        
        create_serviceeoip_additional(f"eoip_additional_kharej_{i}", script_path)
        
        opposite_ip = calculate_oppose_ip(private_ips[i - 1], ipv4)
        
        script_eoip(opposite_ip, i)  
        ping_eoip_service(i)
        
    print("\033[93m────────────────────────────────────────\033[0m")
    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_server_eoip(psk, num_servers, private_ips, ipv4=ipv4) 
        enable_reset_ipsec()

def ipsec_service_remove():

    try:
        devnull = open(os.devnull, "w")
        display_notification("\033[93mRemoving stuff...\033[0m")

        commands = [
            "rm /etc/ipsec2.sh",
            "systemctl disable ipsecreset.service",
            "systemctl stop ipsecreset.service",
            "sudo rm /etc/systemd/system/ipsecreset.service",
            "sudo rm /etc/reset_ipsec.sh" "sudo rm /usr/local/bin/ipsec_daemon.sh",
            "systemctl daemon-reload",
        ]

        for command in commands:
            subprocess.run(command, shell=True, stdout=devnull, stderr=devnull)

        devnull.close()

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", str(e))

def display_checkmark(message):
    print("\u2714 " + message)


def display_error(message):
    print("\u2718 Error: " + message)


def display_notification(message):
    print("\u2728 " + message)

def enable_reset_ipsec():
    ipsec_service_remove()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    enable_reset = input(
        "\033[93mDo you want to enable \033[96mIPSEC \033[92mreset time\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m"
    ).lower()
    if enable_reset in ["yes", "y"]:
        print("\033[93m╭───────────────────────────────────────╮\033[0m")
        print("1. \033[92mHour\033[0m")
        print("2. \033[93mMinute\033[0m")
        print("\033[93m╰───────────────────────────────────────╯\033[0m")

        time_unit_choice = input("\033[93mEnter your choice :\033[0m ").strip()
        if time_unit_choice == "1":
            time_unit = "hour"
        elif time_unit_choice == "2":
            time_unit = "minute"
        else:
            print("\033[91mWrong choice\033[0m")
            return

        time_value = input(
            "\033[93mEnter the \033[92mdesired input\033[93m:\033[0m "
        ).strip()
        interval_seconds = (
            int(time_value) * 3600 if time_unit == "hour" else int(time_value) * 60
        )
        reset_ipsec(interval_seconds)
        print("\033[93m────────────────────────────────────────\033[0m")


def reset_ipsec(interval):
    service_name = "ipsecreset.service"

    daemon_script_content = f"""#!/bin/bash
INTERVAL={interval}

while true; do
    /bin/bash /etc/reset_ipsec.sh
    sleep $INTERVAL
done
"""

    with open("/usr/local/bin/ipsec_daemon.sh", "w") as daemon_script_file:
        daemon_script_file.write(daemon_script_content)

    subprocess.run(["chmod", "+x", "/usr/local/bin/ipsec_daemon.sh"])

    service_content = f"""[Unit]
Description=Custom Daemon

[Service]
ExecStart=/usr/local/bin/ipsec_daemon.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""

    with open(f"/etc/systemd/system/{service_name}", "w") as service_file:
        service_file.write(service_content)

    ipsec_reset_script_content = """#!/bin/bash
systemctl daemon-reload 
sudo ipsec stop
systemctl restart strong-azumi1 

"""

    with open("/etc/reset_ipsec.sh", "w") as script_file:
        script_file.write(ipsec_reset_script_content)

    subprocess.run(["chmod", "+x", "/etc/reset_ipsec.sh"])
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", service_name])
    subprocess.run(["systemctl", "restart", service_name])

def iran_eoip_1():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [1] Public IPv4\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[1]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[1]: \033[0m")
    
    
    dev_name = "eoipir1"
    eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 101 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_1", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_1", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir1(opposite_ip)
    ping_eoipir1_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip1(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip_2():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [2] Public IPv4\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[2]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[2]: \033[0m")
    
    dev_name = "eoipir2"
    eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 102 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_2", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_2", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir2(opposite_ip)
    ping_eoipir2_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip2(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip_3():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [3] Public IPv4\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[3]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[3]: \033[0m")
    
    dev_name = "eoipir3"
    eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 103 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_3", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_3", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir3(opposite_ip)
    ping_eoipir3_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip3(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")


def iran_eoip_4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [4] Public IPv4\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[4]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[4]: \033[0m")
    
    dev_name = "eoipir4"
    eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 104 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_4", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_4", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir4(opposite_ip)
    ping_eoipir4_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip4(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip_5():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [5] Public IPv4\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[5]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[5]: \033[0m")
    
    dev_name = "eoipir5"
    eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 105 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_5", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_5", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir5(opposite_ip)
    ping_eoipir5_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip5(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")


#v6
def iran_eoip6_1():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [1] Public IPv6\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[1]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[1]: \033[0m")
    
    dev_name = "eoipir1"
    eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 101 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_1", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_1", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir1(opposite_ip)
    ping_eoipir1_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip1(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip6_2():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [2] Public IPv6\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[2]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[2]: \033[0m")
    
    dev_name = "eoipir2"
    eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 102 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_2", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_2", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir2(opposite_ip)
    ping_eoipir2_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip2(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip6_3():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [3] Public IPv6\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[3]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[3]: \033[0m")
    
    dev_name = "eoipir3"
    eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 103 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_3", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_3", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir3(opposite_ip)
    ping_eoipir3_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip3(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip6_4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [4] Public IPv6\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[4]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[4]: \033[0m")
    
    dev_name = "eoipir4"
    eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 104 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_4", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_4", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir4(opposite_ip)
    ping_eoipir4_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip4(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iran_eoip6_5():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    iran_public_ip = input("\033[93mEnter \033[92mIran [5] Public IPv6\033[93m: \033[0m")
    kharej_public_ip = input("\033[93mEnter \033[92mKharej Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[5]: \033[0m") 
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[5]: \033[0m")
    
    dev_name = "eoipir5"
    eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id 105 mtu {mtu_value}"
    create_serviceeoip("eoip_iran_5", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("additional_irancmd_5", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir5(opposite_ip)
    ping_eoipir5_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip5(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")


def eoip_menu():
    os.system("clear")
    logo()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("0  \033[91mStatus\033[0m")
    print("1  \033[93mEOIP Public IPV4\033[0m")
    print("2  \033[92mEOIP Public IPV6\033[0m")
    print("3  \033[93mEdit Eoip\033[0m")
    print("4  \033[91mUninstall\033[0m")
    print("0. \033[94mback to the main script\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "0":
            eoip_status()
        elif choice == "1":
            eoip_ipv4()
            break
        elif choice == "2":
            eoip_ipv6()
            break
        elif choice == "3":
            eoip_editlocal()
            break
        elif choice == "4":
            eoip_uninstall()
            break
        elif choice == "0":
            clear()
            os._exit(0)
            break
        else:
            print("Invalid choice.")

def eoip_ipv4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V4\033[93m Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93m[1] Kharej [5] IRAN\033[0m")
    print("2  \033[92m[5] Kharej [1] IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            onekharej5iran_eoip_mnu()
            break
        elif choice == "2":
            oneiran5kharej_eoip_mnu()
            break
        elif choice == "0":
            clear()
            eoip_menu()
            break
        else:
            print("Invalid choice.")

def eoip_ipv6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93m[1] Kharej [5] IRAN\033[0m")
    print("2  \033[92m[5] Kharej [1] IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            onekharej5iran_eoip6_mnu()
            break
        elif choice == "2":
            oneiran5kharej_eoip6_mnu()
            break
        elif choice == "0":
            clear()
            eoip_menu()
            break
        else:
            print("Invalid choice.")

def onekharej5iran_eoip_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V4\033[93m [1]Kharej [5]IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1.\033[93m IRAN [1]\033[0m")
    print("2.\033[93m IRAN [2]\033[0m")
    print("3.\033[93m IRAN [3]\033[0m")
    print("4.\033[93m IRAN [4]\033[0m")
    print("5.\033[93m IRAN [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6.\033[92m Kharej\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    choice = input("\033[93mEnter your choice :\033[0m ")

    if choice == '1':
        iran_eoip_1()
    elif choice == '2':
        iran_eoip_2()
    elif choice == '3':
        iran_eoip_3()
    elif choice == '4':
        iran_eoip_4()
    elif choice == '5':
        iran_eoip_5()
    elif choice == '6':
        kharejserver_eoip()
    elif choice == '0':
        eoip_menu()

def oneiran5kharej_eoip_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V4\033[93m [1]IRAN [5]Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1.\033[93m Kharej [1]\033[0m")
    print("2.\033[93m Kharej [2]\033[0m")
    print("3.\033[93m Kharej [3]\033[0m")
    print("4.\033[93m Kharej [4]\033[0m")
    print("5.\033[93m Kharej [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6.\033[92m IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    choice = input("\033[93mEnter your choice :\033[0m ")

    if choice == '1':
        kharej_eoip_1()
    elif choice == '2':
        kharej_eoip_2()
    elif choice == '3':
        kharej_eoip_3()
    elif choice == '4':
        kharej_eoip_4()
    elif choice == '5':
        kharej_eoip_5()
    elif choice == '6':
        iranserver_eoip()
    elif choice == '0':
        eoip_menu()

def onekharej5iran_eoip6_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m [1]Kharej [5]IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1.\033[93m IRAN [1]\033[0m")
    print("2.\033[93m IRAN [2]\033[0m")
    print("3.\033[93m IRAN [3]\033[0m")
    print("4.\033[93m IRAN [4]\033[0m")
    print("5.\033[93m IRAN [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6.\033[92m Kharej\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    choice = input("\033[93mEnter your choice :\033[0m ")

    if choice == '1':
        iran_eoip6_1()
    elif choice == '2':
        iran_eoip6_2()
    elif choice == '3':
        iran_eoip6_3()
    elif choice == '4':
        iran_eoip6_4()
    elif choice == '5':
        iran_eoip6_5()
    elif choice == '6':
        kharejserver_eoip6()
    elif choice == '0':
        eoip_menu()

def oneiran5kharej_eoip6_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m [1]IRAN [5]Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1.\033[93m Kharej [1]\033[0m")
    print("2.\033[93m Kharej [2]\033[0m")
    print("3.\033[93m Kharej [3]\033[0m")
    print("4.\033[93m Kharej [4]\033[0m")
    print("5.\033[93m Kharej [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6.\033[92m IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    choice = input("\033[93mEnter your choice :\033[0m ")

    if choice == '1':
        kharej_eoip6_1()
    elif choice == '2':
        kharej_eoip6_2()
    elif choice == '3':
        kharej_eoip6_3()
    elif choice == '4':
        kharej_eoip6_4()
    elif choice == '5':
        kharej_eoip6_5()
    elif choice == '6':
        iranserver_eoip6()
    elif choice == '0':
        eoip_menu()

def kharej_eoip_1():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [1] Public IPv4\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[1]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[1]: \033[0m")
    
    dev_name = "eoipkh1"
    eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 101 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_1", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_1", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir1(opposite_ip)
    ping_eoipir1_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh1(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")


def kharej_eoip_2():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [2] Public IPv4\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[2]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[2]: \033[0m")
    
    dev_name = "eoipkh2"
    eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 102 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_2", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(2, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_2", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir2(opposite_ip)
    ping_eoipir2_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh2(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip_3():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [3] Public IPv4\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[3]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[3]: \033[0m")
    
    dev_name = "eoipkh3"
    eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 103 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_3", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_3", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir3(opposite_ip)
    ping_eoipir3_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh3(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip_4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [4] Public IPv4\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[4]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[4]: \033[0m")
    
    dev_name = "eoipkh4"
    eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 104 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_4", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_4", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir4(opposite_ip)
    ping_eoipir4_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh4(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip_5():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [5] Public IPv4\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[5]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[5]: \033[0m")
    
    dev_name = "eoipkh5"
    eoip_command = f"eoip -4 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 105 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_5", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_5", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir5(opposite_ip)
    ping_eoipir5_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh5(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iranserver_eoip():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V4\033[93m IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    num_servers = int(input("\033[93mHow many \033[92mKharej servers\033[93m do you have? \033[0m"))
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv4\033[93m: \033[0m")    
    
    kharej_public_ips = [input(f"\033[93mEnter \033[92mKharej \033[96m{i+1}\033[93m Public IPv4: \033[0m") for i in range(num_servers)]
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    private_ips = [input(f"\033[93mEnter \033[92mPrivate IP \033[93mfor Iran server {i+1}: \033[0m") for i in range(num_servers)]
    
    for i, kharej_public_ip in enumerate(kharej_public_ips, start=1):
        print("\033[93m───────────────────────────────────────\033[0m")
        mtu_value = input(f"\033[93mEnter \033[92mMTU value \033[93mfor \033[97mconfig \033[96m{i}: \033[0m")
        dev_name = f"eoipir{i}"
        eoip_command = f"eoip -4 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id {100 + i} mtu {mtu_value}"
        
        create_serviceeoip(f"eoip_iran_{i}", eoip_command)

        private_ip, subnet, script_path = additional_commands(i, private_ips[i - 1], dev=dev_name, ipv4=ipv4)
        
        display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")
        create_serviceeoip_additional(f"eoip_additional_irancmd_{i}", script_path)
        
        opposite_ip = calculate_oppose_ip(private_ips[i - 1], ipv4)
        script_eoip(opposite_ip, i)  
        ping_eoip_service(i)
    
    print("\033[93m────────────────────────────────────────\033[0m")
    
    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_server_eoip(psk, num_servers, private_ips, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def script_eoip_ir1(oppositeip):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = "/etc/ping_eoip_1.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoipir1_service():
    service_content = """[Unit]
Description=keepalive for EOIP
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_1.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = "/etc/systemd/system/ping_eoip_1.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_eoip_1"])
    subprocess.run(["systemctl", "start", "ping_eoip_1"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_eoip_1"])

def script_eoip_ir2(oppositeip):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = "/etc/ping_eoip_2.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoipir2_service():
    service_content = """[Unit]
Description=keepalive for EOIP
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_2.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = "/etc/systemd/system/ping_eoip_2.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_eoip_2"])
    subprocess.run(["systemctl", "start", "ping_eoip_2"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_eoip_2"])

def script_eoip_ir3(oppositeip):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = "/etc/ping_eoip_3.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoipir3_service():
    service_content = """[Unit]
Description=keepalive for EOIP
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_3.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = "/etc/systemd/system/ping_eoip_3.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_eoip_3"])
    subprocess.run(["systemctl", "start", "ping_eoip_3"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_eoip_3"])

def script_eoip_ir4(oppositeip):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = "/etc/ping_eoip_4.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoipir4_service():
    service_content = """[Unit]
Description=keepalive for EOIP
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_4.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = "/etc/systemd/system/ping_eoip_4.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_eoip_4"])
    subprocess.run(["systemctl", "start", "ping_eoip_4"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_eoip_4"])


def script_eoip_ir5(oppositeip):
    script_content = f"""#!/bin/bash
ip_address="{oppositeip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    script_path = "/etc/ping_eoip_5.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(script_path, 0o755)


def ping_eoipir5_service():
    service_content = """[Unit]
Description=keepalive for EOIP
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_eoip_5.sh
Restart=always

[Install]
WantedBy=multi-user.target
"""
    service_file_path = "/etc/systemd/system/ping_eoip_5.service"
    with open(service_file_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_eoip_5"])
    subprocess.run(["systemctl", "start", "ping_eoip_5"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_eoip_5"])

def kharej_eoip6_1():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [1] Public IPv6\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[1]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[1]: \033[0m")
    
    dev_name = "eoipkh1"
    eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 101 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_1", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_1", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir1(opposite_ip)
    ping_eoipir1_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh1(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip6_2():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [2] Public IPv6\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[2]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[2]: \033[0m")
    
    dev_name = "eoipkh2"
    eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 102 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_2", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_2", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir2(opposite_ip)
    ping_eoipir2_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh2(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")


def kharej_eoip6_3():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [3] Public IPv6\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[3]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[3]: \033[0m")
    
    dev_name = "eoipkh3"
    eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 103 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_3", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_3", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir3(opposite_ip)
    ping_eoipir3_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh3(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip6_4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [4] Public IPv6\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[4]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[4]: \033[0m")
    
    dev_name = "eoipkh4"
    eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 104 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_4", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_4", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir4(opposite_ip)
    ping_eoipir4_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh4(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def kharej_eoip6_5():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m Kharej [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    kharej_public_ip = input("\033[93mEnter \033[92mKharej [5] Public IPv6\033[93m: \033[0m")
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")
    
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    
    private_ip = input("\033[93mEnter \033[92mPrivate IP \033[93m[5]: \033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter \033[92mMTU value \033[92mfor EOIP tunnel \033[93m[5]: \033[0m")
    
    dev_name = "eoipkh5"
    eoip_command = f"eoip -6 {dev_name} local {kharej_public_ip} remote {iran_public_ip} id 105 mtu {mtu_value}"
    create_serviceeoip("eoip_kharej_5", eoip_command)
    
    private_ip, subnet, script_path = additional_commands(1, private_ip, dev=dev_name, ipv4=ipv4)

    display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")

    create_serviceeoip_additional("eoip_additional_kharej_5", script_path)
    opposite_ip = calculate_oppose_ip(private_ip, ipv4)
    script_eoip_ir5(opposite_ip)
    ping_eoipir5_service()
    
    print("\033[93m────────────────────────────────────────\033[0m")

    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_client_eoip_kh5(psk, private_ip, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def iranserver_eoip6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP V6\033[93m IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    
    eoip_directory = "/usr/local/bin/eoip"
    if os.path.exists(eoip_directory):
        print(f"\033[93meoip exists, skipping\033[0m")
    else:
        dependencies()
        clone_eoip()
        
    print("\033[93m───────────────────────────────────────\033[0m")
    
    num_servers = int(input("\033[93mHow many \033[92mKharej servers\033[93m do you have? \033[0m"))
    iran_public_ip = input("\033[93mEnter \033[92mIRAN Public IPv6\033[93m: \033[0m")    
    
    kharej_public_ips = [input(f"\033[93mEnter \033[92mKharej \033[96m{i+1}\033[93m Public IPv6: \033[0m") for i in range(num_servers)]
    ip_version = input("\033[93mAre you using \033[92mIPv4\033[93m or \033[96mIPv6\033[93m for private IPs? \033[97m(Enter 4 for IPv4, 6 for IPv6):\033[0m ")
    ipv4 = ip_version == "4"
    private_ips = [input(f"\033[93mEnter \033[92mPrivate IP \033[93mfor Iran server {i+1}: \033[0m") for i in range(num_servers)]
    
    for i, kharej_public_ip in enumerate(kharej_public_ips, start=1):
        print("\033[93m───────────────────────────────────────\033[0m")
        mtu_value = input(f"\033[93mEnter \033[92mMTU value \033[93mfor \033[97mconfig \033[96m{i}: \033[0m")
        dev_name = f"eoipir{i}"
        eoip_command = f"eoip -6 {dev_name} local {iran_public_ip} remote {kharej_public_ip} id {100 + i} mtu {mtu_value}"
        
        create_serviceeoip(f"eoip_iran_{i}", eoip_command)

        private_ip, subnet, script_path = additional_commands(i, private_ips[i - 1], dev=dev_name, ipv4=ipv4)
        
        display_checkmark(f"\033[92mConfigured EOIP for private IP: {private_ip} with subnet: {subnet}\033[0m")
        create_serviceeoip_additional(f"eoip_additional_irancmd_{i}", script_path)
        
        opposite_ip = calculate_oppose_ip(private_ips[i - 1], ipv4)
        script_eoip(opposite_ip, i)  
        ping_eoip_service(i)
    
    print("\033[93m────────────────────────────────────────\033[0m")
    
    ipsec_enable = input(
        "\033[93mDo you want \033[92mIPSEC Encryption \033[93mto be enabled? (\033[92myes\033[93m/\033[91mno\033[93m):\033[0m "
    ).lower()
    
    if ipsec_enable in ["yes", "y"]:
        psk = input("\033[93mEnter \033[92mIPSEC \033[93mSecret Key:\033[0m ")
        config_server_eoip(psk, num_servers, private_ips, ipv4=ipv4)
        print("\033[93m────────────────────────────────────────\033[0m")
        enable_reset_ipsec()
    
    print("\033[93m────────────────────────────────────────\033[0m")

def clear():
    os.system("clear")

def extrct_privateips(content):
    ipv4_pattern = r'\b(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3})\b'
    ipv6_pattern = r'\b(fc00:[0-9a-fA-F:]+|fd00:[0-9a-fA-F:]+)\b'

    ipv4_matches = re.findall(ipv4_pattern, content)
    ipv6_matches = re.findall(ipv6_pattern, content)

    return ipv4_matches + ipv6_matches

def eoip_uninstall():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEOIP Remove Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1. \033[92mEOIP Kharej [1] IRAN [5]\033[0m")
    print("2. \033[93mEOIP Kharej [5] IRAN [1]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "1":
            eoip_uninstall_5iran_1kharej()
            break
        elif server_type == "2":
            eoip_uninstall_5kharej_1iran()
            break
        elif server_type == "0":
            os.system("clear")
            eoip_menu()
            break
        else:
            print("Invalid choice.")

def eoip_uninstall_5kharej_1iran():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEOIP Remove Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1. \033[92mEOIP Kharej [1]\033[0m")
    print("2. \033[92mEOIP Kharej [2]\033[0m")
    print("3. \033[93mEOIP Kharej [3]\033[0m")
    print("4. \033[92mEOIP Kharej [4]\033[0m")
    print("5. \033[92mEOIP Kharej [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6. \033[93mEOIP IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "1":
            remove_eoip_kh1()
            break
        elif server_type == "2":
            remove_eoip_kh2()
            break
        elif server_type == "3":
            remove_eoip_kh3()
            break
        elif server_type == "4":
            remove_eoip_kh4()
            break
        elif server_type == "5":
            remove_eoip_kh5()
            break
        elif server_type == "6":
            remove_eoip_irservers()
            break
        elif server_type == "0":
            os.system("clear")
            eoip_uninstall()
            break
        else:
            print("Invalid choice.")

def remove_eoip_irservers():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEOIP Remove Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1. \033[92mEOIP IRAN Config [1]\033[0m")
    print("2. \033[92mEOIP IRAN Config [2]\033[0m")
    print("3. \033[93mEOIP IRAN Config [3]\033[0m")
    print("4. \033[92mEOIP IRAN Config [4]\033[0m")
    print("5. \033[92mEOIP IRAN Config [5]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "1":
            remove_eoip_ir1()
            break
        elif server_type == "2":
            remove_eoip_ir2()
            break
        elif server_type == "3":
            remove_eoip_ir3()
            break
        elif server_type == "4":
            remove_eoip_ir4()
            break
        elif server_type == "5":
            remove_eoip_ir5()
            break
        elif server_type == "0":
            os.system("clear")
            eoip_uninstall_5kharej_1iran()
            break
        else:
            print("Invalid choice.")

def eoip_uninstall_5iran_1kharej():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEOIP Remove Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1. \033[92mEOIP IRAN [1]\033[0m")
    print("2. \033[92mEOIP IRAN [2]\033[0m")
    print("3. \033[93mEOIP IRAN [3]\033[0m")
    print("4. \033[92mEOIP IRAN [4]\033[0m")
    print("5. \033[92mEOIP IRAN [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6. \033[93mEOIP Kharej\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "1":
            remove_eoip_ir1()
            break
        elif server_type == "2":
            remove_eoip_ir2()
            break
        elif server_type == "3":
            remove_eoip_ir3()
            break
        elif server_type == "4":
            remove_eoip_ir4()
            break
        elif server_type == "5":
            remove_eoip_ir5()
            break
        elif server_type == "6":
            remove_eoip_khservers()
            break
        elif server_type == "0":
            os.system("clear")
            eoip_uninstall()
            break
        else:
            print("Invalid choice.")

def remove_eoip_khservers():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mEOIP Remove Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1. \033[92mEOIP Kharej Config [1]\033[0m")
    print("2. \033[92mEOIP Kharej Config [2]\033[0m")
    print("3. \033[93mEOIP Kharej Config [3]\033[0m")
    print("4. \033[92mEOIP Kharej Config [4]\033[0m")
    print("5. \033[92mEOIP Kharej Config [5]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if server_type == "1":
            remove_eoip_kh1()
            break
        elif server_type == "2":
            remove_eoip_kh2()
            break
        elif server_type == "3":
            remove_eoip_kh3()
            break
        elif server_type == "4":
            remove_eoip_kh4()
            break
        elif server_type == "5":
            remove_eoip_kh5()
            break
        elif server_type == "0":
            os.system("clear")
            eoip_uninstall_5iran_1kharej()
            break
        else:
            print("Invalid choice.")

def remove_eoip_kh1():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_1.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_1.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_1.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_kharej_1.service",
            "/etc/systemd/system/eoip_additional_kharej_1.service"
        ]
        
        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_1", "strong-azumi1",
            "eoip_kharej_1", "eoip_additional_kharej_1"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)
        
        try:
            subprocess.run("ip link set dev eoipkh1 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipkh1 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("not possible to bring down or delete eoipkh1 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("deleting eoip wasn't possible. Continuing..")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing..")

def remove_eoip_kh2():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_2.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File {file_path} not found. Continuing..")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_2.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_2.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_kharej_2.service",
            "/etc/systemd/system/eoip_additional_kharej_2.service"
        ]
        
        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_2", "strong-azumi1",
            "eoip_kharej_2", "eoip_additional_kharej_2"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)
        
        try:
            subprocess.run("ip link set dev eoipkh2 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipkh2 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("not possible to bring down or delete eoipkh2 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("deleting eoip wasn't possible. Continuing..")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing..")

def remove_eoip_kh3():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_3.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File {file_path} not found. Continuing..")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_3.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_3.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_kharej_3.service",
            "/etc/systemd/system/eoip_additional_kharej_3.service"
        ]
        
        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_3", "strong-azumi1",
            "eoip_kharej_3", "eoip_additional_kharej_3"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)
        
        try:
            subprocess.run("ip link set dev eoipkh3 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipkh3 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("not possible to bring down or delete eoipkh3 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("deleting eoip wasn't possible. Continuing..")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing..")

def remove_eoip_kh4():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_4.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File {file_path} not found. Continuing..")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_4.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_4.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_kharej_4.service",
            "/etc/systemd/system/eoip_additional_kharej_4.service"
        ]
        
        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_4", "strong-azumi1",
            "eoip_kharej_4", "eoip_additional_kharej_4"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)
        
        try:
            subprocess.run("ip link set dev eoipkh4 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipkh4 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("not possible to bring down or delete eoipkh4 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("deleting eoip wasn't possible. Continuing..")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing..")


def remove_eoip_kh5():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_5.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File {file_path} not found. Continuing..")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_5.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_5.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_kharej_5.service",
            "/etc/systemd/system/eoip_additional_kharej_5.service"
        ]
        
        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_5", "strong-azumi1",
            "eoip_kharej_5", "eoip_additional_kharej_5"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)
        
        try:
            subprocess.run("ip link set dev eoipkh5 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipkh5 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("not possible to bring down or delete eoipkh5 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("deleting eoip wasn't possible. Continuing..")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing..")

def remove_eoip_ir1():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_1.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_1.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_1.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_iran_1.service",
            "/etc/systemd/system/additional_irancmd_1.service"
        ]

        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_1", "strong-azumi1",
            "eoip_iran_1", "additional_irancmd_1"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)

        try:
            subprocess.run("ip link set dev eoipir1 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipir1 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Not possible to bring down or delete eoipir1 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("Deleting eoip wasn't possible. Continuing...")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing...")

def remove_eoip_ir2():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_2.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_2.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_2.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_iran_2.service",
            "/etc/systemd/system/additional_irancmd_2.service"
        ]

        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_2", "strong-azumi1",
            "eoip_iran_2", "additional_irancmd_2"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)

        try:
            subprocess.run("ip link set dev eoipir2 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipir2 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Not possible to bring down or delete eoipir2 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("Deleting eoip wasn't possible. Continuing...")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing...")

def remove_eoip_ir3():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_3.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_3.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_3.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_iran_3.service",
            "/etc/systemd/system/additional_irancmd_3.service"
        ]

        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_3", "strong-azumi1",
            "eoip_iran_3", "additional_irancmd_3"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)

        try:
            subprocess.run("ip link set dev eoipir3 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipir3 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Not possible to bring down or delete eoipir3 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("Deleting eoip wasn't possible. Continuing...")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing...")

def remove_eoip_ir4():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_4.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_4.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_4.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_iran_4.service",
            "/etc/systemd/system/additional_irancmd_4.service"
        ]

        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_4", "strong-azumi1",
            "eoip_iran_4", "additional_irancmd_4"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)

        try:
            subprocess.run("ip link set dev eoipir4 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipir4 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Not possible to bring down or delete eoipir4 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("Deleting eoip wasn't possible. Continuing...")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing...")

def remove_eoip_ir5():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mEOIP\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        file_path = "/usr/local/bin/cmd/eoip_additional_commands_5.sh"
        private_ips = []

        try:
            with open(file_path, 'r') as file:
                content = file.read()
                private_ips = extrct_privateips(content)
        except FileNotFoundError:
            print(f"File not found. Continuing...")

        if private_ips:
            for private_ip in private_ips:
                try:
                    subprocess.run(f"sudo ufw delete allow from {private_ip}", shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Failed to delete rule for IP {private_ip}. Continuing...")

        files_to_remove = [
            file_path,
            "/etc/ping_eoip.sh",
            "/etc/ping_eoip_5.sh",
            "/etc/ipsec1.conf",
            "/etc/ipsec.secrets",
            "/etc/systemd/system/ping_eoip.service",
            "/etc/systemd/system/ping_eoip_5.service",
            "/etc/systemd/system/strong-azumi1.service",
            "/etc/systemd/system/eoip_iran_5.service",
            "/etc/systemd/system/additional_irancmd_5.service"
        ]

        for file in files_to_remove:
            subprocess.run(f"sudo rm {file} > /dev/null 2>&1", shell=True)

        services_to_disable_stop = [
            "ping_eoip", "ping_eoip_5", "strong-azumi1",
            "eoip_iran_5", "additional_irancmd_5"
        ]

        for service in services_to_disable_stop:
            try:
                subprocess.run(f"systemctl stop {service} > /dev/null 2>&1", shell=True)
                subprocess.run(f"systemctl disable {service} > /dev/null 2>&1", shell=True)
            except subprocess.CalledProcessError:
                print(f"Failed to stop or disable {service}. Continuing...")

        subprocess.run("systemctl daemon-reload", shell=True)

        try:
            subprocess.run("ip link set dev eoipir5 down > /dev/null", shell=True, check=True)
            subprocess.run("ip link delete eoipir5 > /dev/null", shell=True, check=True)
        except subprocess.CalledProcessError:
            print("Not possible to bring down or delete eoipir5 interface. Continuing...")

        user_input = input("\033[93mDo you want to delete \033[92meoip \033[93mproject? (\033[92my\033[93m/\033[91mn\033[93m): \033[0m").strip().lower()

        if user_input in ['yes', 'y']:
            try:
                subprocess.run("sudo rm /usr/local/sbin/eoip", shell=True, check=True)
                subprocess.run("sudo rm -rf /usr/local/bin/eoip", shell=True, check=True)
                print("\033[92mdirectory has been deleted\033[0m")
            except subprocess.CalledProcessError:
                print("Deleting eoip wasn't possible. Continuing...")
        else:
            print("\033[92mSkip deleting\033[0m")

        print("Progress: ", end="")
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 1
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print(f"\r[{frame}] Loading...  ", end="")
                time.sleep(delay)
                print(f"\r[{frame}]             ", end="")
                time.sleep(delay)

        display_checkmark("\033[92mUninstall completed!\033[0m")

    except Exception as e:
        print(f"error: {str(e)}. Continuing...")

SERVICE_FILE_IRAN1 = "/etc/systemd/system/eoip_iran_1.service"
SERVICE_FILE_IRAN2 = "/etc/systemd/system/eoip_iran_2.service"
SERVICE_FILE_IRAN3 = "/etc/systemd/system/eoip_iran_3.service"
SERVICE_FILE_IRAN4 = "/etc/systemd/system/eoip_iran_4.service"
SERVICE_FILE_IRAN5 = "/etc/systemd/system/eoip_iran_5.service"
SERVICE_FILE_KHAREJ1 = "/etc/systemd/system/eoip_kharej_1.service"
SERVICE_FILE_KHAREJ2 = "/etc/systemd/system/eoip_kharej_2.service"
SERVICE_FILE_KHAREJ3 = "/etc/systemd/system/eoip_kharej_3.service"
SERVICE_FILE_KHAREJ4 = "/etc/systemd/system/eoip_kharej_4.service"
SERVICE_FILE_KHAREJ5 = "/etc/systemd/system/eoip_kharej_5.service"
PRIVATE_IP_FILE1 = "/usr/local/bin/cmd/eoip_additional_commands_1.sh"
PRIVATE_IP_FILE2 = "/usr/local/bin/cmd/eoip_additional_commands_2.sh"
PRIVATE_IP_FILE3 = "/usr/local/bin/cmd/eoip_additional_commands_3.sh"
PRIVATE_IP_FILE4 = "/usr/local/bin/cmd/eoip_additional_commands_4.sh"
PRIVATE_IP_FILE5 = "/usr/local/bin/cmd/eoip_additional_commands_5.sh"
IPSEC_CONF_FILE = "/etc/ipsec1.conf"
IPSEC_SECRETS_FILE = "/etc/ipsec.secrets"
PING_SCRIPT_PATH1 = '/etc/ping_eoip_1.sh'
PING_SCRIPT_PATH2 = '/etc/ping_eoip_2.sh'
PING_SCRIPT_PATH3 = '/etc/ping_eoip_3.sh'
PING_SCRIPT_PATH4 = '/etc/ping_eoip_4.sh'
PING_SCRIPT_PATH5 = '/etc/ping_eoip_5.sh'
SERVICE_FILE_PING1 = '/etc/systemd/system/ping_eoip_1.service'
SERVICE_FILE_PING2 = '/etc/systemd/system/ping_eoip_2.service'
SERVICE_FILE_PING3 = '/etc/systemd/system/ping_eoip_3.service'
SERVICE_FILE_PING4 = '/etc/systemd/system/ping_eoip_4.service'
SERVICE_FILE_PING5 = '/etc/systemd/system/ping_eoip_5.service'
ADDITIONAL_SERVICE_IRAN1 = "/etc/systemd/system/additional_irancmd_1.service"
ADDITIONAL_SERVICE_IRAN2 = "/etc/systemd/system/additional_irancmd_2.service"
ADDITIONAL_SERVICE_IRAN3 = "/etc/systemd/system/additional_irancmd_3.service"
ADDITIONAL_SERVICE_IRAN4 = "/etc/systemd/system/additional_irancmd_4.service"
ADDITIONAL_SERVICE_IRAN5 = "/etc/systemd/system/additional_irancmd_5.service"
ADDITIONAL_SERVICE_KHAREJ1 = "/etc/systemd/system/eoip_additional_kharej_1.service"
ADDITIONAL_SERVICE_KHAREJ2 = "/etc/systemd/system/eoip_additional_kharej_2.service"
ADDITIONAL_SERVICE_KHAREJ3 = "/etc/systemd/system/eoip_additional_kharej_3.service"
ADDITIONAL_SERVICE_KHAREJ4 = "/etc/systemd/system/eoip_additional_kharej_4.service"
ADDITIONAL_SERVICE_KHAREJ5 = "/etc/systemd/system/eoip_additional_kharej_5.service"

def eoip_editlocal():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Edit Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1  \033[93m[1] Kharej [5] IRAN\033[0m")
    print("2  \033[92m[5] Kharej [1] IRAN\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            eoip_edit_1kharej_5iran()
            break
        elif choice == "2":
            eoip_edit_5kharej_1iran()
            break
        elif choice == "0":
            clear()
            eoip_menu()
            break
        else:
            print("Invalid choice.")

def eoip_edit_5kharej_1iran():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP Kharej\033[93m Edit Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1  \033[93mKharej [1]\033[0m")
    print("2  \033[93mKharej [2]\033[0m")
    print("3  \033[93mKharej [3]\033[0m")
    print("4  \033[93mKharej [4]\033[0m")
    print("5  \033[93mKharej [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6  \033[93mIRAN configs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            edit_local_eoip_kharej1()
            break
        elif choice == "2":
            edit_local_eoip_kharej2()
            break
        elif choice == "3":
            edit_local_eoip_kharej3()
            break
        elif choice == "4":
            edit_local_eoip_kharej4()
            break
        elif choice == "5":
            edit_local_eoip_kharej5()
            break
        elif choice == "6":
            edit_local_eoip_iranmenu()
            break
        elif choice == "0":
            clear()
            eoip_editlocal()
            break
        else:
            print("Invalid choice.")

def edit_local_eoip_iranmenu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP IRAN\033[93m Edit Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1  \033[93mIRAN config [1]\033[0m")
    print("2  \033[93mIRAN config [2]\033[0m")
    print("3  \033[92mIRAN config [3]\033[0m")
    print("4  \033[93mIRAN config [4]\033[0m")
    print("5  \033[93mIRAN config [5]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            edit_local_eoip_iranconfig1()
            break
        elif choice == "2":
            edit_local_eoip_iranconfig2()
            break
        elif choice == "3":
            edit_local_eoip_iranconfig3()
            break
        elif choice == "4":
            edit_local_eoip_iranconfig4()
            break
        elif choice == "5":
            edit_local_eoip_iranconfig5()
            break
        elif choice == "0":
            clear()
            eoip_edit_5kharej_1iran()
            break
        else:
            print("Invalid choice.")

# 1 kharej 5iran
def eoip_edit_1kharej_5iran():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP IRAN\033[93m Edit Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1  \033[93mIRAN [1]\033[0m")
    print("2  \033[93mIRAN [2]\033[0m")
    print("3  \033[93mIRAN [3]\033[0m")
    print("4  \033[93mIRAN [4]\033[0m")
    print("5  \033[93mIRAN [5]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("6  \033[93mKharej configs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            edit_local_eoip_iran1()
            break
        elif choice == "2":
            edit_local_eoip_iran2()
            break
        elif choice == "3":
            edit_local_eoip_iran3()
            break
        elif choice == "4":
            edit_local_eoip_iran4()
            break
        elif choice == "5":
            edit_local_eoip_iran5()
            break
        elif choice == "6":
            edit_local_eoip_kharejmenu()
            break
        elif choice == "0":
            clear()
            eoip_editlocal()
            break
        else:
            print("Invalid choice.")

def edit_local_eoip_kharejmenu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP Kharej\033[93m Edit Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("1  \033[93mKharej config [1]\033[0m")
    print("2  \033[93mKharej config [2]\033[0m")
    print("3  \033[92mKharej config [3]\033[0m")
    print("4  \033[93mKharej config [4]\033[0m")
    print("5  \033[93mKharej config [5]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            edit_local_eoip_kharejconfig1()
            break
        elif choice == "2":
            edit_local_eoip_kharejconfig2()
            break
        elif choice == "3":
            edit_local_eoip_kharejconfig3()
            break
        elif choice == "4":
            edit_local_eoip_kharejconfig4()
            break
        elif choice == "5":
            edit_local_eoip_kharejconfig5()
            break
        elif choice == "0":
            clear()
            eoip_edit_1kharej_5iran()
            break
        else:
            print("Invalid choice.")

def extract_ips(service_file):
    with open(service_file, 'r') as f:
        content = f.read()
    local_ip = re.search(r"local (\S+)", content).group(1)
    remote_ip = re.search(r"remote (\S+)", content).group(1)
    return local_ip, remote_ip


def extract_ipsec_secrets():
    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return None, None, None

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        content = f.read()
    ip_pair = re.search(r"(\S+) (\S+) : PSK \"(.*?)\"", content)
    if ip_pair:
        left_ip, right_ip, secret_key = ip_pair.groups()
        return left_ip, right_ip, secret_key
    return None, None, None

def calculate_opposite_ip(ip):
    if ':' in ip:  
        return re.sub(r"::(\d+)", lambda m: f"::{int(m.group(1)) + 1}", ip)
    else:  
        parts = ip.split('.')
        parts[-1] = str(int(parts[-1]) + 1)
        return '.'.join(parts)
#1
def extract_private_ip1():
    with open(PRIVATE_IP_FILE1, 'r') as f:
        content = f.read()
    private_ip = re.search(r"ip addr add (\S+)/", content).group(1)
    return private_ip

def extract_private_ip2():
    with open(PRIVATE_IP_FILE2, 'r') as f:
        content = f.read()
    private_ip = re.search(r"ip addr add (\S+)/", content).group(1)
    return private_ip

def extract_private_ip3():
    with open(PRIVATE_IP_FILE3, 'r') as f:
        content = f.read()
    private_ip = re.search(r"ip addr add (\S+)/", content).group(1)
    return private_ip

def extract_private_ip4():
    with open(PRIVATE_IP_FILE4, 'r') as f:
        content = f.read()
    private_ip = re.search(r"ip addr add (\S+)/", content).group(1)
    return private_ip

def extract_private_ip5():
    with open(PRIVATE_IP_FILE5, 'r') as f:
        content = f.read()
    private_ip = re.search(r"ip addr add (\S+)/", content).group(1)
    return private_ip

def update_ipsec_conf_and_secrets_kh1(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipkh1.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_kh2(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipkh2.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_kh3(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipkh3.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_kh4(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipkh4.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_kh5(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipkh5.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_ir1(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipir1.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_ir2(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipir2.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_ir3(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipir3.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_ir4(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipir4.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_ipsec_conf_and_secrets_ir5(new_ip):
    opposite_ip = calculate_opposite_ip(new_ip)

    if not os.path.exists(IPSEC_CONF_FILE):
        print("\033[91mError:\033[0m Ipsec not available.")
        return

    with open(IPSEC_CONF_FILE, 'r') as f:
        ipsec_content = f.read()

    conn_block = re.search(r"(conn eoip_eoipir5.*?)(?=conn|\Z)", ipsec_content, re.DOTALL)
    if conn_block:
        conn_block_content = conn_block.group(1)

        conn_block_content = re.sub(r"leftid=\S+", f"leftid={new_ip}", conn_block_content)
        conn_block_content = re.sub(r"leftsubnet=\S+", f"leftsubnet={new_ip}/64", conn_block_content)

        conn_block_content = re.sub(r"right=\S+", f"right={opposite_ip}", conn_block_content)
        conn_block_content = re.sub(r"rightsubnet=\S+", f"rightsubnet={opposite_ip}/64", conn_block_content)

        ipsec_content = ipsec_content.replace(conn_block.group(1), conn_block_content)

        with open(IPSEC_CONF_FILE, 'w') as f:
            f.write(ipsec_content)

    if not os.path.exists(IPSEC_SECRETS_FILE):
        print("\033[91mError:\033[0m PSK not available.")
        return

    with open(IPSEC_SECRETS_FILE, 'r') as f:
        secrets_content = f.read()

    updated_secrets = re.sub(r"(\S+) (\S+) : PSK ", f"{opposite_ip} {new_ip} : PSK ", secrets_content)

    with open(IPSEC_SECRETS_FILE, 'w') as f:
        f.write(updated_secrets)

def update_private_ip_kh1(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return

    with open(PRIVATE_IP_FILE1, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    
    with open(PRIVATE_IP_FILE1, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH1)
    restart_ping_service(SERVICE_FILE_PING1)
    update_ipsec_conf_and_secrets_kh1(new_ip)

def update_ping_script(new_ip, ping_script_path):
    opposite_ip = calculate_opposite_ip(new_ip)
    script_content = f"""#!/bin/bash
ip_address="{opposite_ip}"
max_pings=5
interval=2
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" '{{{{print $2}}}}' | awk '{{{{print $1}}}}' | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
"""
    with open(ping_script_path, "w") as script_file:
        script_file.write(script_content)

    os.chmod(ping_script_path, 0o755)


def restart_ping_service(service_file):
    if not os.path.exists(service_file):
        print(f"\033[91mError:\033[0m {service_file} does not exist. Exiting...")
        return
    
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', os.path.basename(service_file)])

def update_private_ip_kh2(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return

    with open(PRIVATE_IP_FILE2, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    
    with open(PRIVATE_IP_FILE2, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH2)
    restart_ping_service(SERVICE_FILE_PING2)
    update_ipsec_conf_and_secrets_kh2(new_ip)


def update_private_ip_kh3(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE3, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE3, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH3)

    restart_ping_service(SERVICE_FILE_PING3)

    update_ipsec_conf_and_secrets_kh3(new_ip)

def update_private_ip_kh4(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE4, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE4, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH4)

    restart_ping_service(SERVICE_FILE_PING4)

    update_ipsec_conf_and_secrets_kh4(new_ip)

def update_private_ip_kh5(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE5, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE5, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH5)

    restart_ping_service(SERVICE_FILE_PING5)

    update_ipsec_conf_and_secrets_kh5(new_ip)

def update_private_ip_ir1(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE1, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE1, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH1)

    restart_ping_service(SERVICE_FILE_PING1)

    update_ipsec_conf_and_secrets_ir1(new_ip)

def update_private_ip_ir2(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE2, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE2, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH2)

    restart_ping_service(SERVICE_FILE_PING2)

    update_ipsec_conf_and_secrets_ir2(new_ip)

def update_private_ip_ir3(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE3, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE3, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH3)

    restart_ping_service(SERVICE_FILE_PING3)

    update_ipsec_conf_and_secrets_ir3(new_ip)

def update_private_ip_ir4(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE4, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE4, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH4)

    restart_ping_service(SERVICE_FILE_PING4)

    update_ipsec_conf_and_secrets_ir4(new_ip)


def update_private_ip_ir5(new_ip):
    try:
        ip = ipaddress.ip_address(new_ip)
        if ip.version == 4:
            cidr = 24
        elif ip.version == 6:
            cidr = 64
        else:
            raise ValueError("unsupported IP")
    except ValueError as e:
        print(f"Wrong IP address: {e}")
        return
    
    with open(PRIVATE_IP_FILE5, 'r') as f:
        content = f.read()

    updated_content = re.sub(r"ip addr add \S+/\d+", f"ip addr add {new_ip}/{cidr}", content)
    with open(PRIVATE_IP_FILE5, 'w') as f:
        f.write(updated_content)

    update_ping_script(new_ip, PING_SCRIPT_PATH5)

    restart_ping_service(SERVICE_FILE_PING5)

    update_ipsec_conf_and_secrets_ir5(new_ip)

def save_and_restart_services_kharej1():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_kharej_1'])
    subprocess.run(['systemctl', 'restart', 'eoip_additional_kharej_1'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_1'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_kharej2():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_kharej_2'])
    subprocess.run(['systemctl', 'restart', 'eoip_additional_kharej_2'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_2'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_kharej3():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_kharej_3'])
    subprocess.run(['systemctl', 'restart', 'eoip_additional_kharej_3'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_3'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_kharej4():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_kharej_4'])
    subprocess.run(['systemctl', 'restart', 'eoip_additional_kharej_4'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_4'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_kharej5():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_kharej_5'])
    subprocess.run(['systemctl', 'restart', 'eoip_additional_kharej_5'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_5'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_iran1():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_iran_1'])
    subprocess.run(['systemctl', 'restart', 'additional_irancmd_1'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_1'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_iran2():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_iran_2'])
    subprocess.run(['systemctl', 'restart', 'additional_irancmd_2'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_2'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_iran3():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_iran_3'])
    subprocess.run(['systemctl', 'restart', 'additional_irancmd_3'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_3'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_iran4():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_iran_4'])
    subprocess.run(['systemctl', 'restart', 'additional_irancmd_4'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_4'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def save_and_restart_services_iran5():
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'restart', 'eoip_iran_5'])
    subprocess.run(['systemctl', 'restart', 'additional_irancmd_5'])
    subprocess.run(['systemctl', 'restart', 'ping_eoip_5'])
    subprocess.run(['systemctl', 'restart', 'strong-azumi1'])

def display_status_box_kharej1():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_KHAREJ1)
    private_ip = extract_private_ip1()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mKharej IP: \033[97m {local_ip}\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:  \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_kharej2():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_KHAREJ2)
    private_ip = extract_private_ip2()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mKharej IP: \033[97m {local_ip}\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:  \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_kharej3():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_KHAREJ3)
    private_ip = extract_private_ip3()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mKharej IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mIRAN IP:     \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:  \033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:    \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_kharej4():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_KHAREJ4)
    private_ip = extract_private_ip4()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mKharej IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mIRAN IP:     \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:  \033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:    \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_kharej5():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_KHAREJ5)
    private_ip = extract_private_ip5()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m Kharej [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mKharej IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mIRAN IP:     \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:  \033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:    \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_iran1():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_IRAN1)
    private_ip = extract_private_ip1()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [1] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mKharej IP: \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:  \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_iran2():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_IRAN2)
    private_ip = extract_private_ip2()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [2] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m   {local_ip}\033[0m")
    print(f"\033[93mKharej IP: \033[97m   {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m   {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:   \033[97m \"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_iran3():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_IRAN3)
    private_ip = extract_private_ip3()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [3] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m   {local_ip}\033[0m")
    print(f"\033[93mKharej IP: \033[97m   {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m   {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:   \033[97m \"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_iran4():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_IRAN4)
    private_ip = extract_private_ip4()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [4] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mKharej IP: \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:  \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def display_status_box_iran5():
    os.system("clear")
    local_ip, remote_ip = extract_ips(SERVICE_FILE_IRAN5)
    private_ip = extract_private_ip5()
    left_ip, right_ip, secret_key = extract_ipsec_secrets()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mEOIP\033[93m IRAN [5] Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭─────────\033[97mCurrent Config\033[93m──────────────╮\033[0m")
    print(f"\033[93mIRAN IP:   \033[97m {local_ip}\033[0m")
    print(f"\033[93mKharej IP: \033[97m {remote_ip}\033[0m")
    print(f"\033[93mPrivate IP:\033[97m {private_ip}\033[0m")
    if left_ip and right_ip:
        print(f"\033[93mPSK:  \033[97m\"{secret_key}\"\033[0m")
    else:
        print("\033[91mPSK information not available.\033[0m")
    print("\033[93m╰─────────────────────────────────────╯\033[0m")

def update_service_file(service_file, ip_type, new_ip):
    with open(service_file, 'r') as f:
        content = f.read()
    updated_content = re.sub(fr"{ip_type} \S+", f"{ip_type} {new_ip}", content)
    with open(service_file, 'w') as f:
        f.write(updated_content)

def edit_local_eoip_kharej1():
    """Allows the user to edit the Kharej1 EOIP configuration."""
    while True:
        display_status_box_kharej1()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej [1]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ1)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej [1]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ1, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ1)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ1, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip1()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh1(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej1()
            print("Changes saved and services restarted.")
        elif choice == '5':
            os.system("clear")
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Please try again.\033[0m")

def edit_local_eoip_kharej2():
    while True:
        display_status_box_kharej2()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej [2]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ2)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej [2]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ2, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ2)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ2, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip2()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh2(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej2()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")


def edit_local_eoip_kharej3():
    while True:
        display_status_box_kharej3()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej [3]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ3)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej [3]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ3, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ3)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ3, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip3()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh3(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej3()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharej4():
    while True:
        display_status_box_kharej4()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej [4]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ4)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej [4]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ4, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ4)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ4, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip4()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh4(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej4()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharej5():
    while True:
        display_status_box_kharej5()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej [5]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ5)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej [5]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ5, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ5)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ5, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip5()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh5(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej5()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iranconfig1():
    while True:
        display_status_box_iran1()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej [1] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN1)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN1, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN1)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej [1] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN1, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip1()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir1(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran1()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iranconfig2():
    while True:
        display_status_box_iran2()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej [2] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN2)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN2, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN2)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej [2] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN2, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip2()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir2(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran2()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iranconfig3():
    while True:
        display_status_box_iran3()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej [3] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN3)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN3, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN3)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej [3] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN3, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip3()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir3(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran3()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iranconfig4():
    while True:
        display_status_box_iran4()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej [4] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN4)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN4, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN4)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej [4] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN4, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip4()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir4(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran4()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iranconfig5():
    while True:
        display_status_box_iran5()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej [5] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN5)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN5, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN5)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej [5] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN5, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip5()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir5(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran5()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_5kharej_1iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharejconfig1():
    while True:
        display_status_box_kharej1()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN [1] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ1)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ1, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ1)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN [1] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ1, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip1()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh1(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej1()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharejconfig2():
    while True:
        display_status_box_kharej2()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN [2] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ2)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ2, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ2)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN [2] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ2, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip2()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh2(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej2()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharejconfig3():
    while True:
        display_status_box_kharej3()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN [3] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ3)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ3, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ3)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN [3] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ3, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip3()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh3(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej3()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharejconfig4():
    while True:
        display_status_box_kharej4()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN [4] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ4)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ4, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ4)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN [4] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ4, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip4()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh4(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej4()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_kharejconfig5():
    while True:
        display_status_box_kharej5()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mKharej\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mIRAN [5] IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_KHAREJ5)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mKharej\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ5, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_KHAREJ5)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mIRAN [5] \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_KHAREJ5, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip5()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_kh5(new_private_ip)
        elif choice == '4':
            save_and_restart_services_kharej5()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iran1():
    while True:
        display_status_box_iran1()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN [1]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN1)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN [1]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN1, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN1)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN1, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip1()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir1(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran1()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iran2():
    while True:
        display_status_box_iran2()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN [2]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN2)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN [2]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN2, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN2)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN2, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip2()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir2(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran2()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iran3():
    while True:
        display_status_box_iran3()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN [3]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN3)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN [3]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN3, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN3)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN3, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip3()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir3(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran3()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iran4():
    while True:
        display_status_box_iran4()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN [4]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN4)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN [4]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN4, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN4)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN4, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip4()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir4(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran4()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

def edit_local_eoip_iran5():
    while True:
        display_status_box_iran5()
        print("\033[93m───────────────────────────────────────\033[0m")
        print("1.\033[93m Change \033[92mIRAN [5]\033[93m IP\033[0m")
        print("2.\033[93m Change \033[92mKharej IP\033[0m")
        print("3.\033[93m Change Private IP\033[0m")
        print("4.\033[92m Save and Restart Services\033[0m")
        print("5.\033[97m back to the menu\033[0m")
        print("\033[93m───────────────────────────────────────\033[0m")

        choice = input("Enter your choice: ")

        if choice == '1':
            local_ip, _ = extract_ips(SERVICE_FILE_IRAN5)
            print(f"\033[93mCurrent Local IP: \033[97m{local_ip}\033[0m")
            new_local_ip = input("\033[92mEnter New \033[97mIRAN [5]\033[92m IP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN5, "local", new_local_ip)
        elif choice == '2':
            _, remote_ip = extract_ips(SERVICE_FILE_IRAN5)
            print(f"\033[93mCurrent Remote IP: \033[97m{remote_ip}\033[0m")
            new_remote_ip = input("\033[92mEnter New \033[97mKharej \033[92mIP: \033[0m")
            update_service_file(SERVICE_FILE_IRAN5, "remote", new_remote_ip)
        elif choice == '3':
            private_ip = extract_private_ip5()
            print(f"\033[93mCurrent Private IP: \033[97m{private_ip}\033[0m")
            new_private_ip = input("\033[92mEnter new \033[97mPrivate IP\033[92m: \033[0m")
            update_private_ip_ir5(new_private_ip)
        elif choice == '4':
            save_and_restart_services_iran5()
            print("Changes saved and services restarted.")
        elif choice == '5':
            clear()
            eoip_edit_1kharej_5iran()
        else:
            print("\033[91mWrong choice. Plz try again\033[0m")

eoip_menu()
