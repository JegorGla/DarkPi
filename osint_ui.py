import customtkinter as ctk
from Osint.find_user_ui import create_find_user_ui
from Osint.email_osint import email_osint
from Osint.phone_number_osint import create_PN_ui
from virtual_keyboard import NormalKeyboard
import threading
import os

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_osint_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    fnd_usr = ctk.CTkButton(parent_frame, text="Find User", command=lambda: create_find_user_ui(parent_frame, go_back_callback), width=150, height=50)
    fnd_usr.pack(pady=10)

    osint_email = ctk.CTkButton(parent_frame, text="Check Email", command= lambda: email_osint(parent_frame, go_back_callback), width=150, height=50)
    osint_email.pack(pady=10)

    osint_number = ctk.CTkButton(parent_frame, text="Check Phone Numer", command=lambda: create_PN_ui(parent_frame, go_back_callback), width=150, height=50)
    osint_number.pack(pady=10)

    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback, height=40, width=200, corner_radius=10, fg_color="#f44336", hover_color="#e53935")
    back_btn.pack(pady=10)