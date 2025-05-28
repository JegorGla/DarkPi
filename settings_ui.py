import json
import customtkinter as ctk
import os
from date_time_config import *

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
        "edition": "Normal edition",
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
                selected_edition = data.get("edition", "Normal edition")
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
        selected_edition = "Normal edition"
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
    


    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Кнопка "Назад"
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
    back_btn.place(relx=0.01, rely=0.01, anchor="nw")

    # ==== Блок Use Proxies ====  
    setting_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    setting_frame.place(relx=0.54, rely=0.25, anchor="center", relwidth=1)

    setting_label = ctk.CTkLabel(setting_frame, text="Use proxies", anchor="w", font=("Arial", 16))
    setting_label.pack(side="left", fill="x", expand=True, padx=(10, 0))

    global use_proxies_var
    use_proxies_var = ctk.BooleanVar(value=get_use_proxy_value())
    checkbox = ctk.CTkCheckBox(
        setting_frame,
        variable=use_proxies_var,
        text="",
        command=save_timeout_setting  # сохраняем при изменении
    )
    checkbox.pack(side="right")

    # ==================== About Device ====================
    about_device_btn = ctk.CTkButton(
        parent_frame, 
        text="About Device", 
        command=lambda: about_device_ui(parent_frame, go_back_callback), 
        font=("Arial", 16)
    )
    about_device_btn.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.9)

    # Горизонтальная линия
    separator = ctk.CTkFrame(parent_frame, height=1, fg_color="#444444")
    separator.place(relx=0.05, rely=0.3, relwidth=0.9)

    # ==== Настройка времени для GIF-анимации ====
    global timeout_combo
    timeout_combo = ctk.CTkComboBox(
        parent_frame, 
        values=["5 seconds", "10 seconds", "30 seconds", "1 minute", "5 minutes"],
        font=("Arial", 16), 
        state="readonly",
    )
    timeout_combo.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9)

    timeout_combo.set(selected_timeout if selected_timeout else "Select timeout")
    timeout_combo.bind("<<ComboboxSelected>>", set_gif_timeout)

    global update_checker_combo
    update_checker_combo = ctk.CTkComboBox(
        parent_frame,
        values=["1 day", "5 day", "1 month", "1 year", "Never"],
        font=("Arial", 16), 
        state="readonly"
    )
    update_checker_combo.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9)
    update_checker_combo.set(selected_check_update if selected_check_update else "Select interval")
    update_checker_combo.bind("<<ComboboxSelected>>", set_update_check_interval)

    edition_combo = ctk.CTkComboBox(
        parent_frame, 
        values=["Normal edition", "P Diddy edition"],
        font=("Arial", 16), 
        state="readonly",
    )
    edition_combo.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.9)
    edition_combo.set(selected_edition if selected_edition else "Select edition")
    edition_combo.bind("<<ComboboxSelected>>", set_edition)


    # ==== Блок Fullscreen ====
    fullscreen_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    fullscreen_frame.place(relx=0.54, rely=0.33, anchor="center", relwidth=1)

    fullscreen_label = ctk.CTkLabel(fullscreen_frame, text="Fullscreen", anchor="w", font=("Arial", 16))
    fullscreen_label.pack(side="left", fill="x", expand=True, padx=(10, 0))


    global fullscreen_var
    fullscreen_var = ctk.BooleanVar(value=get_fullscreen_value())
    fullscreen_check_box = ctk.CTkCheckBox(
        fullscreen_frame,
        variable=fullscreen_var,
        text="",
        command=save_timeout_setting
    )
    fullscreen_check_box.pack(side="right")

    customithation_raspberry_pi = ctk.CTkButton(
        parent_frame, 
        text="Customithation Raspberry Pi", 
        command=lambda: create_customization_ui(parent_frame, go_back_callback), 
        font=("Arial", 16)
    )
    customithation_raspberry_pi.place(relx=0.5, rely=0.9, anchor="center", relwidth=0.9)        

# Загружаем сохранённую настройку при запуске
load_timeout_setting()