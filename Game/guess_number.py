import customtkinter as ctk
import random
from virtual_keyboard import Keyboard_For_Game  # Импорт виртуальной клавиатуры

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def start_guess_number_game(parent_frame, go_back_callback=None):
    """Запускает игру 'Угадай число'."""
    clear_frame(parent_frame)
    target_number = random.randint(1, 100)
    ask_for_guess(parent_frame, target_number, go_back_callback)

def show_info(parent_frame, title, message, go_back_callback=None):
    """Показывает информационное сообщение."""
    clear_frame(parent_frame)

    label_title = ctk.CTkLabel(parent_frame, text=title, font=("Arial", 24))
    label_title.pack(pady=(20, 10))

    label_message = ctk.CTkLabel(parent_frame, text=message, font=("Arial", 16), wraplength=400)
    label_message.pack(pady=(10, 20))

    button_play_again = ctk.CTkButton(
        parent_frame,
        text="Play Again",
        command=lambda: start_guess_number_game(parent_frame, go_back_callback)
    )
    button_play_again.pack(pady=10)

    if go_back_callback:
        button_back = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
        button_back.pack(pady=10)

def show_input(parent_frame, title, message, callback, go_back_callback=None):
    """Отображает поле ввода и клавиатуру."""
    clear_frame(parent_frame)

    # Левая часть (информация и ввод)
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.9)

    # Правая часть (виртуальная клавиатура)
    keyboard_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    keyboard_frame.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.9)

    label_title = ctk.CTkLabel(input_frame, text=title, font=("Arial", 20))
    label_title.pack(pady=(10, 5))

    label_message = ctk.CTkLabel(input_frame, text=message, font=("Arial", 14), wraplength=250)
    label_message.pack(pady=(5, 10))

    entry = ctk.CTkEntry(input_frame, font=("Arial", 16))
    entry.pack(pady=10)
    entry.focus()

    def submit_input():
        try:
            guess = int(entry.get())
            callback(parent_frame, guess)
        except ValueError:
            show_info(parent_frame, "Error", "Please enter a valid number!", go_back_callback)

    button_submit = ctk.CTkButton(input_frame, text="Submit", command=submit_input)
    button_submit.pack(pady=10)

    if go_back_callback:
        button_back = ctk.CTkButton(input_frame, text="Back", command=go_back_callback)
        button_back.pack(pady=10)

    # Клавиатура привязана к полю ввода
    Keyboard_For_Game(keyboard_frame, entry)

def ask_for_guess(parent_frame, target_number, go_back_callback=None):
    """Запрашивает догадку пользователя."""
    show_input(
        parent_frame,
        "Guess the Number",
        "Enter your guess:",
        lambda pf, guess: check_guess(pf, target_number, guess, go_back_callback),
        go_back_callback
    )

def check_guess(parent_frame, target_number, guess, go_back_callback=None):
    """Проверяет введённое число и даёт подсказку."""
    if guess < target_number:
        show_input(
            parent_frame,
            "Too Low!",
            "Try a higher number:",
            lambda pf, g: check_guess(pf, target_number, g, go_back_callback),
            go_back_callback
        )
    elif guess > target_number:
        show_input(
            parent_frame,
            "Too High!",
            "Try a lower number:",
            lambda pf, g: check_guess(pf, target_number, g, go_back_callback),
            go_back_callback
        )
    else:
        show_info(
            parent_frame,
            "Congratulations!",
            f"You guessed the number: {target_number} 🎉",
            go_back_callback
        )
