#
# 6to4 Configuration Script
# Author: github.com/Azumi67
# This is for educational use and my own learning, please provide me with feedback if possible
# This script is designed to simplify the configuration of 6to4 tunnels.
#
# Supported operating systems: Ubuntu 20, Debian 12
#
# Usage:
#   - Run the script with root privileges.
#   - Follow the on-screen prompts to install, configure, or uninstall the tunnel.
#
#
# Disclaimer:
# This script comes with no warranties or guarantees. Use it at your own risk.
import sys
import os
import time
import colorama
from colorama import Fore, Style
import subprocess
from time import sleep
import readline
import netifaces
import netifaces as ni
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')

if os.geteuid() != 0:
    print("\033[91mThis script must be run as root. Please use sudo -i.\033[0m")
    sys.exit(1)


def display_progress(total, current):
    width = 40
    percentage = current * 100 // total
    completed = width * current // total
    remaining = width - completed

    print('\r[' + '=' * completed + '>' + ' ' * remaining + '] %d%%' % percentage, end='')


def display_checkmark(message):
    print('\u2714 ' + message)


def display_error(message):
    print('\u2718 Error: ' + message)


def display_notification(message):
    print('\u2728 ' + message)


def display_loading():
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    delay = 0.1
    duration = 5  

    end_time = time.time() + duration

    while time.time() < end_time:
        for frame in frames:
            print('\r[' + frame + '] Loading...  ', end='')
            time.sleep(delay)
            print('\r[' + frame + ']             ', end='')
            time.sleep(delay)

    
def display_logo2():
    colorama.init()
    logo2 = colorama.Style.BRIGHT + colorama.Fore.GREEN + """
     _____       _     _      
    / ____|     (_)   | |     
   | |  __ _   _ _  __| | ___ 
   | | |_ | | | | |/ _` |/ _ \\
   | |__| | |_| | | (_| |  __/
    \_____|\__,_|_|\__,_|\___|
""" + colorama.Style.RESET_ALL
    print(logo2)
    
def display_logo():
    colorama.init()  
    logo = """ 
\033[1;96m          
                 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⠤⠒⠊⠉⠀⠀⠀⠀⠈⠁⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀\033[1;93m⠀⢀⠔⠉⠀⠀⠀⠀⢀⡠⠤⠐⠒⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⣀⡠⠤⠤⠀⠀⠂⠐\033[1;96m⠀⠠⢤⠎⢑⡭⣽⣳⠶⣖⡶⣤⣖⣬⡽⡭⣥⣄\033[1;93m⠒⠒⠀⠐⠁⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢀⠴⠊⠁⠀⠀⠀⠀⡀⠀\033[1;96m⣠⣴⡶⣿⢏⡿⣝⡳⢧⡻⣟⡻⣞⠿⣾⡽⣳⣯⣳⣞⡻⣦⡀⠀⠀\033[1;93m⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢨⠀⠀⠀⢀⠤⠂⠁\033[1;96m⢠⣾⡟⣧⠿⣝⣮⣽⢺⣝⣳⡽⣎⢷⣫⡟⡵⡿⣵⢫⡷⣾⢷⣭⢻⣦⡄\033[1;93m⠤⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⡄⠀⠀⠓⠂⠀\033[1;96m⣴⣿⢷⡿⣝⣻⣏⡷⣾⣟⡼⣣⢟⣼⣣⢟⣯⢗⣻⣽⣏⡾⡽⣟⣧⠿⡼⣿⣦\033[1;93m⣃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠇⠀⠀⠀⠀\033[1;96m⣼⣿⢿⣼⡻⣼⡟⣼⣧⢿⣿⣸⡧⠿⠃⢿⣜⣻⢿⣤⣛⣿⢧⣻⢻⢿⡿⢧⣛⣿⣧⠀\033[1;93m⠛⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⢸⠁⠀⠀⠀⠀\033[1;96m⣼⣻⡿⣾⣳⡽⣾⣽⡷⣻⣞⢿⣫⠕⣫⣫⣸⢮⣝⡇⠱⣏⣾⣻⡽⣻⣮⣿⣻⡜⣞⡿⣷\033[1;93m⢀⠀⠀⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠘⣧⠀⠀⠀\033[1;96m⣼⣳⢯⣿⣗⣿⣏⣿⠆⣟⣿⣵⢛⣵⡿⣿⣏⣟⡾⣜⣻⠀⢻⡖⣷⢳⣏⡶⣻⡧⣟⡼⣻⡽⣇\033[1;93m⠁⠢⡀⠠⡀⠑⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠈⢦⠀\033[1;96m⣰⣯⣟⢯⣿⢾⣹⢾⡟⠰⣏⡾⣾⣟⡷⣿⣻⣽⣷⡶⣟⠿⡆⠀⢻⣝⣯⢷⣹⢧⣿⢧⡻⣽⣳⢽⡀\033[1;93m⠀⠈⠀⠈⠂⡼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠀⡀⢵\033[1;96m⣟⣾⡟⣾⣿⣻⢽⣺⠇⠀⣿⡱⢿⡞⣵⡳⣭⣿⡜⣿⣭⣻⣷⠲⠤⢿⣾⢯⢯⣛⢿⣳⡝⣾⣿⢭⡇⠀\033[1;93m⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⢀⠤⠊⠀\033[1;96m⣼⢻⣿⢞⣯⢿⡽⣸⣹⡆⠀⢷⣏⢯⣿⣧⣛⠶⣯⢿⣽⣷⣧⣛⣦⠀⠀⠙⢿⣳⣽⣿⣣⢟⡶⣿⣫⡇⠀⠀\033[1;93m⠀⠰⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⣠⠖⠁⠀⠀⡄\033[1;96m⡿⣯⣷⣻⡽⣞⡟⣿⣿⣟⠉⠈⢯⣗⣻⣕⢯⣛⡞⣯⢮⣷⣭⡚⠓⠋⠀⠀⠀⠈⠉⣿⡽⣎⠷⡏⡷⣷⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠐⣇⠀⠀⢀⠊\033[1;96m⣼⣇⣿⡗⣿⣽⣷⡿⣿⣱⡿⣆⠀⠀⠙⠒⠛⠓⠋⠉⠉⠀⠀⠀\033[1;91m⢠⣴⣯⣶⣶⣤⡀\033[1;96m ⠀⣿⣟⡼⣛⡇⣟⣿⡆\033[1;93m⡀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⢤⠀⠃⠌\033[1;96m⣸⣿⢾⡽⣹⣾⠹⣞⡵⣳⣽⡽⣖⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\033[1;91m⣤⣖⣻⣾⣝⢿⡄\033[1;96m ⢸⣯⢳⣏⡿⣏⣾⢧\033[1;93m⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠘⠀⠈⠀\033[1;96m⡿⣿⣻⡽⣽⣿⢧⠌⠉\033[1;91m⠉⣴⣿⣿⣫⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣛⠿⠿⢟⢙⡄⠙\033[1;96m ⠘⣯⢳⣞⡟⣯⢾⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⠀⠀\033[1;96m⡿⣿⣿⢵⣫⣿⣆⠁⠂\033[1;91m⣼⡿⢹⣿⡿⠽⠟⢢⠀⠀⠀⠀⠀⠀⠀⢹⠀⢄⢀⠀⡿⠀⠀\033[1;96m ⢰⣯⢷⣺⣏⣯⢻⡽⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⡇⠀⢀⠠\033[1;96m⣿⣿⢾⣛⡶⣽⠈⢓⠀\033[1;91m⢻⠁⢸⠇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠑⠠⠤⠔⠂⠀⠀\033[1;96m ⢸⣿⢮⣽⠿⣜⣻⡝⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀\033[1;93m⠀⠑⠊⠁\033[1;96m⢠⡷⡇⣿⣿⢼⣹⡀⠀⠑⢄⠀\033[1;91m⠀⠃⠌⣁⠦⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⠀\033[1;96m⢀⣿⢾⡝⣾⡽⣺⢽⣹⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣻⢽⣻⡟⣮⣝⡷⢦⣄⣄⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⢿⡺⣟⢷⡹⢾⣷⡞⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⡿⣎⢿⡽⣳⢮⣿⣹⣾⣯⡝⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⣀⣴⡟⣿⢧⣏⢷⡟⣮⠝⢿⣹⣯⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣯⡷⣏⣾⡳⣽⢺⣷⡹⣟⢶⡹⣾⡽⣷⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⣾⢯⣷⡇⣿⢳⣎⢿⡞⣽⢦⣼⡽⣧⢻⡽⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⢾⡷⣭⣿⢳⣭⢻⣷⡻⣜⣻⡵⣻⡼⣿⠾⠫\033[1;96m⣽⣟⣶⣶⣶⠒⠒⠂⠉⠀\033[1;96m⢸⣽⢺⡷⣷⣯⢗⣮⣟⢾⢧⣻⠼⡿⣿⢣⡟⣼⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣝⣾⢳⢧⣟⡳⣎⣿⣿⣱⢏⣾⣽⣳⠟\033[1;92m⠁⠀⡌⠈\033[1;96m⢹⡯⠟⠛⠀⠀⠀⠀⠀⠈\033[1;96m⣷⢻⣼⣽⣿⡾⣼⣏⣾⣻⡜⣯⣷⢿⣟⣼⡳⣞⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢿⡸⣎⠿⣾⡏⣷⣉⣷⣿⢹⣎⡿\033[1;92m⠎⡎⠀⠀⠀⡇⠀⣾⠱⡀⠀⠀⠀⠀⠀⠀⠀⠈⣹⠉⡏⠀\033[1;96m⠹⣾⣏⢹⣶⢹⣶⢿⡾⣿⢶⣿⣸⠾⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣾⢫⣞⡽⣯⢿⣹⡟⣶⣹⢷⣻\033[1;92m⡷⠊⠀⡜⠀⠀⠀⠀⢱⠀⣿⡀⠈⠢⢀⣀⣀⠠⠄⠒⢈⡏⡰⠀⠀⠀\033[1;96m⠀⣿⡜⣮⢟⡼⣻⡵⣻⣗⠾⣟⣯⢻⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⢣⣟⡾⣽⣯⢳⣿⡹⣖⣿⡳\033[1;92m⠋⠀⠀⡸⠀⠀⠀⠀⠀⢸⠀⢺⢂⠀⠀⠀⠀⠀⠀⠀⢠⡺⡱⠁⠀⠀⠀⠀\033[1;96m⢹⣧⣻⢮⡳⣝⡷⢧⣻⢯⢿⣻⣳⢞⡆⠀⠀⠀
⠀⠀⠀⠀⢀⡾⣽⣣⡿⣼⣏⡿⣼⣳⡯⢷⣹⣯⠇\033[1;92m⠀⠀⢠⠁⠀⠀⠀⠀⠀⠈⡆⠈⢹⡰⠤⡀⠀⠀⠀⢠⡼⢱⠁⠀⠀⠀⠀⠀⠀\033[1;96m⠹⣿⣿⣱⣻⣼⣏⢷⣯⣿⡳⣿⣎⢿⡀⠀⠀
⠀⠀⠀⠀⣾⣽⠷⣿⣵⡿⣼⡟⣭⣷⡟⣿⢯⡏⠀\033[1;92m⠀⠀⠘⠀⠀⠒⠈⢡⠀⠀⢗⢄⠀⠃⠀⠺⢁⢈⠥⠋⣀⠇⠀⠀⠀⠀⠀⠀⡀⠀\033[1;96m⠈⠙⢿⣳⢞⣽⢯⣞⣾⣯⡝⣿⡾⡇⠀⠀\033[1;92mAuthor: github.com/Azumi67  \033[1;96m  ⠀⠀
  \033[96m  ______   \033[1;94m _______  \033[1;92m __    \033[1;93m  _______     \033[1;91m    __      \033[1;96m  _____  ___  
 \033[96m  /    " \  \033[1;94m|   __ "\ \033[1;92m|" \  \033[1;93m  /"      \    \033[1;91m   /""\     \033[1;96m (\"   \|"  \ 
 \033[96m // ____  \ \033[1;94m(. |__) :)\033[1;92m||  |  \033[1;93m|:        |   \033[1;91m  /    \   \033[1;96m  |.\\   \    |
 \033[96m/  /    ) :)\033[1;94m|:  ____/ \033[1;92m|:  |  \033[1;93m|_____/   )   \033[1;91m /' /\  \   \033[1;96m |: \.   \\  |
\033[96m(: (____/ // \033[1;94m(|  /     \033[1;92m|.  | \033[1;93m //       /   \033[1;91m //  __'  \  \033[1;96m |.  \    \ |
 \033[96m\        / \033[1;94m/|__/ \   \033[1;92m/\  |\ \033[1;93m |:  __   \  \033[1;91m /   /  \\   \ \033[1;96m |    \    \|
 \033[96m \"_____ / \033[1;94m(_______) \033[1;92m(__\_|_)\033[1;93m |__|  \___) \033[1;91m(___/    \___) \033[1;96m\___|\____\)
"""
    print(logo)
def main_menu():
    try:
        while True:
            display_logo()
            border = "\033[93m+" + "="*70 + "+\033[0m"
            content = "\033[93m║            ▌║█║▌│║▌│║▌║▌█║ \033[92mMain Menu\033[93m  ▌│║▌║▌│║║▌█║▌                  ║"
            footer = " \033[92m    Open issues at \033[34mhttps://github.com/Azumi67/6TO4-GRE-IPIP-SIT\033[0m "

            border_length = len(border) - 2
            centered_content = content.center(border_length)

            print(border)
            print(centered_content)
            print(border)


            print(border)
            print(footer)
            print(border)
            print("\033[93m─────────────────────────────────────────────────────────────────────\033[0m")
            display_notification("\033[92mSingle Server\033[0m")
            print("\033[93m─────────────────────────────────────────────────────────────────────\033[0m")
            print("1. \033[36mExtra Native IPV6\033[0m")
            print("2. \033[93mEdit \033[92mMTU\033[0m")
            print("3. \033[92mGeneve UDP \033[0m")
            print("4. \033[96mIP6IP6\033[0m")
            print("5. \033[93mPrivate IP\033[0m")
            print("6. \033[92mGRE\033[0m")
            print("7. \033[96mGRE6\033[0m")
            print("8. \033[93m6TO4 \033[0m")
            print("9. \033[92m6TO4 \033[97m[Anycasnt] \033[0m")
            print("10. \033[91mUninstall\033[0m")
            print("\033[93m─────────────────────────────────────────────────────────────────────\033[0m")
            display_notification("\033[93m Multiple Servers\033[0m")
            print("\033[93m─────────────────────────────────────────────────────────────────────\033[0m")
            print("11. \033[96mIP6IP6 Multiple Servers\033[0m")
            print("12. \033[92mGRE6 Multiple Servers\033[0m")
            print("13. \033[93m6tO4 Multiple Servers\033[0m")
            print("14. \033[96mAnycast Multiple Servers\033[0m")
            print("15. \033[93mEdit \033[92mMTU\033[0m")
            print("16. \033[91mUninstall\033[0m")
            print("q. Exit")
            print("\033[93m╰─────────────────────────────────────────────────────────────────────╯\033[0m")

            choice = input("\033[5mEnter your choice Please: \033[0m")
            print("choice:", choice)
            if choice == '1':
                Native_menu()
            elif choice == '2':
                mtu_menu() 
            elif choice == '3':
                genz_ip()                 
            elif choice == '4':
                ipip_menu()                
            elif choice == '5':
                private_ip()
            elif choice == '6':
                gre_menu()
            elif choice == '7':
                gre6_menu()
            elif choice == '8':
                i6to4_no()
            elif choice == '9':
                i6to4_any()
            elif choice == '10':
                remove_menu()
            elif choice == '11':
                ip6_mnu_ip()
            elif choice == '12':
                gre6_mnu_ip()
            elif choice == '13':
                priv_mnu_ip()
            elif choice == '14':
                i6to41_any()
            elif choice == '15':
                mtu2_menu()
            elif choice == '16':
                remove2_menu()
            elif choice == 'q':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice.")

            input("Press Enter to continue...")

    except KeyboardInterrupt:
        display_error("\033[91m\nProgram interrupted. Exiting...\033[0m")
        sys.exit()
        
