import customtkinter as ctk
import pywifi
from pywifi import const
import time
import json
import os
from virtual_keyboard import NormalKeyboard  # Импортируем виртуальную клавиатуру

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

def connect_to_wifi(ssid, password):
    """Подключается к Wi-Fi сети с указанным SSID и паролем."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()  # Отключаемся от текущей сети
    time.sleep(1)  # Ждем перед подключением

    profile = pywifi.Profile()  # Создаем профиль для подключения
    profile.ssid = ssid  # Устанавливаем SSID
    profile.auth = const.AUTH_ALG_OPEN  # Алгоритм аутентификации
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Тип шифрования
    profile.cipher = const.CIPHER_TYPE_CCMP  # Тип шифрования данных
    profile.key = password  # Устанавливаем пароль

    iface.remove_all_network_profiles()  # Удаляем все существующие профили
    tmp_profile = iface.add_network_profile(profile)  # Добавляем новый профиль
    iface.connect(tmp_profile)  # Подключаемся к сети
    time.sleep(5)  # Ждем подключения

    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

def create_wifi_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Доступные Wi-Fi сети", font=("Arial", 20))
    label_title.pack(pady=10)

    # Фрейм для кнопок сетей
    networks_frame = ctk.CTkFrame(parent_frame)
    networks_frame.pack(pady=10)

    def on_password_submit(ssid, entry, keyboard_frame):
        """Обрабатывает ввод пароля и подключается к сети."""
        password = entry.get()
        clear_frame(keyboard_frame)  # Очищаем клавиатуру после ввода
        success = connect_to_wifi(ssid, password)
        if success:
            label_status = ctk.CTkLabel(parent_frame, text=f"Успешно подключено к {ssid}!", font=("Arial", 14))
            try:
                # Проверяем, существует ли файл
                if os.path.exists("settings.json"):
                    # Если файл существует, загружаем данные
                    with open("settings.json", "r") as file:
                        data = json.load(file)
                else:
                    # Если файл не существует, создаем пустой словарь
                    data = {}

                # Добавляем или обновляем SSID
                data["ssid"] = ssid

                # Записываем обновленные данные обратно в файл
                with open("settings.json", "w") as file:
                    json.dump(data, file, indent=4)
                print(f"[INFO] SSID '{ssid}' saved to settings.json")
            except Exception as e:
                print(f"[ERROR] Failed to save SSID to settings.json: {e}")

        else:
            label_status = ctk.CTkLabel(parent_frame, text=f"Не удалось подключиться к {ssid}.", font=("Arial", 14))
        label_status.pack(pady=10)

    def on_network_click(ssid):
        """Отображает поле ввода пароля и виртуальную клавиатуру."""
        clear_frame(parent_frame)  # Очищаем текущий интерфейс

        # Заголовок
        label_title = ctk.CTkLabel(parent_frame, text=f"Подключение к {ssid}", font=("Arial", 20))
        label_title.pack(pady=10)

        # Поле ввода пароля
        entry = ctk.CTkEntry(parent_frame, font=("Arial", 14), show="*")
        entry.pack(pady=10)
        entry.focus()

        # !!! СНАЧАЛА создаём фрейм для клавиатуры
        keyboard_frame = ctk.CTkFrame(parent_frame, width=200, height=400)
        keyboard_frame.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.8)

        # !!! Теперь создаём клавиатуру
        keyboard = NormalKeyboard(keyboard_frame, entry)

        # Кнопка Подключиться
        connect_button = ctk.CTkButton(parent_frame, text="Connect", command=lambda: on_password_submit(ssid, entry, keyboard_frame))
        connect_button.pack(pady=10)

        # Кнопка Назад
        back_button = ctk.CTkButton(parent_frame, text="← Back", command=lambda: create_wifi_ui(parent_frame, go_back_callback))
        back_button.place(relx=0.05, rely=0.05, anchor="nw")

    def on_scan_button_click():
        """Обрабатывает нажатие на кнопку 'Сканировать сети'"""
        # Очищаем фрейм с кнопками сетей перед сканированием
        for widget in networks_frame.winfo_children():
            widget.destroy()

        # Сканируем доступные сети
        networks = scan_wifi_networks()
        
        if networks:
            # Создаем кнопку для каждой доступной сети
            for network in networks:
                connect_button = ctk.CTkButton(networks_frame, text=network, command=lambda ssid=network: on_network_click(ssid))
                connect_button.pack(pady=5)
        else:
            # Если сетей нет, показываем сообщение
            no_network_label = ctk.CTkLabel(networks_frame, text="Нет доступных сетей.", font=("Arial", 14))
            no_network_label.pack(pady=10)

    # Кнопка для сканирования сетей
    scan_button = ctk.CTkButton(parent_frame, text="Сканировать сети", command=on_scan_button_click)
    scan_button.pack(pady=10)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
    back_button.pack(pady=10)