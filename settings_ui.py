import customtkinter as ctk

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def init_settings_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback)
    back_btn.place(relx=0.01, rely=0.01, anchor="nw")

    # ==== Блок Use Proxies ====
    # Контейнер-фрейм для строки с текстом и чекбоксом
    setting_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    setting_frame.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.9)

    #====================Proxy Settings====================
    setting_label = ctk.CTkLabel(setting_frame, text="Use proxies", anchor="w", font=("Arial", 16))
    setting_label.pack(side="left", fill="x", expand=True)

    # Чекбокс
    use_proxies_var = ctk.BooleanVar()
    checkbox = ctk.CTkCheckBox(setting_frame, variable=use_proxies_var, text="")
    checkbox.pack(side="right")
    #========================================================

    # Горизонтальная линия под блоком
    separator = ctk.CTkFrame(parent_frame, height=1, fg_color="#444444")
    separator.place(relx=0.05, rely=0.3, relwidth=0.9)
