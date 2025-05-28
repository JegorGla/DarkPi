import customtkinter as ctk
from Proxy.get_proxy import create_get_proxy_ui
from Proxy.proxy_setting import create_proxy_setting_frame
from Proxy.list_of_proxy import creat_look_at_list_of_proxy

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
        command=lambda: create_get_proxy_ui(parent_frame, go_back_callback),
        fg_color="black",
        border_color="#323232",
        border_width=2,
        hover_color="#323232",
        width=parent_frame.winfo_width() - 250
    )
    get_proxy_btn.pack(pady=10)

    proxy_sett = ctk.CTkButton(
        parent_frame,
        text="Proxy Settings",
        command=lambda: create_proxy_setting_frame(parent_frame, go_back_callback),
        fg_color="black",
        border_color="#323232",
        border_width=2,
        hover_color="#323232",
        width=parent_frame.winfo_width() - 250
    )
    proxy_sett.pack(pady=10)

    proxy_list = ctk.CTkButton(
        parent_frame,
        text="Proxy List",
        command=lambda: creat_look_at_list_of_proxy(parent_frame, go_back_callback),
        fg_color="black",
        border_color="#323232",
        border_width=2,
        hover_color="#323232",
        width=parent_frame.winfo_width() - 250
    )
    proxy_list.pack(pady=10)

    back_btn = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=go_back_callback,
        fg_color="black",
        border_color="#323232",
        border_width=2,
        hover_color="#323232",
        height=40
    )
    back_btn.pack(pady=10)