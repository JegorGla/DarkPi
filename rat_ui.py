import customtkinter as ctk
from RAT.server import server

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_rat_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Заголовок
    title_label = ctk.CTkLabel(parent_frame, text="Remote Access Tool (RAT)", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(pady=(20, 10))

    command_line = ctk.CTkButton(parent_frame, text="💻 Command line", command=lambda: server(parent_frame, go_back_callback))
    command_line.pack(pady=10)

    # Кнопка "назад"
    if go_back_callback:
        back_btn = ctk.CTkButton(
            parent_frame, 
            text="← Back", 
            command=go_back_callback, 
            fg_color="transparent", 
            text_color="blue", 
            hover_color="#e0e0e0"
        )
        back_btn.pack(pady=(30, 10))

