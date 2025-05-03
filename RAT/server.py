import customtkinter as ctk
from virtual_keyboard import NormalKeyboard

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def server(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Основной контейнер с горизонтальным разделением (левая и правая части)
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(fill="both", expand=True)

    # Левая часть (панель кнопок)
    left_frame = ctk.CTkFrame(main_frame, width=200)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Правая часть (состоит из верхней и нижней)
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Верхняя часть правой панели (текстбокс и поле ввода)
    top_right_frame = ctk.CTkFrame(right_frame)
    top_right_frame.pack(side="top", fill="both", expand=True)

    # Нижняя часть правой панели (виртуальная клавиатура)
    bottom_right_frame = ctk.CTkFrame(right_frame, height=200)
    bottom_right_frame.pack(side="bottom", fill="x")

    # === Левая панель ===
    title = ctk.CTkLabel(left_frame, text="RAT Server 💀", font=ctk.CTkFont(weight="bold"))
    title.pack(pady=5)

    back_btn = ctk.CTkButton(left_frame, text="← Back", command=go_back_callback)
    back_btn.pack(pady=10)
    

    # === Правая верхняя панель ===
    ctk.CTkLabel(top_right_frame, text="Target Input").pack(anchor="w", padx=5, pady=5)
    entry_target = ctk.CTkEntry(top_right_frame, placeholder_text="Enter target here...")
    entry_target.pack(fill="x", padx=5, pady=5)

    text_box = ctk.CTkTextbox(top_right_frame)
    text_box.pack(fill="both", expand=True, padx=5, pady=5)

    # === Правая нижняя панель (клавиатура) ===
    keyboard = NormalKeyboard(bottom_right_frame, entry_target)
