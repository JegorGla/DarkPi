import requests
import json
import customtkinter as ctk
import os
import platform
import random

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

def proxy_from_settings():
    global current_proxy
    """Загружает прокси из settings.json."""
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            current_proxy = settings.get("current_proxy")
    except (FileNotFoundError, json.JSONDecodeError):
        return None

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

    def load_current_proxy():
        """Загружает текущий прокси из settings.json."""
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                return settings.get("current_proxy")
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        
    def fetch_ip_info(ip, proxies=None):
        """Получает подробную информацию по IP через ip-api.com."""
        try:
            url = f"https://ipinfo.io/{ip}"
            print(ip)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "fail", "message": str(e)}


    def fetch_ip(retry=3):
        if retry <= 0:
            return {"error": "Не удалось получить IP после нескольких попыток", "proxy_worked": False}

        proxy = load_current_proxy()
        if not proxy:
            return {"error": "Прокси не найден в settings.json", "proxy_worked": False}

        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

        try:
            response = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)
            response.raise_for_status()
            ip_info = response.json()
            ip = ip_info.get("ip")

            detailed_info = fetch_ip_info(ip, proxies)
            detailed_info["ip"] = ip
            detailed_info["proxy_worked"] = True  # ✅ Успешно

            return detailed_info

        except requests.RequestException as e:
            remove_proxy_from_file(proxy)
            new_proxy = get_new_proxy_and_save()
            if new_proxy is None:
                return {"error": "Нет доступных прокси", "proxy_worked": False}
            else:
                return fetch_ip(retry=retry - 1)


    def remove_proxy_from_file(proxy):
        try:
            with open("working_proxies.txt", "r", encoding="utf-8") as f:
                proxies = [line.strip() for line in f if line.strip()]
            proxies = [p for p in proxies if p != proxy]
            with open("working_proxies.txt", "w", encoding="utf-8") as f:
                for p in proxies:
                    f.write(p + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to remove proxy: {e}")

    def get_new_proxy_and_save():
        try:
            with open("working_proxies.txt", "r", encoding="utf-8") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                return None
            new_proxy = random.choice(proxies)
            # Сохраняем в settings.json
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings = {}
            settings["current_proxy"] = new_proxy
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            return new_proxy
        except Exception as e:
            print(f"[ERROR] Failed to get new proxy: {e}")
            return None

    def on_ip_loaded(data):
        clear_frame(parent_frame)

        title = ctk.CTkLabel(parent_frame, text="Check IP", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        if not data or "ip" not in data:
            label = ctk.CTkLabel(parent_frame, text="Ошибка при получении IP-информации", font=("Arial", 16), text_color="red")
            label.place(relx=0.5, rely=0.3, anchor="center")
            return

        # ✅ Получаем статус прокси
        is_worked = data.get("proxy_worked", False)

        fields = [
            f"IP: {data.get('ip', 'N/A')}",
            f"Is worked: {'Yes' if is_worked else 'No'}",
            f"City: {data.get('city', 'N/A')}",
            f"Region: {data.get('region', 'N/A')}",
            f"Country: {data.get('country', 'N/A')}",
            f"Location: {data.get('loc', 'N/A')}",
            f"Org: {data.get('org', 'N/A')}",
            f"ISP (ASN): {data.get('asn', {}).get('name', 'N/A') if isinstance(data.get('asn'), dict) else 'N/A'}",
        ]

        for i, line in enumerate(fields):
            lbl = ctk.CTkLabel(parent_frame, text=line, font=("Arial", 16))
            lbl.place(relx=0.5, rely=0.3 + i * 0.05, anchor="center")

        local_ip_label = ctk.CTkLabel(parent_frame, text=f"Local IP: {get_local_ip()}", font=("Arial", 16))
        local_ip_label.place(relx=0.5, rely=0.75, anchor="center")

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