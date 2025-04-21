import customtkinter as ctk

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def init_settings_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Добавляем заголовок
    title = ctk.CTkLabel(parent_frame, text="Настройки", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")  # Используем place для позиционирования

    # Кнопка "Сохранить настройки"
    save_btn = ctk.CTkButton(parent_frame, text="Сохранить настройки", command=lambda: print("Настройки сохранены"))
    save_btn.place(relx=0.5, rely=0.4, anchor="center")  # Используем place для позиционирования

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
    back_btn.place(relx=0.5, rely=0.7, anchor="center")  # Используем place для позиционирования