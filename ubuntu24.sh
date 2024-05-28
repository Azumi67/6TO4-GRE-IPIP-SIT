#!/bin/bash
apt update -y
apt install wget -y
wget -O /etc/logo.sh https://github.com/Azumi67/UDP2RAW_FEC/raw/main/logo.sh
chmod +x /etc/logo.sh
wget https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/test/ubuntu24.py
python3 ubuntu24.py
