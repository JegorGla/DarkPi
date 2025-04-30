import customtkinter as ctk
import psutil
import netifaces
import subprocess
import socket
import os
from functools import partial

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_temp():
    try:
        output = subprocess.check_output("vcgencmd measure_temp", shell=True).decode()
        return output.strip().replace("temp=", "")
    except:
        return "N/A"

def get_cpu():
    return f"{psutil.cpu_percent()}%"

def get_ram():
    return f"{psutil.virtual_memory().percent}%"

def get_ip():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != "lo":
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    return addrs[netifaces.AF_INET][0]['addr']
        return "Нет IP"
    except:
        return "Ошибка"

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def auto_reconnect():
    os.system("sudo ifconfig wlan0 down")
    os.system("sudo ifconfig wlan0 up")

def update_info(temp_label, cpu_label, ram_label, ip_label, internet_label):
    temp_label.configure(text="Температура: " + get_temp())
    cpu_label.configure(text="CPU: " + get_cpu())
    ram_label.configure(text="RAM: " + get_ram())
    ip_label.configure(text="IP: " + get_ip())
    conn_status = "Интернет: Да" if is_connected() else "Интернет: Нет"
    internet_label.configure(text=conn_status)

def reconnect_wifi(temp_label, cpu_label, ram_label, ip_label, internet_label):
    auto_reconnect()
    update_info(temp_label, cpu_label, ram_label, ip_label, internet_label)

def pi_helper_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="Состояние системы", font=("Arial", 20))
    title.pack(pady=10)

    temp_label = ctk.CTkLabel(parent_frame, text="")
    temp_label.pack()

    cpu_label = ctk.CTkLabel(parent_frame, text="")
    cpu_label.pack()

    ram_label = ctk.CTkLabel(parent_frame, text="")
    ram_label.pack()

    ip_label = ctk.CTkLabel(parent_frame, text="")
    ip_label.pack()

    internet_label = ctk.CTkLabel(parent_frame, text="")
    internet_label.pack()

    # Привязываем данные к кнопкам
    refresh_btn = ctk.CTkButton(
        parent_frame,
        text="Обновить",
        command=partial(update_info, temp_label, cpu_label, ram_label, ip_label, internet_label)
    )
    refresh_btn.pack(pady=10)

    reconnect_btn = ctk.CTkButton(
        parent_frame,
        text="Переподключить WiFi",
        command=partial(reconnect_wifi, temp_label, cpu_label, ram_label, ip_label, internet_label)
    )
    reconnect_btn.pack()

    # Первичная инициализация данных
    update_info(temp_label, cpu_label, ram_label, ip_label, internet_label)

    # Кнопка Назад (если нужно)
    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="Назад", command=go_back_callback)
        back_btn.pack(pady=10)
