import customtkinter as ctk
import os

def show_greeting(parent_frame, callback=None):
    """Показывает приветствие Welcome с fade-in и fade-out, затем вызывает callback."""

    greeting_frame = ctk.CTkFrame(parent_frame, fg_color="black")
    greeting_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    greeting_label = ctk.CTkLabel(
        greeting_frame,
        text=f"Welcome to the DarkPi,\n{os.getlogin()}!",
        font=("Arial", 24),
        text_color="#000000"
    )
    greeting_label.place(relx=0.5, rely=0.4, anchor="center")

    # Fade-функция
    def fade(widget, start, end, step, delay, on_complete=None):
        def _fade(opacity=start):
            if (step > 0 and opacity <= end) or (step < 0 and opacity >= end):
                val = int(255 * opacity)
                color = f"#{val:02x}{val:02x}{val:02x}"
                widget.configure(text_color=color)
                parent_frame.after(delay, _fade, opacity + step)
            else:
                if on_complete:
                    on_complete()
        _fade()

    def finish():
        greeting_frame.destroy()
        if callback:
            callback()

    # Анимация: появление → задержка → исчезновение → callback
    fade(greeting_label, start=0, end=1, step=0.05, delay=30, on_complete=lambda:
        parent_frame.after(1500, lambda: fade(greeting_label, start=1, end=0, step=-0.05, delay=30, on_complete=finish)))
