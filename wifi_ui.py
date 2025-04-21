import customtkinter as ctk
import pywifi
from pywifi import const
import time

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def scan_wifi_networks():
    """Сканирует доступные Wi-Fi сети и возвращает список их имен (SSID)."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Получаем первый доступный интерфейс
    iface.scan()  # Запускаем сканирование
    time.sleep(2)  # Ждем несколько секунд для завершения сканирования
    scan_results = iface.scan_results()  # Получаем результаты сканирования

    networks = []
    for network in scan_results:
        networks.append(network.ssid)  # Добавляем SSID сети в список
    return networks

def create_wifi_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Доступные Wi-Fi сети", font=("Arial", 20))
    label_title.pack(pady=10)

    # Фрейм для кнопок сетей
    networks_frame = ctk.CTkFrame(parent_frame)
    networks_frame.pack(pady=10)

    def connect_to_network(ssid):
        print(f"Попытка подключения к сети: {ssid}")

    def on_scan_button_click():
        for widget in networks_frame.winfo_children():
            widget.destroy()

        networks = scan_wifi_networks()
        if networks:
            for network in networks:
                connect_button = ctk.CTkButton(networks_frame, text=network, command=lambda ssid=network: connect_to_network(ssid))
                connect_button.pack(pady=5)
        else:
            no_network_label = ctk.CTkLabel(networks_frame, text="Нет доступных сетей.", font=("Arial", 14))
            no_network_label.pack(pady=10)

    scan_button = ctk.CTkButton(parent_frame, text="Сканировать сети", command=on_scan_button_click)
    scan_button.pack(pady=10)

    back_button = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
    back_button.pack(pady=10)
