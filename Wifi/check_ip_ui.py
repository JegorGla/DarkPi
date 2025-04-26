import requests
import json
import customtkinter as ctk

from loading_screen import show_loading_screen  # Импортируем функцию загрузки

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
        """Функция загрузки IP."""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=10)
            ip_info = response.json()
            return ip_info.get("ip", "Unknown IP")
        except requests.RequestException as e:
            return f"Error: {e}"

    def on_ip_loaded(ip_address):
        """Отображение IP после загрузки."""
        clear_frame(parent_frame)

        title = ctk.CTkLabel(parent_frame, text="Check IP", font=("Arial", 24))
        title.place(relx=0.5, rely=0.1, anchor="center")

        ip_label = ctk.CTkLabel(parent_frame, text=f"Current IP: {ip_address}", font=("Arial", 16))
        ip_label.place(relx=0.5, rely=0.3, anchor="center")

        back_btn = ctk.CTkButton(
            parent_frame,
            text="← Back",
            command=lambda: go_back_callback() if go_back_callback else None,
            font=("Arial", 16)
        )
        back_btn.place(relx=0.5, rely=0.9, anchor="center")

    # Показать экран загрузки
    show_loading_screen(parent_frame, message="Loading IP...", fetch_function=fetch_ip, callback=on_ip_loaded)