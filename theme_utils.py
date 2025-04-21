# theme_utils.py

import customtkinter as ctk

def apply_theme_colors(widget):
    current_theme = ctk.get_appearance_mode()
    text_color = "#FFFFFF" if current_theme == "Dark" else "#000000"
    bg_color = "#000000" if current_theme == "Dark" else "#FFFFFF"

    if hasattr(widget, "configure"):
        config = widget.configure()
        if config:
            if "text_color" in config:
                widget.configure(text_color=text_color)
            if "fg_color" in config:
                widget.configure(fg_color=bg_color)

    for child in widget.winfo_children():
        apply_theme_colors(child)
