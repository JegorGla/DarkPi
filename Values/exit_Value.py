import customtkinter as ctk
import platform
import os
import sys

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def shutdown_device():
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("shutdown /s /t 1")
    elif system_platform in ("Linux", "Darwin"):
        os.system("shutdown -h now")
    else:
        print("Shutdown not supported on this OS.")

def restart_device():
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("shutdown /r /t 1")
    elif system_platform in ("Linux", "Darwin"):
        os.system("shutdown -r now")
    else:
        print("Restart not supported on this OS.")

def exit_values(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    parent_frame.update_idletasks()

    # Размеры окна
    parent_width = parent_frame.winfo_width()
    parent_height = parent_frame.winfo_height()

    # Размеры exit_frame
    frame_height = parent_height // 2
    frame_width = parent_width // 2  # Сделаем шире, чем 1/5

    # Центрируем exit_frame
    exit_frame = ctk.CTkFrame(parent_frame, width=frame_width, height=frame_height)
    exit_frame.place(relx=0.5, rely=0.5, anchor="center")
    exit_frame.pack_propagate(False)

    # Заголовок
    title = ctk.CTkLabel(exit_frame, text="Выберите действие", font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(pady=(10, 15))

    # Фрейм для кнопок
    btn_frame = ctk.CTkFrame(exit_frame)
    btn_frame.pack(pady=5)

    btn_width = 120
    btn_height = 40

    # Верхний ряд кнопок
    exit_btn = ctk.CTkButton(btn_frame, text="Exit", width=btn_width, height=btn_height, command=sys.exit)
    shutdown_btn = ctk.CTkButton(btn_frame, text="Power off", width=btn_width, height=btn_height, command=shutdown_device)
    restart_btn = ctk.CTkButton(btn_frame, text="Reboot", width=btn_width, height=btn_height, command=restart_device)

    exit_btn.grid(row=0, column=0, padx=10, pady=10)
    shutdown_btn.grid(row=0, column=1, padx=10, pady=10)
    restart_btn.grid(row=0, column=2, padx=10, pady=10)

    # Нижний ряд — кнопка "Back"
    back_btn = ctk.CTkButton(btn_frame, text="Back", width=btn_width * 3 + 40, height=btn_height, command=go_back_callback)
    back_btn.grid(row=1, column=0, columnspan=3, pady=(20, 10))
