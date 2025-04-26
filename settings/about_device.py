import os
import customtkinter as ctk
import platform

def clear_frame(frame):
    """Очистка фрейма от всех виджетов."""
    for widget in frame.winfo_children():
        widget.destroy()

def about_device_ui(parent_frame, go_back_callback=None):
    """Отображение информации об устройстве."""
    clear_frame(parent_frame)  # Очистить перед созданием UI

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="About Device", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Информация об устройстве
    try:
        uname = os.uname()
        device_info = {
            "OS": uname.sysname,
            "Node Name": uname.nodename,
            "Release": uname.release,
            "Version": uname.version,
            "Machine": uname.machine,
            "Processor": platform.processor(),
        }
    except AttributeError:
        # Для Windows fallback через platform
        device_info = {
            "OS": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
        }

    # Отображение информации
    for i, (key, value) in enumerate(device_info.items()):
        label = ctk.CTkLabel(parent_frame, text=f"{key}: {value}", font=("Arial", 16))
        label.place(relx=0.5, rely=0.3 + i * 0.05, anchor="center")

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(
        parent_frame, 
        text="← Back", 
        command=lambda: go_back_callback() if go_back_callback else None, 
        font=("Arial", 16)
    )
    back_btn.place(relx=0.5, rely=0.9, anchor="center")