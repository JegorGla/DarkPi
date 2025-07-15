import customtkinter as ctk
from DOS.slowloris_ui import slowloris_ui
from DOS.ICMP_flood import create_icmp_flood_ui
from DOS.UDP_flood import create_udp_flood_ui
import platform

# Функция для очистки всех виджетов в фрейме
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# ====== Интерфейс ======
def create_ddos_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Основные цвета
    default_color = "#000000"
    
    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="DDoS Attack 💀", font=("Arial", 24), text_color="#FF0000")
    title.place(relx=0.5, rely=0.1, anchor="center")

    # === SYN Flood Button ===
    syn_flood_button = ctk.CTkButton(
        parent_frame,
        text="SYN Flood",
        fg_color=default_color,
        border_color="#8d33ff",
        border_width=2,
        font=("Arial", 16),
        command=lambda: print("SYN Flood Attack Initiated"),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    syn_flood_button.place(relx=0.5, rely=0.3, anchor="center")

    # === Slowloris Button ===
    slowloris_button = ctk.CTkButton(
        parent_frame,
        text="Slowloris",
        fg_color=default_color,
        border_color="#8d33ff",
        border_width=2,
        font=("Arial", 16),
        command=lambda: slowloris_ui(parent_frame, go_back_callback),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    slowloris_button.place(relx=0.5, rely=0.4, anchor="center")

    #=== ICMP Flood Button ===
    icmp_flood_button = ctk.CTkButton(
        parent_frame,
        text="ICMP Flood",
        fg_color=default_color,
        border_color="#8d33ff",
        border_width=2,
        font=("Arial", 16),
        command=lambda: create_icmp_flood_ui(parent_frame, go_back_callback),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    icmp_flood_button.place(relx=0.5, rely=0.5, anchor="center")

    #=== UDP Flood Button ===
    udp_flood_button = ctk.CTkButton(
        parent_frame,
        text="UDP Flood",
        fg_color=default_color,
        border_color="#8d33ff",
        border_width=2,
        font=("Arial", 16),
        command=lambda: create_udp_flood_ui(parent_frame, go_back_callback),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    udp_flood_button.place(relx=0.5, rely=0.6, anchor="center")

    # Назад
    if go_back_callback:
        back_button = ctk.CTkButton(
            parent_frame,
            text="← Back",
            font=("Arial", 16),
            command=go_back_callback
        )
        back_button.place(relx=0.01, rely=0.01, anchor="nw")