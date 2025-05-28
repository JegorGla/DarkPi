import customtkinter as ctk

def clear_frame(frame):
    """
    Clear all widgets from the given frame.
    """
    for widget in frame.winfo_children():
        widget.destroy()

def creat_look_at_list_of_proxy(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    viev_frame = ctk.CTkScrollableFrame(
        parent_frame,
        width=parent_frame.winfo_width() - 250,
        height=parent_frame.winfo_height() - 400,
        corner_radius=10
    )
    viev_frame.pack(pady=(10, 20), padx=10, fill="both", expand=True)

    with open("working_proxies.txt", "r") as f:
        proxy_list = f.readlines()

    for i, proxy in enumerate(proxy_list):
        proxy_label = ctk.CTkLabel(
            viev_frame,
            text=proxy.strip(),
            font=("Arial", 14)
        )
        proxy_label.pack(pady=5)
    
    back_btn = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=go_back_callback,
        fg_color="black",
        border_color="#323232",
        border_width=2,
        hover_color="#323232"
    )
    back_btn.pack(pady=10)