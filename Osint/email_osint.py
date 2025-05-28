import customtkinter as ctk
import requests
import re
import tkinter as tk
from virtual_keyboard import NormalKeyboard

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def email_osint(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    container = ctk.CTkFrame(parent_frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    top_frame = ctk.CTkFrame(container)
    top_frame.pack(side="top", fill="both", expand=True)

    bottom_frame = ctk.CTkFrame(container)
    bottom_frame.pack(side="bottom", fill="x")

    left_panel = ctk.CTkFrame(top_frame, width=250)
    left_panel.pack(side="left", fill="y", padx=10, pady=10)

    right_panel = ctk.CTkFrame(top_frame)
    right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    top_right = ctk.CTkFrame(right_panel)
    top_right.pack(side="top", fill="both", expand=True)

    bottom_right = ctk.CTkFrame(right_panel)
    bottom_right.pack(side="bottom", fill="x")

    email = ctk.CTkEntry(left_panel, placeholder_text="Enter email")
    email.pack(pady=10)

    text_box = ctk.CTkTextbox(top_right)
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    def check_has_been_pwnd():
        ck_email = email.get()
        text_box.delete("1.0", "end")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", ck_email):
            text_box.insert("end", f"[-] Неверный формат email: {ck_email}\n")
            return

        headers = {"User-Agent": "EmailOSINTChecker"}
        url = f"https://haveibeenpwned.com/unifiedsearch/{ck_email}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                breaches = data.get("Breaches", [])
                if breaches:
                    for b in breaches:
                        text_box.insert("end", f"[+] Найдено в утечках: {b['Name']} ({b['BreachDate']})\n")
                else:
                    text_box.insert("end", "[✓] Email не найден в утечках.\n")
            elif response.status_code == 404:
                text_box.insert("end", "[✓] Email не найден в утечках.\n")
            else:
                text_box.insert("end", f"[!] Ошибка: статус {response.status_code}\n")
        except Exception as e:
            text_box.insert("end", f"[!] Ошибка запроса: {e}\n")

    check = ctk.CTkButton(left_panel, text="Check", command=check_has_been_pwnd)
    check.pack(pady=10)

    back_btn = ctk.CTkButton(left_panel, text="← Back", command=go_back_callback,
                              height=40, width=200, corner_radius=10, fg_color="#f44336", hover_color="#e53935")
    back_btn.pack(pady=10)

    keyboard = NormalKeyboard(bottom_right, email)

    def set_keyboard_target(e):
        keyboard.target_entry = email

    email.bind("<FocusIn>", set_keyboard_target)