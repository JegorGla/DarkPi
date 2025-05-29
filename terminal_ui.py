import customtkinter as ctk

from Terminal.normal_terminal_ui import create_normal_terminal_ui

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def terminal_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    terminal_btn = ctk.CTkButton(parent_frame, text="Terminal", command=lambda: create_normal_terminal_ui(parent_frame, go_back_callback))
    terminal_btn.pack(pady=10)

    install_tool = ctk.CTkButton(parent_frame, text="Install tool")
    install_tool.pack(pady=10)

    back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
    back_btn.pack(pady=10)