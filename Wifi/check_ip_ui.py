import requests
import json
import customtkinter as ctk
import os
import platform

from loading_screen import show_loading_screen  # Импортируем функцию загрузки

def detect_os():
    """Определяет операционную систему."""
    system = platform.system()

    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "MacOS"
    elif system == "Linux":
        # Теперь уточняем дистрибутив Linux
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "raspbian" in content or "raspberry" in content:
                    return "Raspberry Pi OS"
                elif "ubuntu" in content:
                    return "Ubuntu"
                elif "debian" in content:
                    return "Debian"
                elif "arch" in content:
                    return "Arch Linux"
                elif "fedora" in content:
                    return "Fedora"
                else:
                    return "Other Linux"
        else:
            return "Linux (Unknown)"
    else:
        return "Unknown OS"
    
def get_local_ip():
    """Получает локальный IP-адрес."""
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        return f"Error: {e}"

def clear_frame(frame):
    """Очистка фрейма от всех виджетов."""
    for widget in frame.winfo_children():
        widget.destroy()

def check_ip_ui(parent_frame, go_back_callback=None):
    """Отображение информации о текущем IP-адресе."""
    clear_frame(parent_frame)

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Check IP", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    def fetch_ip():
        """Функция загрузки IP через прокси."""
        proxy = load_current_proxy()
        if not proxy:
            return "Прокси не найден в settings.json"

        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

        try:
            response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
            ip_info = response.json()
            return ip_info.get("ip", "Unknown IP")
        except requests.RequestException as e:
            return f"Error через прокси: {e}"


    def on_ip_loaded(ip_address):
        """Отображение IP после загрузки."""
        clear_frame(parent_frame)

        title = ctk.CTkLabel(parent_frame, text="Check IP", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        ip_label = ctk.CTkLabel(parent_frame, text=f"Current public IP: {ip_address}", font=("Arial", 16))
        ip_label.place(relx=0.5, rely=0.3, anchor="center")

        ip_local_label = ctk.CTkLabel(parent_frame, text=f"Local IP: {get_local_ip()}", font=("Arial", 16))
        ip_local_label.place(relx=0.5, rely=0.4, anchor="center")

        back_btn = ctk.CTkButton(
            parent_frame,
            text="← Back",
            command=lambda: go_back_callback() if go_back_callback else None,
            font=("Arial", 16)
        )
        back_btn.place(relx=0.5, rely=0.9, anchor="center")

    # Показать экран загрузки
    show_loading_screen(parent_frame, message="Loading IP...", fetch_function=fetch_ip, callback=on_ip_loaded)
    current_os = detect_os()

    def load_current_proxy():
        """Загружает текущий прокси из settings.json."""
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get("current_proxy")
        except (FileNotFoundError, json.JSONDecodeError):
            return None
