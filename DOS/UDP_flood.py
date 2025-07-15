import customtkinter as ctk
import socket
from ping3 import ping
import threading
import time
import sys

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_udp_flood_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="UDP Flood Attack", font=("Arial", 24))
    label_title.pack(pady=10)

    # Поле для ввода IP адреса
    ip_label = ctk.CTkLabel(parent_frame, text="Target IP:")
    ip_label.pack(pady=5)
    ip_entry = ctk.CTkEntry(parent_frame, width=300)
    ip_entry.pack(pady=5)

    # Поле для ввода порта
    port_label = ctk.CTkLabel(parent_frame, text="Target Port:")
    port_label.pack(pady=5)
    port_entry = ctk.CTkEntry(parent_frame, width=300)
    port_entry.pack(pady=5)

    # Кнопка запуска атаки
    start_button = ctk.CTkButton(
        parent_frame,
        text="Start UDP Flood",
        #command=lambda: start_udp_flood(ip_entry.get(), int(port_entry.get())),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    start_button.pack(pady=20)

    # Кнопка возврата
    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    back_button.pack(pady=10)