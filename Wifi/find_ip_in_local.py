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
import os

def set_allowed_anim(value: bool):
    try:
        settings = {}

        # Если файл существует, загрузить его содержимое
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)

        # Обновляем или добавляем ключ
        settings["allowed_anim"] = value

        # Записываем обратно обновлённый словарь
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    except Exception as e:
        print("Ошибка при записи файла:", e)


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

def enrich_device_info(devices, log_callback=None):
    mac_lookup = MacLookup()
    nm = nmap.PortScanner()

    for i, device in enumerate(devices, 1):
        ip = device['ip']
        mac = device['mac']
        if log_callback:
            log_callback(f"[{i}/{len(devices)}] Обработка IP: {ip}...\n")

        # Hostname
        device['hostname'] = get_hostname(ip)
        if log_callback:
            log_callback(f" → Hostname получен\n")

        # MAC Vendor
        try:
            device['vendor'] = mac_lookup.lookup(mac)
        except:
            device['vendor'] = "Unknown"
        if log_callback:
            log_callback(f" → MAC-вендор получен\n")

        # Nmap
        try:
            log_callback(f" → Запуск Nmap...\n")
            nm.scan(ip, arguments='-O -p 1-1024')
            host_info = nm[ip]
            device['status'] = host_info.state()

            if 'osmatch' in host_info and host_info['osmatch']:
                device['os'] = host_info['osmatch'][0]['name']
                device['os_accuracy'] = host_info['osmatch'][0]['accuracy']
            else:
                device['os'] = "Unknown"
                device['os_accuracy'] = "N/A"

            ports_info = []
            if 'tcp' in host_info:
                for port, port_data in host_info['tcp'].items():
                    ports_info.append(f"{port}/{port_data['name']} ({port_data['state']})")
            device['ports'] = ports_info
        except:
            device['status'] = "error"
            device['os'] = "Unknown"
            device['os_accuracy'] = "N/A"
            device['ports'] = []
            log_callback(f" × Ошибка при Nmap\n")

        # HTTP
        server, title = probe_http(ip)
        device['http_server'] = server
        device['http_title'] = title
        log_callback(f" → HTTP проверен\n")

        # SMB
        shares, user_info = smb_info(ip)
        device['smb_shares'] = shares
        device['smb_userinfo'] = user_info
        log_callback(f" → SMB проверен\n")

    return devices

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def find_ip_in_local_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    label_title = ctk.CTkLabel(parent_frame, text="Find IP in Local", font=("Arial", 24))
    label_title.pack(pady=10)

    text_box = ctk.CTkTextbox(parent_frame, width=600, height=300, font=("Arial", 14))
    text_box.pack(pady=10)

    def append_text(text):
        if not text.endswith('\n'):
            text += '\n'
        text_box.after(0, lambda: text_box.insert("end", text))
        text_box.after(0, lambda: text_box.see("end"))

    def scan_and_update():
        subnet = get_local_subnet()
        append_text(f"[+] Начинаем сканирование сети: {subnet}\n")
        start = time.time()

        devices = arp_scan(subnet)
        append_text(f"[+] Найдено устройств: {len(devices)}\n")
        append_text("[*] Начинаю сбор данных...\n")

        full_info = enrich_device_info(devices, log_callback=append_text)

        duration = round(time.time() - start, 2)
        append_text(f"[✓] Сканирование завершено за {duration} сек.\n")
        append_text(f"[✓] Вывод полной информации:\n")

        for dev in full_info:
            append_text(f"📍 Устройство: {dev['ip']}\n")
            append_text(f"   ├ MAC       : {dev['mac']}\n")
            append_text(f"   ├ Hostname  : {dev['hostname']}\n")
            append_text(f"   ├ Vendor    : {dev['vendor']}\n")
            append_text(f"   ├ Status    : {dev.get('status', '-')}\n")
            append_text(f"   ├ OS        : {dev.get('os')} (точность: {dev.get('os_accuracy')}%)\n")
            append_text(f"   ├ HTTP      : {dev['http_server']} | Title: {dev['http_title']}\n")
            append_text(f"   ├ SMB User  : {dev['smb_userinfo']}\n")
            append_text(f"   ├ SMB Shares: {dev['smb_shares']}\n")
            append_text(f"   └ Ports     :\n")  # <-- добавлен перенос строки здесь
            for p in dev.get('ports', []):
                append_text(f"       - {p}\n")
            append_text("-" * 60 + "\n")



    def on_search():
        set_allowed_anim(False)
        print("Starting")
        text_box.delete("0.0", "end")
        text_box.insert("0.0", "Scanning network...\n")
        # Запускаем сканирование в отдельном потоке
        thread = threading.Thread(target=scan_and_update, daemon=True)
        thread.start()

    # Кнопка поиска
    buttons_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    buttons_frame.pack(pady=10)

    button_search = ctk.CTkButton(buttons_frame, text="Search", font=("Arial", 16), command=on_search)
    button_search.pack(side="left", padx=10)  # расстояние между кнопками

    button_back = ctk.CTkButton(buttons_frame, text="← Back", command=go_back_callback, font=("Arial", 16))
    button_back.pack(side="left", padx=10)
