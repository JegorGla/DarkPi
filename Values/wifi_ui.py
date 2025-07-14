import customtkinter as ctk

from Wifi.wifi_settings import create_wifi_ui
from Wifi.check_ip_ui import check_ip_ui
from Wifi.find_ip_in_local import find_ip_in_local_ui

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_main_wifi_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для подключения к Wi-Fi."""
    clear_frame(parent_frame)

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="Wi-Fi", font=("Arial", 24))
    label_title.pack(pady=10)

    #####============Wifi connect=================#####
    wifi_connect_button = ctk.CTkButton(
        parent_frame,
        text="Wifi Settings",
        command=lambda: create_wifi_ui(parent_frame, go_back_callback),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    wifi_connect_button.place(relx=0.5, rely=0.4, anchor="center")
    #==================================================

    #==============Check IP===================
    check_ip_button = ctk.CTkButton(
        parent_frame,
        text="Check IP",
        command=lambda: check_ip_ui(parent_frame, go_back_callback),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    check_ip_button.place(relx=0.5, rely=0.5, anchor="center")
    #==========================================

    #====================Find ip in local button===================
    find_ip_button = ctk.CTkButton(
        parent_frame,
        text="Find IP in Local",
        command=lambda: find_ip_in_local_ui(parent_frame, go_back_callback),
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    find_ip_button.place(relx=0.5, rely=0.6, anchor="center")
    #====================Back button===================
    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    back_button.place(relx=0.5, rely=0.7, anchor="center")
    #==================================================

