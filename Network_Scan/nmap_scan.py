import platform
import subprocess
import customtkinter as ctk
import threading
import time
import os
import json
import datetime
from virtual_keyboard import NormalKeyboard  # Поменяйте на вашу виртуальную клавиатуру

scan_data = {}

nmap_flags = [
    {"flag": "-sS", "description": "TCP SYN scan (быстрое и малозаметное сканирование)"},
    {"flag": "-sT", "description": "TCP connect scan (использует системные вызовы, менее скрытное)"},
    {"flag": "-sU", "description": "UDP scan (сканирование UDP-портов)"},
    {"flag": "-sV", "description": "Определение версий сервисов (service version detection)"},
    {"flag": "-O",  "description": "Определение операционной системы хоста"},
    {"flag": "-A",  "description": "Агрессивное сканирование (включает -O, -sV, скрипты и traceroute)"},
    {"flag": "-T4", "description": "Установка скорости сканирования (T4 — быстро, но не слишком шумно)"},
    {"flag": "-Pn", "description": "Не пинговать хост (считается, что он активен)"},
    {"flag": "-p-", "description": "Сканировать все 65535 портов"},
    {"flag": "-F",  "description": "Быстрое сканирование (сканирует только самые популярные порты)"},
    {"flag": "-n",  "description": "Не делать DNS-резолвинг (ускоряет сканирование)"},
    {"flag": "--open", "description": "Показать только открытые порты"},
    {"flag": "-v",  "description": "Режим подробного вывода (verbose)"},
    {"flag": "-vv", "description": "Ещё более подробный вывод"},
    {"flag": "-iL", "description": "Сканировать список хостов из файла"},
    {"flag": "-oN", "description": "Сохранить результат в обычный (normal) текстовый файл"},
    {"flag": "-oX", "description": "Сохранить результат в XML формате"},
    {"flag": "--script", "description": "Выполнить NSE-скрипты (например, --script vuln)"},
]

def save_inf_to_the_IPMap():
    try:
        os.makedirs("IPMapper", exist_ok=True)
        filepath = "IPMapper/ip.json"
        existing_data = {}

        # Загружаем старые данные, если файл существует
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        # Обновляем их новыми
        existing_data.update(scan_data)

        # Сохраняем обратно
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Ошибка при сохранении IP данных: {e}")



