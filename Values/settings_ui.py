import json
import customtkinter as ctk
import os
from Values.date_time_config import *

from settings.about_device import about_device_ui  # Импортируем функцию очистки фрейма из about_device.py
from settings.customithation_ui import create_customization_ui  # Импортируем функцию очистки фрейма из customithation_ui.py

def clear_frame(frame):
    """Очистить все виджеты в переданном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

selected_timeout = None  # Глобальная переменная для хранения значения времени
selected_edition = None  # Глобальная переменная для хранения выбранной редакции
fullscreen = None
selected_check_update = None
use_proxy = None

def create_default_settings():
    """Создание файла с настройками по умолчанию."""
    default_settings = {
        "timeout": "5 seconds",
        "edition": "Evil eye",
        "fullscreen": "Yes",
        "Time to check update": "1 day",
        "use_proxy": "Yes"
    }
    try:
        with open("settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)
        print("[INFO] Default settings file created with default values.")
    except Exception as e:
        print(f"[ERROR] Error creating settings file: {e}")


def load_timeout_setting():
    global selected_timeout, selected_edition, fullscreen, selected_check_update, use_proxy
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                selected_timeout = data.get("timeout", "5 seconds")
                selected_edition = data.get("edition", "Evil eye")
                fullscreen = data.get("fullscreen", "No")
                selected_check_update = data.get("update_check_interval", "1 day")
                use_proxy = data.get("use_proxy", "Yes")
                print(f"[INFO] Loaded settings: timeout={selected_timeout}, edition={selected_edition}, fullscreen={fullscreen}")
        except (json.JSONDecodeError, KeyError):
            selected_timeout = None
            selected_edition = None
            fullscreen = "No"
            selected_check_update = "Never"
            use_proxy = "Yes"
            print("[WARNING] Failed to parse settings.json, setting values to defaults")
    else:
        print("[WARNING] settings.json not found, creating default settings...")
        create_default_settings()
        selected_timeout = "5 seconds"
        selected_edition = "Evil eye"
        fullscreen = "No"
        selected_check_update = "1 day"
        use_proxy = "Yes"

def save_timeout_setting():
    global selected_timeout, selected_edition, fullscreen_var, selected_check_update, use_proxy
    if selected_timeout and selected_edition:
        try:
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    try:
                        settings = json.load(f)
                    except json.JSONDecodeError:
                        settings = {}

            settings["timeout"] = selected_timeout
            settings["edition"] = selected_edition
            settings["fullscreen"] = "Yes" if fullscreen_var.get() else "No"
            settings["update_check_interval"] = selected_check_update
            settings["use_proxy"] = "Yes" if use_proxies_var.get() else "No"


            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            
            print(f"[INFO] Settings saved successfully: {settings}")
        except Exception as e:
            print(f"[ERROR] Error saving settings: {e}")


def set_gif_timeout(event=None):
    """Функция для обработки выбранного времени без задержки."""
    global selected_timeout
    selected_timeout = timeout_combo.get()
    print(f"[DEBUG] New timeout selected: {selected_timeout}")
    save_timeout_setting()

def get_fullscreen_value():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data.get("fullscreen", "No") == "Yes"
    except:
        return False  # по умолчанию выключено
    
def get_time_to_check_update():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data.get("Time to check update", "1 day")
    except:
        return False  # по умолчанию выключено

def get_use_proxy_value():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data.get("use_proxy", "Yes") == "Yes"
    except:
        return False  # по умолчанию выключено


def init_settings_ui(parent_frame, go_back_callback):
    """Функция для инициализации UI настроек."""
    clear_frame(parent_frame)


    def set_edition(event=None):
        """Функция для обработки выбранной редакции."""
        global selected_edition
        selected_edition = edition_combo.get()
        print(f"[DEBUG] New edition selected: {selected_edition}")
        save_timeout_setting()

    def set_update_check_interval(event=None):
        global selected_check_update
        selected_check_update = update_checker_combo.get()
        print(f"[DEBUG] Update check interval: {selected_check_update}")
        save_timeout_setting()
    


    # Заголовок (оставляем через place, чтобы был сверху по центру)
    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Основной скроллируемый фрейм с отступом сверху, чтобы не закрывать заголовок
    main_frame = ctk.CTkScrollableFrame(parent_frame)
    main_frame.pack(fill="both", expand=True, pady=(60, 20), padx=20)

    def go_back():
        global selected_timeout, selected_edition, selected_check_update, selected_fullscreen, use_proxy
        selected_timeout = timeout_combo.get()
        selected_edition = edition_combo.get()
        selected_check_update = update_checker_combo.get()
        selected_fullscreen = fullscreen_var.get()
        use_proxy = use_proxies_var.get()
        save_timeout_setting()
        go_back_callback()

    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back)
    back_btn.pack(anchor="nw", pady=10, padx=10)

    # Use proxies блок
    setting_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    setting_frame.pack(fill="x", pady=10, padx=10)

    setting_label = ctk.CTkLabel(setting_frame, text="Use proxies", anchor="w", font=("Arial", 16))
    setting_label.pack(side="left", fill="x", expand=True, padx=(10, 0))

    global use_proxies_var
    use_proxies_var = ctk.BooleanVar(value=get_use_proxy_value())
    checkbox = ctk.CTkCheckBox(setting_frame, variable=use_proxies_var, text="", command=save_timeout_setting)
    checkbox.pack(side="right")

    # Fullscreen блок
    fullscreen_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    fullscreen_frame.pack(fill="x", pady=10, padx=10)

    fullscreen_label = ctk.CTkLabel(fullscreen_frame, text="Fullscreen", anchor="w", font=("Arial", 16))
    fullscreen_label.pack(side="left", fill="x", expand=True, padx=(10, 0))

    global fullscreen_var
    fullscreen_var = ctk.BooleanVar(value=get_fullscreen_value())
    fullscreen_check_box = ctk.CTkCheckBox(fullscreen_frame, variable=fullscreen_var, text="", command=save_timeout_setting)
    fullscreen_check_box.pack(side="right")

    # About Device кнопка
    about_device_btn = ctk.CTkButton(
        main_frame,
        text="About Device",
        command=lambda: about_device_ui(main_frame, go_back_callback),
        font=("Arial", 16)
    )
    about_device_btn.pack(fill="x", pady=10, padx=10)

    # Разделитель
    separator = ctk.CTkFrame(main_frame, height=1, fg_color="#444444")
    separator.pack(fill="x", padx=10, pady=10)

    # Таймаут комбобокс
    global timeout_combo
    timeout_combo = ctk.CTkComboBox(
        main_frame,
        values=["5 seconds", "10 seconds", "30 seconds", "1 minute", "5 minutes"],
        font=("Arial", 16),
        state="readonly",
    )
    timeout_combo.pack(fill="x", padx=10, pady=10)
    timeout_combo.set(selected_timeout if selected_timeout else "Select timeout")
    timeout_combo.bind("<<ComboboxSelected>>", set_gif_timeout)

    # Интервал проверки обновлений
    global update_checker_combo
    update_checker_combo = ctk.CTkComboBox(
        main_frame,
        values=["1 day", "5 day", "1 month", "1 year", "Never"],
        font=("Arial", 16),
        state="readonly",
    )
    update_checker_combo.pack(fill="x", padx=10, pady=10)
    update_checker_combo.set(selected_check_update if selected_check_update else "Select interval")
    update_checker_combo.bind("<<ComboboxSelected>>", set_update_check_interval)

    # Редакция
    edition_combo = ctk.CTkComboBox(
        main_frame,
        values=["Evil eye", "P Diddy", "Smile ascii", "Matrix", "Boom", "Car", "Space warp", "Earth"],
        font=("Arial", 16),
        state="readonly",
    )
    edition_combo.pack(fill="x", padx=10, pady=10)
    edition_combo.set(selected_edition if selected_edition else "Select edition")
    edition_combo.bind("<<ComboboxSelected>>", set_edition)

    # Кнопка Customization Raspberry Pi
    customithation_raspberry_pi = ctk.CTkButton(
        main_frame,
        text="Customization Raspberry Pi",
        command=lambda: create_customization_ui(main_frame, go_back_callback),
        font=("Arial", 16),
    )
    customithation_raspberry_pi.pack(fill="x", pady=20, padx=10)

# Загружаем сохранённую настройку при запуске
load_timeout_setting()