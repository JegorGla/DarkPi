import customtkinter as ctk

#=========Import from DDoS==========
from DDOS.slowloris_ui import slowloris_ui  # Импорт функции slowloris_socket из модуля slowloris.py
#=========Import from DDoS==========

# Функция для очистки всех виджетов в фрейме
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Функция для создания интерфейса DDoS
def create_ddos_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)  # Очистить перед созданием UI

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="DDoS Attack 💀", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    #=======SYN Flood=======
    syn_flood_button = ctk.CTkButton(parent_frame, text="SYN Flood", fg_color="black", border_color="#8d33ff", hover_color="#2a104c", border_width=2, font=("Arial", 16), command=lambda: print("SYN Flood Attack Initiated"), width=parent_frame.winfo_width() * 0.7, height=40)
    syn_flood_button.place(relx=0.5, rely=0.3, anchor="center")

    #=======Slowloris=========
    slowloris_btn = ctk.CTkButton(parent_frame, text="Slowloris", fg_color="black", border_color="#8d33ff", hover_color="#2a104c", border_width=2, font=("Arial", 16), command=lambda: slowloris_ui(parent_frame, go_back_callback), width=parent_frame.winfo_width() * 0.7, height=40)
    slowloris_btn.place(relx=0.5, rely=0.4, anchor="center")


    #=======Back Button=======
    if go_back_callback:
        back_button = ctk.CTkButton(parent_frame, text="← Back", font=("Arial", 16), command=go_back_callback)
        back_button.place(relx=0.01, rely=0.01, anchor="nw")
