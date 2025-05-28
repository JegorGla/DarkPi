import customtkinter as ctk
import platform

from ScanSite.nslookup import nslookup_ui

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def scan_site_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="Выберите инструмент", font=ctk.CTkFont(size=18, weight="bold"))
    title.pack(pady=(20, 10))

    button_frame = ctk.CTkFrame(parent_frame)
    button_frame.pack(pady=10)

    # Общие инструменты (подходят и для Windows)
    ctk.CTkButton(button_frame, text="nslookup", command=lambda: nslookup_ui(parent_frame, go_back_callback)).pack(pady=5, padx=20)
    ctk.CTkButton(button_frame, text="traceroute / tracert").pack(pady=5, padx=20)

    # Инструменты только для Linux/macOS
    if platform.system() != "Windows":
        linux_label = ctk.CTkLabel(parent_frame, text="Инструменты Linux", font=ctk.CTkFont(size=14, weight="bold"))
        linux_label.pack(pady=(20, 5))

        linux_frame = ctk.CTkFrame(parent_frame)
        linux_frame.pack(pady=10)

        ctk.CTkButton(linux_frame, text="whois").pack(pady=5)
        ctk.CTkButton(linux_frame, text="nikto").pack(pady=5)
        ctk.CTkButton(linux_frame, text="dirb").pack(pady=5)
        ctk.CTkButton(linux_frame, text="whatweb").pack(pady=5)
        ctk.CTkButton(linux_frame, text="theHarvester").pack(pady=5)
    else:
        ctk.CTkLabel(parent_frame, text="Linux-инструменты недоступны в Windows", text_color="gray").pack(pady=10)

    # Назад
    if go_back_callback:
        ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback).pack(pady=20)
