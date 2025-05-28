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

def start_auto_update(temp_label, cpu_label, ram_label, internet_label, interval_ms=1):
    update_info(temp_label, cpu_label, ram_label, internet_label)
    temp_label.after(interval_ms, lambda: start_auto_update(temp_label, cpu_label, ram_label, internet_label, interval_ms))


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

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except:
        return False

def auto_reconnect():
    os.system("sudo ifconfig wlan0 down")
    os.system("sudo ifconfig wlan0 up")

def update_info(temp_label, cpu_label, ram_label, internet_label):
    temp_label.configure(text="Температура: " + get_temp())
    cpu_label.configure(text="CPU: " + get_cpu())
    ram_label.configure(text="RAM: " + get_ram())
    conn_status = "Интернет: Да" if is_connected() else "Интернет: Нет"
    internet_label.configure(text=conn_status)

def reconnect_wifi(temp_label, cpu_label, ram_label, internet_label):
    auto_reconnect()
    update_info(temp_label, cpu_label, ram_label, internet_label)

def pi_helper_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Состояние системы", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=(20, 10))

    # Фрейм для информации
    info_frame = ctk.CTkFrame(parent_frame)
    info_frame.pack(pady=10, padx=20, fill="both", expand=False)

    temp_label = ctk.CTkLabel(info_frame, text="Температура:", font=ctk.CTkFont(size=16))
    temp_label.pack(anchor="w", pady=2, padx=10)

    cpu_label = ctk.CTkLabel(info_frame, text="CPU:", font=ctk.CTkFont(size=16))
    cpu_label.pack(anchor="w", pady=2, padx=10)

    ram_label = ctk.CTkLabel(info_frame, text="RAM:", font=ctk.CTkFont(size=16))
    ram_label.pack(anchor="w", pady=2, padx=10)

    internet_label = ctk.CTkLabel(info_frame, text="Интернет:", font=ctk.CTkFont(size=16))
    internet_label.pack(anchor="w", pady=2, padx=10)

    # Кнопки действий
    button_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    button_frame.pack(pady=10)

    reconnect_btn = ctk.CTkButton(
        button_frame,
        text="🔄 Переподключить WiFi",
        font=ctk.CTkFont(size=14),
        command=partial(reconnect_wifi, temp_label, cpu_label, ram_label, internet_label)
    )
    reconnect_btn.pack(pady=5)

    # Назад (если передан коллбэк)
    if go_back_callback:
        back_btn = ctk.CTkButton(
            parent_frame,
            text="← Назад",
            font=ctk.CTkFont(size=14),
            command=go_back_callback
        )
        back_btn.pack(pady=(10, 20))

    # Запускаем автообновление
    update_info(temp_label, cpu_label, ram_label, internet_label)
    start_auto_update(temp_label, cpu_label, ram_label, internet_label, interval_ms=1000)