def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def nmap_scan_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для сканирования портов через Nmap."""
    clear_frame(parent_frame)

    main_frame = ctk.CTkFrame(parent_frame, fg_color="#0f0f0f")
    main_frame.pack(fill="both", expand=True)

    # Основной контейнер (горизонтальный фрейм)
    container = ctk.CTkFrame(main_frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    keyboard_toggle_frame = ctk.CTkFrame(container, height=40)
    keyboard_toggle_frame.pack(side="bottom", fill="x")

    # Горизонтальный фрейм для заголовка и поля ввода
    top_row_frame = ctk.CTkFrame(container, fg_color="transparent")
    top_row_frame.pack(fill="x", padx=10, pady=(10, 0))

    label_title = ctk.CTkLabel(top_row_frame, text="Nmap Port Scanner", font=("Arial", 24))
    label_title.pack(side="left", padx=(0, 10))

    # Кнопка для начала сканирования
    scan_button = ctk.CTkButton(
        keyboard_toggle_frame,
        text="Start Scan",
        command=lambda: threading.Thread(target=run_scan, daemon=True).start(),
        font=("Arial", 16),
        fg_color="#000000",      # Чёрный фон
        text_color="#00FF00",    # Ярко-зелёный текст
        border_color="#00FF00",  # Зелёная рамка
        width=200,
        height=30
    )
    scan_button.pack(side="left", padx=10)

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        keyboard_toggle_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=200,
        height=30
    )
    back_button.pack(side="left", padx=10)

    # Кнопка "Сохранить результаты"
    save_button = ctk.CTkButton(
        keyboard_toggle_frame,
        text="Save Results",
        command=lambda: save_results(),
        font=("Arial", 16),
        width=200,
        height=30
    )
    save_button.pack(side="left", padx=10)

    entry_command = ctk.CTkEntry(
        top_row_frame,
        placeholder_text="Введите IP и флаги, например: 192.168.1.1 -sS -T4 -p 1-1000",
        font=("Arial", 16),
        width=400
    )
    entry_command.pack(side="left", fill="x", expand=True)

    menu_frame = ctk.CTkFrame(main_frame, width=700, fg_color="#08080A", corner_radius=10)

    commands_container = ctk.CTkScrollableFrame(menu_frame, width=650, height=300)
    commands_container.place(x=10, y=50)  # Под заголовками, с небольшим отступом

    for widget in commands_container.winfo_children():
        widget.destroy()

    for flags in nmap_flags:
        text = f"{flags['flag']} — {flags['description']}"
        nmap_flag = ctk.CTkLabel(commands_container, text=text, width=660, wraplength=650)
        nmap_flag.pack(pady=3)

    close_menu = ctk.CTkButton(menu_frame, text="X", width=50, height=50, command=lambda: animate_sidebar_close(menu_frame))
    close_menu.place(relx=0.99, rely=0.05, anchor="ne")
    close_menu.lift()

    sidebar_visible = False  # Флаг

    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            animate_sidebar_close(menu_frame)
            # sidebar_visible = False  <- убираем отсюда
        else:
            main_frame.update_idletasks()
            start_x = main_frame.winfo_width()
            target_x = start_x - 900
            menu_frame.place(x=start_x, y=0, relheight=1.0)
            animate_sidebar_open(menu_frame, target_x)
            sidebar_visible = True

    
    # Анимация появления
    def animate_sidebar_open(frame, target_x, step=20):
        current_x = main_frame.winfo_width()
        def slide():
            nonlocal current_x
            if current_x > target_x:
                current_x -= step
                frame.place(x=current_x, y=0, relheight=1.0)
                main_frame.after(10, slide)
            else:
                frame.place(x=target_x, y=0, relheight=1.0)
        slide()

    def animate_sidebar_close(frame, step=20):
        current_x = frame.winfo_x()
        target_x = main_frame.winfo_width()

        def slide():
            nonlocal current_x
            if current_x < target_x:
                current_x += step
                frame.place(x=current_x, y=0, relheight=1.0)
                main_frame.after(10, slide)
            else:
                frame.place_forget()
                nonlocal sidebar_visible
                sidebar_visible = False  # Меняем флаг здесь, после анимации закрытия
        slide()

    # TextBox для результатов (в верхней правой части)
    text_result = ctk.CTkTextbox(container, font=("Arial", 14))
    text_result.pack(fill="both", expand=True, padx=10, pady=10)

    # Нижняя часть (виртуальная клавиатура)
    bottom_frame = ctk.CTkFrame(container, height=400, width=600)
    bottom_frame.pack_propagate(True)  # чтобы высота сохранялась при скрытии

    hamburger_btn = ctk.CTkButton(
        main_frame,
        command=toggle_sidebar,
        text="☰",  # Символ гамбургера
        width=40,
        height=40,
        fg_color="#ff0000"  # Ярко-красный, чтобы точно было видно
    )
    hamburger_btn.place(relx=0.99, rely=0.1, anchor="ne")
    hamburger_btn.lift()

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

    def run_nmap_command(target, flags, text_widget):
        if platform.system() != "Windows":
            command = ["proxychains"] + ["nmap"] + flags + [target]
        else:
            command = ["nmap"] + flags + [target]
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            while True:
                line = proc.stdout.readline()
                if not line:

                    break
                text_widget.insert("end", line)
                text_widget.see("end")
                text_widget.update_idletasks()

            error = proc.stderr.read()

            if error:
                text_widget.insert("end", f"Error while scanning: {error}")
                text_widget.see("end")
            proc.wait()
        except subprocess.CalledProcessError as e:
            return f"Ошибка запуска nmap: {e}"

    def run_scan():
        text_result.delete("1.0", "end")
        full_input = entry_command.get()

        if not full_input:
            text_result.insert("end", "Please enter the target and flags\n")
            return

        parts = full_input.strip().split()
        target = parts[0]
        flags = parts[1:]

        current_time = time.strftime("%H:%M:%S", time.localtime())
        scan_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        text_result.insert("end", f"Scanning {target} started at {current_time} with flags: {' '.join(flags)}\n")
        text_result.update()

        run_nmap_command(target, flags, text_result)

        text_result.insert("end", "\nScanning is ended.\n")
        text_result.see("end")

        # Получаем результат сканирования
        scan_output = text_result.get("1.0", "end").strip()

        # Парсим минимальные данные
        open_ports = []
        os_info = "Unavailable"
        hostname = "Unavailable"

        for line in scan_output.splitlines():
            if "/tcp" in line or "/udp" in line:
                if "open" in line:
                    try:
                        port = int(line.split("/")[0])
                        open_ports.append(port)
                    except:
                        pass
            elif "Running:" in line:
                os_info = line.split("Running:")[1].strip()
            elif "Nmap scan report for" in line:
                parts = line.split("for")
                if len(parts) > 1:
                    hostname = parts[1].strip()

        # Обновляем scan_data
        scan_data[target] = {
            "country": "Unavailable",  # Можем подключить IP API позже
            "city": "Unavailable",
            "hostname": hostname,
            "os": os_info,
            "open_ports": open_ports,
            "last_checked": scan_timestamp
        }

        save_inf_to_the_IPMap()

    def save_results():
        if not os.path.exists("results"):
            os.makedirs("results")
        filename = f"results/{entry_command.get()}_scan_results.txt"
        with open(filename, "w") as file:
            file.write(text_result.get("1.0", "end"))

    # Виртуальная клавиатура в нижнем фрейме
    keyboard = NormalKeyboard(bottom_frame, entry_command)

    # Привязка клавиатуры
    entry_command.bind("<FocusIn>", lambda e: [set_target_entry(entry_command, "Command Input"), show_keyboard()])
    keyboard_visible = False

    def slide_keyboard(target_y, step=10):
        main_frame.update()
        container_width = container.winfo_width()
        x_pos = (container_width - keyboard_width) // 2

        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        main_frame.after(10, lambda: slide_keyboard(target_y, step))


    def show_keyboard():
        nonlocal keyboard_visible
        if keyboard_visible:
            return
        keyboard_visible = True
        slide_keyboard(target_y=main_frame.winfo_height() - 300)

    def hide_keyboard():
        nonlocal keyboard_visible
        if not keyboard_visible:
            return
        keyboard_visible = False
        slide_keyboard(target_y=main_frame.winfo_height())

    def toggle_keyboard():
        if keyboard_visible:
            hide_keyboard()
        else:
            show_keyboard()

    toggle_button = ctk.CTkButton(keyboard_toggle_frame, text="⌨ Клавиатура", command=toggle_keyboard)
    toggle_button.pack(pady=5)

    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    keyboard_width = 750
    keyboard_height = 500

    def place_keyboard_at(y_pos):
        main_frame.update()
        container_width = container.winfo_width()
        x_pos = (container_width - keyboard_width) // 2
        bottom_frame.place(in_=container, x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)

    # Изначально скрываем клавиатуру
    place_keyboard_at(main_frame.winfo_height())