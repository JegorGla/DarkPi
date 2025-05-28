import customtkinter as ctk
from virtual_keyboard import NumericKeyboard

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_setting_task_scheduler(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    # Поле ввода времени
    time_entry = ctk.CTkEntry(parent_frame, placeholder_text="Time to run command")
    time_entry.pack(pady=10)

    # Комбобокс
    tool = ctk.CTkComboBox(parent_frame, values=["Proxy"])
    tool.pack(pady=10)

    # Чекбокс
    is_every_day = ctk.CTkCheckBox(parent_frame, text="Every day")
    is_every_day.pack(pady=10)

    # Кнопка Назад
    back_btn = ctk.CTkButton(parent_frame, command=go_back_callback, text="Back")
    back_btn.pack(pady=10)

    # Рамка для клавиатуры
    bottom_frame = ctk.CTkFrame(parent_frame, height=300)
    bottom_frame.pack_propagate(False)

    # Инициализация клавиатуры
    keyboard = NumericKeyboard(bottom_frame, time_entry)

    # Размеры клавиатуры
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

    # Кнопка показа/скрытия клавиатуры
    toggle_button = ctk.CTkButton(parent_frame, text="⌨ Клавиатура", command=toggle_keyboard)
    toggle_button.pack(pady=10)

    # Показ клавиатуры при фокусе
    time_entry.bind("<FocusIn>", lambda e: show_keyboard())

    # Изначально скрыта
    place_keyboard_at(parent_frame.winfo_height())
