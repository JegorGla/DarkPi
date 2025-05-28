import customtkinter as ctk
import threading
from TaskScheduler.Proxy.proxy import main

stop_flag = threading.Event()  # глобальный флаг

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def proxy_task_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    quantity_of_proxies = ctk.CTkEntry(
        parent_frame,
        placeholder_text="Enter number of proxies",
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    quantity_of_proxies.pack(pady=10)

    def start_proxy_task(quantity):
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError as e:
            ctk.CTkLabel(parent_frame, text=str(e)).pack()
            return

        # Сбрасываем флаг остановки и запускаем новый поток
        stop_flag.clear()
        thread = threading.Thread(target=run_proxy_task, args=(quantity,), daemon=True)
        thread.start()

    def run_proxy_task(quantity):
        try:
            with open("working_proxies.txt", "r") as file:
                proxies = [line.strip() for line in file if line.strip()]
                proxies = list(set(proxies))

            if len(proxies) < quantity:
                main(quantity, stop_flag)  # передаём флаг корректно
            else:
                print("Достаточно прокси, задача не запущена.")
        except Exception as e:
            print("Ошибка в run_proxy_task:", e)

    ctk.CTkButton(
        parent_frame,
        text="Start Proxy Task",
        command=lambda: start_proxy_task(quantity_of_proxies.get()),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    ).pack(pady=10)

    ctk.CTkButton(parent_frame, command=go_back_callback, text="Back").pack(pady=10)
