import json
import customtkinter as ctk
import os

from settings.about_device import about_device_ui  # Импортируем функцию очистки фрейма из about_device.py

def clear_frame(frame):
    """Очистить все виджеты в переданном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

selected_timeout = None  # Глобальная переменная для хранения значения времени
selected_edition = None  # Глобальная переменная для хранения выбранной редакции


def create_default_settings():
    """Создание файла с настройками по умолчанию."""
    default_settings = {
        "timeout": "5 seconds",
        "edition": "Normal edition"
    }
    try:
        with open("settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)
        print("[INFO] Default settings file created with default values.")
    except Exception as e:
        print(f"[ERROR] Error creating settings file: {e}")


def load_timeout_setting():
    """Загрузка сохраненных настроек из файла JSON."""
    global selected_timeout, selected_edition
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                selected_timeout = data.get("timeout", None)
                selected_edition = data.get("edition", None)
                print(f"[INFO] Loaded settings: timeout={selected_timeout}, edition={selected_edition}")
        except (json.JSONDecodeError, KeyError):
            selected_timeout = None
            selected_edition = None
            print("[WARNING] Failed to parse settings.json, setting values to None")
    else:
        print("[WARNING] settings.json not found, creating default settings...")
        create_default_settings()
        selected_timeout = "5 seconds"
        selected_edition = "Normal edition"


def save_timeout_setting():
    """Обновляет настройки в settings.json без потери других данных."""
    if selected_timeout and selected_edition:
        try:
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    try:
                        settings = json.load(f)
                        print(f"[DEBUG] Loaded existing settings for update: {settings}")
                    except json.JSONDecodeError:
                        print("[WARNING] settings.json was corrupted. Overwriting with new settings.")
                        settings = {}

            # Обновляем только нужные поля
            settings["timeout"] = selected_timeout
            settings["edition"] = selected_edition

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

def init_settings_ui(parent_frame, go_back_callback):
    """Функция для инициализации UI настроек."""
    clear_frame(parent_frame)

    def set_edition(event=None):
        """Функция для обработки выбранной редакции."""
        global selected_edition
        selected_edition = edition_combo.get()
        print(f"[DEBUG] New edition selected: {selected_edition}")
        save_timeout_setting()


    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Кнопка "Назад"
    def go_back():
        global selected_timeout, selected_edition
        selected_timeout = timeout_combo.get()
        selected_edition = edition_combo.get()  # Сначала обновляем всё
        save_timeout_setting()                  # Потом сохраняем
        go_back_callback()


    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back)
    back_btn.place(relx=0.01, rely=0.01, anchor="nw")

    # ==== Блок Use Proxies ====  
    setting_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    setting_frame.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.9)

    setting_label = ctk.CTkLabel(setting_frame, text="Use proxies", anchor="w", font=("Arial", 16))
    setting_label.pack(side="left", fill="x", expand=True)

    use_proxies_var = ctk.BooleanVar()
    checkbox = ctk.CTkCheckBox(setting_frame, variable=use_proxies_var, text="")
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

    edition_combo = ctk.CTkComboBox(
        parent_frame, 
        values=["Normal edition", "P Diddy edition"],
        font=("Arial", 16), 
        state="readonly",
    )
    # edition_combo.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9)
    # edition_combo.set(selected_edition if selected_edition else "Select edition")
    # edition_combo.bind("<<ComboboxSelected>>", set_edition)




# Загружаем сохранённую настройку при запуске
load_timeout_setting()