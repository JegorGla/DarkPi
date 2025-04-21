import customtkinter as ctk
from theme_utils import apply_theme_colors

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

def init_settings_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)  # очищаем перед загрузкой UI

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Настройки", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Переключатель темы (CheckBox)
    def on_theme_toggle():
        toggle_theme()
        apply_theme_colors(parent_frame)  # <--- Обновляем цвета после смены темы
    theme_checkbox = ctk.CTkCheckBox(
        parent_frame,
        text="Тёмная тема",
        command=on_theme_toggle
    )
    # Устанавливаем изначальное состояние чекбокса в зависимости от текущей темы
    if ctk.get_appearance_mode() == "Dark":
        theme_checkbox.select()
    else:
        theme_checkbox.deselect()

    theme_checkbox.place(relx=0.5, rely=0.3, anchor="center")

    # Кнопка "Сохранить настройки"
    save_btn = ctk.CTkButton(parent_frame, text="Сохранить настройки", command=lambda: print("Настройки сохранены"))
    save_btn.place(relx=0.5, rely=0.4, anchor="center")

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
    back_btn.place(relx=0.5, rely=0.7, anchor="center")