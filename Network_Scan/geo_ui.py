import requests
import customtkinter as ctk
import json
import os

def clear_frame(frame):
    """Очищает все виджеты внутри переданного фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()

def get_ip_info(ip):
    """Получаем информацию о IP-адресе с помощью ipinfo.io API."""
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching IP info: {e}")
        return None
    
def display_ip_info(ip_info, frame, go_back_callback):
    """Отображает информацию о IP в фрейме."""
    clear_frame(frame)

    ip_entry = ctk.CTkEntry(frame, placeholder_text="Enter IP Address")
    ip_entry.pack(pady=10)

    # Кнопка для поиска IP
    find_btn = ctk.CTkButton(frame, text="Find IP", command=lambda: fetch_and_display_info(ip_entry.get(), frame, go_back_callback))
    find_btn.pack(pady=10)
    
    if ip_info:
        ip_label = ctk.CTkLabel(frame, text=f"IP: {ip_info.get('ip', 'N/A')}")
        ip_label.pack(pady=5)

        city_label = ctk.CTkLabel(frame, text=f"City: {ip_info.get('city', 'N/A')}")
        city_label.pack(pady=5)

        region_label = ctk.CTkLabel(frame, text=f"Region: {ip_info.get('region', 'N/A')}")
        region_label.pack(pady=5)

        country_label = ctk.CTkLabel(frame, text=f"Country: {ip_info.get('country', 'N/A')}")
        country_label.pack(pady=5)

        loc_label = ctk.CTkLabel(frame, text=f"Location: {ip_info.get('loc', 'N/A')}")
        loc_label.pack(pady=5)

        org_label = ctk.CTkLabel(frame, text=f"Organization: {ip_info.get('org', 'N/A')}")
        org_label.pack(pady=5)
    else:
        error_label = ctk.CTkLabel(frame, text="Error fetching IP information.")
        error_label.pack(pady=5)

    # Кнопка "Назад"
    go_back_button = ctk.CTkButton(frame, text="Go Back", command=go_back_callback)
    go_back_button.pack(pady=10)

def fetch_and_display_info(ip, frame, go_back_callback):
    """Функция для получения данных и отображения их на экране."""
    ip_info = get_ip_info(ip)
    display_ip_info(ip_info, frame, go_back_callback)