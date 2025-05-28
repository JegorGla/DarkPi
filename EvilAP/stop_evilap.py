import os

os.system("killall hostapd dnsmasq python3")
os.system("iptables -F")
os.system("systemctl start NetworkManager")
print("[+] EvilAP остановлен.")