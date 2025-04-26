import nmap
import customtkinter as ctk
import threading
import time
import os
from virtual_keyboard import NumericKeyboard  # Поменяйте на вашу виртуальную клавиатуру

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def nmap_scan_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для сканирования портов через Nmap."""
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
    label_title = ctk.CTkLabel(left_frame, text="Nmap Port Scanner", font=("Arial", 24))
    label_title.pack(pady=10)

    # Поле ввода IP-адреса или домена
    label_target = ctk.CTkLabel(left_frame, text="Target IP / Domain:", font=("Arial", 16))
    label_target.pack(pady=5)
    entry_target = ctk.CTkEntry(left_frame, placeholder_text="Enter IP or Domain", font=("Arial", 16))
    entry_target.pack(pady=5)

    # Поле ввода диапазона портов
    label_ports = ctk.CTkLabel(left_frame, text="Ports (e.g., 20-80 or 22,80,443):", font=("Arial", 16))
    label_ports.pack(pady=5)
    entry_ports = ctk.CTkEntry(left_frame, placeholder_text="Enter Ports", font=("Arial", 16))
    entry_ports.pack(pady=5)

    # Кнопка для начала сканирования
    scan_button = ctk.CTkButton(
        left_frame,
        text="Start Scan",
        command=lambda: threading.Thread(target=run_scan, daemon=True).start(),
        font=("Arial", 16),
        width=200,
        height=40
    )
    scan_button.pack(pady=20)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        left_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=200,
        height=40
    )
    back_button.pack(pady=10)

    # Кнопка "Сохранить результаты"
    save_button = ctk.CTkButton(
        left_frame,
        text="Save Results",
        command=lambda: save_results(),
        font=("Arial", 16),
        width=200,
        height=40
    )
    save_button.pack(pady=10)

    # TextBox для результатов (в верхней правой части)
    text_result = ctk.CTkTextbox(top_right_frame, font=("Arial", 14))
    text_result.pack(fill="both", expand=True, padx=10, pady=10)

    # Переменная для хранения активного поля
    active_entry = None

    def set_target_entry(entry, name):
        keyboard.target_entry = entry
        print(f"[DEBUG] Активное поле ввода: {name}")

    # Функции для обработки ввода с клавиатуры
    def on_key_pressed(key):
        """Функция для обработки нажатия клавиш на виртуальной клавиатуре."""
        if active_entry:
            current = active_entry.get()
            active_entry.delete(0, ctk.END)
            active_entry.insert(0, current + key)

    def run_scan():
        text_result.delete("1.0", "end")
        """Функция для запуска сканирования."""
        target = entry_target.get()
        ports = entry_ports.get()

        if not target:
            text_result.insert("end", "Please enter a target.\n")
            return

        current_time = time.strftime("%H:%M:%S", time.localtime())

        scanner = nmap.PortScanner()

        try:
            text_result.insert("end", f"Scanning {target} on ports {ports} is started at {current_time}...\n")
            text_result.update()

            scanner.scan(hosts=target, ports=ports)

            for host in scanner.all_hosts():
                text_result.insert("end", f"\nHost: {host} ({scanner[host].hostname()})\n")
                text_result.insert("end", f"State: {scanner[host].state()}\n")

                for proto in scanner[host].all_protocols():
                    text_result.insert("end", f"Protocol: {proto}\n")
                    ports = scanner[host][proto].keys()
                    for port in ports:
                        state = scanner[host][proto][port]['state']
                        text_result.insert("end", f"Port: {port}\tState: {state}\n")

            text_result.insert("end", "\nScan complete.\n")
        except Exception as e:
            text_result.insert("end", f"Error: {str(e)}\n")

    def save_results():
        # Проверяем, существует ли папка results
        if not os.path.exists("results"):
            os.makedirs("results")  # создаём папку, если её нет

        # Теперь сохраняем файл
        with open(f"results/{entry_target.get()}_scan_results.txt", "w") as file:
            file.write(text_result.get("1.0", "end"))

    # Виртуальная клавиатура
    keyboard = NumericKeyboard(bottom_right_frame, entry_target)
    
    # Привязка клавиатуры к полям
    entry_target.bind("<FocusIn>", lambda event: set_target_entry(entry_target, "Target (IP/Domain)"))
    entry_ports.bind("<FocusIn>", lambda event: set_target_entry(entry_ports, "Ports"))
    

# В этом примере, когда вы щелкаете на поле ввода, оно становится активным. 
# Виртуальная клавиатура будет вставлять символы в это активное поле.
