import customtkinter as ctk
from DDOS.slowloris_ui import slowloris_ui  # Импорт интерфейса Slowloris
import platform

# Функция для очистки всех виджетов в фрейме
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# ===== Цветовая анимация =====
def smooth_color_transition(button, start_color, end_color, step=30, delay=15):
    def update_color(index):
        r = int(start_color[1:3], 16) + index * (int(end_color[1:3], 16) - int(start_color[1:3], 16)) // step
        g = int(start_color[3:5], 16) + index * (int(end_color[3:5], 16) - int(start_color[3:5], 16)) // step
        b = int(start_color[5:7], 16) + index * (int(end_color[5:7], 16) - int(start_color[5:7], 16)) // step

        new_color = f"#{r:02x}{g:02x}{b:02x}"
        button.configure(fg_color=new_color)

        if index < step:
            button.after(delay, update_color, index + 1)

    update_color(0)

# ====== Интерфейс ======
def create_ddos_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Основные цвета
    default_color = "#000000"
    hover_color = "#FF6A00"

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="DDoS Attack 💀", font=("Arial", 24), text_color="#FF0000")
    title.place(relx=0.5, rely=0.1, anchor="center")

    # === SYN Flood Button ===
    syn_flood_button = ctk.CTkButton(
        parent_frame,
        text="SYN Flood",
        fg_color=default_color,
        border_color="#8d33ff",
        hover_color=None,  # отключаем встроенный hover
        border_width=2,
        font=("Arial", 16),
        command=lambda: print("SYN Flood Attack Initiated"),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    syn_flood_button.place(relx=0.5, rely=0.3, anchor="center")

    syn_flood_button.bind("<Enter>", lambda e: smooth_color_transition(syn_flood_button, default_color, hover_color))
    syn_flood_button.bind("<Leave>", lambda e: smooth_color_transition(syn_flood_button, hover_color, default_color))

    # === Slowloris Button ===
    slowloris_button = ctk.CTkButton(
        parent_frame,
        text="Slowloris",
        fg_color=default_color,
        border_color="#8d33ff",
        hover_color=None,
        border_width=2,
        font=("Arial", 16),
        command=lambda: slowloris_ui(parent_frame, go_back_callback),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    slowloris_button.place(relx=0.5, rely=0.4, anchor="center")

    OR = ctk.CTkLabel(parent_frame, text="OR", font=("Arial", 16), text_color="#FFFFFF")
    OR.place(relx=0.5, rely=0.45, anchor="center")

    install_btn = ctk.CTkButton(
        parent_frame,
        text="Install Linux dos tools",
        fg_color=default_color,
        border_color="#8d33ff",
        hover_color=None,
        border_width=2,
        font=("Arial", 16),
        command=lambda: print("Slowloris Installation Initiated"),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    install_btn.place(relx=0.5, rely=0.55, anchor="center")
    
    install_btn.bind("<Enter>", lambda e: smooth_color_transition(install_btn, default_color, hover_color))
    slowloris_button.bind("<Enter>", lambda e: smooth_color_transition(slowloris_button, default_color, hover_color))
    slowloris_button.bind("<Leave>", lambda e: smooth_color_transition(slowloris_button, hover_color, default_color))

    # Назад
    if go_back_callback:
        back_button = ctk.CTkButton(
            parent_frame,
            text="← Back",
            font=("Arial", 16),
            command=go_back_callback
        )
        back_button.place(relx=0.01, rely=0.01, anchor="nw")