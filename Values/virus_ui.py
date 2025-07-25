import customtkinter as ctk
from PIL import Image
import os

from Values.rat_ui import create_rat_ui

# Галерея карточек
gallery_items = [
    {"image": "images/RAT.png", "text": "RAT", "action": "rat_action"},
    {"image": "images/Hack_Cam.png", "text": "Hack Camera", "action":"hack_camera_action"},
    {"image": "images/Pyinstaller.png", "text": "Build virus", "action": "build_virus_action"}
    # Добавляй сколько хочешь
]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_gallery_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    # Здесь создаём действия, когда параметры уже доступны
    actions = {
        "rat_action": lambda: create_rat_ui(parent_frame, go_back_callback),
        "hack_camera_action": lambda: print("Hello"),
        "build_virus_action": lambda: print("Building virus...")
        # другие действия...
    }

    scroll_frame = ctk.CTkScrollableFrame(parent_frame)
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

    columns = 3
    for idx, item in enumerate(gallery_items):
        row = idx // columns
        col = idx % columns

        if not os.path.exists(item["image"]):
            continue
        img = Image.open(item["image"]).resize((200, 200))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))

        action_func = actions.get(item["action"], lambda: print("Unknown action"))

        btn = ctk.CTkButton(
            scroll_frame,
            image=ctk_img,
            text=item["text"],
            compound="top",
            width=180,
            height=220,
            command=action_func
        )
        btn.grid(row=row, column=col, padx=10, pady=10)

    back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
    back_btn.pack(pady=5)

