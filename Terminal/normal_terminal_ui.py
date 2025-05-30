import customtkinter as ctk
import subprocess
import threading
import os
import getpass
import socket

from virtual_keyboard import NormalKeyboard

def get_prompt():
    user = getpass.getuser()                  # имя пользователя
    hostname = socket.gethostname()           # имя хоста
    cwd = os.getcwd()                         # текущая рабочая директория

    # Для красоты показываем ~ вместо полного пути домашней директории
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd_display = "~" + cwd[len(home):]
    else:
        cwd_display = cwd

    return f"{user}@{hostname}:{cwd_display}$ "


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def execute_command():
    command = command_entry.get()
    if not command.strip():
        return

    output_box.configure(state="normal")
    output_box.insert("end", get_prompt())
    output_box.configure(state="disabled")
    output_box.see("end")
    command_entry.delete(0, "end")

    def run():
        try:
            process = subprocess.Popen(
                command, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            for line in process.stdout:
                output_box.configure(state="normal")
                output_box.insert("end", line)
                output_box.configure(state="disabled")
                output_box.see("end")
            process.wait()
        except Exception as e:
            output_box.configure(state="normal")
            output_box.insert("end", f"Error: {e}\n")
            output_box.configure(state="disabled")
            output_box.see("end")
        finally:
            output_box.configure(state="normal")
            output_box.insert("end", get_prompt())
            output_box.configure(state="disabled")
            output_box.see("end")
            command_entry.focus_set()


    threading.Thread(target=run, daemon=True).start()

def create_normal_terminal_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    global command_entry, output_box

    # Output window
    output_box = ctk.CTkTextbox(main_frame, width=600, height=int(parent_frame.winfo_height() * 0.5))
    output_box.pack(padx=10, pady=10)
    output_box.configure(state="disabled")

    # Command entry
    command_entry = ctk.CTkEntry(main_frame, width=600, text_color="#ffffff", placeholder_text="Input command...")
    command_entry.pack(padx=10, pady=(0, 10))
    command_entry.bind("<Return>", lambda event: execute_command())

    # Убираем pack у bottom_frame, используем place только
    bottom_frame = ctk.CTkFrame(main_frame)
    # НЕ вызываем bottom_frame.pack()

    close_keyboard_button = ctk.CTkButton(
        bottom_frame,
        text="X",
        font=("Arial", 25),
        command=lambda: hide_keyboard(),
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        width=50,
        height=50,
        border_width=2
    )
    close_keyboard_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    # Optional back button
    back_button = ctk.CTkButton(main_frame, text="Back", command=go_back_callback)
    back_button.pack(pady=5)

    # Переменная для хранения активного поля
    active_entry = None
    def set_target_entry(entry, name):
        nonlocal active_entry
        active_entry = entry
        keyboard.target_entry = entry
        #print(f"[DEBUG] Активное поле ввода: {name}")

    # Виртуальная клавиатура в нижнем фрейме
    keyboard = None  # Клавиатура будет создана позже


    # Привязка клавиатуры к полям ввода
    command_entry.bind("<FocusIn>", lambda e: [set_target_entry(command_entry, "Target (IP/Domain)"), show_keyboard()])

    keyboard_visible = False

    def slide_keyboard(target_y, step=10):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2

        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        parent_frame.after(10, lambda: slide_keyboard(target_y, step))


    def show_keyboard():
        nonlocal keyboard_visible, keyboard
        if keyboard_visible:
            return

        if keyboard is None:
            keyboard = NormalKeyboard(bottom_frame, command_entry)
            # Привязка только при первом создании:
            command_entry.bind("<FocusIn>", lambda e: [set_target_entry(command_entry, "Target (IP/Domain)"), show_keyboard()])

        keyboard_visible = True
        slide_keyboard(target_y=parent_frame.winfo_height() - 300)
        bottom_frame.lift()  # Поднять клавиатуру поверх других виджетов


    def hide_keyboard():
        nonlocal keyboard_visible
        if not keyboard_visible:
            return
        keyboard_visible = False
        slide_keyboard(target_y=parent_frame.winfo_height())

    def toggle_keyboard():
        if keyboard_visible:
            hide_keyboard()
        else:
            show_keyboard()

    toggle_button = ctk.CTkButton(
        main_frame,
        text="⌨ Клавиатура",
        command=toggle_keyboard,
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        border_width=2
    )
    toggle_button.pack(side="left", padx=10)


    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    keyboard_width = 750
    keyboard_height = 300

    def place_keyboard_at(y_pos):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2
        bottom_frame.place(in_=parent_frame, x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)
        bottom_frame.lift()  # Поднять клавиатуру поверх других виджетов

    place_keyboard_at(parent_frame.winfo_height())  # Скрыть сразу (внизу за пределами окна)