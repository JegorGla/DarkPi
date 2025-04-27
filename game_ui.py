#game_ui.py

import customtkinter as ctk
from Game.guess_number import start_guess_number_game  # Импортируем игру "Угадай число"
from Game.clicker_game import ClickerGame  # Импортируем игру "Кликер"

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def init_game_ui(parent_frame, go_back_callback):
    """Создает главное меню игр."""

    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Меню игр", font=("Arial", 24))
    label_title.pack(pady=20)

    # Кнопка для игры "Угадай число"
    button_guess_number = ctk.CTkButton(
        parent_frame, text="Угадай число", font=("Arial", 16),
        command=lambda: start_guess_number_game(parent_frame, go_back_callback=go_back_callback)  # Запуск игры "Угадай число"
    )
    button_guess_number.pack(pady=10)

    # Кнопка для игры "Кликер"
    button_clicker_game = ctk.CTkButton(
        parent_frame, text="Кликер", font=("Arial", 16),
        command=lambda: ClickerGame(parent_frame)  # Запуск игры "Кликер"
    )
    button_clicker_game.pack(pady=10)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        parent_frame, text="← Назад", font=("Arial", 16),
        command=go_back_callback  # Возврат в главное меню
    )
    back_button.pack(pady=20)