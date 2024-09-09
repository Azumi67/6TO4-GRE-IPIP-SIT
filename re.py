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

def clear():
    os.system("clear")
    
def robot_menu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot\033[93m Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mSingle\033[0m")
    print("2  \033[92mMulti \033[97m[IP6IP6 Added]\033[0m")
    print("0. \033[94mback to the main script\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_mnu()
            break
        elif choice == "2":
            robot_multi_mnu()
            break
        elif choice == "0":
            clear()
            os._exit(0)
            break
        else:
            print("Invalid choice.")
            
def robot_single_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mSingle\033[93m Robot Menu\033[0m"
    )
    print('\033[92m "-"\033[93m══════════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mWhich one to edit:\033[0m")
    print("1.  \033[92m IP6IP6\033[0m")
    print("2.  \033[93m IP6IP6 + IPSEC\033[0m")
    print("3.  \033[92m GRE6\033[0m")
    print("4.  \033[93m GRE6 + IPSEC\033[0m")
    print("5.  \033[92m GRE6TAP \033[96m [IPV4]\033[0m")
    print("6.  \033[93m GRE6TAP \033[96m [IPV4] + IPSEC\033[0m")
    print("7.  \033[92m Private\033[0m")
    print("8.  \033[93m Private + IPSEC\033[0m")
    print("9.  \033[92m Geneve UDP\033[0m")
    print("10. \033[93m Geneve UDP + IPSEC\033[0m")
    print("11. \033[92m Geneve GRE6\033[0m")
    print("12. \033[93m Geneve GRE6 + IPSEC\033[0m")
    print("13. \033[91m Remove\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_single_ip6ip6()
            break
        elif choice == "2":
            robotreconfig_single_ip6ip6sec()
            break
        elif choice == "3":
            robotreconfig_single_gre6()
            break
        elif choice == "4":
            robotreconfig_single_gre6sec()
            break
        elif choice == "5":
            robotreconfig_single_gre6tap()
            break
        elif choice == "6":
            robotreconfig_single_gre6tapsec()
            break
        elif choice == "7":
            robotreconfig_single_private()
            break
        elif choice == "8":
            robotreconfig_single_privatesec()
            break
        elif choice == "9":
            robotreconfig_single_geneve()
            break
        elif choice == "10":
            robotreconfig_single_genevesec()
            break
        elif choice == "11":
            robotreconfig_single_gengre()
            break
        elif choice == "12":
            robotreconfig_single_gengresec()
            break
        elif choice == "13":
            remove()
            break
        elif choice == "0":
            clear()
            robot_menu()
            break
        else:
            print("Invalid choice.")
 
def robotreconfig_single_ip6ip6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_ip6ip6_kharej()
            break
        elif choice == "2":
            robot_single_ip6ip6_iran()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single ip6ip6                      
def singleip6ip6_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '6'

    inputs['private_kharej_ip'] = '2002:0db8:1234:a220::1'
    inputs['private_iran_ip'] = '2002:0db8:1234:a220::2'

    inputs['ip6ip6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '1'

    return inputs

def generate_bash_script_singleip6ip6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleip6ip6kharej(inputs):
    with open("/usr/local/bin/single_ip6ip6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleip6ip6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_ip6ip6_kharej():
    inputs = singleip6ip6_kharejuser_input()
    store_inputs_singleip6ip6kharej(inputs)
    generate_bash_script_singleip6ip6_kharej(inputs)
    create_script_singleip6ip6kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single ip6ip6 

def singleip6ip6_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '6'

    inputs['private_kharej_ip'] = '2002:0db8:1234:a220::1'
    inputs['private_iran_ip'] = '2002:0db8:1234:a220::2'

    inputs['ip6ip6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '1' 

    return inputs

def generate_bash_script_singleip6ip6_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleip6ip6iran(inputs):
    with open("/usr/local/bin/single_ip6ip6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleip6ip6iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_ip6ip6_iran():
    inputs = singleip6ip6_iranuser_input()
    store_inputs_singleip6ip6iran(inputs)
    generate_bash_script_singleip6ip6_iran(inputs)
    create_script_singleip6ip6iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
#robot ip6ip6 ipsec single 

def robotreconfig_single_ip6ip6sec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_ip6ip6_kharejsec()
            break
        elif choice == "2":
            robot_single_ip6ip6_iransec()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single ip6ip6                      
def singleip6ip6_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '7'

    inputs['private_kharej_ip'] = '2002:0db8:1234:a220::1'
    inputs['private_iran_ip'] = '2002:0db8:1234:a220::2'

    inputs['ip6ip6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '2' 

    return inputs

def generate_bash_script_singleip6ip6_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6sec.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleip6ip6kharejsec(inputs):
    with open("/usr/local/bin/single_ip6ip6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleip6ip6kharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_ip6ip6_kharejsec():
    inputs = singleip6ip6_kharejuser_inputsec()
    store_inputs_singleip6ip6kharejsec(inputs)
    generate_bash_script_singleip6ip6_kharejsec(inputs)
    create_script_singleip6ip6kharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single ip6ip6                      
def singleip6ip6_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '7'

    inputs['private_kharej_ip'] = '2002:0db8:1234:a220::1'
    inputs['private_iran_ip'] = '2002:0db8:1234:a220::2'

    inputs['ip6ip6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '2' 

    return inputs

def generate_bash_script_singleip6ip6_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6sec.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleip6ip6iransec(inputs):
    with open("/usr/local/bin/single_ip6ip6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleip6ip6iransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_ip6ip6_iransec():
    inputs = singleip6ip6_iranuser_inputsec()
    store_inputs_singleip6ip6iransec(inputs)
    generate_bash_script_singleip6ip6_iransec(inputs)
    create_script_singleip6ip6iransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 
    
#gre6

def robotreconfig_single_gre6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGRE6 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gre6_kharej()
            break
        elif choice == "2":
            robot_single_gre6_iran()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single gre6                    
def singlegre6_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '11'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '6' 

    return inputs

def generate_bash_script_singlegre6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6.sh"
    service_path = "/etc/systemd/system/robot_gre6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6kharej(inputs):
    with open("/usr/local/bin/single_gre6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6_kharej():
    inputs = singlegre6_kharejuser_input()
    store_inputs_singlegre6kharej(inputs)
    generate_bash_script_singlegre6_kharej(inputs)
    create_script_singlegre6kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single gre6

def singlegre6_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '11'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '6' 

    return inputs

def generate_bash_script_singlegre6_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6.sh"
    service_path = "/etc/systemd/system/robot_gre6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6iran(inputs):
    with open("/usr/local/bin/single_gre6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6_iran():
    inputs = singlegre6_iranuser_input()
    store_inputs_singlegre6iran(inputs)
    generate_bash_script_singlegre6_iran(inputs)
    create_script_singlegre6iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
#robot gre6 ipsec single 

def robotreconfig_single_gre6sec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGRE6 IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gre6_kharejsec()
            break
        elif choice == "2":
            robot_single_gre6_iransec()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single gre6                     
def singlegre6_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '12'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '7' 

    return inputs

def generate_bash_script_singlegre6_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6sec.sh"
    service_path = "/etc/systemd/system/robot_gre6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6kharejsec(inputs):
    with open("/usr/local/bin/single_gre6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6kharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6_kharejsec():
    inputs = singlegre6_kharejuser_inputsec()
    store_inputs_singlegre6kharejsec(inputs)
    generate_bash_script_singlegre6_kharejsec(inputs)
    create_script_singlegre6kharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single gre6                     
def singlegre6_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '12'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '7' 

    return inputs

def generate_bash_script_singlegre6_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6sec.sh"
    service_path = "/etc/systemd/system/robot_gre6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6iransec(inputs):
    with open("/usr/local/bin/single_gre6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6iransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6_iransec():
    inputs = singlegre6_iranuser_inputsec()
    store_inputs_singlegre6iransec(inputs)
    generate_bash_script_singlegre6_iransec(inputs)
    create_script_singlegre6iransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 
    
#gre6tap ipv4

def robotreconfig_single_gre6tap():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGRE6tap \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gre6tap_kharej()
            break
        elif choice == "2":
            robot_single_gre6tap_iran()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single gre6tap                    
def singlegre6tap_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '13'
    inputs['ipv4_or_ipv6'] = '1'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '8' 

    return inputs

def generate_bash_script_singlegre6tap_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6.sh"
    service_path = "/etc/systemd/system/robot_gre6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6tapkharej(inputs):
    with open("/usr/local/bin/single_gre6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6tapkharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ipv4_or_ipv6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6tap_kharej():
    inputs = singlegre6tap_kharejuser_input()
    store_inputs_singlegre6tapkharej(inputs)
    generate_bash_script_singlegre6tap_kharej(inputs)
    create_script_singlegre6tapkharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single gre6tap

def singlegre6tap_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '13'
    inputs['ipv4_or_ipv6'] = '1'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '8' 

    return inputs

def generate_bash_script_singlegre6tap_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6.sh"
    service_path = "/etc/systemd/system/robot_gre6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6tapiran(inputs):
    with open("/usr/local/bin/single_gre6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6tapiran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ipv4_or_ipv6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6tap_iran():
    inputs = singlegre6tap_iranuser_input()
    store_inputs_singlegre6tapiran(inputs)
    generate_bash_script_singlegre6tap_iran(inputs)
    create_script_singlegre6tapiran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#robot gre6tap ipsec single 

def robotreconfig_single_gre6tapsec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGRE6tap IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gre6tap_kharejsec()
            break
        elif choice == "2":
            robot_single_gre6tap_iransec()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single gre6tap                     
def singlegre6tap_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '14'
    inputs['ipv4_or_ipv6'] = '1'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '9' 

    return inputs

def generate_bash_script_singlegre6tap_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6sec.sh"
    service_path = "/etc/systemd/system/robot_gre6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6tapkharejsec(inputs):
    with open("/usr/local/bin/single_gre6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6tapkharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ipv4_or_ipv6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6tap_kharejsec():
    inputs = singlegre6tap_kharejuser_inputsec()
    store_inputs_singlegre6tapkharejsec(inputs)
    generate_bash_script_singlegre6tap_kharejsec(inputs)
    create_script_singlegre6tapkharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single gre6tap                     
def singlegre6tap_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '14'
    inputs['ipv4_or_ipv6'] = '1'

    inputs['private_kharej_ip'] = '2002:831a::1'
    inputs['private_iran_ip'] = '2002:831a::2'

    inputs['gre6_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '9' 

    return inputs

def generate_bash_script_singlegre6tap_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gre6sec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gre6sec.sh"
    service_path = "/etc/systemd/system/robot_gre6sec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gre6sec.service"])
    subprocess.run(["systemctl", "restart", "robot_gre6sec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegre6tapiransec(inputs):
    with open("/usr/local/bin/single_gre6sec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegre6tapiransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gre6sec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ipv4_or_ipv6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['gre6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gre6tap_iransec():
    inputs = singlegre6tap_iranuser_inputsec()
    store_inputs_singlegre6tapiransec(inputs)
    generate_bash_script_singlegre6tap_iransec(inputs)
    create_script_singlegre6tapiransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 
    
#private 

def robotreconfig_single_private():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mPrivate \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_private_kharej()
            break
        elif choice == "2":
            robot_single_private_iran()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single private                    
def singleprivate_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '8'

    inputs['private_kharej_ip'] = '2002:831b::1'
    inputs['private_iran_ip'] = '2002:831b::2'

    inputs['private_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_6to4'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '10' 

    return inputs

def generate_bash_script_singleprivate_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_private.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_private.sh"
    service_path = "/etc/systemd/system/robot_private.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_private.service"])
    subprocess.run(["systemctl", "restart", "robot_private.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleprivatekharej(inputs):
    with open("/usr/local/bin/single_private_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleprivatekharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_private.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['private_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_private_kharej():
    inputs = singleprivate_kharejuser_input()
    store_inputs_singleprivatekharej(inputs)
    generate_bash_script_singleprivate_kharej(inputs)
    create_script_singleprivatekharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single private

def singleprivate_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '8'

    inputs['private_kharej_ip'] = '2002:831b::1'
    inputs['private_iran_ip'] = '2002:831b::2'

    inputs['private_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_6to4'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '10' 

    return inputs

def generate_bash_script_singleprivate_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_private.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_private.sh"
    service_path = "/etc/systemd/system/robot_private.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_private.service"])
    subprocess.run(["systemctl", "restart", "robot_private.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleprivateiran(inputs):
    with open("/usr/local/bin/single_private_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleprivateiran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_private.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['private_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_private_iran():
    inputs = singleprivate_iranuser_input()
    store_inputs_singleprivateiran(inputs)
    generate_bash_script_singleprivate_iran(inputs)
    create_script_singleprivateiran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
#robot private ipsec single 

def robotreconfig_single_privatesec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mPrivate IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_private_kharejsec()
            break
        elif choice == "2":
            robot_single_private_iransec()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single private                     
def singleprivate_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '9'

    inputs['private_kharej_ip'] = '2002:831b::1'
    inputs['private_iran_ip'] = '2002:831b::2'

    inputs['private_method'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_6to4'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '11' 

    return inputs

def generate_bash_script_singleprivate_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_privatesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_privatesec.sh"
    service_path = "/etc/systemd/system/robot_privatesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_privatesec.service"])
    subprocess.run(["systemctl", "restart", "robot_privatesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleprivatekharejsec(inputs):
    with open("/usr/local/bin/single_privatesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleprivatekharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_privatesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['private_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_private_kharejsec():
    inputs = singleprivate_kharejuser_inputsec()
    store_inputs_singleprivatekharejsec(inputs)
    generate_bash_script_singleprivate_kharejsec(inputs)
    create_script_singleprivatekharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single private                    
def singleprivate_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '9'

    inputs['private_kharej_ip'] = '2002:831b::1'
    inputs['private_iran_ip'] = '2002:831b::2'

    inputs['private_method'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['change_default_route'] = 'n'
    inputs['set_mtu_6to4'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '11' 

    return inputs

def generate_bash_script_singleprivate_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_privatesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_privatesec.sh"
    service_path = "/etc/systemd/system/robot_privatesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_privatesec.service"])
    subprocess.run(["systemctl", "restart", "robot_privatesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singleprivateiransec(inputs):
    with open("/usr/local/bin/single_privatesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singleprivateiransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_privatesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['private_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['change_default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_private_iransec():
    inputs = singleprivate_iranuser_inputsec()
    store_inputs_singleprivateiransec(inputs)
    generate_bash_script_singleprivate_iransec(inputs)
    create_script_singleprivateiransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 
    
#geneve

def robotreconfig_single_geneve():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mPrivate IPversion 4\033[0m")
    print("2  \033[92mPrivate IPversion 6\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_single_geneve4()
            break
        elif choice == "2":
            robotreconfig_single_geneve6()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")
            
def robotreconfig_single_geneve4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve V4 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_geneve4_kharej()
            break
        elif choice == "2":
            robot_single_geneve4_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_geneve()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_geneve6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve V6 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_geneve6_kharej()
            break
        elif choice == "2":
            robot_single_geneve6_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_geneve()
            break
        else:
            print("Invalid choice.")
            
#kharej robot reconfig single geneve                   
def singlegeneve4_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '1'
    inputs['geneve_pointip'] = '1'
    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '1' 

    return inputs

def generate_bash_script_singlegeneve4_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_geneve.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_geneve.sh"
    service_path = "/etc/systemd/system/robot_geneve.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_geneve.service"])
    subprocess.run(["systemctl", "restart", "robot_geneve.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve4kharej(inputs):
    with open("/usr/local/bin/single_geneve_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve4kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_geneve.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_pointip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve4_kharej():
    inputs = singlegeneve4_kharejuser_input()
    store_inputs_singlegeneve4kharej(inputs)
    generate_bash_script_singlegeneve4_kharej(inputs)
    create_script_singlegeneve4kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve

def singlegeneve4_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '1'
    inputs['geneve_pointip'] = '1'

    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '1' 

    return inputs

def generate_bash_script_singlegeneve4_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_geneve.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_geneve.sh"
    service_path = "/etc/systemd/system/robot_geneve.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_geneve.service"])
    subprocess.run(["systemctl", "restart", "robot_geneve.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve4iran(inputs):
    with open("/usr/local/bin/single_geneve_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve4iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_geneve.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_pointip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve4_iran():
    inputs = singlegeneve4_iranuser_input()
    store_inputs_singlegeneve4iran(inputs)
    generate_bash_script_singlegeneve4_iran(inputs)
    create_script_singlegeneve4iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

def ipv4_to_ipv6_prefix(ipv4):
    return "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split(".")))

#geneve no sec ipv6
def singlegeneve6_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '1'
    inputs['geneve_pointip'] = '1'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address [Again]: \033[0m")
    inputs['private_iran_ip'] = ipv4_to_ipv6_prefix(inputs['iran_ip']) 
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '1' 

    return inputs

def generate_bash_script_singlegeneve6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_geneve.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_geneve.sh"
    service_path = "/etc/systemd/system/robot_geneve.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_geneve.service"])
    subprocess.run(["systemctl", "restart", "robot_geneve.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve6kharej(inputs):
    with open("/usr/local/bin/single_geneve_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_geneve.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_pointip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve6_kharej():
    inputs = singlegeneve6_kharejuser_input()
    store_inputs_singlegeneve6kharej(inputs)
    generate_bash_script_singlegeneve6_kharej(inputs)
    create_script_singlegeneve6kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve

def singlegeneve6_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '1'
    inputs['geneve_pointip'] = '1'


    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address[Again]: \033[0m")
    inputs['private_kharej_ip'] = ipv4_to_ipv6_prefix(inputs['kharej_ip']) 
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '1' 

    return inputs

def generate_bash_script_singlegeneve6_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_geneve.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_geneve.sh"
    service_path = "/etc/systemd/system/robot_geneve.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_geneve.service"])
    subprocess.run(["systemctl", "restart", "robot_geneve.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve6iran(inputs):
    with open("/usr/local/bin/single_geneve_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve6iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_geneve.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_pointip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve6_iran():
    inputs = singlegeneve6_iranuser_input()
    store_inputs_singlegeneve6iran(inputs)
    generate_bash_script_singlegeneve6_iran(inputs)
    create_script_singlegeneve6iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#robot geneve ipsec single 

def robotreconfig_single_genevesec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve + IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mPrivate IPversion 4\033[0m")
    print("2  \033[92mPrivate IPversion 6\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_single_geneve4sec()
            break
        elif choice == "2":
            robotreconfig_single_geneve6sec()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_geneve4sec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve V4 IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_geneve4_kharejsec()
            break
        elif choice == "2":
            robot_single_geneve4_iransec()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_genevesec()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_geneve6sec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGeneve V6 IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_geneve6_kharejsec()
            break
        elif choice == "2":
            robot_single_geneve6_iransec()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_genevesec()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single geneve                    
def singlegeneve4_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '1'
    inputs['geneve_address'] = '2'

    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.1.2'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6'
    inputs['uninstall_input5'] = '1'  

    return inputs

def generate_bash_script_singlegeneve4_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_genevesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_genevesec.sh"
    service_path = "/etc/systemd/system/robot_genevesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_genevesec.service"])
    subprocess.run(["systemctl", "restart", "robot_genevesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve4kharejsec(inputs):
    with open("/usr/local/bin/single_genevesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve4kharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_genevesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_address']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve4_kharejsec():
    inputs = singlegeneve4_kharejuser_inputsec()
    store_inputs_singlegeneve4kharejsec(inputs)
    generate_bash_script_singlegeneve4_kharejsec(inputs)
    create_script_singlegeneve4kharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single private                    
def singlegeneve4_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '1'
    inputs['geneve_address'] = '2'

    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.1.2'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6'
    inputs['uninstall_input5'] = '1'  

    return inputs

def generate_bash_script_singlegeneve4_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_genevesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_genevesec.sh"
    service_path = "/etc/systemd/system/robot_genevesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_genevesec.service"])
    subprocess.run(["systemctl", "restart", "robot_genevesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve4iransec(inputs):
    with open("/usr/local/bin/single_genevesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve4iransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_genevesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_address']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve4_iransec():
    inputs = singlegeneve4_iranuser_inputsec()
    store_inputs_singlegeneve4iransec(inputs)
    generate_bash_script_singlegeneve4_iransec(inputs)
    create_script_singlegeneve4iransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 

#geneve v6 ipsec
def singlegeneve6_kharejuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '1'
    inputs['geneve_address'] = '2'

    inputs['private_kharej_ip'] = '2001:db8::1'
    inputs['private_iran_ip'] = '2001:db8::2'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6'
    inputs['uninstall_input5'] = '1'  

    return inputs

def generate_bash_script_singlegeneve6_kharejsec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_genevesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_genevesec.sh"
    service_path = "/etc/systemd/system/robot_genevesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_genevesec.service"])
    subprocess.run(["systemctl", "restart", "robot_genevesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve6kharejsec(inputs):
    with open("/usr/local/bin/single_genevesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve6kharejsec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_genevesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_address']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve6_kharejsec():
    inputs = singlegeneve6_kharejuser_inputsec()
    store_inputs_singlegeneve6kharejsec(inputs)
    generate_bash_script_singlegeneve6_kharejsec(inputs)
    create_script_singlegeneve6kharejsec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#iran robot reconfig single private                    
def singlegeneve6_iranuser_inputsec():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '1'
    inputs['geneve_address'] = '2'

    inputs['private_kharej_ip'] = '2001:db8::1'
    inputs['private_iran_ip'] = '2001:db8::2'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret key\033[93m: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6'
    inputs['uninstall_input5'] = '1'  

    return inputs

def generate_bash_script_singlegeneve6_iransec(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_genevesec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_genevesec.sh"
    service_path = "/etc/systemd/system/robot_genevesec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_genevesec.service"])
    subprocess.run(["systemctl", "restart", "robot_genevesec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegeneve6iransec(inputs):
    with open("/usr/local/bin/single_genevesec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegeneve6iransec():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_genevesec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_address']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_geneve6_iransec():
    inputs = singlegeneve6_iranuser_inputsec()
    store_inputs_singlegeneve6iransec(inputs)
    generate_bash_script_singlegeneve6_iransec(inputs)
    create_script_singlegeneve6iransec() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m") 

# geneve gre 

def robotreconfig_single_gengre():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mPrivate IPversion 4\033[0m")
    print("2  \033[92mPrivate IPversion 6\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_single_gengre4()
            break
        elif choice == "2":
            robotreconfig_single_gengre6()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_gengre4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 V4 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gengre4_kharej()
            break
        elif choice == "2":
            robot_single_gengre4_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_gengre()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_gengre6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 V6\033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gengre6_kharej()
            break
        elif choice == "2":
            robot_single_gengre6_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_gengre()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single geneve gre 4                 
def singlegengre4_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '3'
    inputs['geneve_gremenu'] = '3'
    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '4' 

    return inputs

def generate_bash_script_singlegengre4_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengre.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengre.sh"
    service_path = "/etc/systemd/system/robot_gengre.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengre.service"])
    subprocess.run(["systemctl", "restart", "robot_gengre.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengre4kharej(inputs):
    with open("/usr/local/bin/single_gengre_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengre4kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengre.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengre4_kharej():
    inputs = singlegengre4_kharejuser_input()
    store_inputs_singlegengre4kharej(inputs)
    generate_bash_script_singlegengre4_kharej(inputs)
    create_script_singlegengre4kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve gre 4

def singlegengre4_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '3'
    inputs['geneve_gremenu'] = '3'

    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '4' 

    return inputs

def generate_bash_script_singlegengre4_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengre.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengre.sh"
    service_path = "/etc/systemd/system/robot_gengre.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengre.service"])
    subprocess.run(["systemctl", "restart", "robot_gengre.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengre4iran(inputs):
    with open("/usr/local/bin/single_gengre_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengre4iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengre.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengre4_iran():
    inputs = singlegengre4_iranuser_input()
    store_inputs_singlegengre4iran(inputs)
    generate_bash_script_singlegengre4_iran(inputs)
    create_script_singlegengre4iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# gen gre v6
#kharej robot reconfig single geneve gre 6               
def singlegengre6_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '3'
    inputs['geneve_gremenu'] = '3'


    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['set_mtu_geneve'] = 'n'
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address[again]: \033[0m")
    inputs['private_iran_ip'] = ipv4_to_ipv6_prefix(inputs['iran_ip']) 
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '4' 

    return inputs

def generate_bash_script_singlegengre6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengre.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengre.sh"
    service_path = "/etc/systemd/system/robot_gengre.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengre.service"])
    subprocess.run(["systemctl", "restart", "robot_gengre.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengre6kharej(inputs):
    with open("/usr/local/bin/single_gengre_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengre6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengre.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengre6_kharej():
    inputs = singlegengre6_kharejuser_input()
    store_inputs_singlegengre6kharej(inputs)
    generate_bash_script_singlegengre6_kharej(inputs)
    create_script_singlegengre6kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve gre 6

def singlegengre6_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '3'
    inputs['geneve_choose'] = '3'
    inputs['geneve_gremenu'] = '3'


    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['set_mtu_geneve'] = 'n'
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address[again]: \033[0m")
    inputs['private_kharej_ip'] = ipv4_to_ipv6_prefix(inputs['kharej_ip'])
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '4' 

    return inputs

def generate_bash_script_singlegengre6_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengre.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengre.sh"
    service_path = "/etc/systemd/system/robot_gengre.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengre.service"])
    subprocess.run(["systemctl", "restart", "robot_gengre.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengre6iran(inputs):
    with open("/usr/local/bin/single_gengre_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengre6iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengre.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengre6_iran():
    inputs = singlegengre6_iranuser_input()
    store_inputs_singlegengre6iran(inputs)
    generate_bash_script_singlegengre6_iran(inputs)
    create_script_singlegengre6iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


# gre gen ipsec 
def robotreconfig_single_gengresec():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 IPSEC \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mPrivate IPversion 4\033[0m")
    print("2  \033[92mPrivate IPversion 6\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_single_gengresec4()
            break
        elif choice == "2":
            robotreconfig_single_gengresec6()
            break
        elif choice == "0":
            clear()
            robot_single_mnu()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_gengresec4():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 IPSEC V4 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gengresec4_kharej()
            break
        elif choice == "2":
            robot_single_gengresec4_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_gengresec()
            break
        else:
            print("Invalid choice.")

def robotreconfig_single_gengresec6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mGen GRE6 IPSEC V6\033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs\033[0m")
    print("2  \033[92mIRAN Inputs\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_single_gengresec6_kharej()
            break
        elif choice == "2":
            robot_single_gengresec6_iran()
            break
        elif choice == "0":
            clear()
            robotreconfig_single_gengresec()
            break
        else:
            print("Invalid choice.")

#kharej robot reconfig single geneve gresec 4                 
def singlegengresec4_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '2'
    inputs['geneve_gremenu'] = '3'
    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['additioanl_ip'] = input("\033[93mEnter the \033[92mnumber of additional IPs\033[93m for the GRE6 tunnel: \033[0m")
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret Key: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6' 
    inputs['uninstall_input5'] = '2' 

    return inputs

def generate_bash_script_singlegengresec4_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengresec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengresec.sh"
    service_path = "/etc/systemd/system/robot_gengresec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengresec.service"])
    subprocess.run(["systemctl", "restart", "robot_gengresec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengresec4kharej(inputs):
    with open("/usr/local/bin/single_gengresec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengresec4kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengresec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additioanl_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengresec4_kharej():
    inputs = singlegengresec4_kharejuser_input()
    store_inputs_singlegengresec4kharej(inputs)
    generate_bash_script_singlegengresec4_kharej(inputs)
    create_script_singlegengresec4kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve gresec 4

def singlegengresec4_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '2'
    inputs['geneve_gremenu'] = '3'
    inputs['private_kharej_ip'] = '80.200.1.1'
    inputs['private_iran_ip'] = '80.200.2.1'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['additioanl_ip'] = input("\033[93mEnter the \033[92mnumber of additional IPs\033[93m for the GRE6 tunnel: \033[0m")
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret Key: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6' 
    inputs['uninstall_input5'] = '2' 

    return inputs

def generate_bash_script_singlegengresec4_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengresec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengresec.sh"
    service_path = "/etc/systemd/system/robot_gengresec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengresec.service"])
    subprocess.run(["systemctl", "restart", "robot_gengresec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengresec4iran(inputs):
    with open("/usr/local/bin/single_gengresec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengresec4iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengresec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additioanl_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengresec4_iran():
    inputs = singlegengresec4_iranuser_input()
    store_inputs_singlegengresec4iran(inputs)
    generate_bash_script_singlegengresec4_iran(inputs)
    create_script_singlegengresec4iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# gen gresec v6
#kharej robot reconfig single geneve gre 6               
def singlegengresec6_kharejuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '2'
    inputs['geneve_gremenu'] = '3'
    inputs['private_kharej_ip'] = '2001:db8::1'
    inputs['private_iran_ip'] = '2001:db8::2'

    inputs['geneve_method'] = '1'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['additioanl_ip'] = input("\033[93mEnter the \033[92mnumber of additional IPs\033[93m for the GRE6 tunnel: \033[0m")
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret Key: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6' 
    inputs['uninstall_input5'] = '2'  

    return inputs

def generate_bash_script_singlegengresec6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengresec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengresec.sh"
    service_path = "/etc/systemd/system/robot_gengresec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengresec.service"])
    subprocess.run(["systemctl", "restart", "robot_gengresec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengresec6kharej(inputs):
    with open("/usr/local/bin/single_gengresec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengresec6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengresec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additioanl_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengresec6_kharej():
    inputs = singlegengresec6_kharejuser_input()
    store_inputs_singlegengresec6kharej(inputs)
    generate_bash_script_singlegengresec6_kharej(inputs)
    create_script_singlegengresec6kharej() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")


#iran robot reconfig single geneve gresec 6

def singlegengresec6_iranuser_input():
    
    inputs = {}

    inputs['input_value'] = '2'
    inputs['local_tunnel'] = '4'
    inputs['geneve_choose'] = '2'
    inputs['geneve_gremenu'] = '3'

    inputs['private_kharej_ip'] = '2001:db8::1'
    inputs['private_iran_ip'] = '2001:db8::2'

    inputs['geneve_method'] = '2'
    inputs['ip_version'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['set_mtu_6to4'] = 'n'
    inputs['additioanl_ip'] = input("\033[93mEnter the \033[92mnumber of additional IPs\033[93m for the GRE6 tunnel: \033[0m")
    inputs['default_route'] = 'n'
    inputs['set_mtu_gre6'] = 'n'
    inputs['secret_key'] = input("\033[93mEnter the \033[92mSecret Key: \033[0m")
    inputs['set_mtu_geneve'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '2'
    inputs['uninstall_input2'] = '19'
    inputs['uninstall_input3'] = '13' 
    inputs['uninstall_input4'] = '6' 
    inputs['uninstall_input5'] = '2' 

    return inputs

def generate_bash_script_singlegengresec6_iran(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_gengresec.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_gengresec.sh"
    service_path = "/etc/systemd/system/robot_gengresec.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_gengresec.service"])
    subprocess.run(["systemctl", "restart", "robot_gengresec.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_singlegengresec6iran(inputs):
    with open("/usr/local/bin/single_gengresec_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_singlegengresec6iran():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_gengresec.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/single_ip6ip6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_gremenu']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['geneve_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['ip_version']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['additioanl_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_gre6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['secret_key']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(7)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_geneve']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_single_gengresec6_iran():
    inputs = singlegengresec6_iranuser_input()
    store_inputs_singlegengresec6iran(inputs)
    generate_bash_script_singlegengresec6_iran(inputs)
    create_script_singlegengresec6iran() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

services = [
    ("robot_ip6ip6", [
        "/usr/local/bin/robot_ip6ip6.py",
        "/usr/local/bin/robot_ip6ip6.sh",
        "/etc/systemd/system/robot_ip6ip6.service",
        "/usr/local/bin/single_ip6ip6_inputs.txt"
    ]),
    ("robot_ip6ip6sec", [
        "/usr/local/bin/robot_ip6ip6sec.py",
        "/usr/local/bin/robot_ip6ip6sec.sh",
        "/etc/systemd/system/robot_ip6ip6sec.service",
        "/usr/local/bin/single_ip6ip6sec_inputs.txt"
    ]),
    ("robot_gre6", [
        "/usr/local/bin/robot_gre6.py",
        "/usr/local/bin/robot_gre6.sh",
        "/etc/systemd/system/robot_gre6.service",
        "/usr/local/bin/single_gre6_inputs.txt"
    ]),
    ("robot_gre6sec", [
        "/usr/local/bin/robot_gre6sec.py",
        "/usr/local/bin/robot_gre6sec.sh",
        "/etc/systemd/system/robot_gre6sec.service",
        "/usr/local/bin/single_gre6sec_inputs.txt"
    ]),
    ("robot_private", [
        "/usr/local/bin/robot_private.py",
        "/usr/local/bin/robot_private.sh",
        "/etc/systemd/system/robot_private.service",
        "/usr/local/bin/single_private_inputs.txt"
    ]),
    ("robot_privatesec", [
        "/usr/local/bin/robot_privatesec.py",
        "/usr/local/bin/robot_privatesec.sh",
        "/etc/systemd/system/robot_privatesec.service",
        "/usr/local/bin/single_privatesec_inputs.txt"
    ]),
    ("robot_geneve", [
        "/usr/local/bin/robot_geneve.py",
        "/usr/local/bin/robot_geneve.sh",
        "/etc/systemd/system/robot_geneve.service",
        "/usr/local/bin/single_geneve_inputs.txt"
    ]),
    ("robot_genevesec", [
        "/usr/local/bin/robot_genevesec.py",
        "/usr/local/bin/robot_genevesec.sh",
        "/etc/systemd/system/robot_genevesec.service",
        "/usr/local/bin/single_genevesec_inputs.txt"
    ]),
    ("robot_gengre", [
        "/usr/local/bin/robot_gengre.py",
        "/usr/local/bin/robot_gengre.sh",
        "/etc/systemd/system/robot_gengre.service",
        "/usr/local/bin/single_gengre_inputs.txt"
    ]),
    ("robot_gengresec", [
        "/usr/local/bin/robot_gengresec.py",
        "/usr/local/bin/robot_gengresec.sh",
        "/etc/systemd/system/robot_gengresec.service",
        "/usr/local/bin/single_gengresec_inputs.txt"
    ]),
]

def command(command):
    try:
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        pass  

def remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass  
    except Exception as e:
        pass 

def uninstall_service(service_name, files):
    command(f"systemctl stop {service_name}")
    command(f"systemctl disable {service_name}")
    command(f"systemctl daemon-reload")  

    for file in files:
        remove_file(file)

def remove():
    for service_name, files in services:
        uninstall_service(service_name, files)
    print("\033[92mUninstallation is done.\033[0m")


def remove_ip6ip6_multi_iran1kharej10():
    services = [
        ("robot_ip6ip6_kharej1", [
            "/usr/local/bin/robot_ip6ip6_kharej1.py",
            "/usr/local/bin/robot_ip6ip6_kharej1.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej1.service",
            "/usr/local/bin/multi_ip6ip6_kharej1_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej2", [
            "/usr/local/bin/robot_ip6ip6_kharej2.py",
            "/usr/local/bin/robot_ip6ip6_kharej2.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej2.service",
            "/usr/local/bin/multi_ip6ip6_kharej2_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej3", [
            "/usr/local/bin/robot_ip6ip6_kharej3.py",
            "/usr/local/bin/robot_ip6ip6_kharej3.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej3.service",
            "/usr/local/bin/multi_ip6ip6_kharej3_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej4", [
            "/usr/local/bin/robot_ip6ip6_kharej4.py",
            "/usr/local/bin/robot_ip6ip6_kharej4.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej4.service",
            "/usr/local/bin/multi_ip6ip6_kharej4_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej5", [
            "/usr/local/bin/robot_ip6ip6_kharej5.py",
            "/usr/local/bin/robot_ip6ip6_kharej5.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej5.service",
            "/usr/local/bin/multi_ip6ip6_kharej5_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej6", [
            "/usr/local/bin/robot_ip6ip6_kharej6.py",
            "/usr/local/bin/robot_ip6ip6_kharej6.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej6.service",
            "/usr/local/bin/multi_ip6ip6_kharej6_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej7", [
            "/usr/local/bin/robot_ip6ip6_kharej7.py",
            "/usr/local/bin/robot_ip6ip6_kharej7.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej7.service",
            "/usr/local/bin/multi_ip6ip6_kharej7_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej8", [
            "/usr/local/bin/robot_ip6ip6_kharej8.py",
            "/usr/local/bin/robot_ip6ip6_kharej8.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej8.service",
            "/usr/local/bin/multi_ip6ip6_kharej8_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej9", [
            "/usr/local/bin/robot_ip6ip6_kharej9.py",
            "/usr/local/bin/robot_ip6ip6_kharej9.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej9.service",
            "/usr/local/bin/multi_ip6ip6_kharej9_inputs.txt"
        ]),
        ("robot_ip6ip6_kharej10", [
            "/usr/local/bin/robot_ip6ip6_kharej10.py",
            "/usr/local/bin/robot_ip6ip6_kharej10.sh",
            "/etc/systemd/system/robot_ip6ip6_kharej10.service",
            "/usr/local/bin/multi_ip6ip6_kharej10_inputs.txt"
        ]),
        ("robot_ip6ip6_iran1", [
            "/usr/local/bin/robot_ip6ip6_iran1.py",
            "/usr/local/bin/robot_ip6ip6_iran1.sh",
            "/etc/systemd/system/robot_ip6ip6_iran1.service",
            "/usr/local/bin/multi_ip6ip6_iran1_inputs.txt"
        ]),
        ("robot_ip6ip6_iran2", [
            "/usr/local/bin/robot_ip6ip6_iran2.py",
            "/usr/local/bin/robot_ip6ip6_iran2.sh",
            "/etc/systemd/system/robot_ip6ip6_iran2.service",
            "/usr/local/bin/multi_ip6ip6_iran2_inputs.txt"
        ]),
        ("robot_ip6ip6_iran3", [
            "/usr/local/bin/robot_ip6ip6_iran3.py",
            "/usr/local/bin/robot_ip6ip6_iran3.sh",
            "/etc/systemd/system/robot_ip6ip6_iran3.service",
            "/usr/local/bin/multi_ip6ip6_iran3_inputs.txt"
        ]),
        ("robot_ip6ip6_iran4", [
            "/usr/local/bin/robot_ip6ip6_iran4.py",
            "/usr/local/bin/robot_ip6ip6_iran4.sh",
            "/etc/systemd/system/robot_ip6ip6_iran4.service",
            "/usr/local/bin/multi_ip6ip6_iran4_inputs.txt"
        ]),
        ("robot_ip6ip6_iran5", [
            "/usr/local/bin/robot_ip6ip6_iran5.py",
            "/usr/local/bin/robot_ip6ip6_iran5.sh",
            "/etc/systemd/system/robot_ip6ip6_iran5.service",
            "/usr/local/bin/multi_ip6ip6_iran5_inputs.txt"
        ]),
        ("robot_ip6ip6_iran6", [
            "/usr/local/bin/robot_ip6ip6_iran6.py",
            "/usr/local/bin/robot_ip6ip6_iran6.sh",
            "/etc/systemd/system/robot_ip6ip6_iran6.service",
            "/usr/local/bin/multi_ip6ip6_iran6_inputs.txt"
        ]),
        ("robot_ip6ip6_iran7", [
            "/usr/local/bin/robot_ip6ip6_iran7.py",
            "/usr/local/bin/robot_ip6ip6_iran7.sh",
            "/etc/systemd/system/robot_ip6ip6_iran7.service",
            "/usr/local/bin/multi_ip6ip6_iran7_inputs.txt"
        ]),
        ("robot_ip6ip6_iran8", [
            "/usr/local/bin/robot_ip6ip6_iran8.py",
            "/usr/local/bin/robot_ip6ip6_iran8.sh",
            "/etc/systemd/system/robot_ip6ip6_iran8.service",
            "/usr/local/bin/multi_ip6ip6_iran8_inputs.txt"
        ]),
        ("robot_ip6ip6_iran9", [
            "/usr/local/bin/robot_ip6ip6_iran9.py",
            "/usr/local/bin/robot_ip6ip6_iran9.sh",
            "/etc/systemd/system/robot_ip6ip6_iran9.service",
            "/usr/local/bin/multi_ip6ip6_iran9_inputs.txt"
        ]),
        ("robot_ip6ip6_iran10", [
            "/usr/local/bin/robot_ip6ip6_iran10.py",
            "/usr/local/bin/robot_ip6ip6_iran10.sh",
            "/etc/systemd/system/robot_ip6ip6_iran10.service",
            "/usr/local/bin/multi_ip6ip6_iran10_inputs.txt"
        ]),
    ]

    for service_name, files in services:
        uninstall_service(service_name, files)

    print("\033[92mUninstallation is done.\033[0m")

def remove_services_ip6ip6_multi_iran10kharej1():
    services = [
        ("robot_ip6ip61_kharejserver1", [
            "/usr/local/bin/robot_ip6ip6_kharejserver1.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver1.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver1.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver1_inputs.txt"
        ]),
        ("robot_ip6ip62_kharejserver2", [
            "/usr/local/bin/robot_ip6ip6_kharejserver2.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver2.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver2.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver2_inputs.txt"
        ]),
        ("robot_ip6ip63_kharejserver3", [
            "/usr/local/bin/robot_ip6ip6_kharejserver3.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver3.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver3.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver3_inputs.txt"
        ]),
        ("robot_ip6ip64_kharejserver4", [
            "/usr/local/bin/robot_ip6ip6_kharejserver4.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver4.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver4.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver4_inputs.txt"
        ]),
        ("robot_ip6ip65_kharejserver5", [
            "/usr/local/bin/robot_ip6ip6_kharejserver5.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver5.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver5.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver5_inputs.txt"
        ]),
        ("robot_ip6ip66_kharejserver6", [
            "/usr/local/bin/robot_ip6ip6_kharejserver6.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver6.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver6.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver6_inputs.txt"
        ]),
        ("robot_ip6ip67_kharejserver7", [
            "/usr/local/bin/robot_ip6ip6_kharejserver7.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver7.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver7.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver7_inputs.txt"
        ]),
        ("robot_ip6ip68_kharejserver8", [
            "/usr/local/bin/robot_ip6ip6_kharejserver8.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver8.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver8.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver8_inputs.txt"
        ]),
        ("robot_ip6ip69_kharejserver9", [
            "/usr/local/bin/robot_ip6ip6_kharejserver9.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver9.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver9.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver9_inputs.txt"
        ]),
        ("robot_ip6ip610_kharejserver10", [
            "/usr/local/bin/robot_ip6ip6_kharejserver10.py",
            "/usr/local/bin/robot_ip6ip6_kharejserver10.sh",
            "/etc/systemd/system/robot_ip6ip6_kharejserver10.service",
            "/usr/local/bin/multi_ip6ip6_kharejserver10_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver1", [
            "/usr/local/bin/robot_ip6ip6_iranserver1.py",
            "/usr/local/bin/robot_ip6ip6_iranserver1.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver1.service",
            "/usr/local/bin/multi_ip6ip6_iranserver1_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver2", [
            "/usr/local/bin/robot_ip6ip6_iranserver2.py",
            "/usr/local/bin/robot_ip6ip6_iranserver2.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver2.service",
            "/usr/local/bin/multi_ip6ip6_iranserver2_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver3", [
            "/usr/local/bin/robot_ip6ip6_iranserver3.py",
            "/usr/local/bin/robot_ip6ip6_iranserver3.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver3.service",
            "/usr/local/bin/multi_ip6ip6_iranserver3_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver4", [
            "/usr/local/bin/robot_ip6ip6_iranserver4.py",
            "/usr/local/bin/robot_ip6ip6_iranserver4.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver4.service",
            "/usr/local/bin/multi_ip6ip6_iranserver4_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver5", [
            "/usr/local/bin/robot_ip6ip6_iranserver5.py",
            "/usr/local/bin/robot_ip6ip6_iranserver5.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver5.service",
            "/usr/local/bin/multi_ip6ip6_iranserver5_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver6", [
            "/usr/local/bin/robot_ip6ip6_iranserver6.py",
            "/usr/local/bin/robot_ip6ip6_iranserver6.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver6.service",
            "/usr/local/bin/multi_ip6ip6_iranserver6_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver7", [
            "/usr/local/bin/robot_ip6ip6_iranserver7.py",
            "/usr/local/bin/robot_ip6ip6_iranserver7.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver7.service",
            "/usr/local/bin/multi_ip6ip6_iranserver7_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver8", [
            "/usr/local/bin/robot_ip6ip6_iranserver8.py",
            "/usr/local/bin/robot_ip6ip6_iranserver8.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver8.service",
            "/usr/local/bin/multi_ip6ip6_iranserver8_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver9", [
            "/usr/local/bin/robot_ip6ip6_iranserver9.py",
            "/usr/local/bin/robot_ip6ip6_iranserver9.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver9.service",
            "/usr/local/bin/multi_ip6ip6_iranserver9_inputs.txt"
        ]),
        ("robot_ip6ip6_iranserver10", [
            "/usr/local/bin/robot_ip6ip6_iranserver10.py",
            "/usr/local/bin/robot_ip6ip6_iranserver10.sh",
            "/etc/systemd/system/robot_ip6ip6_iranserver10.service",
            "/usr/local/bin/multi_ip6ip6_iranserver10_inputs.txt"
        ]),
    ]

    for service_name, files in services:
        uninstall_service(service_name, files)

    print("\033[92mUninstallation is done.\033[0m")

def robot_multi_mnu():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mMulti\033[93m Robot Menu\033[0m"
    )
    print(
        '\033[92m "-"\033[93m══════════════════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mWhich one to edit:\033[0m")
    print("1.  \033[92m IP6IP6\033[0m")
    print("2.  \033[91m Remove\033[0m")
    print("0.  \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robotreconfig_multi_ip6ip6()
            break
        elif choice == "2":
            remove_multi_robot()
            break
        elif choice == "0":
            clear()
            robot_menu()
            break
        else:
            print("Invalid choice.")

def remove_multi_robot():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mRemove Robot \033[92mIP6IP6 multi \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej [10] IRAN [1]\033[0m")
    print("2  \033[92mKharej [1] IRAN [10]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            remove_ip6ip6_multi_iran1kharej10()
            break
        elif choice == "2":
            remove_services_ip6ip6_multi_iran10kharej1()
            break
        elif choice == "0":
            clear()
            robot_multi_mnu()
            break
        else:
            print("Invalid choice.")

def robotreconfig_multi_ip6ip6():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93mMenu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej [10] IRAN [1]\033[0m")
    print("2  \033[92mKharej [1] IRAN [10]\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_multimenu_ip6ip6_kharej()
            break
        elif choice == "2":
            robot_multi_menu_ip6ip6_iran()
            break
        elif choice == "0":
            clear()
            robot_multi_mnu()
            break
        else:
            print("Invalid choice.")


def robot_multimenu_ip6ip6_kharej():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93m Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs [1]\033[0m")
    print("2  \033[93mKharej Inputs [2]\033[0m")
    print("3  \033[93mKharej Inputs [3]\033[0m")
    print("4  \033[93mKharej Inputs [4]\033[0m")
    print("5  \033[93mKharej Inputs [5]\033[0m")
    print("6  \033[93mKharej Inputs [6]\033[0m")
    print("7  \033[93mKharej Inputs [7]\033[0m")
    print("8  \033[93mKharej Inputs [8]\033[0m")
    print("9  \033[93mKharej Inputs [9]\033[0m")
    print("10 \033[93mKharej Inputs [10]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("11 \033[92mIRAN Inputs \033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_multi_ip6ip6_kharej1()
            break
        elif choice == "2":
            robot_multi_ip6ip6_kharej2()
            break
        elif choice == "3":
            robot_multi_ip6ip6_kharej3()
            break
        elif choice == "4":
            robot_multi_ip6ip6_kharej4()
            break
        elif choice == "5":
            robot_multi_ip6ip6_kharej5()
            break
        elif choice == "6":
            robot_multi_ip6ip6_kharej6()
            break
        elif choice == "7":
            robot_multi_ip6ip6_kharej7()
            break
        elif choice == "8":
            robot_multi_ip6ip6_kharej8()
            break
        elif choice == "9":
            robot_multi_ip6ip6_kharej9()
            break
        elif choice == "10":
            robot_multi_ip6ip6_kharej10()
            break
        elif choice == "11":
            robot_multimenu_ip6ip6_iran()
            break
        elif choice == "0":
            clear()
            robot_multi_mnu()
            break
        else:
            print("Invalid choice.")


def robot_multimenu_ip6ip6_iran():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93m IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mIRAN Inputs [1]\033[0m")
    print("2  \033[93mIRAN Inputs [2]\033[0m")
    print("3  \033[93mIRAN Inputs [3]\033[0m")
    print("4  \033[93mIRAN Inputs [4]\033[0m")
    print("5  \033[93mIRAN Inputs [5]\033[0m")
    print("6  \033[93mIRAN Inputs [6]\033[0m")
    print("7  \033[93mIRAN Inputs [7]\033[0m")
    print("8  \033[93mIRAN Inputs [8]\033[0m")
    print("9  \033[93mIRAN Inputs [9]\033[0m")
    print("10 \033[93mIRAN Inputs [10]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_multi_ip6ip6_iran1()
            break
        elif choice == "2":
            robot_multi_ip6ip6_iran2()
            break
        elif choice == "3":
            robot_multi_ip6ip6_iran3()
            break
        elif choice == "4":
            robot_multi_ip6ip6_iran4()
            break
        elif choice == "5":
            robot_multi_ip6ip6_iran5()
            break
        elif choice == "6":
            robot_multi_ip6ip6_iran6()
            break
        elif choice == "7":
            robot_multi_ip6ip6_iran7()
            break
        elif choice == "8":
            robot_multi_ip6ip6_iran8()
            break
        elif choice == "9":
            robot_multi_ip6ip6_iran9()
            break
        elif choice == "10":
            robot_multi_ip6ip6_iran10()
            break
        elif choice == "0":
            clear()
            robot_multimenu_ip6ip6_kharej()
            break
        else:
            print("Invalid choice.")


def multiip6ip6_kharejuser_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a022::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a022::2'

    inputs['ip6ip6_method'] = '1'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip1'] = input(
        "\033[93mEnter \033[92mKharej [1] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1'

    return inputs


def generate_bash_script_multiip6ip6_kharej(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej1.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej1.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej1.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej1.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej1.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej1_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej1.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej1_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej1():
    inputs = multiip6ip6_kharejuser_input()
    store_inputs_multiip6ip6kharej(inputs)
    generate_bash_script_multiip6ip6_kharej(inputs)
    create_script_multiip6ip6kharej()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")


# server 2

def multiip6ip6_kharejuser_input2():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a122::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a122::2'

    inputs['ip6ip6_method'] = '2'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip2'] = input(
        "\033[93mEnter \033[92mKharej [2] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2'

    return inputs


def generate_bash_script_multiip6ip6_kharej2(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej2.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej2.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej2.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej2.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej2.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej2(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej2_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej2():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej2.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej2_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej2():
    inputs = multiip6ip6_kharejuser_input2()
    store_inputs_multiip6ip6kharej2(inputs)
    generate_bash_script_multiip6ip6_kharej2(inputs)
    create_script_multiip6ip6kharej2()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 3

def multiip6ip6_kharejuser_input3():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a222::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a222::2'

    inputs['ip6ip6_method'] = '3'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip3'] = input(
        "\033[93mEnter \033[92mKharej [3] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '3'

    return inputs


def generate_bash_script_multiip6ip6_kharej3(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej3.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej3.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej3.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej3.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej3.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej3(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej3_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej3():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej3.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej3_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej3():
    inputs = multiip6ip6_kharejuser_input3()
    store_inputs_multiip6ip6kharej3(inputs)
    generate_bash_script_multiip6ip6_kharej3(inputs)
    create_script_multiip6ip6kharej3()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#server 4 kharej

def multiip6ip6_kharejuser_input4():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a322::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a322::2'

    inputs['ip6ip6_method'] = '4'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip4'] = input(
        "\033[93mEnter \033[92mKharej [4] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '4'

    return inputs


def generate_bash_script_multiip6ip6_kharej4(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej4.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej4.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej4.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej4.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej4.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej4(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej4_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej4():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej4.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej4_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej4():
    inputs = multiip6ip6_kharejuser_input4()
    store_inputs_multiip6ip6kharej4(inputs)
    generate_bash_script_multiip6ip6_kharej4(inputs)
    create_script_multiip6ip6kharej4()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 5 kharej

def multiip6ip6_kharejuser_input5():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a422::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a422::2'

    inputs['ip6ip6_method'] = '5'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip5'] = input(
        "\033[93mEnter \033[92mKharej [5] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '5'

    return inputs


def generate_bash_script_multiip6ip6_kharej5(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej5.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej5.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej5.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej5.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej5.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej5(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej5_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej5():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej5.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej5_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej5():
    inputs = multiip6ip6_kharejuser_input5()
    store_inputs_multiip6ip6kharej5(inputs)
    generate_bash_script_multiip6ip6_kharej5(inputs)
    create_script_multiip6ip6kharej5()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 6 kharej

def multiip6ip6_kharejuser_input6():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a522::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a522::2'

    inputs['ip6ip6_method'] = '6'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip6'] = input(
        "\033[93mEnter \033[92mKharej [6] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '6'

    return inputs


def generate_bash_script_multiip6ip6_kharej6(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej6.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej6.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej6(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej6():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej6.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej6():
    inputs = multiip6ip6_kharejuser_input6()
    store_inputs_multiip6ip6kharej6(inputs)
    generate_bash_script_multiip6ip6_kharej6(inputs)
    create_script_multiip6ip6kharej6()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 7 kharej

def multiip6ip6_kharejuser_input7():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a622::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a622::2'

    inputs['ip6ip6_method'] = '7'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip7'] = input(
        "\033[93mEnter \033[92mKharej [7] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '7'

    return inputs


def generate_bash_script_multiip6ip6_kharej7(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej7.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej7.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej7.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej7.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej7.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej7(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej7_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej7():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej7.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej7_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej7():
    inputs = multiip6ip6_kharejuser_input7()
    store_inputs_multiip6ip6kharej7(inputs)
    generate_bash_script_multiip6ip6_kharej7(inputs)
    create_script_multiip6ip6kharej7()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 8 kharej

def multiip6ip6_kharejuser_input8():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a722::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a722::2'

    inputs['ip6ip6_method'] = '8'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip8'] = input(
        "\033[93mEnter \033[92mKharej [8] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '8'

    return inputs


def generate_bash_script_multiip6ip6_kharej8(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej8.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej8.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej8.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej8.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej8.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej8(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej8_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej8():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej8.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej8_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip8']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej8():
    inputs = multiip6ip6_kharejuser_input8()
    store_inputs_multiip6ip6kharej8(inputs)
    generate_bash_script_multiip6ip6_kharej8(inputs)
    create_script_multiip6ip6kharej8()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 9 kharej

def multiip6ip6_kharejuser_input9():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a822::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a822::2'

    inputs['ip6ip6_method'] = '9'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip9'] = input(
        "\033[93mEnter \033[92mKharej [9] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '9'

    return inputs


def generate_bash_script_multiip6ip6_kharej9(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej9.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej9.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej9.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej9.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej9.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej9(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej9_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej9():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej9.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej9_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip9']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej9():
    inputs = multiip6ip6_kharejuser_input9()
    store_inputs_multiip6ip6kharej9(inputs)
    generate_bash_script_multiip6ip6_kharej9(inputs)
    create_script_multiip6ip6kharej9()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
# server 10 kharej

def multiip6ip6_kharejuser_input10():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '1'
    inputs['private_kharej_ip'] = '2002:db8:1234:a922::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a922::2'

    inputs['ip6ip6_method'] = '9'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip10'] = input(
        "\033[93mEnter \033[92mKharej [10] \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '10'

    return inputs


def generate_bash_script_multiip6ip6_kharej10(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharej10.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharej10.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharej10.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharej10.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharej10.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6kharej10(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharej10_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharej10():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharej10.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharej10_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip10']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharej10():
    inputs = multiip6ip6_kharejuser_input10()
    store_inputs_multiip6ip6kharej10(inputs)
    generate_bash_script_multiip6ip6_kharej10(inputs)
    create_script_multiip6ip6kharej10()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 1    
def multiip6ip6_iranuser_input1():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['ip6ip6_choose'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a022::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a022::2'

    inputs['ip6ip6_method'] = '11'
    inputs['iranserver_choose'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [1] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '11' 
    inputs['uninstall_input6'] = '1' 

    return inputs

def generate_bash_script_multiip6ip6_iran1(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran1.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran1.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran1.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran1.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran1.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran1(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran1_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran1():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran1.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran1_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran1():
    inputs = multiip6ip6_iranuser_input1()
    store_inputs_multiip6ip6iran1(inputs)
    generate_bash_script_multiip6ip6_iran1(inputs)
    create_script_multiip6ip6iran1() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 2   
def multiip6ip6_iranuser_input2():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a122::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a122::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [2] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '2'

    return inputs

def generate_bash_script_multiip6ip6_iran2(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran2.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran2.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran2.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran2.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran2.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran2(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran2_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran2():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran2.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran2_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran2():
    inputs = multiip6ip6_iranuser_input2()
    store_inputs_multiip6ip6iran2(inputs)
    generate_bash_script_multiip6ip6_iran2(inputs)
    create_script_multiip6ip6iran2() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 3   
def multiip6ip6_iranuser_input3():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a222::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a222::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '3'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [3] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '3'

    return inputs

def generate_bash_script_multiip6ip6_iran3(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran3.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran3.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran3.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran3.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran3.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran3(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran3_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran3():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran3.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran3_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran3():
    inputs = multiip6ip6_iranuser_input3()
    store_inputs_multiip6ip6iran3(inputs)
    generate_bash_script_multiip6ip6_iran3(inputs)
    create_script_multiip6ip6iran3() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 4   
def multiip6ip6_iranuser_input4():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a322::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a322::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '4'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [4] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '4'

    return inputs

def generate_bash_script_multiip6ip6_iran4(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran4.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran4.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran4.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran4.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran4.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran4(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran4_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran4():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran4.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran4_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran4():
    inputs = multiip6ip6_iranuser_input4()
    store_inputs_multiip6ip6iran4(inputs)
    generate_bash_script_multiip6ip6_iran4(inputs)
    create_script_multiip6ip6iran4() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 5   
def multiip6ip6_iranuser_input5():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a422::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a422::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '5'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [5] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '5'

    return inputs

def generate_bash_script_multiip6ip6_iran5(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran5.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran5.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran5.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran5.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran5.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran5(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran5_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran5():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran5.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran5_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran5():
    inputs = multiip6ip6_iranuser_input5()
    store_inputs_multiip6ip6iran5(inputs)
    generate_bash_script_multiip6ip6_iran5(inputs)
    create_script_multiip6ip6iran5() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 6   
def multiip6ip6_iranuser_input6():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a522::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a522::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '6'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [6] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '6'

    return inputs

def generate_bash_script_multiip6ip6_iran6(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran6(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran6():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran6():
    inputs = multiip6ip6_iranuser_input6()
    store_inputs_multiip6ip6iran6(inputs)
    generate_bash_script_multiip6ip6_iran6(inputs)
    create_script_multiip6ip6iran6() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 7   
def multiip6ip6_iranuser_input7():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a622::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a622::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '7'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [7] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '7'

    return inputs

def generate_bash_script_multiip6ip6_iran7(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran7.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran7.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran7.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran7.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran7.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran7(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran7_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran7():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran7.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran7_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran7():
    inputs = multiip6ip6_iranuser_input7()
    store_inputs_multiip6ip6iran7(inputs)
    generate_bash_script_multiip6ip6_iran7(inputs)
    create_script_multiip6ip6iran7() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 8   
def multiip6ip6_iranuser_input8():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a722::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a722::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '8'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [8] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '8'

    return inputs

def generate_bash_script_multiip6ip6_iran8(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran8.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran8.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran8.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran8.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran8.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran8(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran8_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran8():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran8.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran8_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran8():
    inputs = multiip6ip6_iranuser_input8()
    store_inputs_multiip6ip6iran8(inputs)
    generate_bash_script_multiip6ip6_iran8(inputs)
    create_script_multiip6ip6iran8() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 9   
def multiip6ip6_iranuser_input9():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a822::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a822::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '9'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [9] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '9'

    return inputs

def generate_bash_script_multiip6ip6_iran9(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran9.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran9.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran9.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran9.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran9.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran9(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran9_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran9():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran9.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran9_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran9():
    inputs = multiip6ip6_iranuser_input9()
    store_inputs_multiip6ip6iran9(inputs)
    generate_bash_script_multiip6ip6_iran9(inputs)
    create_script_multiip6ip6iran9() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran server 10  
def multiip6ip6_iranuser_input10():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a922::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a922::2'

    inputs['ip6ip6_method'] = '1'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '10'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej [10] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '1' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '10'

    return inputs

def generate_bash_script_multiip6ip6_iran10(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iran10.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iran10.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iran10.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iran10.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iran10.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6iran10(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iran10_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iran10():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iran10.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iran10_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iran10():
    inputs = multiip6ip6_iranuser_input10()
    store_inputs_multiip6ip6iran10(inputs)
    generate_bash_script_multiip6ip6_iran10(inputs)
    create_script_multiip6ip6iran10() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

# iran menu
def robot_multi_menu_ip6ip6_iran():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93m IRAN Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mIRAN Inputs [1]\033[0m")
    print("2  \033[93mIRAN Inputs [2]\033[0m")
    print("3  \033[93mIRAN Inputs [3]\033[0m")
    print("4  \033[93mIRAN Inputs [4]\033[0m")
    print("5  \033[93mIRAN Inputs [5]\033[0m")
    print("6  \033[93mIRAN Inputs [6]\033[0m")
    print("7  \033[93mIRAN Inputs [7]\033[0m")
    print("8  \033[93mIRAN Inputs [8]\033[0m")
    print("9  \033[93mIRAN Inputs [9]\033[0m")
    print("10 \033[93mIRAN Inputs [10]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("11 \033[92mKharej Inputs \033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_multi_ip6ip6_iranserver1()
            break
        elif choice == "2":
            robot_multi_ip6ip6_iranserver2()
            break
        elif choice == "3":
            robot_multi_ip6ip6_iranserver3()
            break
        elif choice == "4":
            robot_multi_ip6ip6_iranserver4()
            break
        elif choice == "5":
            robot_multi_ip6ip6_iranserver5()
            break
        elif choice == "6":
            robot_multi_ip6ip6_iranserver6()
            break
        elif choice == "7":
            robot_multi_ip6ip6_iranserver7()
            break
        elif choice == "8":
            robot_multi_ip6ip6_iranserver8()
            break
        elif choice == "9":
            robot_multi_ip6ip6_iranserver9()
            break
        elif choice == "10":
            robot_multi_ip6ip6_iranserver10()
            break
        elif choice == "11":
            robot_multimenu_ip6ip6_kharejservers()
            break
        elif choice == "0":
            clear()
            robot_multi_mnu()
            break
        else:
            print("Invalid choice.")


def robot_multimenu_ip6ip6_kharejservers():
    os.system("clear")
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print(
        "\033[92m(   ) \033[92mReconfig Robot \033[92mIP6IP6 \033[93m Kharej Menu\033[0m")
    print('\033[92m "-"\033[93m══════════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1  \033[93mKharej Inputs [1]\033[0m")
    print("2  \033[93mKharej Inputs [2]\033[0m")
    print("3  \033[93mKharej Inputs [3]\033[0m")
    print("4  \033[93mKharej Inputs [4]\033[0m")
    print("5  \033[93mKharej Inputs [5]\033[0m")
    print("6  \033[93mKharej Inputs [6]\033[0m")
    print("7  \033[93mKharej Inputs [7]\033[0m")
    print("8  \033[93mKharej Inputs [8]\033[0m")
    print("9  \033[93mKharej Inputs [9]\033[0m")
    print("10 \033[93mKharej Inputs [10]\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    print("0. \033[94mback to the previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        choice = input("\033[38;5;205mEnter your choice Please: \033[0m")
        if choice == "1":
            robot_multi_ip6ip6_kharejserver1()
            break
        elif choice == "2":
            robot_multi_ip6ip6_kharejserver2()
            break
        elif choice == "3":
            robot_multi_ip6ip6_kharejserver3()
            break
        elif choice == "4":
            robot_multi_ip6ip6_kharejserver4()
            break
        elif choice == "5":
            robot_multi_ip6ip6_kharejserver5()
            break
        elif choice == "6":
            robot_multi_ip6ip6_kharejserver6()
            break
        elif choice == "7":
            robot_multi_ip6ip6_kharejserver7()
            break
        elif choice == "8":
            robot_multi_ip6ip6_kharejserver8()
            break
        elif choice == "9":
            robot_multi_ip6ip6_kharejserver9()
            break
        elif choice == "10":
            robot_multi_ip6ip6_kharejserver10()
            break
        elif choice == "0":
            clear()
            robot_multi_menu_ip6ip6_iran()
            break
        else:
            print("Invalid choice.")

def multiip6ip6_iranserveruser1_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a022::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a022::2'

    inputs['ip6ip6_method'] = '1'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [1] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '1'

    return inputs


def generate_bash_script_multiip6ip6_iranserver1(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver1.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver1.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver1.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver1.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver1.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver1(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver1_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver1():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver1.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver1_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver1():
    inputs = multiip6ip6_iranserveruser1_input()
    store_inputs_multiip6ip6iranserver1(inputs)
    generate_bash_script_multiip6ip6_iranserver1(inputs)
    create_script_multiip6ip6iranserver1()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
#2
def multiip6ip6_iranserveruser2_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a122::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a122::2'

    inputs['ip6ip6_method'] = '2'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [2] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '2'

    return inputs


def generate_bash_script_multiip6ip6_iranserver2(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver2.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver2.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver2.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver2.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver2.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver2(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver2_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver2():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver2.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver2_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver2():
    inputs = multiip6ip6_iranserveruser2_input()
    store_inputs_multiip6ip6iranserver2(inputs)
    generate_bash_script_multiip6ip6_iranserver2(inputs)
    create_script_multiip6ip6iranserver2()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#3
def multiip6ip6_iranserveruser3_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a222::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a222::2'

    inputs['ip6ip6_method'] = '3'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [3] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '3'

    return inputs


def generate_bash_script_multiip6ip6_iranserver3(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver3.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver3.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver3.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver3.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver3.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver3(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver3_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver3():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver3.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver3_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver3():
    inputs = multiip6ip6_iranserveruser3_input()
    store_inputs_multiip6ip6iranserver3(inputs)
    generate_bash_script_multiip6ip6_iranserver3(inputs)
    create_script_multiip6ip6iranserver3()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#4
def multiip6ip6_iranserveruser4_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a322::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a322::2'

    inputs['ip6ip6_method'] = '4'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [4] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '4'

    return inputs


def generate_bash_script_multiip6ip6_iranserver4(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver4.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver4.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver4.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver4.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver4.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver4(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver4_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver4():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver4.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver4_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver4():
    inputs = multiip6ip6_iranserveruser4_input()
    store_inputs_multiip6ip6iranserver4(inputs)
    generate_bash_script_multiip6ip6_iranserver4(inputs)
    create_script_multiip6ip6iranserver4()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#5
def multiip6ip6_iranserveruser5_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a422::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a422::2'

    inputs['ip6ip6_method'] = '5'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [5] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '5'

    return inputs


def generate_bash_script_multiip6ip6_iranserver5(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver5.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver5.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver5.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver5.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver5.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver5(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver5_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver5():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver5.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver5_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver5():
    inputs = multiip6ip6_iranserveruser5_input()
    store_inputs_multiip6ip6iranserver5(inputs)
    generate_bash_script_multiip6ip6_iranserver5(inputs)
    create_script_multiip6ip6iranserver5()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#6
def multiip6ip6_iranserveruser6_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a522::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a522::2'

    inputs['ip6ip6_method'] = '6'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [6] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '6'

    return inputs


def generate_bash_script_multiip6ip6_iranserver6(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver6.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver6.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver6(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver6():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver6.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver6():
    inputs = multiip6ip6_iranserveruser6_input()
    store_inputs_multiip6ip6iranserver6(inputs)
    generate_bash_script_multiip6ip6_iranserver6(inputs)
    create_script_multiip6ip6iranserver6()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#7
def multiip6ip6_iranserveruser7_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a622::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a622::2'

    inputs['ip6ip6_method'] = '7'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [7] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '7'

    return inputs


def generate_bash_script_multiip6ip6_iranserver7(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver7.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver7.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver7.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver7.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver7.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver7(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver7_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver7():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver7.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver7_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver7():
    inputs = multiip6ip6_iranserveruser7_input()
    store_inputs_multiip6ip6iranserver7(inputs)
    generate_bash_script_multiip6ip6_iranserver7(inputs)
    create_script_multiip6ip6iranserver7()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#8
def multiip6ip6_iranserveruser8_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a722::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a722::2'

    inputs['ip6ip6_method'] = '8'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [8] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '8'

    return inputs


def generate_bash_script_multiip6ip6_iranserver8(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver8.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver8.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver8.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver8.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver8.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver8(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver8_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver8():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver8.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver8_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver8():
    inputs = multiip6ip6_iranserveruser8_input()
    store_inputs_multiip6ip6iranserver8(inputs)
    generate_bash_script_multiip6ip6_iranserver8(inputs)
    create_script_multiip6ip6iranserver8()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#9
def multiip6ip6_iranserveruser9_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a822::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a822::2'

    inputs['ip6ip6_method'] = '9'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [9] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '9'

    return inputs


def generate_bash_script_multiip6ip6_iranserver9(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver9.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver9.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver9.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver9.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver9.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver9(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver9_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver9():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver9.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver9_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver9():
    inputs = multiip6ip6_iranserveruser9_input()
    store_inputs_multiip6ip6iranserver9(inputs)
    generate_bash_script_multiip6ip6_iranserver9(inputs)
    create_script_multiip6ip6iranserver9()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#10
def multiip6ip6_iranserveruser10_input():

    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '1'
    inputs['multi_choose'] = '2'
    inputs['private_kharej_ip'] = '2002:db8:1234:a922::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a922::2'

    inputs['ip6ip6_method'] = '10'
    print(
        "\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['iran_ip'] = input(
        "\033[93mEnter \033[92mIRAN [10] \033[93mIPV4 address: \033[0m")
    inputs['kharej_ip'] = input(
        "\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input(
        "\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['default_route'] = 'n'
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input(
        "\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input(
        "\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print(
        "\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '12'
    inputs['uninstall_input3'] = '1'
    inputs['uninstall_input4'] = '2'
    inputs['uninstall_input5'] = '10'

    return inputs


def generate_bash_script_multiip6ip6_iranserver10(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_iran_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_iranserver10.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_iranserver10.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_iranserver10.service"

    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_iranserver10.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_iranserver10.service"])

    print(f"\033[92mscript saved and service created\033[0m")


def store_inputs_multiip6ip6iranserver10(inputs):
    with open("/usr/local/bin/multi_ip6ip6_iranserver10_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6iranserver10():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_iranserver10.py")

    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_iranserver10_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['multi_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['default_route']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_iranserver10():
    inputs = multiip6ip6_iranserveruser10_input()
    store_inputs_multiip6ip6iranserver10(inputs)
    generate_bash_script_multiip6ip6_iranserver10(inputs)
    create_script_multiip6ip6iranserver10()
    print(
        "\033[92mInputs have been saved and the service has been created successfully\033[0m")
    
#kharej1
def multiip6ip6_kharejserveruser_input1():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a122::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a122::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '1'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [1] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '1'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver1(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver1.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver1.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver1.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver1.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver1.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver1(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver1_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver1():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver1.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver1_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver1():
    inputs = multiip6ip6_kharejserveruser_input1()
    store_inputs_multiip6ip6kharejserver1(inputs)
    generate_bash_script_multiip6ip6_kharejserver1(inputs)
    create_script_multiip6ip6kharejserver1() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej2
def multiip6ip6_kharejserveruser_input2():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a222::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a222::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '2'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [2] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '2'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver2(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver2.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver2.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver2.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver2.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver2.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver2(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver2_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver2():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver2.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver2_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver2():
    inputs = multiip6ip6_kharejserveruser_input2()
    store_inputs_multiip6ip6kharejserver2(inputs)
    generate_bash_script_multiip6ip6_kharejserver2(inputs)
    create_script_multiip6ip6kharejserver2() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej3
def multiip6ip6_kharejserveruser_input3():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a222::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a222::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '3'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [3] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '3'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver3(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver3.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver3.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver3.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver3.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver3.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver3(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver3_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver3():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver3.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver3_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver3():
    inputs = multiip6ip6_kharejserveruser_input3()
    store_inputs_multiip6ip6kharejserver3(inputs)
    generate_bash_script_multiip6ip6_kharejserver3(inputs)
    create_script_multiip6ip6kharejserver3() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej4
def multiip6ip6_kharejserveruser_input4():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a322::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a322::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '4'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [4] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '4'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver4(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver4.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver4.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver4.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver4.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver4.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver4(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver4_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver4():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver4.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver4_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver4():
    inputs = multiip6ip6_kharejserveruser_input4()
    store_inputs_multiip6ip6kharejserver4(inputs)
    generate_bash_script_multiip6ip6_kharejserver4(inputs)
    create_script_multiip6ip6kharejserver4() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#5
def multiip6ip6_kharejserveruser_input5():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a422::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a422::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '5'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [5] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '5'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver5(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver5.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver5.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver5.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver5.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver5.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver5(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver5_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver5():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver5.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver5_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver5():
    inputs = multiip6ip6_kharejserveruser_input5()
    store_inputs_multiip6ip6kharejserver5(inputs)
    generate_bash_script_multiip6ip6_kharejserver5(inputs)
    create_script_multiip6ip6kharejserver5() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej6

def multiip6ip6_kharejserveruser_input6():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a522::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a522::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '6'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [6] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '6'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver6(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver6.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver6.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver6.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver6.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver6.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver6(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver6_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver6():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver6.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver6_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver6():
    inputs = multiip6ip6_kharejserveruser_input6()
    store_inputs_multiip6ip6kharejserver6(inputs)
    generate_bash_script_multiip6ip6_kharejserver6(inputs)
    create_script_multiip6ip6kharejserver6() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej 7

def multiip6ip6_kharejserveruser_input7():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a622::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a622::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '7'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [7] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '7'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver7(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver7.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver7.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver7.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver7.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver7.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver7(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver7_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver7():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver7.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver7_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver7():
    inputs = multiip6ip6_kharejserveruser_input7()
    store_inputs_multiip6ip6kharejserver7(inputs)
    generate_bash_script_multiip6ip6_kharejserver7(inputs)
    create_script_multiip6ip6kharejserver7() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej 8

def multiip6ip6_kharejserveruser_input8():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a722::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a722::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '8'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [8] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '8'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver8(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver8.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver8.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver8.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver8.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver8.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver8(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver8_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver8():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver8.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver8_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver8():
    inputs = multiip6ip6_kharejserveruser_input8()
    store_inputs_multiip6ip6kharejserver8(inputs)
    generate_bash_script_multiip6ip6_kharejserver8(inputs)
    create_script_multiip6ip6kharejserver8() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej 9

def multiip6ip6_kharejserveruser_input9():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a822::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a822::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '9'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [9] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '9'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver9(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver9.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver9.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver9.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver9.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver9.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver9(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver9_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver9():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver9.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver9_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver9():
    inputs = multiip6ip6_kharejserveruser_input9()
    store_inputs_multiip6ip6kharejserver9(inputs)
    generate_bash_script_multiip6ip6_kharejserver9(inputs)
    create_script_multiip6ip6kharejserver9() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

#kharej10

def multiip6ip6_kharejserveruser_input10():
    
    inputs = {}

    inputs['input_value'] = '3'
    inputs['local_tunnel'] = '10'
    inputs['ip6ip6_choose'] = '1'
    inputs['ip6ip6_choose2'] = '1'

    inputs['private_kharej_ip'] = '2002:db8:1234:a922::1'
    inputs['private_iran_ip'] = '2002:db8:1234:a922::2'

    inputs['ip6ip6_method'] = '2'
    inputs['iranserver_choose'] = '11'
    inputs['iranserver_choose2'] = '10'
    print("\033[93m╭────────────────────────────────────────────────────────╮\033[0m")
    inputs['kharej_ip'] = input("\033[93mEnter \033[92mKharej \033[93mIPV4 address: \033[0m")
    inputs['iran_ip'] = input("\033[93mEnter \033[92mIRAN [10] \033[93mIPV4 address: \033[0m")
    

    inputs['set_mtu_6to4'] = 'n'
    inputs['additional_ips'] = input("\033[93mHow many \033[92madditional IPs \033[93mdo you need?\033[0m ")
    inputs['set_mtu_ip6ip6'] = 'n'
    inputs['ping_count'] = input("\033[93mEnter the \033[92mping count\033[93m [1-5]:\033[0m ")
    inputs['ping_interval'] = input("\033[93mEnter the \033[92mping interval\033[93m in seconds:\033[0m ")
    print("\033[93m╰────────────────────────────────────────────────────────╯\033[0m")

    inputs['uninstall_input1'] = '3'
    inputs['uninstall_input2'] = '10'
    inputs['uninstall_input3'] = '2' 
    inputs['uninstall_input4'] = '1'
    inputs['uninstall_input5'] = '2' 
    inputs['uninstall_input6'] = '11' 
    inputs['uninstall_input7'] = '10'

    return inputs

def generate_bash_script_multiip6ip6_kharejserver10(inputs):
    bash_script = f"""#!/bin/bash
while true; do
    ping -c {inputs['ping_count']} -W {inputs['ping_interval']} {inputs['private_kharej_ip']}
    if [ $? -ne 0 ]; then
        echo "Ping failed, running script.."
        python3 /usr/local/bin/robot_ip6ip6_kharejserver10.py
    fi
    sleep {inputs['ping_interval']}
done
"""

    script_path = "/usr/local/bin/robot_ip6ip6_kharejserver10.sh"
    service_path = "/etc/systemd/system/robot_ip6ip6_kharejserver10.service"


    with open(script_path, "w") as script_file:
        script_file.write(bash_script)

    os.chmod(script_path, 0o755)

    service_content = f"""[Unit]
Description=Ping Check Service

[Service]
ExecStart={script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "robot_ip6ip6_kharejserver10.service"])
    subprocess.run(["systemctl", "restart", "robot_ip6ip6_kharejserver10.service"])

    print(f"\033[92mscript saved and service created\033[0m")

def store_inputs_multiip6ip6kharejserver10(inputs):
    with open("/usr/local/bin/multi_ip6ip6_kharejserver10_inputs.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{key}={value}\n")


def create_script_multiip6ip6kharejserver10():
    directory = "/usr/local/bin"
    script_path = os.path.join(directory, "robot_ip6ip6_kharejserver10.py")


    lines = [
        "import time",
        "import subprocess",
        "import os",
        "",
        "def read_inputs():",
        "    inputs = {}",
        "    with open('/usr/local/bin/multi_ip6ip6_kharejserver10_inputs.txt', 'r') as f:",
        "        for line in f:",
        "            key, value = line.strip().split('=')",
        "            inputs[key] = value",
        "    return inputs",
        "",
        "def run_script(inputs):",
        "    subprocess.run(['rm', '-f', 'light_script.py'])",
        "    subprocess.run(['wget', 'https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/light_script.py'])",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input1']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input3']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input5']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input6']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['uninstall_input7']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "    process = subprocess.Popen(['python3', 'light_script.py'], stdin=subprocess.PIPE, text=True)",
        "    time.sleep(10)",
        "",
        "    process.stdin.write(f\"{inputs['input_value']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['local_tunnel']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['ip6ip6_method']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iranserver_choose2']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['kharej_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['iran_ip']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_6to4']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['additional_ips']}\\n\")",
        "    process.stdin.flush()",
        "    time.sleep(5)",
        "",
        "    process.stdin.write(f\"{inputs['set_mtu_ip6ip6']}\\n\")",
        "    process.stdin.flush()",
        "",
        "    process.stdin.close()",
        "    process.wait()",
        "",
        "def main():",
        "    inputs = read_inputs()",
        "",
        "    run_script(inputs)",
        "",
        "main()"
    ]

    with open(script_path, "w") as script_file:
        script_file.write("\n".join(lines))

    print(f"\033[92mScript saved\033[0m")


def robot_multi_ip6ip6_kharejserver10():
    inputs = multiip6ip6_kharejserveruser_input10()
    store_inputs_multiip6ip6kharejserver10(inputs)
    generate_bash_script_multiip6ip6_kharejserver10(inputs)
    create_script_multiip6ip6kharejserver10() 
    print("\033[92mInputs have been saved and the service has been created successfully\033[0m")

robot_menu()
