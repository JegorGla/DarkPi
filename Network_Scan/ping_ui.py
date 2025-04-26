import customtkinter as ctk
import subprocess
import threading

def ping_target(target_ip):
    """Функция для пинга целевого IP через subprocess."""
    try:
        result = subprocess.run(["ping", target_ip], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Ошибка: {str(e)}"

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def ping_scan_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для Ping Scan."""
    clear_frame(parent_frame)

    label_title = ctk.CTkLabel(parent_frame, text="Ping Scan", font=("Arial", 24))
    label_title.pack(pady=10)

    ip_target = ctk.CTkEntry(
        parent_frame,
        placeholder_text="Enter target IP",
        font=("Arial", 16),
        width=300,
        height=40
    )
    ip_target.place(relx=0.5, rely=0.2, anchor='center')

    # Создаем текстбокс сразу для вывода результатов
    output_textbox = ctk.CTkTextbox(parent_frame, width=500, height=250, font=("Arial", 14))
    output_textbox.place(relx=0.5, rely=0.65, anchor="center")

    def do_ping_scan():
        """Запуск пинга в отдельном потоке."""
        output_textbox.delete("1.0", "end")  # Очищаем старый текст
        output_textbox.insert("end", "Pinging...\n")  # Начальный текст

        def ping_thread():
            """Функция для выполнения пинга в потоке."""
            target_ip = ip_target.get()
            result = ping_target(target_ip)
            output_textbox.delete("1.0", "end")  # Очищаем старый текст
            output_textbox.insert("end", result)  # Вставляем новый результат

        # Создаем и запускаем поток
        ping_threading = threading.Thread(target=ping_thread)
        ping_threading.start()

    ping_button = ctk.CTkButton(
        parent_frame,
        text="Ping Scan",
        command=do_ping_scan,
        font=("Arial", 16),
        width=200,
        height=40
    )
    ping_button.place(relx=0.5, rely=0.35, anchor='center')

    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=200,
        height=40
    )
    back_button.place(relx=0.5, rely=0.45, anchor='center')