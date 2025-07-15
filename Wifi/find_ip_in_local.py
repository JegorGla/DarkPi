from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
import socket
import nmap
import requests
import threading
import time
import re
import subprocess
import customtkinter as ctk
import netifaces
import json


def get_local_subnet():
    for iface in netifaces.interfaces():
        try:
            addrs = netifaces.ifaddresses(iface)
            ip_info = addrs[netifaces.AF_INET][0]
            ip = ip_info['addr']
            netmask = ip_info['netmask']
            cidr = sum([bin(int(x)).count('1') for x in netmask.split('.')])
            return f"{ip}/{cidr}"
        except (KeyError, IndexError):
            continue
    return "192.168.1.0/24"  # запасной вариант

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def arp_scan(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    answered, _ = srp(packet, timeout=2, verbose=0)

    results = []
    for sent, received in answered:
        results.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })
    return results

def probe_http(ip):
    try:
        r = requests.get(f"http://{ip}", timeout=2)
        server = r.headers.get('Server', 'Unknown')
        title_match = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        title = title_match.group(1) if title_match else 'N/A'
        return server, title
    except:
        return "No response", "N/A"

def smb_info(ip):
    try:
        output = subprocess.check_output(
            ['nmap', '-p445', '--script', 'smb-os-discovery,smb-enum-shares', ip],
            stderr=subprocess.DEVNULL,
            timeout=10
        ).decode()
        shares = re.findall(r'\|\s+(\S+)\s+\(.*?\)', output)
        user_match = re.search(r'OS:\s+(.*)', output)
        user_info = user_match.group(1) if user_match else "N/A"
        return ', '.join(shares) if shares else "Нет", user_info
    except:
        return "Нет", "N/A"

def enrich_device_info(devices):
    mac_lookup = MacLookup()
    nm = nmap.PortScanner()

    for device in devices:
        ip = device['ip']
        mac = device['mac']

        # Имя устройства
        device['hostname'] = get_hostname(ip)

        # Производитель MAC
        try:
            device['vendor'] = mac_lookup.lookup(mac)
        except:
            device['vendor'] = "Unknown"

        # Nmap скан
        try:
            nm.scan(ip, arguments='-O -p 1-1024')
            host_info = nm[ip]
            device['status'] = host_info.state()

            # ОС
            if 'osmatch' in host_info and host_info['osmatch']:
                device['os'] = host_info['osmatch'][0]['name']
                device['os_accuracy'] = host_info['osmatch'][0]['accuracy']
            else:
                device['os'] = "Unknown"
                device['os_accuracy'] = "N/A"

            # Порты
            ports_info = []
            if 'tcp' in host_info:
                for port, port_data in host_info['tcp'].items():
                    ports_info.append(f"{port}/{port_data['name']} ({port_data['state']})")
            device['ports'] = ports_info

        except Exception:
            device['status'] = "error"
            device['os'] = "Unknown"
            device['os_accuracy'] = "N/A"
            device['ports'] = []

        # HTTP Server & Title
        server, title = probe_http(ip)
        device['http_server'] = server
        device['http_title'] = title

        # SMB Info
        shares, user_info = smb_info(ip)
        device['smb_shares'] = shares
        device['smb_userinfo'] = user_info

    return devices

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def find_ip_in_local_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    label_title = ctk.CTkLabel(parent_frame, text="Find IP in Local", font=("Arial", 24))
    label_title.pack(pady=10)

    text_box = ctk.CTkTextbox(parent_frame, width=600, height=300, font=("Arial", 14), state="disabled")
    text_box.pack(pady=10)

    def append_text(text):
        # Метод для безопасного обновления text_box из другого потока
        text_box.after(0, lambda: text_box.insert("end", text))
        text_box.after(0, lambda: text_box.see("end"))  # автопрокрутка вниз

    def scan_and_update():
        subnet = get_local_subnet()
        append_text(f"[+] Скан сети: {subnet}\n\n")
        start = time.time()

        devices = arp_scan(subnet)
        full_info = enrich_device_info(devices)

        append_text(f"Найдено устройств: {len(full_info)}\n\n")
        for dev in full_info:
            append_text(f"IP         : {dev['ip']}\n")
            append_text(f"MAC        : {dev['mac']}\n")
            append_text(f"Hostname   : {dev['hostname']}\n")
            append_text(f"Vendor     : {dev['vendor']}\n")
            append_text(f"Status     : {dev.get('status', '-')}\n")
            append_text(f"OS         : {dev.get('os')} (accuracy: {dev.get('os_accuracy')}%)\n")
            append_text(f"HTTP       : {dev['http_server']} | Title: {dev['http_title']}\n")
            append_text(f"SMB User   : {dev['smb_userinfo']}\n")
            append_text(f"SMB Shares : {dev['smb_shares']}\n")
            append_text("Ports      :\n")
            for p in dev.get('ports', []):
                append_text(f"   - {p}\n")
            append_text("-" * 50 + "\n\n")

        append_text(f"\nВремя выполнения: {round(time.time() - start, 2)} секунд\n")

    def on_search():
        text_box.delete("0.0", "end")
        # Запускаем сканирование в отдельном потоке
        thread = threading.Thread(target=scan_and_update, daemon=True)
        thread.start()

    # Кнопка поиска
    button_search = ctk.CTkButton(parent_frame, text="Search", font=("Arial", 16), command=on_search)
    button_search.pack(pady=10)

    button_back = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback, font=("Arial", 16))
    button_back.pack(pady=10)