import customtkinter as ctk
import json
from tkinter.colorchooser import askcolor

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def load_theme_settings():
    try:
        with open("theme.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "button_color": "#1f6aa5",
            "label_color": "#ffffff",
            "text_color": "#ffffff",
            "bg_color": "#121212",
            "entry_color": "#2e2e2e"
        }

def save_theme_settings(theme_name: str):
    try:
        with open("settings.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data["theme"] = theme_name
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump({"theme": theme_name}, f, indent=4)


def create_customization_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)
    settings = load_theme_settings()

    # Вкладки
    tabs = ctk.CTkTabview(parent_frame, width=380, height=400)
    tabs.pack(pady=10, padx=10, fill="both", expand=True)

    theme_tab = tabs.add("Тема")
    color_tab = tabs.add("Цвета")
    preview_tab = tabs.add("Превью")

    # ============ Вкладка "Тема" ============
    def on_theme_change(choice):
        if choice in ("Light", "Dark"):
            ctk.set_appearance_mode(choice.lower())
        elif choice == "Flipper Zero":
            pass

    theme_combo = ctk.CTkComboBox(theme_tab, values=["Light", "Dark", "Custom", "Flipper Zero", "Blackout"],
                                  command=on_theme_change)
    theme_combo.set("Custom")
    theme_combo.pack(pady=20)

    # ============ Вкладка "Цвета" ============
    def choose_color(setting_key, title):
        color = askcolor(title=title, color=settings.get(setting_key, "#ffffff"))[1]
        if color:
            settings[setting_key] = color
            update_preview_colors()

    ctk.CTkButton(color_tab, text="Цвет кнопок",
                  command=lambda: choose_color("button_color", "Выберите цвет кнопок")).pack(pady=5)

    ctk.CTkButton(color_tab, text="Цвет меток",
                  command=lambda: choose_color("label_color", "Выберите цвет меток")).pack(pady=5)

    ctk.CTkButton(color_tab, text="Цвет текста",
                  command=lambda: choose_color("text_color", "Выберите цвет текста")).pack(pady=5)

    ctk.CTkButton(color_tab, text="Цвет фона",
                  command=lambda: choose_color("bg_color", "Выберите цвет фона")).pack(pady=5)

    ctk.CTkButton(color_tab, text="Цвет полей ввода",
                  command=lambda: choose_color("entry_color", "Выберите цвет полей ввода")).pack(pady=5)

    # ============ Вкладка "Превью" ============
    preview_button = ctk.CTkButton(preview_tab, text="Пример кнопки", width=150, height=40)
    preview_button.pack(pady=10)

    preview_label = ctk.CTkLabel(preview_tab, text="Пример метки")
    preview_label.pack(pady=5)

    preview_entry = ctk.CTkEntry(preview_tab, width=150)
    preview_entry.pack(pady=5)

    def update_preview_colors():
        preview_button.configure(fg_color=settings.get("button_color", "#1f6aa5"),
                                 text_color=settings.get("text_color", "#ffffff"))
        preview_label.configure(text_color=settings.get("label_color", "#ffffff"))
        preview_entry.configure(fg_color=settings.get("entry_color", "#2e2e2e"),
                                text_color=settings.get("text_color", "#ffffff"))
        preview_tab.configure(fg_color=settings.get("bg_color", "#121212"))
        color_tab.configure(fg_color=settings.get("bg_color", "#121212"))
        theme_tab.configure(fg_color=settings.get("bg_color", "#121212"))

    update_preview_colors()

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(theme_tab, text="Назад", width=100, height=30)
    back_btn.pack(pady=10)

    def go_back():
        save_theme_settings(theme_combo.get())
        if go_back_callback:
            go_back_callback()

    back_btn.configure(command=go_back)
