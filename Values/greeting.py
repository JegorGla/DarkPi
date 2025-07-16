import customtkinter as ctk
import os
import json

def set_allowed_anim(value: bool):
    try:
        settings = {}

        # Если файл существует, загрузить его содержимое
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)

        # Обновляем или добавляем ключ
        settings["allowed_anim"] = value

        # Записываем обратно обновлённый словарь
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    except Exception as e:
        print("Ошибка при записи файла:", e)


def show_greeting(parent_frame, callback=None):
    """Показывает приветствие Welcome с fade-in и fade-out, затем вызывает callback."""
    set_allowed_anim(False)
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
        set_allowed_anim(True)
        if callback:
            callback()

    # Анимация: появление → задержка → исчезновение → callback
    fade(greeting_label, start=0, end=1, step=0.05, delay=30, on_complete=lambda:
        parent_frame.after(1500, lambda: fade(greeting_label, start=1, end=0, step=-0.05, delay=30, on_complete=finish)))