def genz_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mGeneve\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print("1. \033[92mGeneve UDP \033[0m")
    print("2. \033[93mGeneve UDP \033[93m+ \033[92mNative \033[93m| \033[92mTunnelbroker \033[0m")
    print("3. \033[96mGeneve UDP + GRE6 \033[0m")
    print("4. \033[92mGeneve + ICMP\033[0m")
    print('0. \033[91mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_ip()
            break
        elif server_type == '2':
            gen2_ip()
            break
        elif server_type == '3':
            genf_ip()
            break
        elif server_type == '4':
            gen_icmp_install()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')        
def gen_icmp_install():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mGen + ICMP\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_ipicmp()
            break
        elif server_type == '2':
            gen_ipicmpi()
            break
        elif server_type == '0':
            clear()
            genz_ip()
            break
        else:
            print('Invalid choice.')
            
def remove2_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Multiple Servers Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mUninstall IPIP6\033[0m')
    print('2. \033[93mUninstall 6to4\033[0m')
    print('3. \033[93mUninstall anycast\033[0m')
    print('4. \033[92mUninstall Gre6\033[0m')
    print('0. \033[91mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            rmv_ipip6()
            break
        elif server_type == '2':
            rmv_private()
            break
        elif server_type == '3':
            remove_6to41()
            break
        elif server_type == '4':
            rmv_gre6()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def rmv_ipip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m IP6IP6\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[3]Kharej | [1]IRAN\033[0m')
    print('2. \033[93m[1]Kharej | [3]IRAN\033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kh_ipip6()
            break
        elif server_type == '2':
            ir_ipip6()
            break
        elif server_type == '0':
            clear()
            remove2_menu()
            break
        else:
            print('Invalid choice.')

def kh_ipip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m IP6IP6 [3]Kharej\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[93mKharej[2]\033[0m')
    print('3. \033[92mKharej[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_ipip61()
            break
        elif server_type == '2':
            remove_ipip62()
            break
        elif server_type == '3':
            remove_ipip63()
            break
        elif server_type == '4':
            rmv1_q()
            break
        elif server_type == '0':
            clear()
            rmv_ipip6()
            break
        else:
            print('Invalid choice.')
def rmv1_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_ipip6{}".format(i)
        globals()[menu_name]()  
def ir_ipip6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m IP6IP6 [3]IRAN\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[93mIRAN[2]\033[0m')
    print('3. \033[92mIRAN[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mKharej \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_ipip61()
            break
        elif server_type == '2':
            remove_ipip62()
            break
        elif server_type == '3':
            remove_ipip63()
            break
        elif server_type == '4':
            rmv2_q()
            break
        elif server_type == '0':
            clear()
            rmv_ipip6()
            break
        else:
            print('Invalid choice.')

def rmv2_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_ipip6{}".format(i)
        globals()[menu_name]()  
        
def remove_ipip64():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip1.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip1.sh", shell=True)
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)
        if subprocess.call("test -f /etc/ipip2.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip2.sh", shell=True)
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)
        if subprocess.call("test -f /etc/ipip3.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip3.sh", shell=True)
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip1.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip2.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip3.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip1.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip2.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip3.sh", shell=True)

        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip3.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip1 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumip2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip2 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumip3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip3 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)

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
        
def remove_ipip61():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip1.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip1.sh", shell=True)
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip1.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip1.sh", shell=True)

        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip1.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip1 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)

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

def remove_ipip62():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip2.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip2.sh", shell=True)
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip2.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip2.sh", shell=True)

        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip2.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip2 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)

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

def remove_ipip63():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip3.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip3.sh", shell=True)
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip3.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip3.sh", shell=True)

        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip3.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip3 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)

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
        
def rmv_gre6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m GRE6\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[3] | IRAN[1]\033[0m')
    print('2. \033[93mKharej[1] | IRAN[3]\033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kh_gre6()
            break
        elif server_type == '2':
            ir_gre6()
            break
        elif server_type == '0':
            clear()
            remove2_menu()
            break
        else:
            print('Invalid choice.')

def kh_gre6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m GRE6 [3]Kharej\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[93mKharej[2]\033[0m')
    print('3. \033[92mKharej[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_gre61()
            break
        elif server_type == '2':
            remove_gre62()
            break
        elif server_type == '3':
            remove_gre63()
            break
        elif server_type == '4':
            rmv3_q()
            break
        elif server_type == '0':
            clear()
            rmv_gre6()
            break
        else:
            print('Invalid choice.')
def rmv3_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_gre6{}".format(i)
        globals()[menu_name]()  
def ir_gre6():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m GRE6 [3]IRAN\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[93mIRAN[2]\033[0m')
    print('3. \033[92mIRAN[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mKharej \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_gre61()
            break
        elif server_type == '2':
            remove_gre62()
            break
        elif server_type == '3':
            remove_gre63()
            break
        elif server_type == '4':
            rmv4_q()
            break
        elif server_type == '0':
            clear()
            rmv_gre6()
            break
        else:
            print('Invalid choice.')

def rmv4_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_gre6{}".format(i)
        globals()[menu_name]()  
        
def remove_gre64():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre61.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre61.sh", shell=True)
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)
        if subprocess.call("test -f /etc/gre62.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre62.sh", shell=True)
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)
        if subprocess.call("test -f /etc/gre63.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre63.sh", shell=True)
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre61.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre62.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre63.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip1.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip2.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_ip3.sh", shell=True)

        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig61 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig61 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumig62 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig62 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumig63 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig63 > /dev/null", shell=True)

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
		
def remove_gre61():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre61.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre61.sh", shell=True)
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre61.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        time.sleep(1)
        subprocess.run("sudo rm /etc/ping_ip1.sh", shell=True)

        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip1.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip1.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig61 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig61 > /dev/null", shell=True)

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

def remove_gre62():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre62.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre62.sh", shell=True)
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre62.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        time.sleep(1)
        subprocess.run("sudo rm /etc/ping_ip2.sh", shell=True)

        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip2.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip2.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig62 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig62 > /dev/null", shell=True)

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

def remove_gre63():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre63.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre63.sh", shell=True)
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre63.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        time.sleep(1)
        subprocess.run("sudo rm /etc/ping_ip3.sh", shell=True)

        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip3.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip3.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig63 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig63 > /dev/null", shell=True)

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

def rmv_private():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Private\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[5] | IRAN[1]\033[0m')
    print('2. \033[93mKharej[1] | IRAN[5] \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kh_private()
            break
        elif server_type == '2':
            ir_private()
            break
        elif server_type == '0':
            clear()
            remove2_menu()
            break
        else:
            print('Invalid choice.')

def rmv5_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_private{}".format(i)
        globals()[menu_name]() 
        
def kh_private():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Private [5]Kharej\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[93mKharej[2]\033[0m')
    print('3. \033[92mKharej[3]\033[0m')
    print('4. \033[92mKharej[4]\033[0m')
    print('5. \033[92mKharej[5]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[93mIRAN \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_private1()
            break
        elif server_type == '2':
            remove_private2()
            break
        elif server_type == '3':
            remove_private3()
            break
        elif server_type == '4':
            remove_private4()
            break
        elif server_type == '5':
            remove_private5()
            break
        elif server_type == '6':
            rmv5_q()
            break
        elif server_type == '0':
            clear()
            rmv_private()
            break
        else:
            print('Invalid choice.')

def ir_private():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Private [5]IRAN\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[93mIRAN[2]\033[0m')
    print('3. \033[92mIRAN[3]\033[0m')
    print('4. \033[92mIRAN[4]\033[0m')
    print('5. \033[92mIRAN[5]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[93mKharej \033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_private1()
            break
        elif server_type == '2':
            remove_private2()
            break
        elif server_type == '3':
            remove_private3()
            break
        elif server_type == '4':
            remove_private4()
            break
        elif server_type == '5':
            remove_private5()
            break
        elif server_type == '6':
            rmv6_q()
            break
        elif server_type == '0':
            clear()
            rmv_private()
            break
        else:
            print('Invalid choice.')

def rmv6_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "remove_private{}".format(i)
        globals()[menu_name]() 
        
def remove_private6():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)
        if subprocess.call("test -f /etc/private4.sh", shell=True) == 0:
            subprocess.run("rm /etc/private4.sh", shell=True)
        if subprocess.call("test -f /etc/private5.sh", shell=True) == 0:
            subprocess.run("rm /etc/private5.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private4.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private5.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v64.sh", shell=True)
        subprocess.run("sudo rm /etc/ping_v65.sh", shell=True)
        
        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v65.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi4 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi4 > /dev/null", shell=True)
        subprocess.run("ip link set dev azumi5 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi5 > /dev/null", shell=True)
        
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
        
def remove_private1():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private1.sh", shell=True) == 0:
            subprocess.run("rm /etc/private1.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private1.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v61.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi1 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi1 > /dev/null", shell=True)
        
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
        
def remove_private2():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private2.sh", shell=True) == 0:
            subprocess.run("rm /etc/private2.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private2.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v62.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi2 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi2 > /dev/null", shell=True)
        
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
        
def remove_private3():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private3.sh", shell=True) == 0:
            subprocess.run("rm /etc/private3.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private3.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v63.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi3 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi3 > /dev/null", shell=True)
        
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


def remove_private4():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private4.sh", shell=True) == 0:
            subprocess.run("rm /etc/private4.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private4.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v64.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v64.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi4 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi4 > /dev/null", shell=True)
        
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
        
def remove_private5():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private5.sh", shell=True) == 0:
            subprocess.run("rm /etc/private5.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private5.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v65.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v65.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi5 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi5 > /dev/null", shell=True)
        
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
## 11
def gre6_mnu_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE6 \033[92m Multiple Servers\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[96mKHAREJ\033[92m[3]  \033[93mIRAN\033[92m[1]\033[0m')
    print('2. \033[96mKHAREJ\033[92m[1]  \033[93mIRAN\033[92m[3]\033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre6_kh_ip()
            break
        elif server_type == '2':
            gre6_ir_ip()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')    
       
def gre6_kh_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE6 \033[92m[3]Kharej\033[96m [1]IRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[93mKharej[2]\033[0m')
    print('3. \033[92mKharej[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_gre61_menu()
            break
        elif server_type == '2':
            kharej_gre62_menu()
            break
        elif server_type == '3':
            kharej_gre63_menu()
            break
        elif server_type == '4':
            kharejgre_q()
            break
        elif server_type == '0':
            os.system("clear")
            gre6_mnu_ip()
            break
        else:
            print('Invalid choice.')

def kharejgre_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "iran_gre6{}_menu".format(i)
        globals()[menu_name]()

def gre6_ir_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIP6IP6 \033[92m[3]IRAN\033[96m [1]Kharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[93mIRAN[2]\033[0m')
    print('3. \033[92mIRAN[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mKharej\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran2_gre61_menu()
            break
        elif server_type == '2':
            iran2_gre62_menu()
            break
        elif server_type == '3':
            iran2_gre63_menu()
            break
        elif server_type == '4':
            irangre_q()
            break
        elif server_type == '0':
            os.system("clear")
            gre6_mnu_ip()
            break
        else:
            print('Invalid choice.')
           
def irangre_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "kharej2_gre6{}_menu".format(i)
        globals()[menu_name]()     
			
   ##kharej1       
def run1_ping():
    try:
        subprocess.run(["ping", "-c", "2", "2001:831b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_kharej1_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:831b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def gre61_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/gre61.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/gre61.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
		
def ping_gre61_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip1.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip1.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip1.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip1.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip1.service'])

def gre61_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre61.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig61 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig61 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig61' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig61 mtu {mtu_value}'
        with open('/etc/gre61.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    
    
    print("\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::1               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


def create_ping1_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def gre61_kharej():
    remote_ip = "2001:831b::2" #iran-ip
    local_ip = "2001:831b::1"   #kharej ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre61_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping1_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre61_service()

    gre61_cronjob()
   
def kharej_gre61_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[1]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"

    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre61_kharej()
    sleep(1)	
    
## kharej1 for iran 1
def kharej2_gre61_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[1]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[1]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre61_kharej()
    sleep(1)	    
   ##kharej2       
def run2_ping():
    try:
        subprocess.run(["ping", "-c", "2", "2001:841b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v62_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v62.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v62.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v62.service'])
    subprocess.run(['systemctl', 'start', 'ping_v62.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v62.service'])
    

	
def display_kharej2_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:841b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		

def add_cron2_job():
    file_path = '/etc/private2.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)

def gre62_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/gre62.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/gre62.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
		
def ping_gre62_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip2.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip2.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip2.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip2.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip2.service'])

def gre62_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre62.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig62 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:841a::1/64 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig62 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:84{i}a::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig62' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig62 mtu {mtu_value}'
        with open('/etc/gre62.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    
    
    print("\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:841a::1               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


def create_ping2_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def gre62_kharej():
    remote_ip = "2001:841b::2" #iran-ip
    local_ip = "2001:841b::1"   #kharej ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre62_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:841a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping2_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre62_service()

    gre62_cronjob()
   
def kharej_gre62_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[2]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre62_kharej()
    sleep(1)	

## kharej 2 for iran 2
def kharej2_gre62_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[2]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre62_kharej()
    sleep(1)	
   ##kharej3       
def run3_ping():
    try:
        subprocess.run(["ping", "-c", "2", "2001:851b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v63_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v63.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v63.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v63.service'])
    subprocess.run(['systemctl', 'start', 'ping_v63.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v63.service'])
    

	
def display_kharej3_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:851b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		

def add_cron3_job():
    file_path = '/etc/private3.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)

def gre63_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/gre63.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/gre63.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
		
def ping_gre63_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip3.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip3.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip3.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip3.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip3.service'])

def gre63_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre63.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig63 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:851a::1/64 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig63 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:85{i}a::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig63' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig63 mtu {mtu_value}'
        with open('/etc/gre63.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    
    
    print("\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:851a::1               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


def create_ping3_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def gre63_kharej():
    remote_ip = "2001:851b::2" #iran-ip
    local_ip = "2001:851b::1"   #kharej ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre63_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:851a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping3_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre63_service()

    gre63_cronjob()
   
def kharej_gre63_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[3]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre63_kharej()
    sleep(1)
## kharej 3 for iran 3
def kharej2_gre63_menu():
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE6 \033[92mKharej[3]\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre63_kharej()
    sleep(1)    
 ##### IRAN gre6 server 1
def iran_ping1():
    try:
        subprocess.run(["ping", "-c", "2", "2001:831b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran1_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:831b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def iran_gre61_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip1.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip1.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip1.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip1.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip1.service'])

def gre61_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre61.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig61 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig61 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig61' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig61 mtu {mtu_value}'
        with open('/etc/gre61.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

##default route iran server 1
def gre61_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre61.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig61 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig61 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig61' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig61' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::2\n".format(interface)
        with open('/etc/gre61.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig61 mtu {mtu_value}\n"
        with open('/etc/gre61.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def iran_ping1_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    

def gre61_iran():
    remote_ip = "2001:831b::1" #kharej ip
    local_ip = "2001:831b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre61_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping1_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre61_service()

    gre61_cronjob()
## default route iran1
def gre61_iran2():
    remote_ip = "2001:831b::1" #kharej ip
    local_ip = "2001:831b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre61_iran2_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping1_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre61_service()

    gre61_cronjob()   

def iran_gre61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping1()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre61_iran()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
##default route iran1 command
def iran2_gre61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[96m [1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping1()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre61_iran2()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")  
    
 ##### IRAN gre6 server 2
def iran_ping2():
    try:
        subprocess.run(["ping", "-c", "2", "2001:841b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran2_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:841b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def iran_gre62_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip2.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip2.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip2.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip2.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip2.service'])

def gre62_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre62.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig62 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:841a::2/64 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig62 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:84{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig62' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig62 mtu {mtu_value}'
        with open('/etc/gre62.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)    

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:841a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
## default route iran server 2
def gre62_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre62.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig62 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:841a::2/64 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig62 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig62' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:84{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig62' >> {file_path}"
        subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:841a::2\n".format(interface)
        with open('/etc/gre62.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig62 mtu {mtu_value}\n"
        with open('/etc/gre62.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:841a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def iran_ping2_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    

def gre62_iran():
    remote_ip = "2001:841b::1" #kharej ip
    local_ip = "2001:841b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre62_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:841a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping2_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre62_service()

    gre62_cronjob()
#default route server iran 2 
def gre62_iran2():
    remote_ip = "2001:841b::1" #kharej ip
    local_ip = "2001:841b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre62_iran2_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:841a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping2_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre62_service()

    gre62_cronjob()
    
def iran_gre62_menu():
 
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping2()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:841b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre62_iran()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")

# default route iran 2 menu
def iran2_gre62_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping2()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:841b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre62_iran2()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    
 ##### IRAN gre6 server 3
def iran_ping3():
    try:
        subprocess.run(["ping", "-c", "2", "2001:851b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran3_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:851b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def iran_gre63_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip3.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip3.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip3.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip3.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip3.service'])

def gre63_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre63.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig63 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:851a::2/64 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig63 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:85{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig63' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumig63 mtu {mtu_value}'
        with open('/etc/gre63.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:851a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

## default route server iran 3

def gre63_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre63.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig63 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:851a::2/64 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig63 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig63' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:85{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig63' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:851a::2\n".format(interface)
        with open('/etc/gre63.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = "ip link set dev azumig63 mtu {mtu_value}\n"
        with open('/etc/gre63.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:851a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def iran_ping3_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    

def gre63_iran():
    remote_ip = "2001:851b::1" #kharej ip
    local_ip = "2001:851b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre63_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:851a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping3_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre63_service()

    gre63_cronjob()
   
## default route iran server 3
def gre63_iran2():
    remote_ip = "2001:851b::1" #kharej ip
    local_ip = "2001:851b::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre63_iran2_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:851a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping3_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre63_service()

    gre63_cronjob()
    
def iran_gre63_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)


    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping3()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:851b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre63_iran()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
#default route
def iran2_gre63_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[96m Server\033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping3()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:851b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre63_iran2()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    
## 10
def ip6_mnu_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIP6IP6 \033[92m Multiple Servers\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[96mKHAREJ\033[92m[3]  \033[93mIRAN\033[92m[1]\033[0m')
    print('2. \033[96mKHAREJ\033[92m[1]  \033[93mIRAN\033[92m[3]\033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ip6_kh_ip()
            break
        elif server_type == '2':
            ip6_ir_ip()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')    
       
def ip6_kh_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIP6IP6 \033[92m[3]Kharej\033[96m [1]IRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[93mKharej[2]\033[0m')
    print('3. \033[92mKharej[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipip61_menu()
            break
        elif server_type == '2':
            kharej_ipip62_menu()
            break
        elif server_type == '3':
            kharej_ipip63_menu()
            break
        elif server_type == '4':
            kharejip_q()
            break
        elif server_type == '0':
            os.system("clear")
            ip6_mnu_ip()
            break
        else:
            print('Invalid choice.')

def kharejip_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "iran_ipip6{}_menu".format(i)
        globals()[menu_name]()

def ip6_ir_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIP6IP6 \033[92m[3]IRAN\033[96m [1]Kharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[93mIRAN[2]\033[0m')
    print('3. \033[92mIRAN[3]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('4. \033[93mKharej\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran2_ipip61_menu()
            break
        elif server_type == '2':
            iran2_ipip62_menu()
            break
        elif server_type == '3':
            iran2_ipip63_menu()
            break
        elif server_type == '4':
            iranip_q()
            break
        elif server_type == '0':
            os.system("clear")
            ip6_mnu_ip()
            break
        else:
            print('Invalid choice.')
            
def iranip_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "kharej2_ipip6{}_menu".format(i)
        globals()[menu_name]()     
        
def run_ping1():
    try:
        subprocess.run(["ping", "-c", "2", "2001:831b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_kharej1_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:831b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    

##ipip6 kharej
def ping_ipip1_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip1.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip1.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip1.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip1.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip1.service'])


def ipip61_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip1 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a220::1/64 dev azumip1' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumip1 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumip1' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:0db8:1234:a22{i}::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumip1' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip1 mtu {mtu_value}'
        with open('/etc/ipip1.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:0db8:1234:a220::1    |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def ipip1_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip1.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip1.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def create_ping1_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip1_kharej():
    remote_ip = "2001:831b::2" #iran-ip
    local_ip = "2001:831b::1"   #kharej ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip61_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::2" #iranip
    max_pings = 3
    interval = 20
    create_ping1_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)
    
    ping_ipip1_service()

    ipip1_cronjob()
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")
    
def kharej_ipip61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip1_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

## kharej 1 for iran 1
def kharej2_ipip61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[1]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip1_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
##kharej2

def run_ping2():
    try:
        subprocess.run(["ping", "-c", "2", "2001:841b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
	
def display_kharej2_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:841b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


##ipip6 kharej
def ping_ipip2_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip2.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip2.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip2.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip2.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip2.service'])


def ipip62_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip2 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a320::1/64 dev azumip2' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumip2 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumip2' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:0db8:1234:a32{i}::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumip2' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip2 mtu {mtu_value}'
        with open('/etc/ipip2.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:0db8:1234:a320::1    |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def ipip2_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip2.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip2.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def create_ping2_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip2_kharej():
    remote_ip = "2001:841b::2" #iran-ip
    local_ip = "2001:841b::1"   #kharej ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip62_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a320::2" #iranip
    max_pings = 3
    interval = 20
    create_ping2_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)
    
    ping_ipip2_service()

    ipip2_cronjob()
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")
    
def kharej_ipip62_menu():
 
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip2_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

# kharej 2 for iran 2
def kharej2_ipip62_menu():
 
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip2_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

##kharej3

def run_ping3():
    try:
        subprocess.run(["ping", "-c", "2", "2001:851b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
	
def display_kharej3_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:851b::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    


##ipip6 kharej
def ping_ipip3_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip3.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip3.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip3.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip3.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip3.service'])


def ipip63_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip3 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a420::1/64 dev azumip3' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumip3 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumip3' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:0db8:1234:a42{i}::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumip3' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip3 mtu {mtu_value}'
        with open('/etc/ipip3.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    

    print("\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:0db8:1234:a420::1    |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def ipip3_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip3.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip3.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def create_ping3_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip3_kharej():
    remote_ip = "2001:851b::2" #iran-ip
    local_ip = "2001:851b::1"   #kharej ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip63_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a420::2" #iranip
    max_pings = 3
    interval = 20
    create_ping3_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)
    
    ping_ipip3_service()

    ipip3_cronjob()
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")
    
def kharej_ipip63_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip3_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

# kharej 3 for iran 3

def kharej2_ipip63_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IP6IP6 \033[92mKharej\033[93m server\033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip3_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")   
 ##### IRAN IPIP6 server 1
def iran_ping1():
    try:
        subprocess.run(["ping", "-c", "2", "2001:831b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran1_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:831b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran


def iran_ipip1_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip1.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip1.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip1.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip1.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip1.service'])


def ipip61_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip1 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a220::2/64 dev azumip1\n')
        f.write('ip link set azumip1 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip1\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a22{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip1\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip1 mtu {mtu_value}'
        with open('/etc/ipip1.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a220::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')

# default route ipip_iran1
def ipip61_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip1 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a220::2/64 dev azumip1\n')
        f.write('ip link set azumip1 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip1\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a22{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip1\n')

    subprocess.run(f'bash {file_path}', shell=True, check=True)   
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:0db8:1234:a220::2\n".format(interface)
        with open('/etc/ipip1.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumip1 mtu {mtu_value}\n"
        with open('/etc/ipip1.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 1:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a220::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    
def ipip1_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip1.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip1.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping1_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip1.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip1_iran():
    remote_ip = "2001:831b::1" #kharej-ip
    local_ip = "2001:831b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip61_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping1_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip1_service()

    ipip1_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

# default route iran 1
def ipip1_iran2():
    remote_ip = "2001:831b::1" #kharej-ip
    local_ip = "2001:831b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip61_iran2_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping1_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip1_service()

    ipip1_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")   
#sit iran
def iran_ipip61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[1]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping1()


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip1_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
##default route iran server 1 menu
def iran2_ipip61_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[1]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private1.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping1()


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip1_iran2()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
 ##### IRAN IPIP6 server 2
def iran_ping2():
    try:
        subprocess.run(["ping", "-c", "2", "2001:841b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran2_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:841b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran2


def iran_ipip2_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip2.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip2.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip2.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip2.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip2.service'])


def ipip62_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip2 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a320::2/64 dev azumip2\n')
        f.write('ip link set azumip2 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip2\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a32{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip2\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip2 mtu {mtu_value}'
        with open('/etc/ipip2.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)


    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a320::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')

##defaul route ipip iran2
def ipip62_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip2 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a320::2/64 dev azumip2\n')
        f.write('ip link set azumip2 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip2\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a32{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip2\n')

    subprocess.run(f'bash {file_path}', shell=True, check=True)    
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:0db8:1234:a320::2\n".format(interface)
        with open('/etc/ipip2.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumip2 mtu {mtu_value}\n"
        with open('/etc/ipip2.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)


    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 2:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a320::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')

def ipip2_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip2.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip2.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping2_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip2.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip2_iran():
    remote_ip = "2001:841b::1" #kharej-ip
    local_ip = "2001:841b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip62_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a320::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping2_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip2_service()

    ipip2_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

#default route iran server 2
def ipip2_iran2():
    remote_ip = "2001:841b::1" #kharej-ip
    local_ip = "2001:841b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip62_iran2_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a320::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping2_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip2_service()

    ipip2_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")
   
#sit iran
def iran_ipip62_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[2]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)           
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping2()


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip2_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

##default route iran server 2 menu
def iran2_ipip62_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[2]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private2.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping2()


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip2_iran2()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")   
    
 ##### IRAN IPIP6 server 3
def iran_ping3():
    try:
        subprocess.run(["ping", "-c", "2", "2001:851b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran3_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "2001:851b::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran3


def iran_ipip3_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip3.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip3.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip3.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip3.service'])
    subprocess.run(['systemctl', 'restart', 'ping_ip3.service'])


def ipip63_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip3 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a420::2/64 dev azumip3\n')
        f.write('ip link set azumip3 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip3\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a42{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip3\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip3 mtu {mtu_value}'
        with open('/etc/ipip3.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a420::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')

##default route ipip iran3
def ipip63_iran2_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip3 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a420::2/64 dev azumip3\n')
        f.write('ip link set azumip3 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip3\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a42{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip3\n')

    subprocess.run(f'bash {file_path}', shell=True, check=True)    
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:0db8:1234:a420::2\n".format(interface)
        with open('/etc/ipip3.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumip3 mtu {mtu_value}\n"
        with open('/etc/ipip3.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 3:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a420::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')

def ipip3_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip3.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip3.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping3_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip3.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip3_iran():
    remote_ip = "2001:851b::1" #kharej-ip
    local_ip = "2001:851b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip63_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a420::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping3_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip3_service()

    ipip3_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

#default route iran server 2
def ipip3_iran2():
    remote_ip = "2001:851b::1" #kharej-ip
    local_ip = "2001:851b::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip63_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a420::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping3_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip3_service()

    ipip3_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")
    
#sit iran
def iran_ipip63_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[3]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)         
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping3()


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip3_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

##default route iran server 3 menu
def iran2_ipip63_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[3]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)           
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private3.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping3()


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip3_iran2()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
 ##### IRAN IPIP6 server 4
def iran_ping4():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b781::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran4_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b781::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran4


def iran_ipip4_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip4.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip4.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip4.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip4.service'])
    subprocess.run(['systemctl', 'restart', 'ping_ip4.service'])


def ipip64_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip4.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip4 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a520::2/64 dev azumip4\n')
        f.write('ip link set azumip4 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip4\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a52{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip4\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip4 mtu {mtu_value}'
        with open('/etc/ipip4.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 4:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a520::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')



def ipip4_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip4.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip4.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping4_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip4.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip4_iran():
    remote_ip = "fd1d:fc98:b73e:b781::1" #kharej-ip
    local_ip = "fd1d:fc98:b73e:b781::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip64_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a520::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping4_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip4_service()

    ipip4_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

   
#sit iran
def iran_ipip64_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[4]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private4.sh"):
        os.remove("/etc/private4.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[4]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi4", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi4", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b781::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi4"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private4.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi4 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi4 up\n")
        f.write("ip addr add fd1d:fc98:b73e:b781::2/64 dev azumi4\n")
        f.write("ip -6 route add fd1d::/16 dev azumi4\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi4 mtu {mtu_value}\n"
        with open("/etc/private4.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private4.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron4_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping4()


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b681::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v64.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v64.sh', 0o755)
    ping_v64_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip4_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
 ##### IRAN IPIP6 server 5
def iran_ping5():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b881::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran5_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b881::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran4


def iran_ipip5_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip5.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip5.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip5.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip5.service'])
    subprocess.run(['systemctl', 'restart', 'ping_ip5.service'])


def ipip65_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip5.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip5 mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a620::2/64 dev azumip5\n')
        f.write('ip link set azumip5 up\n')
        f.write('ip -6 route add 2002::/16 dev azumip5\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a62{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip5\n')

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f'ip link set dev azumip5 mtu {mtu_value}'
        with open('/etc/ipip5.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    
    


    print('\033[93mCreated IPv6 Addresses \033[92mServer 5:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a620::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')



def ipip5_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip5.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip5.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping5_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip5.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip5_iran():
    remote_ip = "fd1d:fc98:b73e:b881::1" #kharej-ip
    local_ip = "fd1d:fc98:b73e:b881::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip65_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a620::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping5_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip5_service()

    ipip5_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

   
#sit iran
def iran_ipip65_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mServer\033[93m\033[96m[5]\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private5.sh"):
        os.remove("/etc/private5.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[5]\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi5", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi5", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b881::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi5"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private5.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi5 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi5 up\n")
        f.write("ip addr add fd1d:fc98:b73e:b881::2/64 dev azumi5\n")
        f.write("ip -6 route add fd1d::/16 dev azumi5\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi5 mtu {mtu_value}\n"
        with open("/etc/private5.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private5.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron5_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping5()


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b681::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v65.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v65.sh', 0o755)
    ping_v65_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip5_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
## 12

    ##### PRIVATE 5 kharej 1 iran
def priv_mnu_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivateIP \033[92m Multiple Servers\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[96mKharej\033[92m[5] \033[93mIRAN\033[92m[1]\033[0m')
    print('2. \033[96mKharej\033[92m[1] \033[93mIRAN\033[92m[5]  \033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            priv_kh_ip()
            break
        elif server_type == '2':
            priv_ir_ip()
            break
        elif server_type == '0':
            os.system("clear")
            main_menu()
            break
        else:
            print('Invalid choice.')    
       
def priv_kh_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivate IP \033[92m[5]Kharej\033[96m [1]IRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej[1]\033[0m')
    print('2. \033[92mKharej[2]\033[0m')
    print('3. \033[93mKharej[3]\033[0m')
    print('4. \033[92mKharej[4]\033[0m')
    print('5. \033[92mKharej[5]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[93mIRAN\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej1_private_menu()
            break
        elif server_type == '2':
            kharej2_private_menu()
            break
        elif server_type == '3':
            kharej3_private_menu()
            break
        elif server_type == '4':
            kharej4_private_menu()
            break
        elif server_type == '5':
            kharej5_private_menu()
            break
        elif server_type == '6':
            kharej_q()
            break
        elif server_type == '0':
            os.system("clear")
            priv_mnu_ip()
            break
        else:
            print('Invalid choice.')
            
def kharej_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mkharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "iran{}_private_menu".format(i)
        globals()[menu_name]()       

def priv_ir_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivate IP \033[92m[5]IRAN\033[96m [1]Kharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN[1]\033[0m')
    print('2. \033[92mIRAN[2]\033[0m')
    print('3. \033[93mIRAN[3]\033[0m')
    print('4. \033[92mIRAN[4]\033[0m')
    print('5. \033[92mIRAN[5]\033[0m')
    print("\033[93m───────────────────────────────────────\033[0m")
    print('6. \033[93mKharej\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran1_private2_menu()
            break
        elif server_type == '2':
            iran2_private2_menu()
            break
        elif server_type == '3':
            iran3_private2_menu()
            break
        elif server_type == '4':
            iran4_private2_menu()
            break
        elif server_type == '5':
            iran5_private2_menu()
            break
        elif server_type == '6':
            iran_q()
            break
        elif server_type == '0':
            os.system("clear")
            priv_mnu_ip()
            break
        else:
            print('Invalid choice.')
            
def iran_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "kharej{}_private2_menu".format(i)
        globals()[menu_name]()       		
## Kharej 1
def add_cron1_job():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/private1.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/private1.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping1():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:831b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)

        
def ping_v61_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v61.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v61.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v61.service'])
    subprocess.run(['systemctl', 'start', 'ping_v61.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v61.service'])
    
        

            
def kharej1_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [1]...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi1"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi1"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
# kharej1 for iran 1
def kharej1_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [1]...\033[0m")

    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[1]\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi1"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi1"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi1"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi1\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"
        with open("/etc/private1.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron1_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping1()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v61.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")    
## Kharej 2
def add_cron2_job():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/private2.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/private2.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping2():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:841b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)

        
def ping_v62_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v62.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v62.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v62.service'])
    subprocess.run(['systemctl', 'start', 'ping_v62.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v62.service'])
    
        

            
def kharej2_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [2]...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi2"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi2"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:84{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
 
# kharej 2 for iran 2

def kharej2_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [2]...\033[0m")

    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:841b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi2"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi2"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi2"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::1/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:84{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi2\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"
        with open("/etc/private2.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping2()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:841b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v62.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
    
## Kharej 3
def add_cron3_job():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/private3.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/private3.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping3():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:851b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)

        
def ping_v63_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v63.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v63.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v63.service'])
    subprocess.run(['systemctl', 'start', 'ping_v63.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v63.service'])
    
        

            
def kharej3_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [3]...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi3"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi3"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add fd1d::/16 dev azumi3\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:85{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")

# kharej 3 for iran 3

def kharej3_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [3]...\033[0m")

    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:851b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi3"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi3"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi3"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::1/64 dev azumi3\n")
        f.write("ip -6 route add fd1d::/16 dev azumi3\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:85{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi3\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"
        with open("/etc/private3.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping3()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:851b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v63.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
    
## Kharej 4
def add_cron4_job():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/private4.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/private4.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping4():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:861b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)

        
def ping_v64_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v64.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v64.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v64.service'])
    subprocess.run(['systemctl', 'start', 'ping_v64.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v64.service'])
    
def kharej4_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[4]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [4]...\033[0m")

    if os.path.isfile("/etc/private4.sh"):
        os.remove("/etc/private4.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[4]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi4", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi4", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:861b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi4"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi4"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi4"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private4.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi4 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi4 up\n")
        f.write("ip addr add 2001:861b::1/64 dev azumi4\n")
        f.write("ip -6 route add 2001::/16 dev azumi4\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:86{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi4\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi4 mtu {mtu_value}\n"
        with open("/etc/private4.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron4_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping4()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:861b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v64.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v64.sh', 0o755)
    ping_v64_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")

# kharej 4 for iran 4
def kharej4_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[4]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [4]...\033[0m")

    if os.path.isfile("/etc/private4.sh"):
        os.remove("/etc/private4.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[4]\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi4", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi4", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:861b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi4"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi4"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi4"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private4.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi4 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi4 up\n")
        f.write("ip addr add 2001:861b::1/64 dev azumi4\n")
        f.write("ip -6 route add 2001::/16 dev azumi4\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:86{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi4\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi4 mtu {mtu_value}\n"
        with open("/etc/private4.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron4_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping4()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:861b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v64.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v64.sh', 0o755)
    ping_v64_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
    
## Kharej 5
def add_cron5_job():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/private5.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/private5.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
        
def run_ping5():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:871b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)

        
def ping_v65_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v65.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v65.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v65.service'])
    subprocess.run(['systemctl', 'start', 'ping_v65.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v65.service'])
    
def kharej5_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[5]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [5]...\033[0m")

    if os.path.isfile("/etc/private5.sh"):
        os.remove("/etc/private5.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej \033[96m[5]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi5", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi5", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:871b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi5"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi5"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi5"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private5.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi5 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi5 up\n")
        f.write("ip addr add 2001:871b::1/64 dev azumi5\n")
        f.write("ip -6 route add 2001::/16 dev azumi5\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:87{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi5\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi5 mtu {mtu_value}\n"
        with open("/etc/private5.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron5_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping5()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:871b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v65.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v65.sh', 0o755)
    ping_v65_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")

# kharej 5 for iran 5 
def kharej5_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server \033[92m[5]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Kharej server [5]...\033[0m")

    if os.path.isfile("/etc/private5.sh"):
        os.remove("/etc/private5.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN \033[96m[5]\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi5", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi5", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:871b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi5"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi5"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi5"], stdout=subprocess.DEVNULL)

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private5.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi5 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi5 up\n")
        f.write("ip addr add 2001:871b::1/64 dev azumi5\n")
        f.write("ip -6 route add 2001::/16 dev azumi5\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:87{ip_suffix}b::1/64"
            f.write(f"ip addr add {ip_addr} dev azumi5\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi5 mtu {mtu_value}\n"
        with open("/etc/private5.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron5_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping5()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:871b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v65.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v65.sh', 0o755)
    ping_v65_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")
    
## IRAN1
def run_ping1_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:831b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def iran1_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[1]...\033[0m")
    
    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[1]\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi1"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi1\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron1_job()

    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping1_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:831b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v61.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()

## route for iran1_private_menu
def iran1_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[1]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[1]...\033[0m")
    
    if os.path.isfile("/etc/private1.sh"):
        os.remove("/etc/private1.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[1]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi1", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi1", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi1"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi1"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi1"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private1.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi1 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi1 up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi1\n")
        f.write("ip -6 route add 2001::/16 dev azumi1\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi1\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:831b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron1_job()

    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping1_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:831b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v61.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v61.sh', 0o755)
    ping_v61_service()
## IRAN2
def run_ping2_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:841b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def iran2_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[2]...\033[0m")
    
    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[2]\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi2"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:84{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi2\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping2_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:841b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v62.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()

## default route iran2_private_menu
def iran2_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[2]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[2]...\033[0m")
    
    if os.path.isfile("/etc/private2.sh"):
        os.remove("/etc/private2.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[2]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi2", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi2", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:841b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi2"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi2"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi2"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private2.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi2 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi2 up\n")
        f.write("ip addr add 2001:841b::2/64 dev azumi2\n")
        f.write("ip -6 route add 2001::/16 dev azumi2\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:84{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi2\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:841b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron2_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping2_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:84{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:841b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v62.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v62.sh', 0o755)
    ping_v62_service()
## IRAN3
def run_ping3_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:851b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def iran3_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[3]...\033[0m")
    
    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[3]\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi3"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:85{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi3\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping3_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:851b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v63.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()
## default route iran3_private_menu
def iran3_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[3]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[3]...\033[0m")
    
    if os.path.isfile("/etc/private3.sh"):
        os.remove("/etc/private3.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[3]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi3", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi3", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:851b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi3"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi3"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi3"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private3.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi3 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi3 up\n")
        f.write("ip addr add 2001:851b::2/64 dev azumi3\n")
        f.write("ip -6 route add 2001::/16 dev azumi3\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:85{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi3\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:851b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron3_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping3_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:85{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:851b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v63.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v63.sh', 0o755)
    ping_v63_service()    
## IRAN4
def run_ping4_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:861b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def iran4_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[4]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[4]...\033[0m")
    
    if os.path.isfile("/etc/private4.sh"):
        os.remove("/etc/private4.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[4]\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi4", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi4", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:861b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi4"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private4.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi4 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi4 up\n")
        f.write("ip addr add 2001:861b::2/64 dev azumi4\n")
        f.write("ip -6 route add 2001::/16 dev azumi4\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:86{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi4\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron4_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping4_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:861b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v64.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v64.sh', 0o755)
    ping_v64_service()
##default route iran4_private_menu
def iran4_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[4]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[4]...\033[0m")
    
    if os.path.isfile("/etc/private4.sh"):
        os.remove("/etc/private4.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[4]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi4", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi4", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:861b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi4"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi4"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi4"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private4.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi4 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi4 up\n")
        f.write("ip addr add 2001:861b::2/64 dev azumi4\n")
        f.write("ip -6 route add 2001::/16 dev azumi4\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:86{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi4\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:861b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron4_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping4_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:86{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:861b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v64.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v64.sh', 0o755)
    ping_v64_service()    
## IRAN5
def run_ping5_iran():
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:871b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def iran5_private_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[5]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[5]...\033[0m")
    
    if os.path.isfile("/etc/private5.sh"):
        os.remove("/etc/private5.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej \033[96m[5]\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi5", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi5", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:871b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi5"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private5.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi5 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi5 up\n")
        f.write("ip addr add 2001:871b::2/64 dev azumi5\n")
        f.write("ip -6 route add 2001::/16 dev azumi5\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:87{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi5\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron5_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping5_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:871b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v65.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v65.sh', 0o755)
    ping_v65_service()

#default route iran5_private_menu
def iran5_private2_menu():

    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Server\033[96m[5]\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mAdding private IP addresses for Server[5]...\033[0m")
    
    if os.path.isfile("/etc/private5.sh"):
        os.remove("/etc/private5.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN \033[96m[5]\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi5", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi5", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:871b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi5"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92madditional private IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "addr", "show", "dev", "azumi5"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "addr", "add", ip_addr, "dev", "azumi5"], stdout=subprocess.DEVNULL)
    

    display_notification("\033[93mAdding commands...\033[0m")
    with open("/etc/private5.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi5 mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi5 up\n")
        f.write("ip addr add 2001:871b::2/64 dev azumi5\n")
        f.write("ip -6 route add 2001::/16 dev azumi5\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:87{ip_suffix}b::2/64"
            f.write(f"ip addr add {ip_addr} dev azumi5\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:871b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron5_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping5_iran()
    sleep(1)
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:87{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:871b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v65.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v65.sh', 0o755)
    ping_v65_service()
    
def mtu2_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mEdit MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m6TO4\033[0m')
    print('2. \033[93mIP6IP6 \033[0m')
    print('3. \033[92mGRE6 \033[0m')
    print('4. \033[96manycast \033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            private_mnu()
            break
        elif server_type == '2':
            ip6_mnu()
            break
        elif server_type == '3':
            gre6_mnu()
            break      
        elif server_type == '4':
            i6to4any2_mtu()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def private_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivateIP Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[5]Kharej [1]IRAN\033[0m')
    print('2. \033[93m[1]Kharej [5]IRAN \033[0m')
    print('0. \033[94mback to the MTU menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khprivate_mnu()
            break
        elif server_type == '2':
            irprivate_mnu()
            break
        elif server_type == '0':
            clear()
            mtu2_menu()
            break
        else:
            print('Invalid choice.')

def khprivate_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[5]Kharej Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej [1]\033[0m')
    print('2. \033[93mKharej [2]\033[0m')
    print('3. \033[93mKharej [3]\033[0m')
    print('4. \033[92mKharej [4]\033[0m')
    print('5. \033[92mKharej [5]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('6. \033[93mIRAN \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            priv_kh1_mtu()
            break
        elif server_type == '2':
            priv_kh2_mtu()
            break
        elif server_type == '3':
            priv_kh3_mtu()
            break
        elif server_type == '4':
            priv_kh4_mtu()
            break
        elif server_type == '5':
            priv_kh5_mtu()
            break
        elif server_type == '6':
            mtu1_q()
            break
        elif server_type == '0':
            clear()
            private_mnu()
            break
        else:
            print('Invalid choice.')  
            
def mtu1_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[93mTunnel [3]\033[0m')
    print('4. \033[92mTunnel [4]\033[0m')
    print('5. \033[92mTunnel [5]\033[0m')
    print('6. \033[96mAll OF Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            priv_ir1_mtu()
            break
        elif server_type == '2':
            priv_ir2_mtu()
            break
        elif server_type == '3':
            priv_ir3_mtu()
            break
        elif server_type == '4':
            priv_ir4_mtu()
            break
        elif server_type == '5':
            priv_ir5_mtu()
            break
        elif server_type == '6':
            mtu1_q1()
            break
        elif server_type == '0':
            clear()
            khprivate_mnu()
            break
        else:
            print('Invalid choice.')   

##later usage  
def mtu1_q1():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "priv_ir{}_mtu".format(i)
        globals()[menu_name]()   
        
def irprivate_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[5]IRAN Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN [1]\033[0m')
    print('2. \033[93mIRAN [2]\033[0m')
    print('3. \033[93mIRAN [3]\033[0m')
    print('4. \033[92mIRAN [4]\033[0m')
    print('5. \033[92mIRAN [5]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('6. \033[93mKharej \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            priv_ir1_mtu()
            break
        elif server_type == '2':
            priv_ir2_mtu()
            break
        elif server_type == '3':
            priv_ir3_mtu()
            break
        elif server_type == '4':
            priv_ir4_mtu()
            break
        elif server_type == '5':
            priv_ir5_mtu()
            break
        elif server_type == '6':
            mtu2_q()
            break
        elif server_type == '0':
            clear()
            private_mnu()
            break
        else:
            print('Invalid choice.')  
def mtu2_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKHAREJ MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[93mTunnel [3]\033[0m')
    print('4. \033[92mTunnel [4]\033[0m')
    print('5. \033[92mTunnel [5]\033[0m')
    print('6. \033[96mAll OF Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            priv_ir1_mtu()
            break
        elif server_type == '2':
            priv_ir2_mtu()
            break
        elif server_type == '3':
            priv_ir3_mtu()
            break
        elif server_type == '4':
            priv_ir4_mtu()
            break
        elif server_type == '5':
            priv_ir5_mtu()
            break
        elif server_type == '6':
            mtu1_q2()
            break
        elif server_type == '0':
            clear()
            irprivate_mnu()
            break
        else:
            print('Invalid choice.')   

#later usage
def mtu1_q2():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "priv_kh{}_mtu".format(i)
        globals()[menu_name]()   
        
## gre6 menu 

def gre6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE6 Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[3]Kharej [1]IRAN\033[0m')
    print('2. \033[93m[1]Kharej [3]IRAN \033[0m')
    print('0. \033[94mback to the MTU menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khgre6_mnu()
            break
        elif server_type == '2':
            irgre6_mnu()
            break
        elif server_type == '0':
            clear()
            mtu2_menu()
            break
        else:
            print('Invalid choice.')
            
## gre6 kharej menu            
def khgre6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[3]Kharej Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej [1]\033[0m')
    print('2. \033[93mKharej [2]\033[0m')
    print('3. \033[92mKharej [3]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre6_kh1_mtu()
            break
        elif server_type == '2':
            gre6_kh2_mtu()
            break
        elif server_type == '3':
            gre6_kh3_mtu()
            break
        elif server_type == '4':
            mtu3_q()
            break
        elif server_type == '0':
            clear()
            gre6_mnu()
            break
        else:
            print('Invalid choice.')  
def mtu3_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[92mTunnel [3]\033[0m')
    print('4. \033[92mAll Of Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre6_ir1_mtu()
            break
        elif server_type == '2':
            gre6_ir2_mtu()
            break
        elif server_type == '3':
            gre6_ir3_mtu()
            break
        elif server_type == '4':
            m3_q()
            break
        elif server_type == '0':
            clear()
            khgre6_mnu()
            break
        else:
            print('Invalid choice.')
        
def m3_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "gre6_ir{}_mtu".format(i)
        globals()[menu_name]()  
        
def irgre6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[3]IRAN Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN [1]\033[0m')
    print('2. \033[93mIRAN [2]\033[0m')
    print('3. \033[92mIRAN [3]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('4. \033[93mKharej \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre6_ir1_mtu()
            break
        elif server_type == '2':
            gre6_ir2_mtu()
            break
        elif server_type == '3':
            gre6_ir3_mtu()
            break
        elif server_type == '4':
            mtu4_q()
            break
        elif server_type == '0':
            clear()
            gre6_mnu()
            break
        else:
            print('Invalid choice.') 
            
def mtu4_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKHAREJ Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[92mTunnel [3]\033[0m')
    print('4. \033[92mAll Of Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre6_kh1_mtu()
            break
        elif server_type == '2':
            gre6_kh2_mtu()
            break
        elif server_type == '3':
            gre6_kh3_mtu()
            break
        elif server_type == '4':
            m4_q()
            break
        elif server_type == '0':
            clear()
            irgre6_mnu()
            break
        else:
            print('Invalid choice.')
        
def m4_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "gre6_kh{}_mtu".format(i)
        globals()[menu_name]()  
        
## ipip6 menu 

def ip6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIP6IP6 Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m[3]Kharej [1]IRAN\033[0m')
    print('2. \033[93m[1]Kharej [3]IRAN \033[0m')
    print('0. \033[94mback to the MTU menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            khip6_mnu()
            break
        elif server_type == '2':
            irip6_mnu()
            break
        elif server_type == '0':
            clear()
            mtu2_menu()
            break
        else:
            print('Invalid choice.')

                      
def khip6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[3]Kharej Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej [1]\033[0m')
    print('2. \033[93mKharej [2]\033[0m')
    print('3. \033[92mKharej [3]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('4. \033[93mIRAN \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ipip_kh1_mtu()
            break
        elif server_type == '2':
            ipip_kh2_mtu()
            break
        elif server_type == '3':
            ipip_kh3_mtu()
            break
        elif server_type == '4':
            mtu5_q()
            break
        elif server_type == '0':
            clear()
            ip6_mnu()
            break
        else:
            print('Invalid choice.')  

def mtu5_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIRAN Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[92mTunnel [3]\033[0m')
    print('4. \033[92mAll Of Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ipip_ir1_mtu()
            break
        elif server_type == '2':
            ipip_ir2_mtu()
            break
        elif server_type == '3':
            ipip_ir3_mtu()
            break
        elif server_type == '4':
            m5_q()
            break
        elif server_type == '0':
            clear()
            khip6_mnu()
            break
        else:
            print('Invalid choice.')

        
def m5_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mKharej Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "ipip_ir{}_mtu".format(i)
        globals()[menu_name]() 
        
def irip6_mnu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m[3]IRAN Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mIRAN [1]\033[0m')
    print('2. \033[93mIRAN [2]\033[0m')
    print('3. \033[92mIRAN [3]\033[0m')
    print("\033[93m──────────────────────────────────────\033[0m")
    print('4. \033[93mKharej \033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ipip_ir1_mtu()
            break
        elif server_type == '2':
            ipip_ir2_mtu()
            break
        elif server_type == '3':
            ipip_ir3_mtu()
            break
        elif server_type == '4':
            mtu6_q()
            break
        elif server_type == '0':
            clear()
            ip6_mnu()
            break
        else:
            print('Invalid choice.') 
def mtu6_q():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKHAREJ Edit Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mTunnel [1]\033[0m')
    print('2. \033[93mTunnel [2]\033[0m')
    print('3. \033[92mTunnel [3]\033[0m')
    print('4. \033[92mAll Of Them\033[0m')
    print('0. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            ipip_kh1_mtu()
            break
        elif server_type == '2':
            ipip_kh2_mtu()
            break
        elif server_type == '3':
            ipip_kh3_mtu()
            break
        elif server_type == '4':
            m6_q()
            break
        elif server_type == '0':
            clear()
            irip6_mnu()
            break
        else:
            print('Invalid choice.')

        
def m6_q():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mQuestion time !\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    num_servers = int(input("\033[93mHow many \033[92mIRAN Servers\033[93m do you have?\033[0m "))
    
    for i in range(1, num_servers + 1):
        menu_name = "ipip_kh{}_mtu".format(i)
        globals()[menu_name]() 
        
def ipip_kh1_mtu():
    
    priv_kh1_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip1 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip1.sh"):
        with open("/etc/ipip1.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip1 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip1 mtu" not in line]

            with open("/etc/ipip1.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip1.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_kh2_mtu():
    
    priv_kh2_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip2 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip2.sh"):
        with open("/etc/ipip2.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip2 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip2 mtu" not in line]

            with open("/etc/ipip2.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip2.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_kh3_mtu():
    
    priv_kh3_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip3 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip3.sh"):
        with open("/etc/ipip3.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip3 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip3 mtu" not in line]

            with open("/etc/ipip3.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip3.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_ir1_mtu():
    
    priv_ir1_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip1 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip1.sh"):
        with open("/etc/ipip1.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip1 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip1 mtu" not in line]

            with open("/etc/ipip1.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip1.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_ir2_mtu():
    
    priv_ir2_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip2 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip2.sh"):
        with open("/etc/ipip2.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip2 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip2 mtu" not in line]

            with open("/etc/ipip2.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip2.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_ir3_mtu():
    
    priv_ir3_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip3 mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip3.sh"):
        with open("/etc/ipip3.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumip3 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumip3 mtu" not in line]

            with open("/etc/ipip3.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/ipip3.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def priv_kh1_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 1\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"

    if os.path.exists("/etc/private1.sh"):
        with open("/etc/private1.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi1 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi1 mtu" not in line]

            with open("/etc/private1.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private1.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def priv_kh2_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 2\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"

    if os.path.exists("/etc/private2.sh"):
        with open("/etc/private2.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi2 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi2 mtu" not in line]

            with open("/etc/private2.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private2.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def priv_kh3_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 3\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"

    if os.path.exists("/etc/private3.sh"):
        with open("/etc/private3.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi3 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi3 mtu" not in line]

            with open("/etc/private3.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private3.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")  

def priv_kh4_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 4\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi4 mtu {mtu_value}\n"

    if os.path.exists("/etc/private4.sh"):
        with open("/etc/private4.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi4 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi4 mtu" not in line]

            with open("/etc/private4.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private4.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def priv_kh5_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 5\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi5 mtu {mtu_value}\n"

    if os.path.exists("/etc/private5.sh"):
        with open("/etc/private5.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi5 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi5 mtu" not in line]

            with open("/etc/private5.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private5.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")   
        
#iran mtu private
def priv_ir1_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 1\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi1 mtu {mtu_value}\n"

    if os.path.exists("/etc/private1.sh"):
        with open("/etc/private1.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi1 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi1 mtu" not in line]

            with open("/etc/private1.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private1.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")     

def priv_ir2_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 2\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi2 mtu {mtu_value}\n"

    if os.path.exists("/etc/private2.sh"):
        with open("/etc/private2.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi2 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi2 mtu" not in line]

            with open("/etc/private2.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private2.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def priv_ir3_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    ddisplay_notification("\033[93m             Server 3\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi3 mtu {mtu_value}\n"

    if os.path.exists("/etc/private3.sh"):
        with open("/etc/private3.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi3 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi3 mtu" not in line]

            with open("/etc/private3.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private3.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")  

def priv_ir4_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    ddisplay_notification("\033[93m             Server 4\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi4 mtu {mtu_value}\n"

    if os.path.exists("/etc/private4.sh"):
        with open("/etc/private4.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi4 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi4 mtu" not in line]

            with open("/etc/private4.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private4.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def priv_ir5_mtu():
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93m             Server 5\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi5 mtu {mtu_value}\n"

    if os.path.exists("/etc/private5.sh"):
        with open("/etc/private5.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi5 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi5 mtu" not in line]

            with open("/etc/private5.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/private5.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")   
     
## gre6 mtu Kharej     
def gre6_kh1_mtu():
    priv_kh1_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig61 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre61.sh"):
        with open("/etc/gre61.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig61 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig61 mtu" not in line]

            with open("/etc/gre61.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre61.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_kh2_mtu():
    priv_kh2_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig62 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre62.sh"):
        with open("/etc/gre62.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig62 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig62 mtu" not in line]

            with open("/etc/gre62.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre62.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_kh3_mtu():
    priv_kh3_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig63 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre63.sh"):
        with open("/etc/gre63.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig63 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig63 mtu" not in line]

            with open("/etc/gre63.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre63.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

##gre6 mtu iran
def gre6_ir1_mtu():
    priv_ir1_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig61 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre61.sh"):
        with open("/etc/gre61.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig61 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig61 mtu" not in line]

            with open("/etc/gre61.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre61.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_ir2_mtu():
    priv_ir2_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig62 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre62.sh"):
        with open("/etc/gre62.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig62 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig62 mtu" not in line]

            with open("/etc/gre62.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre62.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_ir3_mtu():
    priv_ir3_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig63 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre63.sh"):
        with open("/etc/gre63.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumig63 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumig63 mtu" not in line]

            with open("/etc/gre63.sh", "w") as file:
                file.writelines(sh_contents)
            
        with open("/etc/gre63.sh", "a") as file:
            file.write(mtu_command)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
       
        

def i6to4any2_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96m6to4 anycast \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumi6 mtu {mtu_value}\n"

    if os.path.exists("/etc/6to4.sh"):
        with open("/etc/6to4.sh", "r") as file:
            sh_contents = file.readlines()

        if any("link set dev azumi6 mtu" in line for line in sh_contents):
            sh_contents = [line for line in sh_contents if "link set dev azumi6 mtu" not in line]

            with open("/etc/6to4.sh", "w") as file:
                file.writelines(sh_contents)

        with open("/etc/6to4.sh", "a") as file:
            file.write(mtu_command)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")


## original mtu
def mtu_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mEdit MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mPrivate IP\033[0m')
    print('2. \033[93mIP6IP6 \033[0m')
    print('3. \033[96mGRE \033[0m')
    print('4. \033[92mGRE6 \033[0m')
    print('5. \033[93m6to4 \033[0m')
    print('6. \033[96m6to4 anycast \033[0m')
    print('7. \033[92mGeneve \033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            private_mtu()
            break
        elif server_type == '2':
            ipip_mtu()
            break
        elif server_type == '3':
            gre_mtu()
            break
        elif server_type == '4':
            gre6_mtu()
            break
        elif server_type == '5':
            i6to4_mtu()
            break        
        elif server_type == '6':
            i6to4any_mtu()
            break
        elif server_type == '7':
            gen_mtu()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def gen_mtu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGENEVE MTU Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mGENEVE\033[0m')
    print('2. \033[97mGENEVE + Native\033[0m')
    print('3. \033[93mGRE6 + IPV4 GENEVE  \033[0m')
    print('4. \033[96mGRE6 + Native GENEVE \033[0m')
    print('5. \033[92mGENEVE + IP6tnl + GRE6 \033[0m')
    print('6. \033[96mGENEVE + ICMP \033[0m')
    print('0. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen1_mtu()
            break
        elif server_type == '2':
            gen1_mtu()
            break
        elif server_type == '3':
            gen4_mtu()
            break
        elif server_type == '4':
            gen2_mtu()
            break
        elif server_type == '5':
            gen3_mtu()
            break
        elif server_type == '6':
            gen1_mtu()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def gen4_mtu():
    private_mtu()
    gre621_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGeneve \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"

    if os.path.exists("/etc/gen.sh"):
        with open("/etc/gen.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumigen mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gen.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def gen1_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGeneve \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"

    if os.path.exists("/etc/gen.sh"):
        with open("/etc/gen.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumigen mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gen.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gen2_mtu():
    gre621_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGeneve \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"

    if os.path.exists("/etc/gen.sh"):
        with open("/etc/gen.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumigen mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gen.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gen3_mtu():
    private2_mtu()
    gre621_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGeneve \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"

    if os.path.exists("/etc/gen.sh"):
        with open("/etc/gen.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumigen mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gen.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def private2_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[\033[96mIP6tnl\033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"

    if os.path.exists("/etc/private.sh"):
        with open("/etc/private.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumi mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/private.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def private_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mPrivate IP \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"

    if os.path.exists("/etc/private.sh"):
        with open("/etc/private.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumi mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/private.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def gre621_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre6.sh"):
        with open("/etc/gre6.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumig6 mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gre6.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def gre6_mtu():
    private_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE6 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"

    if os.path.exists("/etc/gre6.sh"):
        with open("/etc/gre6.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumig6 mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gre6.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        

def gre_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mGRE \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumig mtu {mtu_value}\n"

    if os.path.exists("/etc/gre.sh"):
        with open("/etc/gre.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumig mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/gre.sh", "w") as file:
            file.writelines(sh_contents)

        print("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
        
def i6to4_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96m6to4 \033[93m]:\033[0m ")
    mtu_command = f"ip link set dev azumi6 mtu {mtu_value}\n"

    if os.path.exists("/etc/6to4.sh"):
        with open("/etc/6to4.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumi6 mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/6to4.sh", "w") as file:
            file.writelines(sh_contents)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def i6to4any_mtu():
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96m6to4 anycast \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumi6 mtu {mtu_value}\n"

    if os.path.exists("/etc/6to4.sh"):
        with open("/etc/6to4.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumi6 mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/6to4.sh", "w") as file:
            file.writelines(sh_contents)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")

def ipip_mtu():
    private_mtu()
    mtu_value = input("\033[93mEnter the \033[92mMTU value \033[93m[ \033[96mIP6IP6 \033[93m]:\033[0m ")
    mtu_command = f"/sbin/ip -6 link set dev azumip mtu {mtu_value}\n"

    if os.path.exists("/etc/ipip.sh"):
        with open("/etc/ipip.sh", "r") as file:
            sh_contents = file.readlines()

        mtu_exists = False
        for i in range(len(sh_contents)):
            if "link set dev azumip mtu" in sh_contents[i]:
                sh_contents[i] = mtu_command
                mtu_exists = True
                break

        if not mtu_exists:
            sh_contents.append(mtu_command)

        with open("/etc/ipip.sh", "w") as file:
            file.writelines(sh_contents)

        display_checkmark("\033[92mMTU command edited successfully\033[0m")
        subprocess.run(mtu_command, shell=True)
    else:
        print("\033[91mCommand file doesn't exist\033[0m")
                                
def ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ip_menu()
            break
        elif server_type == '2':
            iran_ip_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')

def ip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])
	
def ip_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
	
def ip_iran():
    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 20
    ip_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    ip_service()

    print("\033[92mIPIP6 Configuration Completed!\033[0m")
	
def ip_kharej():
    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 20
    ip_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    ip_service()

    print("\033[92mIPIP6 Configuration Completed!\033[0m")
	
## kharej ip
def server_ipv4():

    command = "curl -s https://api.ipify.org"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("Error retrieving server's IPv4 address.")
        return None
    ipv4 = process.stdout.strip()
    return ipv4

def kharej_ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP \033[92mKharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    file_path = '/etc/ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")

 

    num_additional_ips = int(input("Enter the number of additional IPv6 addresses: "))
    

    command = f"echo '/sbin/modprobe sit' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumii mode ipip remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumii' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumii' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip link set azumii up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


   
    config_file_path = '/etc/ip.sh'
 
    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)

   
    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    print("GRE tunnel created and configured successfully.")
    print("Configuration saved to /etc/ip.sh.")
    print("Cronjob added to execute /etc/ip.sh on every reboot.")

    ip_kharej()
	
# iran ip

def iran_ip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP \033[92mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    file_path = '/etc/ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of additional IPv6 addresses: "))
    
    command = f"echo '/sbin/modprobe sit' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumii mode ipip remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumii' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16" 
        command = f"echo 'ip addr add {ip_address} dev azumii' >> {file_path}"
        subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip link set azumii up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


    config_file_path = '/etc/ip.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    print("GRE tunnel created and configured successfully.")
    print("Configuration saved to /etc/ip.sh.")
    print("Cronjob added to execute /etc/ip.sh on every reboot.")
    ip_iran()
    
###menu ipip		
def ipip_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIPIP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_ipip6_menu()
            break
        elif server_type == '2':
            iran_ipip6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def run_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    

	
def display_kharej_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

def add_cron_job():
    file_path = '/etc/private.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)

##ipip6 kharej
def ping_ipip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])


def ipip6_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ipip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumip mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:0db8:1234:a220::1/64 dev azumip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumip up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumip' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:0db8:1234:a22{i}::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumip' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:0db8:1234:a220::1\n".format(interface)
        with open('/etc/ipip.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumip mtu {mtu_value}\n"
        with open('/etc/ipip.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)


    
    

    print("\033[93mCreated IPv6 Addresses :\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:0db8:1234:a220::1    |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

def ipip_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def create_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip_kharej():
    remote_ip = "fd1d:fc98:b73e:b481::2" #iran-ip
    local_ip = "fd1d:fc98:b73e:b481::1"   #kharej ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip6_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::2" #iranip
    max_pings = 3
    interval = 20
    create_ping_script(ip_address, max_pings, interval)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_ipip_service()

    ipip_cronjob()
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")


   
#sit kharej
def kharej_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mKharej\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_kharej()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")



    
 ##### IRAN IPIP6
def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran_ip():
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    
		

##ipip6 iran


def iran_ipip_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])


def ipip6_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/ipip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, 'w') as f:
        f.write('/sbin/modprobe ipip\n')
        f.write(f'ip -6 tunnel add azumip mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n')
        f.write('ip -6 addr add 2002:0db8:1234:a220::2/64 dev azumip\n')
        f.write('ip link set azumip up\n')
        f.write('ip -6 route add 2002::/16 dev azumip\n')
        created_ips = []
        for i in range(2, num_additional_ips + 2):
            ip_address = f'2002:0db8:1234:a22{i}::2'
            created_ips.append(ip_address)
            f.write(f'ip -6 addr add {ip_address}/64 dev azumip\n')

        

    command = f'chmod +x {file_path}'
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'bash {file_path}', shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:0db8:1234:a220::2\n".format(interface)
        with open('/etc/ipip.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [IP6IP6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumip mtu {mtu_value}\n"
        with open('/etc/ipip.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)


    
    

   
    print('\033[93mCreated IPv6 Addresses:\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')
    print('\033[92m' + '| 2002:0db8:1234:a220::2    |' + '\033[0m')
    for ip_address in created_ips:
        print('\033[92m' + f'| {ip_address}    |' + '\033[0m')
    print('\033[92m' + '+---------------------------+' + '\033[0m')



def ipip_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/ipip.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/ipip.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)


def iran_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def ipip_iran():
    remote_ip = "fd1d:fc98:b73e:b481::1" #kharej-ip
    local_ip = "fd1d:fc98:b73e:b481::2"   #iran ip
    num_additional_ips = int(input("\033[93mHow many \033[92madditional ips\033[93m do you need? \033[0m"))
    ipip6_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:0db8:1234:a220::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_ipip_service()

    ipip_cronjob()
   
    display_checkmark("\033[92mIPIP6 Configuration Completed!\033[0m")

   
#sit iran
def iran_ipip6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring IPIP6 \033[92mIran\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    


    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    ipip_iran()
    sleep(1)	
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")


    
    
    ##### PRIVATE & NATIVE
    
       
def private_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mPrivate IP Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_private_menu()
            break
        elif server_type == '2':
            iran_private_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
        
        
def run_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:831b::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
 
def run_ping_iran():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "2001:831b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    
        

            
def kharej_private_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Kharej server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  There is also a cronjob and a ping service that automatically installs")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "-6", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi"], stdout=subprocess.DEVNULL)

    num_ips = int(input("\033[93mHow many \033[92mprivate IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1/64"

        result = subprocess.run(["ip", "-6", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "-6", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip -6 addr add 2001:831b::1/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::1/64"
            f.write(f"ip -6 addr add {ip_addr} dev azumi\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:831b::1\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::1"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    
    print("\033[92mKharej Server Configuration Completed!\033[0m")

def iran_private_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring Iran server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  There is also a cronjob and a ping service that automatically installs")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")
    
    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")
    

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    
    
    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)
    
    
    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "-6", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
    subprocess.run(["ip", "-6", "route", "add", "2001::/16", "dev", "azumi"], stdout=subprocess.DEVNULL)
    
   
    num_ips = int(input("\033[93mHow many \033[92mprivate IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2/64"
        

        result = subprocess.run(["ip", "-6", "addr", "show", "dev", "azumi"], capture_output=True, text=True)
        if ip_addr in result.stdout:
            print(f"IP address {ip_addr} already exists. Skipping...")
        else:
            subprocess.run(["ip", "-6", "addr", "add", ip_addr, "dev", "azumi"], stdout=subprocess.DEVNULL)
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip -6 addr add 2001:831b::2/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
        for i in range(1, num_ips + 1):
            ip_suffix = hex(i)[2:]
            ip_addr = f"2001:83{ip_suffix}b::2/64"
            f.write(f"ip -6 addr add {ip_addr} dev azumi\n")
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2001:831b::2\n".format(interface)
        with open('/etc/private.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    


    add_cron_job()

    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   
    run_ping_iran()
    sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated Private IP Addresses (IRAN):\033[0m")
    for i in range(1, num_ips + 1):
        ip_suffix = hex(i)[2:]
        ip_addr = f"2001:83{ip_suffix}b::2"
        print("\033[92m" + "+---------------------------+" + "\033[0m")
        print("\033[92m" + f" {ip_addr}    " + "\033[0m")
        print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="2001:831b::1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_v6.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

## Native

def Native_menu():
    subprocess.run("clear", shell=True)
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93mNative IP Menu\033[0m")
    print("\033[92m \"-\"\033[93m═════════════════════\033[0m")
    display_logo2()
    print("\033[93m.-------------------------------------------------------------------------------------------------------.\033[0m")
    print("\033[93m| \033[92mIf it didn't work, please uninstall it and add extra IP manually  \033[0m")
    print("\033[93m|\033[0m  If you don't have native IPv6, please use a private IP instead.                                             \033[0m")
    print("\033[93m'-------------------------------------------------------------------------------------------------------'\033[0m")
    display_notification("\033[93mAdding extra Native IPv6 [Kharej]...\033[0m")
    print("\033[93m╭──────────────────────────────────────────────────────────╮\033[0m")

    try:
        interface = subprocess.run("ip route | awk '/default/ {print $5; exit}'", shell=True, capture_output=True, text=True).stdout.strip()
        ipv6_addresses = subprocess.run(f"ip -6 addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}' | cut -d'/' -f1", shell=True, capture_output=True, text=True).stdout.strip().split('\n')

        print("\033[92mCurrent IPv6 addresses on", interface + ":\033[0m")
        for address in ipv6_addresses:
            print(address)

        confirm = input("\033[93mAre these your current IPv6 addresses? (y/n): \033[0m")
        if confirm.lower() != "y":
            display_error("\033[91mAborted. Please manually configure the correct IPv6 addresses.\033[0m")
            return

        sorted_addresses = sorted(ipv6_addresses, reverse=True)
        additional_address = ""
        for i in range(len(sorted_addresses)):
            current_last_part = sorted_addresses[i].split(':')[-1]
            modified_last_part_hex = format(int(current_last_part, 16) + 1, '04x')
            modified_address = ":".join(sorted_addresses[i].split(':')[:-1]) + ":" + modified_last_part_hex

            if modified_address not in sorted_addresses:
                additional_address = modified_address
                break

        if not additional_address:
            display_error("\033[91mNo additional address to add.\033[0m")
            return

        subprocess.run(["ip", "addr", "add", f"{additional_address}/64", "dev", interface])

        script_file = "/etc/ipv6.sh"
        with open(script_file, "a") as file:
            file.write(f"ip addr add {additional_address}/64 dev {interface}\n")

        subprocess.run(["chmod", "+x", script_file])

        subprocess.run("crontab -l | grep -v '/etc/ipv6.sh' | crontab -", shell=True)

        display_notification("\033[93mAdding cronjob for the server..\033[0m")
        subprocess.run("(crontab -l 2>/dev/null; echo \"@reboot /bin/bash /etc/ipv6.sh\") | crontab -", shell=True)

        display_checkmark("\033[92mIPv6 addresses added successfully!\033[0m")
    except ValueError as e:
        display_error("\033[91mAn error occurred while adding IPv6 addresses:", str(e), "\033[0m")
        
###menu gre		
def gre_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE | GRE6 Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mGRE\033[0m')
    print('2. \033[93mGRE6 \033[0m')
    print('3. \033[94mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gre_menu()
            break
        elif server_type == '2':
            gre6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
def gre_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_gre_menu()
            break
        elif server_type == '2':
            iran_gre_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
def gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE6 Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN \033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej_gre6_menu()
            break
        elif server_type == '2':
            iran_gre6_menu()
            break
        elif server_type == '3':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
			
   ##gre6         
def run_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_v6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_v6.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_v6.service'])
    

	
def display_kharej_ip():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::1"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		

def add_cron_job():
    file_path = '/etc/private.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)

##gre6 kharej

def gre6_cronjob():
    try:
        
        subprocess.run(
            "crontab -l | grep -v '/etc/gre6.sh' | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
     
        subprocess.run(
            "(crontab -l ; echo '@reboot /bin/bash /etc/gre6.sh') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )
        
        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
		
def ping_gre6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])

def gre6_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::1"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig6' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::1\n".format(interface)
        with open('/etc/gre6.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n" 
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IPv6 Addresses:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::1               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


def create_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

def gre6_kharej():
    remote_ip = "fd1d:fc98:b73e:b481::2" #iran-ip
    local_ip = "fd1d:fc98:b73e:b481::1"   #kharej ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre6_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre6_service()

    gre6_cronjob()
   
    

   
#sit kharej
def kharej_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[92mKharej\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Kharej server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::1/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
    gre6_kharej()
    sleep(1)	
    
    
 ##### IRAN gre6
def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "fd1d:fc98:b73e:b481::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
    
	
def display_iran_ip():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated Private IP Addresses (Kharej):\033[0m")
    ip_addr = "fd1d:fc98:b73e:b481::2"
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| {ip_addr}    |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
		


def iran_gre6_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])

def gre6_iran_tunnel(remote_ip, local_ip, num_additional_ips):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    created_ips = []
    for i in range(2, num_additional_ips + 2):
        ip_address = f"2002:83{i}a::2"
        created_ips.append(ip_address)
        command = f"echo 'ip -6 addr add {ip_address}/64 dev azumig6' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::2\n".format(interface)
        with open('/etc/gre6.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IPv6 Addresses:\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + f"| 2002:831a::2               |" + "\033[0m")
    for ip_address in created_ips:
        print("\033[92m" + f"| {ip_address}               |" + "\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")



def iran_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    

def gre6_iran():
    remote_ip = "fd1d:fc98:b73e:b481::1" #kharej ip
    local_ip = "fd1d:fc98:b73e:b481::2"   #iran ip
    num_additional_ips = int(input("\033[97mEnter the number of \033[92madditional IPs\033[97m for the \033[92mGRE6\033[97m tunnel: "))
    gre6_iran_tunnel(remote_ip, local_ip, num_additional_ips)


    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre6_service()

    gre6_cronjob()
   
   

   
#sit iran
def iran_gre6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mConfiguring GRE \033[92mIran\033[93m server\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    display_notification("\033[93mAdding private IP addresses for Iran server...\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "fd1d:fc98:b73e:b481::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add fd1d:fc98:b73e:b481::2/64 dev azumi\n")
        f.write("ip -6 route add fd1d::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="fd1d:fc98:b73e:b481::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gre6_iran()
    sleep(1)	
    display_checkmark("\033[92mGRE6 Configuration Completed!\033[0m")
	
## gre
def gre_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_ip.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_ip.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_ip.service'])
    subprocess.run(['systemctl', 'start', 'ping_ip.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_ip.service'])
	
def gre_ping_script(ip_address, max_pings, interval):
    file_path = '/etc/ping_ip.sh'

    if os.path.exists(file_path):
        os.remove(file_path)

    script_content = f'''#!/bin/bash

ip_address="{ip_address}"

max_pings={max_pings}

interval={interval}

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open(file_path, 'w') as file:
        file.write(script_content)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
	
def gre_iran():
    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 20
    gre_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    gre_service()


	
def gre_kharej():
    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    

    ip_address = remote_prefix
    max_pings = 3
    interval = 20
    gre_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)

    gre_service()

	
## kharej gre
def server_ipv4():

    command = "curl -s https://api.ipify.org"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print("Error retrieving server's IPv4 address.")
        return None
    ipv4 = process.stdout.strip()
    return ipv4

def kharej_gre_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE \033[92mKharej\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    file_path = '/etc/gre.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────╮\033[0m")
    
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────╯\033[0m")

    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of \033[92madditional IPv6\033[93m addresses: "))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    

    command = f"echo '/sbin/modprobe gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumig mode gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumig' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("Error: No network interface with IPv6 address.")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, ipv6_address)
        with open('/etc/gre.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig mtu {mtu_value}\n"
        with open('/etc/gre.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
 
    



    config_file_path = '/etc/gre.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_checkmark("\033[92mGRE Configuration Completed!\033[0m")



    gre_kharej()
	
# iran gre

def iran_gre_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGRE \033[92mIRAN\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    file_path = '/etc/gre.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
    display_notification("\033[93mConfiguring...\033[0m")
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────╮\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────╯\033[0m")


    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")



    num_additional_ips = int(input("Enter the number of \033[92madditional IPv6\033[93m addresses: "))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    command = f"echo '/sbin/modprobe gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip tunnel add azumig mode gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip addr add {ipv6}/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    

    for i in range(2, num_additional_ips + 2):
        ip_address = f"{ipv6[:-1]}{i}/16"  
        command = f"echo 'ip addr add {ip_address} dev azumig' >> {file_path}"
        subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("Error: No network interface with IPv6 address.")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, ipv6_address)
        with open('/etc/gre.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig mtu {mtu_value}\n"
        with open('/etc/gre.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    

 
    config_file_path = '/etc/gre.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{file_path}') | crontab -", shell=True, check=True)

  
    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_checkmark("\033[92mGRE Configuration Completed!\033[0m")
    gre_iran()
    
def clear_screen():
    os.system("clear")
    
def i6to4_menu():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(O,O)\033[0m')
    print('\033[92m(   ) \033[93m6TO4 Menu\033[0m')
    print('\033[92m "-"\033[93m════════════════════════════\033[0m')
    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92m6to4 \033[0m')
    print('2. \033[93m6to4 Anycast\033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")

    if server_type == '1':
        i6to4_no()
    elif server_type == '2':
        i6to4_any()
    elif server_type == '3':
        clear_screen()
        main_menu()
    else:
        print("Invalid choice.")
        
def i6to4_no():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92m[Not Anycast]\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print("\033[93mChoose what to do:\033[0m")
    print("1. \033[92mKharej\033[0m")
    print("2. \033[93mIRAN\033[0m")
    print("3. \033[94mback to previous menu\033[0m")
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == "1":
            i6to4_kharej()
            break
        elif server_type == "2":
            i6to4_iran()
            break
        elif server_type == "3":
            clear_screen()
            i6to4_menu()
            break
        else:
            print("Invalid choice.")
            
def ipv6_int():
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        if iface != 'lo' and netifaces.AF_INET6 in netifaces.ifaddresses(iface):
            return iface
    return None
	
def i6to4_kharej():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92mKharej\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m")  
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return    
    sleep(1)
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")

    ipv4 = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True).stdout.strip()


    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split(".")))
    
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    

    if prefix.endswith("::1"):
        gateway = prefix[:-3] + "::2"
    else:
        gateway = prefix[:-3] + "::1"
    
   
    with open("/etc/6to4.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote {} local {} ttl 255\n".format(remote_ip, local_ip))
        
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via {} dev azumi6 metric 1\n".format(gateway))
        f.write("ip -6 route add ::/0 dev azumi6\n")
        answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
        if answer.lower() in ['yes', 'y']:
            interface = ipv6_int()
            if interface is None:
               print("Error: No network interface with IPv6 address.")
            else:
               print("Interface:", interface)
               f.write("ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, prefix))
        else:
            print("Skipping changing the default route.")
    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    start_index = 3
    

    with open("/etc/6to4.sh", "a") as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split(".")), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")
      
    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(["/bin/bash", "/etc/6to4.sh"])

    remote_ipv4 = input("\033[93mEnter \033[92mIran IPv4 address\033[93m [Ping Service]: \033[0m")


    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split(".")))

    sleep(1)

    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(["ping6", "-c", "2", remote_prefix], capture_output=True, text=True).stdout.strip()


    print(ping_result)


    script_content = '''#!/bin/bash


ip_address="''' + remote_prefix + '''"

max_pings=3

interval=20

while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F"time=" "{print $1}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done'''


    with open("/etc/ping_v6.sh", "w") as f:
        f.write(script_content)

    subprocess.run(["chmod", "+x", "/etc/ping_v6.sh"])


    service_content = '''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target'''

    with open("/etc/systemd/system/ping_v6.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_v6.service"])
    subprocess.run(["systemctl", "start", "ping_v6.service"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")

def i6to4_iran():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6TO4 \033[92mIRAN\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your Kharej and Iran IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m") 
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return    
    sleep(1)    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")    

    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPv4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address: \033[0m")

    ipv4 = subprocess.run(["curl", "-s", "https://api.ipify.org"], capture_output=True, text=True).stdout.strip()


    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split(".")))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    

    if prefix.endswith("::1"):
        gateway = prefix[:-3] + "::2"
    else:
        gateway = prefix[:-3] + "::1"
    

    with open("/etc/6to4.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote {} local {} ttl 255\n".format(remote_ip, local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via {} dev azumi6 metric 1\n".format(gateway))
        answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
        if answer.lower() in ['yes', 'y']:
            interface = ipv6_int()
            if interface is None:
               print("Error: No network interface with IPv6 address.")
            else:
               print("Interface:", interface)
               f.write("ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, prefix))
        else:
            print("Skipping changing the default route.")
        

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    start_index = 3
    

    with open("/etc/6to4.sh", "a") as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split(".")), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'

    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(["/bin/bash", "/etc/6to4.sh"])

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4 address\033[93m [Ping Service]: \033[0m")

    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split(".")))

    sleep(1)


    ping_result = subprocess.run(["ping6", "-c", "2", remote_prefix], capture_output=True, text=True).stdout.strip()


    print(ping_result)


    script_content = '''#!/bin/bash


ip_address="''' + remote_prefix + '''"

max_pings=3

interval=20

while true
do
  
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F"time=" "{print $1}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done'''


    with open("/etc/ping_v6.sh", "w") as f:
        f.write(script_content)

    subprocess.run(["chmod", "+x", "/etc/ping_v6.sh"])


    service_content = '''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target'''

    with open("/etc/systemd/system/ping_v6.service", "w") as f:
        f.write(service_content)

    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "ping_v6.service"])
    subprocess.run(["systemctl", "start", "ping_v6.service"])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
	

def clear():
    subprocess.run(['clear'])

def i6to4_any():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92m[Anycast]\033[93m Menu\033[0m")
    print("\033[92m \"-\"\033[93m════════════════════════════\033[0m")
    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")

    if server_type == '1':
        i6to4_any_kharej()
    elif server_type == '2':
        i6to4_any_iran()
    elif server_type == '3':
        clear()
        main_menu()
    else:
        print("Invalid choice.")
		
def i6to4_any_kharej():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m6to4 \033[92mKharej\033[93m  Menu\033[92m[Anycast]\033[0m')  
    print('\033[92m "-"\033[93m════════════════════════════\033[0m')    
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your \033[92mKharej\033[93m IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mIRAN\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")
    
    
    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m") 
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej IPv4\033[93m address: \033[0m")
           
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    
    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")
        
    num_ips = input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    start_index = 3
    
    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + int(num_ips)):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))
    
    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])
    
    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")
    
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    sleep(1)
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    
    print(ping_result)
    
    script_content = '''#!/bin/bash

ip_address="{}"

max_pings=3

interval=20

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''
    with open('/etc/ping_v6.sh', 'w') as f:
        f.write(script_content)
    
    subprocess.run(['chmod', '+x', '/etc/ping_v6.sh'])
    
    with open('/etc/systemd/system/ping_v6.service', 'w') as f:
        f.write('[Unit]\n')
        f.write('Description=Ping Service\n')
        f.write('After=network.target\n')
        f.write('\n')
        f.write('[Service]\n')
        f.write('ExecStart=/bin/bash /etc/ping_v6.sh\n')
        f.write('Restart=always\n')
        f.write('\n')
        f.write('[Install]\n')
        f.write('WantedBy=multi-user.target\n')
    
    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])
    
    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
	
def i6to4_any_iran():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92mIRAN\033[93m  Menu\033[92m[Anycast]\033[0m")
    print("\033[92m\"-\"\033[93m════════════════════════════\033[0m")
    display_logo2()
    print("\033[93m╭───────────────────────────────────────────────────────────────────────────────────────╮")
    print("\033[92m  Please make sure to remove any private IPs that you have created before proceeding")
    print("\033[93m  Enter your \033[92mIRAN\033[93m IPV4 address, it will automatically configure your server")
    print("\033[96m  If you need additional IP address, you can enter the desired number")
    print("\033[97m  For ping service, enter \033[92mKharej\033[97m IPV4 address")
    print("\033[93m╰───────────────────────────────────────────────────────────────────────────────────────╯\033[0m")

    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)    
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIran IPv4\033[93m address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()

    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")

    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")
        answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
        if answer.lower() in ['yes', 'y']:
            interface = ipv6_int()
            if interface is None:
               print("Error: No network interface with IPv6 address.")
            else:
               print("Interface:", interface)
               f.write("ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, prefix))
        else:
            print("Skipping changing the default route.")

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    start_index = 3

    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")
    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))

    subprocess.run(['sleep', '1'])
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    script_content = '''#!/bin/bash

ip_address="{}"
max_pings=3
interval=20

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix)

    with open('/etc/ping_v6.sh', 'w') as f:
        f.write(script_content)

    subprocess.run(['chmod', '+x', '/etc/ping_v6.sh'])

    with open('/etc/systemd/system/ping_v6.service', 'w') as f:
        f.write('''[Unit]
Description=Ping Service
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_v6.sh
Restart=always

[Install]
WantedBy=multi-user.target
''')

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_v6.service'])
    subprocess.run(['systemctl', 'start', 'ping_v6.service'])
    sleep(1)
    subprocess.run(["systemctl", "restart", "ping_v6.service"])

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
    
def remove_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[91mUninstall\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mUninstall IPIP6\033[0m')
    print('2. \033[93mUninstall 6to4\033[0m')
    print('3. \033[92mUninstall 6to4 \033[96manycast\033[0m')
    print('4. \033[96mUninstall Gre\033[0m')
    print('5. \033[92mUninstall Gre6\033[0m')
    print('6. \033[93mUninstall Private IP\033[0m')
    print('7. \033[96mUninstall Extra Native IP\033[0m')
    print('8. \033[92mUninstall Geneve\033[0m')
    print('0. \033[91mback to the main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            remove_ipip6()
            break
        elif server_type == '2':
            remove_6to4()
            break
        elif server_type == '3':
            remove_6to4()
            break
        elif server_type == '4':
            remove_gre()
            break
        elif server_type == '5':
            remove_gre6()
            break
        elif server_type == '6':
            remove_private()
            break
        elif server_type == '7':
            extra_uninstall()
            break
        elif server_type == '8':
            genx_ip()
            break
        elif server_type == '0':
            clear()
            main_menu()
            break
        else:
            print('Invalid choice.')
            
def genx_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[92mGeneve\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print("1. \033[92mGeneve \033[0m")
    print("2. \033[93mGeneve + Native \033[0m")
    print("3. \033[96mGeneve + Gre6 + Native \033[0m")
    print("4. \033[92mGeneve + Gre6 + IPV4 \033[0m")
    print("5. \033[97mGeneve + IP6tnl + Gre6 + Native \033[0m")
    print("7. \033[93mGeneve + ICMP\033[0m")
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_uninstall()
            break
        elif server_type == '2':
            genz_uninstall()
            break
        elif server_type == '3':
            gen2_uninstall()
            break
        elif server_type == '5':
            gen4_uninstall()
            break
        elif server_type == '4':
            gen6_uninstall()
            break    
        elif server_type == '7':
            gen_icmp()
            break
        elif server_type == '0':
            clear()
            remove_menu()
            break
        else:
            print('Invalid choice.')   
## gen ic
def reset_icmp():
    try:
        reset_ipv4 = False
        reset_ipv6 = False

        os.system("sysctl -w net.ipv4.icmp_echo_ignore_all=0")
        reset_ipv4 = True

        os.system("sudo sysctl -w net.ipv6.icmp.echo_ignore_all=0")
        reset_ipv6 = True

        if reset_ipv4 or reset_ipv6:
            display_checkmark("\033[92mICMP has been reset to default!\033[0m")
        else:
            display_notification("\033[93mICMP settings has been reset.\033[0m")
    except Exception as e:
        display_error("\033[91mAn error occurred: {}\033[0m".format(str(e)))

def install_icmp():
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_loading()

    subprocess.run(['sudo', 'tee', '/etc/resolv.conf'], input='nameserver 1.1.1.1\n', capture_output=True, text=True)


    ipv4_forward_status = subprocess.run(["sysctl", "net.ipv4.ip_forward"], capture_output=True, text=True)
    if "net.ipv4.ip_forward = 0" not in ipv4_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"])


    ipv6_forward_status = subprocess.run(["sysctl", "net.ipv6.conf.all.forwarding"], capture_output=True, text=True)
    if "net.ipv6.conf.all.forwarding = 0" not in ipv6_forward_status.stdout:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv6.conf.all.forwarding=1"])


    if os.path.exists("/root/icmptunnel"):
        shutil.rmtree("/root/icmptunnel")


    clone_command = 'git clone https://github.com/jamesbarlow/icmptunnel.git icmptunnel'
    clone_result = os.system(clone_command)
    if clone_result != 0:
        print("Error: Failed to clone Repo.")
        return


    if os.path.exists("/root/icmptunnel"):

        os.chdir("/root/icmptunnel")


        subprocess.run(['sudo', 'apt', 'install', '-y', 'net-tools'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'make'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libssl-dev'], capture_output=True, text=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'g++'], capture_output=True, text=True)


        subprocess.run(['make'], capture_output=True, text=True)


        os.chdir("..")
    else:
        display_error("\033[91micmptunnel folder not found.\033[0m")
def up_up():
    ulimit_setting = 'ulimit -n 65535'
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'r') as f:
        existing_bashrc = f.read()

    if ulimit_setting not in existing_bashrc:
        with open(bashrc_path, 'a') as f:
            f.write('\n')
            f.write(ulimit_setting)
            f.write('\n')

    sysctl_conf_path = '/etc/sysctl.conf'
    sysctl_params = [
        'net.core.rmem_max=26214400',
        'net.core.rmem_default=26214400',
        'net.core.wmem_max=26214400',
        'net.core.wmem_default=26214400',
        'net.core.netdev_max_backlog=2048'
    ]

    with open(sysctl_conf_path, 'r') as f:
        existing_sysctl_conf = f.read()

    params_to_add = []
    for param in sysctl_params:
        if param not in existing_sysctl_conf:
            params_to_add.append(param)

    if params_to_add:
        with open(sysctl_conf_path, 'a') as f:
            f.write('\n')
            f.write('\n'.join(params_to_add))
            f.write('\n')
        try:
            subprocess.run(["sudo", "sysctl", "-p"], stderr=subprocess.DEVNULL, check=True)
            display_checkmark("\033[92mLimit has been Set!\033[0m")
        except subprocess.CalledProcessError:
            print("\033[91mAn error occurred setting it up.\033[0m")
    else:
        display_checkmark("\033[92mLimit Increase was already Done.\033[0m")
        
def ic_kharej():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    up_up()
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring Kharej ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    

    if os.path.exists("/etc/icmp.sh"):
        os.remove("/etc/icmp.sh")

    with open("/etc/icmp.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("/root/icmptunnel/icmptunnel -s -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.1 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp.sh\n"
    with open("/etc/cron.d/icmp-kharej", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-kharej", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")

def ic_iran():
    if not os.path.exists("/root/icmptunnel"):
        install_icmp()
    up_up()    
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mConfiguring IRAN ...\033[0m")
    print("\033[93m──────────────────────────────────────────────────\033[0m")
    

    os.chdir("/root/icmptunnel")

    server_ipv4 = input("\033[93mEnter \033[92mKharej\033[93m IPv4 address:\033[0m ")

    if os.path.exists("/etc/icmp-iran.sh"):
        os.remove("/etc/icmp-iran.sh")

    with open("/etc/icmp-iran.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"/root/icmptunnel/icmptunnel {server_ipv4} -d\n")
        f.write("/sbin/ifconfig tun0 70.0.0.2 netmask 255.255.255.0\n")

    subprocess.run(["chmod", "700", "/etc/icmp-iran.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    os.system("/bin/bash /etc/icmp-iran.sh")

    cron_job_command = "@reboot root /bin/bash /etc/icmp-iran.sh\n"
    with open("/etc/cron.d/icmp-iran", "w") as f:
        f.write(cron_job_command)

    subprocess.call("crontab -u root /etc/cron.d/icmp-iran", shell=True)

    display_checkmark("\033[92mCronjob added successfully!\033[0m")

def gen_ipicmp():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_icmpk_version1()
            break
        elif server_type == '2':
            geneve_icmpk_version2()
            break
        else:
            print('Invalid choice.')
            
def geneve_icmpk_version1():
    ic_kharej()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("70.0.0.1")
    ufw("70.0.0.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "70.0.0.2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.2.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_icmpk_version2():
    ic_kharej()
    ufw("70.0.0.1")
    ufw("70.0.0.2")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "70.0.0.2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
	
def gen_ipicmpi():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_icmpi_version1()
            break
        elif server_type == '2':
            geneve_icmpi_version2()
            break
        else:
            print('Invalid choice.')

def geneve_icmpi_version1():
    ic_iran()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("70.0.0.1")
    ufw("70.0.0.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "70.0.0.1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_icmpi_version2():
    ic_iran()
    ufw("70.0.0.1")
    ufw("70.0.0.2")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "70.0.0.1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m") 
    
def rmv_limit():
    display_notification("\033[93mRestoring Limit ..\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ulimit_setting = 'ulimit -n 65535'
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'r') as f:
        existing_bashrc = f.read()

    if ulimit_setting in existing_bashrc:
        existing_bashrc = existing_bashrc.replace(ulimit_setting, '')

        with open(bashrc_path, 'w') as f:
            f.write(existing_bashrc)

    sysctl_conf_path = '/etc/sysctl.conf'
    sysctl_params = [
        'net.core.rmem_max=26214400',
        'net.core.rmem_default=26214400',
        'net.core.wmem_max=26214400',
        'net.core.wmem_default=26214400',
        'net.core.netdev_max_backlog=2048'
    ]

    with open(sysctl_conf_path, 'r') as f:
        existing_sysctl_conf = f.read()

    params_to_remove = []
    for param in sysctl_params:
        if param in existing_sysctl_conf:
            params_to_remove.append(param)

    if params_to_remove:
        for param in params_to_remove:
            existing_sysctl_conf = existing_sysctl_conf.replace(param, '')

        with open(sysctl_conf_path, 'w') as f:
            f.write(existing_sysctl_conf)

        try:
            subprocess.run(["sudo", "sysctl", "-p"], stderr=subprocess.DEVNULL, check=True)
            display_checkmark("\033[92mLimit removal was Successful!\033[0m")
        except subprocess.CalledProcessError:
            print("\033[91mAn error occurred.\033[0m")
    else:
        display_checkmark("\033[92mNothin was found! moving on..\033[0m")
        
def remove_icmp():
    
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving icmptunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    try:
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        subprocess.run("ip link set dev tun0 down > /dev/null", shell=True)
        subprocess.run("ip link set dev tun1 down > /dev/null", shell=True)
        subprocess.run("systemctl daemon-reload", shell=True)

        print("Progress: ", end="")

        try:
            lsof_process = subprocess.Popen(["lsof", "-t", "/root/icmptunnel/icmptunnel"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            lsof_output, lsof_error = lsof_process.communicate()

            if lsof_output:
                pids = lsof_output.decode().split('\n')[:-1]
                for pid in pids:
                    subprocess.run(["kill", pid])

            subprocess.run(["rm", "-rf", "/root/icmptunnel"])
        except FileNotFoundError:
            print("Error: Directory '/root/icmptunnel' does not exist.")
        except Exception as e:
            print("Error:", e)

        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"/bin/bash /etc/icmp-iran.sh\" | crontab -", shell=True)
        display_checkmark("\033[92mICMPtunnel Uninstallation completed!\033[0m")

        if os.path.isfile("/etc/icmp.sh"):
            os.remove("/etc/icmp.sh")
        if os.path.isfile("/etc/icmp-iran.sh"):
            os.remove("/etc/icmp-iran.sh")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    except Exception as e:
        print("Error:", e)
        

        
            
def remove_ipip6():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mIPIP6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/ipip.sh", shell=True) == 0:
            subprocess.run("rm /etc/ipip.sh", shell=True)
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipip.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        sleep(1)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumip down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumip > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)

        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 3
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
def i6to41_any():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92m[Anycast]\033[93m Menu\033[0m")
    print('\033[92m "-"\033[93m════════════════════════════\033[0m') 
    
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to main menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")
    
    server_type = input("\033[38;5;205mEnter your choice Please: \033[0m")

    if server_type == '1':
        i6to41_any_kharej()
    elif server_type == '2':
        i6to41_any_iran()
    elif server_type == '3':
        clear()
        main_menu()
    else:
        print("Invalid choice.")
		
def i6to41_any_kharej():
    clear_screen()
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93m6to4 \033[92mKharej\033[93m  Menu\033[92m[Anycast]\033[0m')  
    print('\033[92m "-"\033[93m════════════════════════════\033[0m')    
    
    
    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring Kharej..\033[0m") 
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej IPv4\033[93m address: \033[0m")
           
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")
    
    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")
        
    num_ips = input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")
    
    start_index = 3
    
    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + int(num_ips)):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))
    
    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)
    
    display_notification("\033[93mStarting 6to4...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])
    num_servers = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mServers\033[93m[Ping Service]? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(num_servers):
        remote_ipv4 = input(f"\033[93mEnter \033[96mIPv4 address\033[93m of server \033[92m{i+1} [Ping Service]: \033[0m")
    
        remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
        sleep(1)
        print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
        ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
        print(ping_result)

        script_content = '''#!/bin/bash

ip_address="{}"

max_pings=3

interval=20

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

        script_filename = f'/etc/ping_v6{i+1}.sh'
        with open(script_filename, 'w') as f:
            f.write(script_content)

        subprocess.run(['chmod', '+x', script_filename])

        service_filename = f'/etc/systemd/system/ping_v6{i+1}.service'
        with open(service_filename, 'w') as f:
            f.write('[Unit]\n')
            f.write(f'Description=Ping Service {i+1}\n')
            f.write('After=network.target\n')
            f.write('\n')
            f.write('[Service]\n')
            f.write(f'ExecStart=/bin/bash {script_filename}\n')
            f.write('Restart=always\n')
            f.write('\n')
            f.write('[Install]\n')
            f.write('WantedBy=multi-user.target\n')

        subprocess.run(['systemctl', 'daemon-reload'])
        subprocess.run(['systemctl', 'enable', f'ping_v6{i+1}.service'])
        subprocess.run(['systemctl', 'start', f'ping_v6{i+1}.service'])
        sleep(1)
        subprocess.run(["systemctl", "restart", f"ping_v6{i+1}.service"])

        print(f"\033[92mPing service for server {i+1} has been added successfully!\033[0m")
        print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")
   ##### saki _ gretap

		
def gree6_tunnel(remote_ip, local_ip):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::1\n".format(interface)
        with open('/etc/gre6.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    


def gree6_kharej():
    remote_ip = "2001:831b::2" #iran-ip
    local_ip = "2001:831b::1"   #kharej ip
    gree6_tunnel(remote_ip, local_ip)
    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    ping_gre6_service()

    gre6_cronjob()
   
#sit kharej
def kharej_gree6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + GRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print(' \033[93mConfiguring \033[92mKharej\033[93m server\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add 2001:831b::1/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gree6_kharej()
    sleep(1)	
    
    
 ##### IRAN gre6
def iran_ping():
    try:
        subprocess.run(["ping", "-c", "2", "2001:831b::1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
     


def gree6_iran_tunnel(remote_ip, local_ip):
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
        
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::2\n".format(interface)
        with open('/etc/gre6.sh', 'a') as f:
            f.write(rt_command)
        subprocess.run(rt_command, shell=True, check=True)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    


    

def gree6_iran():
    remote_ip = "2001:831b::1" #kharej ip
    local_ip = "2001:831b::2"   #iran ip
    gree6_iran_tunnel(remote_ip, local_ip)


    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)

    
    iran_gre6_service()

    gre6_cronjob()
  
   
#sit iran
def iran_gree6_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + GRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[93mConfiguring \033[92mIran\033[93m server\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "sit", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe sit\n")
        f.write(f"ip tunnel add azumi mode sit remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip link set dev azumi up\n")
        f.write("ip addr add 2001:831b::2/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gree6_iran()
    sleep(1)	
    
def genf_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGR6 + Geneve Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mGRE + Native Geneve\033[0m')
    print('2. \033[96mIP6tnl + GRE + Native Geneve\033[0m')
    print('3. \033[93mGRE + IPV4 Geneve\033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            genfm_ip()
            break
        elif server_type == '2':
            genf3_ip()
            break
        elif server_type == '3':
            genf5_ip()
            break
        elif server_type == '0':
            clear()
            genz_ip()
            break
        else:
            print('Invalid choice.') 
# sit gre gen
def kharej_gree61_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + GRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print(' \033[93mConfiguring \033[92mKharej\033[93m server\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m") 
    ufw("2001:831b::2")
    ufw("2001:831b::1")	

    subprocess.run(["ip", "tunnel", "add", "azumi", "mode", "ip6ip6", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::1/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe ipip\n")
        f.write(f"ip -6 tunnel add azumi mode ip6ip6 remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip -6 link set dev azumi up\n")
        f.write("ip -6 addr add 2001:831b::1/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    run_ping()
    sleep(1)
    


    script_content1 = '''#!/bin/bash


ip_address="2001:831b::2"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()
    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gree61_kharej1()
    sleep(1)	
    
def iran_gree61_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + GRE Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[93mConfiguring \033[92mIran\033[93m server\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    if os.path.isfile("/etc/private.sh"):
        os.remove("/etc/private.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")   
    ufw("2001:831b::2")
    ufw("2001:831b::1")

    subprocess.run(["ip", "-6", "tunnel", "add", "azumi", "mode", "ip6ip6", "remote", remote_ip, "local", local_ip, "ttl", "255"], stdout=subprocess.DEVNULL)
    subprocess.run(["ip", "-6", "link", "set", "dev", "azumi", "up"], stdout=subprocess.DEVNULL)

    initial_ip = "2001:831b::2/64"
    subprocess.run(["ip", "addr", "add", initial_ip, "dev", "azumi"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/private.sh", "w") as f:
        f.write("/sbin/modprobe ipip\n")
        f.write(f"ip -6 tunnel add azumi mode ipip6 remote {remote_ip} local {local_ip} ttl 255\n")
        f.write("ip -6 link set dev azumi up\n")
        f.write("ip -6 addr add 2001:831b::2/64 dev azumi\n")
        f.write("ip -6 route add 2001::/16 dev azumi\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [6to4]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumi mtu {mtu_value}\n"
        with open("/etc/private.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mPrivate ip added successfully!\033[0m")
    file_path = '/etc/private.sh'
    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)

    sleep(1)
    add_cron_job()

    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
    iran_ping()
    

    sleep(1)

    script_content1 = '''#!/bin/bash


ip_address="2001:831b::1"

max_pings=3

interval=20

while true
do
    
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_v6.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_v6.sh', 0o755)
    ping_v6_service()

    display_notification("\033[93mConfiguring...\033[0m")
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gree61_iran1()
    sleep(1)	
    
def gree61_kharej1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
		
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote 2001:831b::2 local 2001:831b::1 ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
    
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    


def gree61_kharej1():
    gree61_kharej1_tunnel()
    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)   
    ping_gre6_service()
    gre6_cronjob()
    
def gree61_iran1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
	
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote 2001:831b::1 local 2001:831b::2 ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    


    

def gree61_iran1():
    gree61_iran1_tunnel()
    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)    
    iran_gre6_service()
    gre6_cronjob()
    
def genf3_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve +  \033[96mNative \033[93m+\033[92m Gre6 + IP6tnl \033[93mMenu\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen1_ipger()
            break
        elif server_type == '2':
            gen1_ipgeri()
            break
        elif server_type == '3':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')    
def gen1_ipger():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_gerk1_version1()
            break
        elif server_type == '2':
            geneve_gerk1_version2()
            break
        else:
            print('Invalid choice.')

def geneve_gerk1_version1():
    kharej_gree61_menu()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.2.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_gerk1_version2():
    kharej_gree61_menu()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
	
def gen1_ipgeri():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_geri1_version1()
            break
        elif server_type == '2':
            geneve_geri1_version2()
            break
        else:
            print('Invalid choice.')

def geneve_geri1_version1():
    iran_gree61_menu()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_geri1_version2():
    iran_gree61_menu()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m") 
## method 1
def genfm_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGR6 + Geneve Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mMethod 1 [no route]\033[0m')
    print('2. \033[93mMethod 2 [/w route]\033[0m')
    print('0. \033[91mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            genf1_ip()
            break
        elif server_type == '2':
            genf12_ip()
            break
        elif server_type == '0':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')  

def genf12_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve +  \033[96mNative \033[93m+\033[92m Gre6 \033[93mM[2]\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            genr_ipger()
            break
        elif server_type == '2':
            genr_ipgeri()
            break
        elif server_type == '3':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')
def genr_ipger():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_gerkr_version1()
            break
        elif server_type == '2':
            geneve_gerkr_version2()
            break
        else:
            print('Invalid choice.')
def gree6r_kharej1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
		
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m") 
    ufw(remote_ip)	
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::1\n".format(interface)
            with open('/etc/gre6.sh', 'a') as f:
                f.write(rt_command)
    else:
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)

    sleep(1)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


def gree6r_kharej1():
    gree6r_kharej1_tunnel()
    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)   
    ping_gre6_service()
    gre6_cronjob()
    
def geneve_gerkr_version1():
    gree6r_kharej1()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.2.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_gerkr_version2():
    gree6r_kharej1()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
	
def genr_ipgeri():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_gerir_version1()
            break
        elif server_type == '2':
            geneve_gerir_version2()
            break
        else:
            print('Invalid choice.')

def gree6r_iran1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")   
    ufw(remote_ip)	
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
    if answer.lower() in ['yes', 'y']:
        interface = ipv6_int()
        if interface is None:
            print("\033[91mError: No network interface with IPv6 address\033[0m")
        else:
            print("Interface:", interface)
            rt_command = "ip -6 route replace default via fe80::1 dev {} src 2002:831a::2\n".format(interface)
            with open('/etc/gre6.sh', 'a') as f:
                f.write(rt_command)
    else:        
        print("Skipping changing the default route.")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
    sleep(1)
    subprocess.run(f"bash {file_path}", shell=True, check=True)


    

def gree6r_iran1():
    gree6r_iran1_tunnel()
    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)    
    iran_gre6_service()
    gre6_cronjob()
    
def geneve_gerir_version1():
    gree6r_iran1()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_gerir_version2():
    gree6r_iran1()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")             

    
def genf1_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve +  \033[96mNative \033[93m+\033[92m Gre6 \033[93mM[1]\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_ipger()
            break
        elif server_type == '2':
            gen_ipgeri()
            break
        elif server_type == '3':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')
            
def genf2_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + \033[96mIPV4 \033[93m+\033[92m Gre6 \033[93mMenu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            genf5_ip()
            break
        elif server_type == '2':
            gen5_ipgeri()
            break
        elif server_type == '3':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')
        
        
def genkh_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.2.1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
 
def genir_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.1.1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def ping_kh_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_gen.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_gen.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_gen.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_gen.service'])
    
        
def gen_job():
    file_path = '/etc/gen.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
def ufw(ip_address):
    subprocess.run(["sudo", "ufw", "allow", "from", ip_address])
def ufwr():
    subprocess.run(["sudo", "ufw", "reload"])
def ipv4_address():
    result = subprocess.run(["curl", "-s", "https://ipinfo.io/ip"], capture_output=True, text=True)
    return result.stdout.strip()            
def kharej1_gen_menu():
    kharej_gree6_menu()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    ufw("2001:831b::1")
    ufw("2001:831b::2")
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m Configuring Kharej server Geneve\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")



    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
 
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")
        
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()
    genkh_ping()
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")


    script_content1 = '''#!/bin/bash


ip_address="80.200.2.1"


max_pings=3


interval=20


while true
do
   
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
       script_file.write(script_content1)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()

    ufwr()
    print("\033[92mKharej Server Geneve Configuration Completed!\033[0m")

def iran1_gen_menu():
    iran_gree6_menu()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    ufw("2001:831b::1")
    ufw("2001:831b::2")
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m Configuring Iran server Geneve\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    
    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")
    

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
 
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")
    


    gen_job()
    genir_ping()
    sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")
   

    sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    


    script_content = '''#!/bin/bash


ip_address="80.200.1.1"


max_pings=3


interval=20


while true
do

    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''


    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)


    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Geneve Configuration Completed!\033[0m")
	
def genf5_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve +  \033[96mIPV4 \033[93m+\033[92m Gre6 \033[93mMenu\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen5_ipger()
            break
        elif server_type == '2':
            gen5_ipgeri()
            break
        elif server_type == '3':
            clear()
            genf_ip()
            break
        else:
            print('Invalid choice.')    
def gen5_ipger():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharej1_gen_menu()
            break
        elif server_type == '2':
            geneve_gerk6_version2()
            break
        else:
            print('Invalid choice.')

    
def geneve_gerk6_version2():
    kharej_gree6_menu()
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    ufw("2001:831b::1")
    ufw("2001:831b::2")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))


    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
	
def gen5_ipgeri():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            iran1_gen_menu()
            break
        elif server_type == '2':
            geneve_geri5_version2()
            break
        else:
            print('Invalid choice.')


    
def geneve_geri5_version2():
    iran_gree6_menu()
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    ufw("2001:831b::1")
    ufw("2001:831b::2")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m") 
    
## test n gre
def gree6_kharej1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
		
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m") 
    ufw(remote_ip)	
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::1/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
 
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    sleep(1)
    


def gree6_kharej1():
    gree6_kharej1_tunnel()
    ip_address = "2002:831a::2" #iranip
    max_pings = 3
    interval = 20
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    create_ping_script(ip_address, max_pings, interval)
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)   
    ping_gre6_service()
    gre6_cronjob()
     


def gree6_iran1_tunnel():
    file_path = '/etc/gre6.sh'

    if os.path.exists(file_path):
        os.remove(file_path)
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV6 address [\033[92mNative\033[93m or\033[96m Tunnelbroker\033[93m]: \033[0m")
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")   
    ufw(remote_ip)	
    command = f"echo '/sbin/modprobe ip6_gre' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 tunnel add azumig6 mode ip6gre remote {remote_ip} local {local_ip} ttl 255' >> {file_path}"
    subprocess.run(command, shell=True, check=True)

    command = f"echo 'ip -6 addr add 2002:831a::2/64 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip link set azumig6 up' >> {file_path}"
    subprocess.run(command, shell=True, check=True)
    
    command = f"echo 'ip -6 route add 2002::/16 dev azumig6' >> {file_path}"
    subprocess.run(command, shell=True, check=True)


    command = f"chmod +x {file_path}"
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f"bash {file_path}", shell=True, check=True)
 
    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [GRE6]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")
    if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
        mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
        mtu_command = f"ip link set dev azumig6 mtu {mtu_value}\n"
        with open('/etc/gre6.sh', 'a') as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
 
    sleep(1)
    


    

def gree6_iran1():
    gree6_iran1_tunnel()
    ip_address = "2002:831a::1" #kharejip
    max_pings = 3
    interval = 20
    iran_ping_script(ip_address, max_pings, interval)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    ping_result = subprocess.run(['ping6', '-c', '2', ip_address], capture_output=True, text=True).stdout.strip()
    print(ping_result)    
    iran_gre6_service()
    gre6_cronjob()

def gen_ipger():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_gerk_version1()
            break
        elif server_type == '2':
            geneve_gerk_version2()
            break
        else:
            print('Invalid choice.')

def geneve_gerk_version1():
    gree6_kharej1()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.2.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_gerk_version2():
    gree6_kharej1()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")

    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::2"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::2\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
	
def gen_ipgeri():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_geri_version1()
            break
        elif server_type == '2':
            geneve_geri_version2()
            break
        else:
            print('Invalid choice.')

def geneve_geri_version1():
    gree6_iran1()
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_geri_version2():
    gree6_iran1()

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw("2002:831a::1")
    ufw("2002:831a::2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", "2002:831a::1"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote 2002:831a::1\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m") 

##azumi native
def gen2_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve + Native  Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKHAREJ \033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_na_k()
            break
        elif server_type == '2':
            gen_na_i()
            break
        elif server_type == '3':
            clear()
            genz_ip()
            break
        else:
            print('Invalid choice.') 

def gen_na_k():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_nk_version1()
            break
        elif server_type == '2':
            geneve_nk_version2()
            break
        else:
            print('Invalid choice.')

def geneve_nk_version1():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[96mNative \033[93m| \033[92mTunnelbroker\033[93m]: \033[0m")
    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.1.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/30", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/30 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.2"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_nk_version2():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV6 address [\033[96mNative \033[93m| \033[92mTunnelbroker\033[93m]: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
    
def gen_na_i():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_ni_version1()
            break
        elif server_type == '2':
            geneve_ni_version2()
            break
        else:
            print('Invalid choice.')

def geneve_ni_version1():
    remote_ip = input("\033[93mEnter \033[92mKHAREJ\033[93m IPV6 address [\033[96mNative \033[93m| \033[92mTunnelbroker\033[93m]: \033[0m")

    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.1.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.2/30", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.2/30 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.2\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_ni_version2():
    remote_ip = input("\033[93mEnter \033[92mKHAREJ\033[93m IPV6 address [\033[96mNative \033[93m| \033[92mTunnelbroker\033[93m]: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")    
   ##### saki no
   
def gen_ip():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve  Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mMethod 1 \033[0m')
    print('2. \033[93mMethod 2\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            gen_ipm1()
            break
        elif server_type == '2':
            gen_ipm2()
            break
        elif server_type == '3':
            clear()
            genz_ip()
            break
        else:
            print('Invalid choice.')  
            
def gen_ipm2():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve \033[92mMethod 2\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharejm2_gen_menu()
            break
        elif server_type == '2':
            iranm2_gen_menu()
            break
        elif server_type == '3':
            clear()
            gen_ip()
            break
        else:
            print('Invalid choice.')    
       
def gen_ipm1():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mGeneve \033[92mMethod 1\033[93m Menu\033[0m')
    print('\033[92m "-"\033[93m══════════════════════════\033[0m')
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose what to do:\033[0m')
    print('1. \033[92mKharej\033[0m')
    print('2. \033[93mIRAN\033[0m')
    print('3. \033[94mback to the previous menu\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            kharejm1_gen_menu()
            break
        elif server_type == '2':
            iranm1_gen_menu()
            break
        elif server_type == '3':
            clear()
            gen_ip()
            break
        else:
            print('Invalid choice.')
        
        
def genkhm1_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.2.1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def genkhm2_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.1.2"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
        
def genirm1_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.1.1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)
def genirm2_ping():
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    try:
        print("\033[96mPlease Wait, Azumi is pinging...")
        subprocess.run(["ping", "-c", "2", "80.200.1.1"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(Fore.LIGHTRED_EX + "Pinging failed:", e, Style.RESET_ALL)   
        
def ping_kh_service():
    service_content = '''[Unit]
Description=keepalive
After=network.target

[Service]
ExecStart=/bin/bash /etc/ping_gen.sh
Restart=always

[Install]
WantedBy=multi-user.target
'''

    service_file_path = '/etc/systemd/system/ping_gen.service'
    with open(service_file_path, 'w') as service_file:
        service_file.write(service_content)

    subprocess.run(['systemctl', 'daemon-reload'])
    subprocess.run(['systemctl', 'enable', 'ping_gen.service'])
    sleep(1)
    subprocess.run(['systemctl', 'restart', 'ping_gen.service'])
    
        
def gen_job():
    file_path = '/etc/gen.sh'

    try:
       
        subprocess.run(
            f"(crontab -l | grep -v '{file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        
        subprocess.run(
            f"(crontab -l ; echo '@reboot /bin/bash {file_path}') | crontab -",
            shell=True,
            capture_output=True,
            text=True
        )

        display_checkmark("\033[92mCronjob added successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("\033[91mFailed to add cronjob:\033[0m", e)
def ufw(ip_address):
    subprocess.run(["sudo", "ufw", "allow", "from", ip_address])
def delufw(ip_address):
    subprocess.run(["sudo", "ufw", "delete", "allow", "from", ip_address])
def ipv4_address():
    result = subprocess.run(["curl", "-s", "https://ipinfo.io/ip"], capture_output=True, text=True)
    return result.stdout.strip() 

def gen_ipvers():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_ipk_version1()
            break
        elif server_type == '2':
            geneve_ipk_version2()
            break
        else:
            print('Invalid choice.')

def geneve_ipk_version1():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.2.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.2.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_ipk_version2():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m") 
    
def kharejm1_gen_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej server \033[92mMethod 1\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mConfiguring Kharej server...\033[0m")

    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    gen_ipvers()

## model 2
def gen_ipvers2():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_ipk1_version1()
            break
        elif server_type == '2':
            geneve_ipk1_version2()
            break
        else:
            print('Invalid choice.')

def geneve_ipk1_version1():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")
    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.1.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.1/30", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.1/30 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.2"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def geneve_ipk1_version2():
    remote_ip = input("\033[93mEnter \033[92mIRAN\033[93m IPV4 address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genkhm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (Kharej):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mIRAN IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mKharej Server Configuration Completed!\033[0m")   
    
def kharejm2_gen_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mKharej server\033[92m Method 2\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mConfiguring Kharej server...\033[0m")

    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")

    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gen_ipvers2()
    
def gen_ipver():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_ip_version1()
            break
        elif server_type == '2':
            geneve_ip_version2()
            break
        else:
            print('Invalid choice.')

def geneve_ip_version1():
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.2.1")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.2.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "route", "add", "80.200.1.1/32", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.2.1/32 dev azumigen\n")
        f.write("sudo ip route add 80.200.1.1/32 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.2.1\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_ip_version2():
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)

    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m") 
    
def iranm1_gen_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIran server\033[92m Method 1\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mConfiguring for Iran server...\033[0m")
    
    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")
    
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    gen_ipver()

def gen1_ipver():
    print("\033[93m╭───────────────────────────────────────╮\033[0m")
    print('\033[93mChoose Geneve IP Version:\033[0m')
    print('1. \033[92mIPV4\033[0m')
    print('2. \033[93mIPV6\033[0m')
    print("\033[93m╰───────────────────────────────────────╯\033[0m")

    while True:
        server_type = input('\033[38;5;205mEnter your choice Please: \033[0m')
        if server_type == '1':
            geneve_ipi_version1()
            break
        elif server_type == '2':
            geneve_ipi_version2()
            break
        else:
            print('Invalid choice.')

def geneve_ipi_version1():
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")
    ufw(remote_ip)
    ufw("80.200.1.1")
    ufw("80.200.1.2")
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", "80.200.1.2/30", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write("sudo ip addr add 80.200.1.2/30 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    genirm1_ping()
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "        80.200.1.2\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    script_content = '''#!/bin/bash
ip_address="80.200.1.1"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{print $2}" | awk -F " " "{print $1}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")   
    
def geneve_ipi_version2():
    remote_ip = input("\033[93mEnter \033[92mKharej\033[93m IPV4 address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))

    ufw(remote_ip)
    
    subprocess.run(["sudo", "ip", "link", "add", "name", "azumigen", "type", "geneve", "id", "1000", "remote", remote_ip], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "link", "set", "azumigen", "up"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "ip", "addr", "add", prefix+"/16", "dev", "azumigen"], stdout=subprocess.DEVNULL)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_notification("\033[93mAdding commands...\033[0m")
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")

    with open("/etc/gen.sh", "w") as f:
        f.write(f"sudo ip link add name azumigen type geneve id 1000 remote {remote_ip}\n")
        f.write("sudo ip link set azumigen up\n")
        f.write(f"sudo ip addr add {prefix}/16 dev azumigen\n")

    set_mtu = input("\033[93mDo you want to set the \033[92mMTU\033[96m [Geneve]\033[93m? (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m")

    if set_mtu.lower() == "yes" or set_mtu.lower() == "y":
        mtu_value = input("\033[93mEnter the desired\033[92m MTU value\033[93m: \033[0m")
        mtu_command = f"ip link set dev azumigen mtu {mtu_value}\n"
        with open("/etc/gen.sh", "a") as f:
            f.write(mtu_command)
        subprocess.run(mtu_command, shell=True, check=True)

    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    display_checkmark("\033[92mConfiguration is done!\033[0m")

    gen_job()

    time.sleep(1)
    display_checkmark("\033[92mkeepalive service Configured!\033[0m")

    
    time.sleep(1)
    print("\033[93m─────────────────────────────────────────────────────────\033[0m")
    print("\033[93mCreated IP Addresses (IRAN):\033[0m")
    print("\033[92m" + "+---------------------------+" + "\033[0m")
    print("\033[92m" + "     {}\033[0m".format(prefix))
    print("\033[92m" + "+---------------------------+" + "\033[0m")

    remote_ipv4 = input("\033[93mEnter \033[92mKharej IPv4\033[93m address [Ping Service]: \033[0m")

    remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
    ufw(remote_prefix)
    
    script_content = '''#!/bin/bash
ip_address="{remote_prefix}"
max_pings=3
interval=20
while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done
    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''.format(remote_prefix=remote_prefix)

    with open('/etc/ping_gen.sh', 'w') as script_file:
        script_file.write(script_content)

    os.chmod('/etc/ping_gen.sh', 0o755)
    ping_kh_service()
    ufwr()
    print("\033[92mIRAN Server Configuration Completed!\033[0m")
    
def iranm2_gen_menu():
    os.system("clear")
    print('\033[92m ^ ^\033[0m')
    print('\033[92m(\033[91mO,O\033[92m)\033[0m')
    print('\033[92m(   ) \033[93mIran server\033[92m Method 2\033[0m')
    print('\033[92m "-"\033[93m═══════════════════════════\033[0m')
    display_notification("\033[93mConfiguring for Iran server...\033[0m")
    
    if os.path.isfile("/etc/gen.sh"):
        os.remove("/etc/gen.sh")
    
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    gen1_ipver()
	
def i6to41_any_iran():
    clear_screen()
    print("\033[92m ^ ^\033[0m")
    print("\033[92m(\033[91mO,O\033[92m)\033[0m")
    print("\033[92m(   ) \033[93m6to4 \033[92mIRAN\033[93m  Menu\033[92m[Anycast]\033[0m")
    print('\033[92m "-"\033[93m════════════════════════════\033[0m') 


    if subprocess.run(['test', '-f', '/etc/6to4.sh'], capture_output=True).returncode == 0:
        subprocess.run(['rm', '/etc/6to4.sh'])
        
    display_notification("\033[93mConfiguring...\033[0m")
    local_ipv4 = server_ipv4()
    if local_ipv4 is None:
        return
    sleep(1)    
    print("\033[93m╭─────────────────────────────────────────────────────────╮\033[0m")
    local_ip = input("\033[93mEnter \033[92mIran IPv4\033[93m address: \033[0m")

    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()

    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    
    ipv6_address = f'ipv4="{local_ipv4}"; printf "2002:%02x%02x:%02x%02x::1" `echo $ipv4 | tr "." " "`'
    ipv6_process = subprocess.run(ipv6_address, shell=True, capture_output=True, text=True)
    if ipv6_process.returncode != 0:
        print("Error generating IPv6 address.")
        return
    
    ipv6 = ipv6_process.stdout.strip()
    print("\033[93m│\033[0m \033[92mGenerated IPv6 address:\033[0m", ipv6, "\033[93m│\033[0m")

    with open('/etc/6to4.sh', 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("/sbin/modprobe sit\n")
        f.write("/sbin/ip tunnel add azumi6 mode sit remote any local {} ttl 255\n".format(local_ip))
        set_mtu = input('\033[93mDo you want to set \033[92m MTU?\033[93m (\033[92myes\033[93m/\033[91mno\033[93m): \033[0m')
        if set_mtu.lower() == 'yes' or set_mtu.lower() == 'y':
            mtu_value = input('\033[93mEnter the desired \033[92mMTU value\033[93m: \033[0m')
            f.write("/sbin/ip -6 link set dev azumi6 mtu {}\n".format(mtu_value))
        else:
            f.write("/sbin/ip -6 link set dev azumi6 mtu 1480\n")
        f.write("/sbin/ip link set dev azumi6 up\n")
        f.write("/sbin/ip -6 addr add {}/16 dev azumi6\n".format(prefix))
        f.write("/sbin/ip -6 route add 2000::/3 via ::192.88.99.1 dev azumi6 metric 1\n")
        answer = input("\033[93mDo you want to change the \033[92mdefault route\033[93m? (\033[92my\033[93m/\033[91mn\033[93m)\033[0m ")
        if answer.lower() in ['yes', 'y']:
            interface = ipv6_int()
            if interface is None:
               print("Error: No network interface with IPv6 address.")
            else:
               print("Interface:", interface)
               f.write("ip -6 route replace default via fe80::1 dev {} src {}\n".format(interface, prefix))
        else:
            print("Skipping changing the default route.")

    num_ips = int(input("\033[93mHow many \033[92madditional IPs\033[93m do you need? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    start_index = 3

    with open('/etc/6to4.sh', 'a') as f:
        for i in range(start_index, start_index + num_ips):
            ip_addr = "2002:{:02x}{:02x}:{:02x}{:02x}::{:02x}/16".format(*map(int, ipv4.split('.')), i)
            f.write("ip -6 addr add {} dev azumi6\n".format(ip_addr))

    display_notification("\033[93mAdding cronjob!\033[0m")

    config_file_path = '/etc/6to4.sh'


    subprocess.run(f"(crontab -l | grep -v -F '{config_file_path}') | crontab -", shell=True, check=True)


    cronjob_command = f"(crontab -l 2>/dev/null; echo '@reboot sh {config_file_path}') | crontab -"
    subprocess.run(cronjob_command, shell=True, check=True)

    display_notification("\033[93mStarting 6to4...\033[0m")
    subprocess.run(['/bin/bash', '/etc/6to4.sh'])

    num_servers = int(input("\033[93mEnter the \033[92mnumber\033[93m of \033[96mServers\033[93m[Ping Service]? \033[0m"))
    print("\033[93m╰─────────────────────────────────────────────────────────╯\033[0m")

    for i in range(num_servers):
        remote_ipv4 = input(f"\033[93mEnter \033[96mIPv4 address\033[93m of server \033[92m{i+1} [Ping Service]: \033[0m")
    
        remote_prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, remote_ipv4.split('.')))
        sleep(1)
        print('\033[92m(\033[96mPlease wait,Azumi is pinging...\033[0m')
        ping_result = subprocess.run(['ping6', '-c', '2', remote_prefix], capture_output=True, text=True).stdout.strip()
        print(ping_result)

        script_content = '''#!/bin/bash

ip_address="{}"

max_pings=3

interval=20

while true
do
    for ((i = 1; i <= max_pings; i++))
    do
        ping_result=$(ping -c 1 $ip_address | grep "time=" | awk -F "time=" "{{print $2}}" | awk -F " " "{{print $1}}" | cut -d "." -f1)
       
        if [ -n "$ping_result" ]; then
            echo "Ping successful! Response time: $ping_result ms"
        else
            echo "Ping failed!"
        fi
    done

    echo "Waiting for $interval seconds..."
    sleep $interval
done
'''

        script_filename = f'/etc/ping_v6{i+1}.sh'
        with open(script_filename, 'w') as f:
            f.write(script_content)

        subprocess.run(['chmod', '+x', script_filename])

        service_filename = f'/etc/systemd/system/ping_v6{i+1}.service'
        with open(service_filename, 'w') as f:
            f.write('[Unit]\n')
            f.write(f'Description=Ping Service {i+1}\n')
            f.write('After=network.target\n')
            f.write('\n')
            f.write('[Service]\n')
            f.write(f'ExecStart=/bin/bash {script_filename}\n')
            f.write('Restart=always\n')
            f.write('\n')
            f.write('[Install]\n')
            f.write('WantedBy=multi-user.target\n')

        subprocess.run(['systemctl', 'daemon-reload'])
        subprocess.run(['systemctl', 'enable', f'ping_v6{i+1}.service'])
        subprocess.run(['systemctl', 'start', f'ping_v6{i+1}.service'])
        sleep(1)
        subprocess.run(["systemctl", "restart", f"ping_v6{i+1}.service"])

        print(f"\033[92mPing service for server {i+1} has been added successfully!\033[0m")

    display_checkmark("\033[92m6to4 Service has been added successfully!\033[0m")	
	
def remove_6to4():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92m6TO4\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/6to4.sh", shell=True) == 0:
            subprocess.run("rm /etc/6to4.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot sh /etc/6to4.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        time.sleep(1)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumi6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi6 > /dev/null", shell=True)

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
        
def remove_6to41():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92m6TO4\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/6to4.sh", shell=True) == 0:
            subprocess.run("rm /etc/6to4.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot sh /etc/6to4.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        time.sleep(1)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v61.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v62.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v63.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v64.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl disable ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v65.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v65.service > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumi6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi6 > /dev/null", shell=True)

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
        
def remove_gre():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot sh /etc/gre.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)
        time.sleep(1)

        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        time.sleep(1)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("ip link set dev azumig down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig > /dev/null", shell=True)


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
		
def remove_gre6():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre6.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre6.sh", shell=True)
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre6.sh\" | crontab -", shell=True)
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        time.sleep(1)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)

        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        sleep(1)
        subprocess.run("ip link set dev azumig6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig6 > /dev/null", shell=True)

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

def remove_gre621():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving \033[92mGRE6\033[93m Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        if subprocess.call("test -f /etc/gre6.sh", shell=True) == 0:
            subprocess.run("rm /etc/gre6.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gre6.sh\" | crontab -", shell=True)
        subprocess.run("sudo rm /etc/ping_ip.sh", shell=True)
        subprocess.run("systemctl disable ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_ip.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_ip.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumig6 down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumig6 > /dev/null", shell=True)

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
		
def remove_private():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving private IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    
    try:
        if subprocess.call("test -f /etc/private.sh", shell=True) == 0:
            subprocess.run("rm /etc/private.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/private.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_v6.sh", shell=True)
        
        time.sleep(1)
        subprocess.run("systemctl disable ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_v6.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_v6.service > /dev/null 2>&1", shell=True)
        time.sleep(1)
        
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("ip link set dev azumi down > /dev/null", shell=True)
        subprocess.run("ip tunnel del azumi > /dev/null", shell=True)
        
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
def prefix_ip_gen():
    gen_path = "/etc/ping_gen.sh"

    if not os.path.isfile(gen_path):
        return None

    with open(gen_path, "r") as ping_gen_sh:
        for line in ping_gen_sh:
            if "ip_address" in line:
                ip_address = line.split("=")[-1].strip().strip('"')
                return ip_address

    return None
    
    return None        
def remote_ip_gen():
    gen_path = "/etc/gen.sh"
    
    if not os.path.isfile(gen_path):
        return None
    
    with open(gen_path, "r") as gen_sh:
        for line in gen_sh:
            if "remote" in line:
                remote_ip = line.split()[-1].strip('"')
                return remote_ip
    
    return None
def genz_uninstall():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    delufw(prefix)
    remote_ip = remote_ip_gen()

    if remote_ip is None:
        print("Unable to retrieve remote IP")
    else:
        delufw(remote_ip)

    remote2_ip = prefix_ip_gen()

    if remote2_ip is None:
        print("Unable to retrieve prefix")
    else:
        delufw(remote2_ip)

    delufw("80.200.1.1")
    delufw("80.200.1.2")
    delufw("80.200.2.1")
    ufwr()

    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)

        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)

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
        
def gen_uninstall():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    delufw(prefix)
    remote_ip = remote_ip_gen()

    if remote_ip is None:
        print("Unable to retrieve remote IP")
    else:
        delufw(remote_ip)

    remote2_ip = prefix_ip_gen()

    if remote2_ip is None:
        print("Unable to retrieve prefix")
    else:
        delufw(remote2_ip)

    delufw("80.200.1.1")
    delufw("80.200.1.2")
    delufw("80.200.2.1")
    ufwr()

    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)

        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)

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

def gen4_uninstall():
    remove_private()
    remove_gre621()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve + \033[92mGRE6 + IP6tnl \033[93m+ \033[96mTunnel\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    delufw(prefix)
    remote_ip = remote_ip_gen()

    if remote_ip is None:
        print("Unable to retrieve remote IP")
    else:
        delufw(remote_ip)

    remote2_ip = prefix_ip_gen()

    if remote2_ip is None:
        print("Unable to retrieve prefix")
    else:
        delufw(remote2_ip)

    delufw("80.200.1.1")
    delufw("80.200.2.1")
    delufw("2002:831a::1")
    delufw("2002:831a::2")
    delufw("2001:831b::2")
    delufw("2001:831b::1")
    ufwr()

    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)

        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)

        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)

        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)

        subprocess.run("systemctl daemon-reload", shell=True)

        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)

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
        
def gen2_uninstall():
    remove_gre621()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve + \033[92mGRE6 \033[93m+ \033[96mNATIVE Tunnel\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    delufw(prefix)
    remote_ip = remote_ip_gen()
    
    if remote_ip is None:
        print("Unable to retrieve remote IP")
    else:
        delufw(remote_ip)
        prefix = prefix_ip_gen()
        
        if prefix is None:
            print("Unable to retrieve prefix")
        else:
            delufw(prefix)
            delufw("80.200.1.1")
            delufw("80.200.2.1")
            delufw("2002:831a::1")
            delufw("2002:831a::2")
            ufwr()
    
    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)
        
        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)
  
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)
        
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

def gen6_uninstall():
    remove_private()
    remove_gre6()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve + \033[92mGRE6 \033[93m+ \033[96mIPV4\033[93m Tunnel\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    delufw("80.200.1.1")
    delufw("80.200.2.1")
    delufw("2002:831a::1")
    delufw("2002:831a::2")
    delufw("2001:831b::1")
    delufw("2001:831b::2")
    ipv4 = subprocess.run(['curl', '-s', 'https://api.ipify.org'], capture_output=True, text=True).stdout.strip()
    prefix = "2002:{:02x}{:02x}:{:02x}{:02x}::1".format(*map(int, ipv4.split('.')))
    delufw(prefix)
    remote_ip = remote_ip_gen()
    
    if remote_ip is None:
        print("Unable to retrieve remote IP")
    else:
        delufw(remote_ip)
        prefix = prefix_ip_gen()
        
        if prefix is None:
            print("Unable to retrieve prefix")
        else:
            delufw(prefix)
            ufwr()
    
    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)
        
        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)
  
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)
        
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
        
def gen3_uninstall():
    remove_gre6()
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve + \033[92mGRE6 \033[93m+ \033[96mNative\033[93m Tunnel\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    delufw("80.200.1.1")
    delufw("80.200.2.1")
    delufw("2002:831a::1")
    delufw("2002:831a::2")
    ufwr()
    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)

            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)
        
        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)
  
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)
        
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
        
def gen_icmp():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Geneve + ICMP Tunnel...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")
    remove_icmp()


    subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/icmp.sh\" | crontab -", shell=True)

    remote2_ip = prefix_ip_gen()
    
    if remote2_ip is None:
        print("Unable to retrieve prefix")
        return
    delufw(remote2_ip)
    delufw("80.200.1.1")
    delufw("80.200.2.1")
    delufw("70.0.0.1")
    delufw("70.0.0.2")
    ufwr()
    try:
        if subprocess.call("test -f /etc/gen.sh", shell=True) == 0:
            subprocess.run("rm /etc/gen.sh", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/gen.sh\" | crontab -", shell=True)
        
        subprocess.run("sudo rm /etc/ping_gen.sh", shell=True)
        
        subprocess.run("systemctl disable ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("systemctl stop ping_gen.service > /dev/null 2>&1", shell=True)
        subprocess.run("rm /etc/systemd/system/ping_gen.service > /dev/null 2>&1", shell=True)
  
        subprocess.run("systemctl daemon-reload", shell=True)
        
        subprocess.run("sudo ip link delete azumigen > /dev/null", shell=True)
        
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
def extra_uninstall():
    os.system("clear")
    print("\033[93m───────────────────────────────────────\033[0m")
    display_notification("\033[93mRemoving Extra IP addresses...\033[0m")
    print("\033[93m───────────────────────────────────────\033[0m")

    try:
        interface = subprocess.check_output("ip route | awk '/default/ {print $5; exit}'", shell=True).decode().strip()
        addresses = subprocess.check_output(f"ip addr show dev {interface} | awk '/inet6 .* global/ {{print $2}}'", shell=True).decode().splitlines()

        for address in addresses:
            subprocess.run(f"ip addr del {address} dev {interface}", shell=True)
            
        display_notification("\033[93mRemoving cronjob...\033[0m")
        subprocess.run("crontab -l | grep -v \"@reboot /bin/bash /etc/ipv6.sh\" | crontab -", shell=True)    

        sleep(1)
        subprocess.run("sudo rm /etc/ipv6.sh", shell=True)
        
        display_notification("\033[93mRemoving Extra ip, Working in the background..\033[0m")
        print("Progress: ", end="")

        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        delay = 0.1
        duration = 3 
        end_time = time.time() + duration

        while time.time() < end_time:
            for frame in frames:
                print("\r[%s] Loading...  " % frame, end="")
                time.sleep(delay)
                print("\r[%s]             " % frame, end="")
                time.sleep(delay)

        display_checkmark("\033[92mExtra IP addresses removed successfully!\033[0m")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output.decode().strip())
    
main_menu()
