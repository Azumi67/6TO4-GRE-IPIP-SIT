#!/bin/bash
apt update -y
apt install wget -y
wget -O /etc/logo.sh https://github.com/Azumi67/UDP2RAW_FEC/raw/main/logo.sh
chmod +x /etc/logo.sh
if [ -f "ubuntu24p2.py" ]; then
    rm ubuntu24p2.py
fi
wget https://github.com/Azumi67/6TO4-GRE-IPIP-SIT/releases/download/ubuntu24/ubuntu24p2.py
python3 ubuntu24p2.py
