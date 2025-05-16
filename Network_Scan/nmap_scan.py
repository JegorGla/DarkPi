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
    bottom_frame = ctk.CTkFrame(container, height=300)
    bottom_frame.pack_propagate(False)  # чтобы высота сохранялась при скрытии

    # Левая часть (ввод данных)
    left_frame = ctk.CTkFrame(top_frame, width=300)
    left_frame.pack(side="left", fill="y", padx=(0, 10), pady=10)

    # Правая часть (результаты)
    right_frame = ctk.CTkFrame(top_frame)
    right_frame.pack(side="left", fill="both", expand=True, pady=10)

    # Верхняя часть правой части (TextBox для результатов)
    top_right_frame = ctk.CTkFrame(right_frame)
    top_right_frame.pack(side="top", fill="both", expand=True, pady=10)

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
        fg_color="#000000",      # Чёрный фон
        text_color="#00FF00",    # Ярко-зелёный текст
        border_color="#00FF00",  # Зелёная рамка
        width=200,
        height=30
    )
    scan_button.pack(pady=7)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        left_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=200,
        height=30
    )
    back_button.pack(pady=7)

    # Кнопка "Сохранить результаты"
    save_button = ctk.CTkButton(
        left_frame,
        text="Save Results",
        command=lambda: save_results(),
        font=("Arial", 16),
        width=200,
        height=30
    )
    save_button.pack(pady=7)

    # TextBox для результатов (в верхней правой части)
    text_result = ctk.CTkTextbox(top_right_frame, font=("Arial", 14))
    text_result.pack(fill="both", expand=True, padx=10, pady=10)

    # Переменная для хранения активного поля
    active_entry = None

    def set_target_entry(entry, name):
        nonlocal active_entry
        active_entry = entry
        keyboard.target_entry = entry
        #print(f"[DEBUG] Активное поле ввода: {name}")

    # Функция обработки нажатия с виртуальной клавиатуры
    def on_key_pressed(key):
        if active_entry:
            current = active_entry.get()
            active_entry.delete(0, ctk.END)
            active_entry.insert(0, current + key)

    def run_scan():
        text_result.delete("1.0", "end")
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
        if not os.path.exists("results"):
            os.makedirs("results")
        filename = f"results/{entry_target.get()}_scan_results.txt"
        with open(filename, "w") as file:
            file.write(text_result.get("1.0", "end"))

    # Виртуальная клавиатура в нижнем фрейме
    keyboard = NumericKeyboard(bottom_frame, entry_target)

    # Привязка клавиатуры к полям ввода
    entry_target.bind("<FocusIn>", lambda e: [set_target_entry(entry_target, "Target (IP/Domain)"), show_keyboard()])
    entry_ports.bind("<FocusIn>", lambda e: [set_target_entry(entry_ports, "Ports"), show_keyboard()])

    # Кнопка-панель для вызова клавиатуры
    keyboard_toggle_frame = ctk.CTkFrame(container, height=40)
    keyboard_toggle_frame.pack(side="bottom", fill="x")

    keyboard_visible = False

    def slide_keyboard(target_y, step=10):
        parent_frame.update()
        container_width = container.winfo_width()
        x_pos = (container_width - keyboard_width) // 2

        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        parent_frame.after(10, lambda: slide_keyboard(target_y, step))


    def show_keyboard():
        nonlocal keyboard_visible
        if keyboard_visible:
            return
        keyboard_visible = True
        slide_keyboard(target_y=parent_frame.winfo_height() - 300)

    def hide_keyboard():
        nonlocal keyboard_visible
        if not keyboard_visible:
            return
        keyboard_visible = False
        slide_keyboard(target_y=parent_frame.winfo_height())

    def toggle_keyboard():
        if keyboard_visible:
            hide_keyboard()
        else:
            show_keyboard()

    toggle_button = ctk.CTkButton(keyboard_toggle_frame, text="⌨ Клавиатура", command=toggle_keyboard)
    toggle_button.pack(pady=5)

    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    keyboard_width = 750
    keyboard_height = 300

    def place_keyboard_at(y_pos):
        parent_frame.update()
        container_width = container.winfo_width()
        x_pos = (container_width - keyboard_width) // 2
        bottom_frame.place(in_=container, x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)

    # Изначально скрываем клавиатуру
    place_keyboard_at(parent_frame.winfo_height())
