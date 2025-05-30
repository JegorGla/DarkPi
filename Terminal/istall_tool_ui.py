import customtkinter as ctk
import platform
import subprocess
import threading

from virtual_keyboard import NormalKeyboard

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_install_tool_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    if platform.system() != "Linux":
        disagree_label = ctk.CTkLabel(
            parent_frame,
            text_color="#ffffff",
            text=f"Not supported on {platform.system()} OS!"
        )
        disagree_label.pack(pady=20)

        back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
        back_btn.pack(pady=10)
        return

    keyboard = None
    keyboard_visible = False
    active_entry = None  # Какое поле активно для клавиатуры

    def toggle_keyboard():
        nonlocal keyboard_visible, keyboard
        if keyboard_visible:
            keyboard.frame.place_forget()
            keyboard_visible = False
        else:
            if keyboard is None:
                keyboard = NormalKeyboard(parent_frame, active_entry)
            else:
                keyboard.target_entry = active_entry
            keyboard.frame.place(relx=0.5, rely=1.0, anchor="s")
            keyboard_visible = True

    def show_keyboard_for_entry(entry):
        nonlocal active_entry, keyboard_visible, keyboard
        active_entry = entry
        if keyboard is None:
            keyboard = NormalKeyboard(parent_frame, active_entry)
        else:
            keyboard.target_entry = active_entry

        if not keyboard_visible:
            keyboard.frame.place(relx=0.5, rely=1.0, anchor="s")
            keyboard_visible = True

    def hide_keyboard():
        nonlocal keyboard_visible
        if keyboard_visible:
            keyboard.frame.place_forget()
            keyboard_visible = False

    def install_tool():
        tool_name = tool_name_entry.get().strip()
        password = password_entry.get()

        if not tool_name:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("end", "Введите имя инструмента.\n")
            output_text.configure(state="disabled")
            return
        if not password:
            output_text.configure(state="normal")
            output_text.delete("1.0", "end")
            output_text.insert("end", "Введите пароль.\n")
            output_text.configure(state="disabled")
            return

        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("end", f"Установка {tool_name}...\n")
        output_text.configure(state="disabled")

        def run_install():
            try:
                # Используем sudo с передачей пароля через stdin
                cmd = ['sudo', '-S', 'apt', 'install', '-y', tool_name]
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                # Передаем пароль и \n
                stdout, _ = process.communicate(password + '\n')
                output_text.configure(state="normal")
                output_text.insert("end", stdout)
                output_text.configure(state="disabled")
                output_text.see("end")
            except Exception as e:
                output_text.configure(state="normal")
                output_text.insert("end", f"Ошибка: {e}\n")
                output_text.configure(state="disabled")

        threading.Thread(target=run_install, daemon=True).start()

    # Поля ввода
    tool_name_entry = ctk.CTkEntry(parent_frame, text_color="#ffffff", placeholder_text="Введите имя инструмента")
    tool_name_entry.pack(pady=(20, 10))
    tool_name_entry.bind("<FocusIn>", lambda e: show_keyboard_for_entry(tool_name_entry))

    password_entry = ctk.CTkEntry(parent_frame, text_color="#ffffff", placeholder_text="Введите пароль", show="*")
    password_entry.pack(pady=(0, 15))
    password_entry.bind("<FocusIn>", lambda e: show_keyboard_for_entry(password_entry))

    toggle_keyboard_btn = ctk.CTkButton(
        parent_frame,
        text="⌨ Переключить клавиатуру",
        command=lambda: toggle_keyboard(),
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        border_width=2,
        width=180,
        height=35
    )
    toggle_keyboard_btn.pack(pady=(0, 15))

    install_btn = ctk.CTkButton(
        parent_frame,
        text="Установить",
        command=install_tool,
        fg_color="#4CAF50",
        hover_color="#45a049",
        width=180,
        height=40
    )
    install_btn.pack(pady=(0, 15))

    output_text = ctk.CTkTextbox(parent_frame, width=700, height=200)
    output_text.pack(pady=(0, 20))
    output_text.configure(state="disabled")

    back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
    back_btn.pack(pady=10)
