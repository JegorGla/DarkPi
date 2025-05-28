import customtkinter as ctk
import time
from threading import Thread
import itertools

def show_loading_screen(parent_frame, message="Loading...", fetch_function=None, callback=None):
    """
    Показать экран загрузки с анимацией спиннера.
    
    :param parent_frame: Родительский фрейм.
    :param message: Сообщение на экране.
    :param fetch_function: Функция для выполнения запроса (например, запрос IP).
    :param callback: Функция, вызываемая после завершения загрузки.
    """

    # Очистка фрейма
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Создание метки со спиннером
    spinner_label = ctk.CTkLabel(parent_frame, text="", font=("Arial", 48))
    spinner_label.place(relx=0.5, rely=0.4, anchor="center")

    # Сообщение под спиннером
    message_label = ctk.CTkLabel(parent_frame, text=message, font=("Arial", 16))
    message_label.place(relx=0.5, rely=0.6, anchor="center")

    # Крутилка спиннера
    spinner_cycle = itertools.cycle(["|", "/", "-", "\\"])

    loading = True

    def animate_spinner():
        while loading:
            spinner_label.configure(text=next(spinner_cycle))
            time.sleep(0.1)

    def fetch_data():
        nonlocal loading
        result = None
        if fetch_function:
            result = fetch_function()
        loading = False  # Останавливаем спиннер
        if callback:
            callback(result)  # Передаем результат обратно

    # Запускаем спиннер и загрузку данных параллельно
    Thread(target=animate_spinner, daemon=True).start()
    Thread(target=fetch_data, daemon=True).start()