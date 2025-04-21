import customtkinter as ctk
import random
from virtual_keyboard import VirtualKeyboard  # Импортируем виртуальную клавиатуру

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def start_guess_number_game(parent_frame):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI
    target_number = random.randint(1, 100)  # Загаданное число
    show_info(parent_frame, "Угадай число", "Я загадал число от 1 до 100. Попробуй угадать!")
    ask_for_guess(parent_frame, target_number)

def show_info(parent_frame, title, message):
    """Отображает информационное сообщение в основном окне."""
    clear_frame(parent_frame)  # Очищаем фрейм перед отображением сообщения

    label_title = ctk.CTkLabel(parent_frame, text=title, font=("Arial", 20))
    label_title.pack(pady=10)

    label_message = ctk.CTkLabel(parent_frame, text=message, font=("Arial", 14))
    label_message.pack(pady=20)

    button = ctk.CTkButton(parent_frame, text="Продолжить", command=lambda: clear_frame(parent_frame))
    button.pack(pady=10)

def show_input(parent_frame, title, message, callback):
    """Отображает поле ввода и сообщения слева, а клавиатуру справа."""
    clear_frame(parent_frame)  # Очищаем весь фрейм перед отображением

    # Создаем фрейм для сообщений и ввода (слева)
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.place(relx=0.05, rely=0.05, relwidth=0.4, relheight=0.9)  # Занимает 40% ширины слева

    # Создаем фрейм для клавиатуры (справа)
    keyboard_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    keyboard_frame.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.9)  # Занимает 45% ширины справа

    # Заголовок
    label_title = ctk.CTkLabel(input_frame, text=title, font=("Arial", 20))
    label_title.pack(pady=10)

    # Сообщение
    label_message = ctk.CTkLabel(input_frame, text=message, font=("Arial", 14))
    label_message.pack(pady=10)

    # Поле ввода
    entry = ctk.CTkEntry(input_frame, font=("Arial", 14))
    entry.pack(pady=10)
    entry.focus()

    # Кнопка отправки
    def submit_input():
        try:
            guess = int(entry.get())
            callback(parent_frame, guess)
        except ValueError:
            show_info(parent_frame, "Ошибка", "Введите корректное число.")

    button = ctk.CTkButton(input_frame, text="Отправить", command=submit_input)
    button.pack(pady=10)

    # Инициализация виртуальной клавиатуры в правом фрейме
    VirtualKeyboard(keyboard_frame, entry)

def ask_for_guess(parent_frame, target_number):
    """Запрашивает у пользователя догадку."""
    show_input(parent_frame, "Угадай число", "Введите ваше предположение:", lambda _, guess: check_guess(parent_frame, target_number, guess))

def check_guess(parent_frame, target_number, guess):
    """Проверяет догадку пользователя и дает обратную связь."""
    if guess < target_number:
        to_nomuch = ctk.CTkLabel(parent_frame, text="Слишком мало! Попробуй ещё раз.", font=("Arial", 14))
        ask_for_guess(parent_frame, target_number)
    elif guess > target_number:
        show_info(parent_frame, "Угадай число", "Слишком много! Попробуй ещё раз.")
        ask_for_guess(parent_frame, target_number)
    else:
        show_info(parent_frame, "Угадай число", "Поздравляю! Вы угадали число!")