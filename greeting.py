import customtkinter as ctk
import os

def show_greeting(parent_frame, callback=None, delay_ms=3000):
    """Показывает приветствие с анимацией и скрывает автоматически через delay_ms."""
    greeting_frame = ctk.CTkFrame(parent_frame, fg_color="black")
    greeting_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    greeting_label = ctk.CTkLabel(
        greeting_frame,
        text=f"Welcome to the DarkPi,\n{os.getlogin()}!",
        font=("Arial", 24),
        text_color="white"
    )
    greeting_label.place(relx=0.5, rely=0.4, anchor="center")

    # Fade-in
    def fade_in_text(opacity=0):
        if opacity <= 1:
            hex_color = f"#{int(255 * opacity):02x}{int(255 * opacity):02x}{int(255 * opacity):02x}"
            greeting_label.configure(text_color=hex_color)
            parent_frame.after(50, fade_in_text, opacity + 0.05)

    # Fade-out
    def fade_out_text(opacity=1):
        if opacity >= 0:
            hex_color = f"#{int(255 * opacity):02x}{int(255 * opacity):02x}{int(255 * opacity):02x}"
            greeting_label.configure(text_color=hex_color)
            parent_frame.after(50, fade_out_text, opacity - 0.05)
        else:
            greeting_frame.destroy()
            if callback:
                callback()

    fade_in_text(0)

    # Запуск fade-out после задержки
    parent_frame.after(delay_ms, lambda: fade_out_text(1))