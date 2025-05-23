import customtkinter as ctk
import json
from virtual_keyboard import NumericKeyboard

def clear_frame(frame):
    """
    Clear all widgets from the given frame.
    """
    for widget in frame.winfo_children():
        widget.destroy()

def create_proxy_setting_frame(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    timeot = ctk.CTkEntry(
        parent_frame,
        placeholder_text="Enter timeout (in minutes)",
        width=200,
        height=40,
        font=("Arial", 14)
    )
    timeot.pack(pady=10)

    save = ctk.CTkButton(
        parent_frame,
        text="Save",
        command=lambda: save_proxy_settings(timeot.get())
    )
    save.pack(pady=10)

    back_btn = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=go_back_callback
    )
    back_btn.pack(pady=10)

    def save_proxy_settings(time):
        try:
            # Пробуем загрузить существующие настройки
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Если файл не найден или некорректный, создаём пустой словарь
            settings = {}

        # Сохраняем новое значение
        settings["proxy_rechoice_interval"] = time

        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            print(f"[INFO] proxy_rechoice_interval saved as {time}")
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")    