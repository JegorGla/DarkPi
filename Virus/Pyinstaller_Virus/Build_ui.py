import customtkinter as ctk
import subprocess
import os

main_dir = "Virus/"
output_dir = "Virus/EXE's/"
list_of_files = [
    main_dir + "CamHack/CamHackSrv.py",
]

def clear_frame(frame):
    """Очистить все виджеты в переданном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()
        
def create_pyinstaller_ui(parent_frame, go_back_callback):
    """Создать интерфейс для сборки вируса с помощью PyInstaller."""
    clear_frame(parent_frame)

    # Здесь можно добавить элементы управления для настройки сборки
    title_label = ctk.CTkLabel(parent_frame, text="PyInstaller Virus Builder", font=("Arial", 24))
    title_label.pack(pady=20)

    for i in list_of_files:
        if not os.path.exists(i):
            continue
        
        file_button = ctk.CTkButton(parent_frame, text=f"File: {i}", command=lambda f=i: subprocess.run(["pyinstaller", "--onefile", "--distpath", output_dir, f], check=True))
        file_button.pack(pady=5)

    # Добавляем кнопку для возврата назад
    back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
    back_btn.pack(pady=5)