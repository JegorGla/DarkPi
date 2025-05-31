import customtkinter as ctk
from PIL import Image
import os

# Галерея карточек
gallery_items = [
    {"image": "images/RAT.png", "text": "RAT", "action": "rat_action"}
    # Добавляй сколько хочешь
]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_gallery_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    scroll_frame = ctk.CTkScrollableFrame(parent_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

    columns = 3  # сколько карточек в ряд
    for idx, item in enumerate(gallery_items):
        row = idx // columns
        col = idx % columns

        # Загрузка изображения
        if not os.path.exists(item["image"]):
            continue
        img = Image.open(item["image"]).resize((200, 200))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))

        # Создание кнопки-карточки
        btn = ctk.CTkButton(
            scroll_frame,
            image=ctk_img,
            text=item["text"],
            compound="top",
            width=120,
            height=150,
            command=item["action"]
        )
        btn.grid(row=row, column=col, padx=10, pady=10)

    back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
    back_btn.pack(pady=1)
