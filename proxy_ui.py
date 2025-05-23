import customtkinter as ctk
from Proxy.get_proxy import create_get_proxy_ui
from Proxy.proxy_setting import create_proxy_setting_frame

def clear_frame(frame):
    """
    Clear all widgets from the given frame.
    """
    for widget in frame.winfo_children():
        widget.destroy()

def create_proxy_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    get_proxy_btn = ctk.CTkButton(
        parent_frame,
        text="Get Proxy",
        command=lambda: create_get_proxy_ui(parent_frame, go_back_callback)
    )
    get_proxy_btn.pack(pady=10)

    proxy_sett = ctk.CTkButton(
        parent_frame,
        text="Proxy Settings",
        command=lambda: create_proxy_setting_frame(parent_frame, go_back_callback)
    )
    proxy_sett.pack(pady=10)

    back_btn = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=go_back_callback
    )
    back_btn.pack(pady=10)