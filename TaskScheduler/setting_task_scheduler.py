import customtkinter as ctk
from virtual_keyboard import NumericKeyboard
import json
from datetime import datetime

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_setting_task_scheduler(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    current_year = datetime.now().year

    # Комбобокс
    tool = ctk.CTkComboBox(parent_frame, values=["Proxy"])
    tool.pack(pady=10)

    # Чекбокс "Every day"
    is_every_day = ctk.CTkCheckBox(parent_frame, text="Every day")
    is_every_day.pack(pady=10)

    # ====== Поля для даты и времени ======
    year_entry = ctk.CTkEntry(parent_frame, placeholder_text="Year")
    year_entry.insert(0, str(current_year))

    month_entry = ctk.CTkEntry(parent_frame, placeholder_text="Month")
    day_entry = ctk.CTkEntry(parent_frame, placeholder_text="Day")

    hour_entry = ctk.CTkEntry(parent_frame, placeholder_text="Hour")
    minute_entry = ctk.CTkEntry(parent_frame, placeholder_text="Minute")

    # Показываем по умолчанию
    year_entry.pack(pady=5)
    month_entry.pack(pady=5)
    day_entry.pack(pady=5)
    hour_entry.pack(pady=5)
    minute_entry.pack(pady=5)

    def update_visibility():
        if is_every_day.get() == 1:
            year_entry.pack_forget()
            month_entry.pack_forget()
            day_entry.pack_forget()
            hour_entry.pack(pady=10)
            minute_entry.pack(pady=10)
        else:
            year_entry.pack(pady=5)
            month_entry.pack(pady=5)
            day_entry.pack(pady=5)
            hour_entry.pack_forget()
            minute_entry.pack_forget()

    is_every_day.configure(command=update_visibility)

    def save_settings():
        # Формируем строку времени
        if is_every_day.get() == 1:
            time_to_run = f"{hour_entry.get()}:{minute_entry.get()}"
        else:
            time_to_run = f"{year_entry.get()}-{month_entry.get()}-{day_entry.get()} {hour_entry.get()}:{minute_entry.get()}"

        # Загружаем текущие настройки, если они есть
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            settings = {}

        # Обновляем или добавляем task_scheduler
        settings["task_scheduler"] = {
            "tool": tool.get(),
            "time": time_to_run,
            "every_day": is_every_day.get() == 1
        }

        # Перезаписываем файл с обновлёнными данными
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

        print("Settings updated.")

    save_btn = ctk.CTkButton(parent_frame, text="Save settings", command=save_settings)
    save_btn.pack(pady=10)

    back_btn = ctk.CTkButton(parent_frame, command=go_back_callback, text="Back")
    back_btn.pack(pady=10)

    # ====== Встроенная клавиатура ======
    bottom_frame = ctk.CTkFrame(parent_frame, height=300)
    bottom_frame.pack_propagate(False)

    keyboard = NumericKeyboard(bottom_frame, hour_entry)  # по умолчанию — на часах

    keyboard_width = 750
    keyboard_height = 150
    keyboard_visible = False

    def place_keyboard_at(y_pos):
        parent_frame.update()
        frame_width = parent_frame.winfo_width()
        x_pos = (frame_width - keyboard_width) // 2
        bottom_frame.place(x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)

    def slide_keyboard(target_y, step=10):
        parent_frame.update()
        frame_width = parent_frame.winfo_width()
        x_pos = (frame_width - keyboard_width) // 2
        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        parent_frame.after(10, lambda: slide_keyboard(target_y, step))

    def show_keyboard():
        nonlocal keyboard_visible
        if not keyboard_visible:
            keyboard_visible = True
            slide_keyboard(parent_frame.winfo_height() - keyboard_height)

    def hide_keyboard():
        nonlocal keyboard_visible
        if keyboard_visible:
            keyboard_visible = False
            slide_keyboard(parent_frame.winfo_height())

    def toggle_keyboard():
        if keyboard_visible:
            hide_keyboard()
        else:
            show_keyboard()

    toggle_button = ctk.CTkButton(parent_frame, text="⌨ Клавиатура", command=toggle_keyboard)
    toggle_button.pack(pady=10)

    # Подключаем клавиатуру к каждому полю ввода
    for entry in [year_entry, month_entry, day_entry, hour_entry, minute_entry]:
        entry.bind("<FocusIn>", lambda e, ent=entry: (keyboard.set_target(ent), show_keyboard()))

    place_keyboard_at(parent_frame.winfo_height())
