import customtkinter as ctk

from Bruteforce.bruteforce import init_classic_bruteforce_ui  # Импортируем класс Bruteforce из файла bruteforce.py

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def init_bruteforce_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Добавляем заголовок
    title = ctk.CTkLabel(parent_frame, text="Bruteforce Attack Interface", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")  # Используем place для позиционирования

    # Создаём кнопки для видов брутфорса
    classic_btn = ctk.CTkButton(parent_frame, text="Classic BruteForce", command=lambda: init_classic_bruteforce_ui(parent_frame, go_back_callback))
    classic_btn.place(relx=0.5, rely=0.25, anchor="center")

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback)
    back_btn.place(relx=0.5, rely=0.7, anchor="center")  # Используем place для позиционирования