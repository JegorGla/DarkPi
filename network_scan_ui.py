import customtkinter as ctk
import os

from Network_Scan.nmap_scan import nmap_scan_ui

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def ns_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для Network Scan."""
    clear_frame(parent_frame)

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Network Scan", font=("Arial", 24))
    label_title.pack(pady=10)

    #=============Nmap scan button=====================
    nmap_button = ctk.CTkButton(
        parent_frame,
        text="Nmap Scan",
        command=lambda: nmap_scan_ui(parent_frame, go_back_callback),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    nmap_button.place(relx=0.5, rely=0.3, anchor='center')
    #===================================================

    #=================Back button===================
    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    back_button.place(relx=0.5, rely=0.5, anchor='center')