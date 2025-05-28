import customtkinter as ctk
from Osint.find_user import user_find
from virtual_keyboard import NormalKeyboard
import threading
import os
import asyncio

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_find_user_ui(parent_frame, go_back_callback=None):
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

    entry_username = ctk.CTkEntry(left_panel, placeholder_text="Enter username", height=40)
    entry_username.pack(pady=10)

    text_box = ctk.CTkTextbox(top_right)
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    def save_results(results):
        if not results.strip():
            text_box.insert("end", "Nothing to save! Run a scan first.\n")
            return
        if not os.path.exists("results"):
            os.makedirs("results")
        filename = f"results/{entry_username.get().strip()}_results.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(results)
        text_box.insert("end", f"Results saved successfully to {filename}\n")
        text_box.yview("end")

    def run_osint():
        username = entry_username.get().strip()
        if not username:
            text_box.insert("end", "Please enter a username!\n")
            return
        find_btn.configure(state="disabled")
        text_box.delete("1.0", "end")

        def task():
            try:
                asyncio.run(user_find(username, text_box))
            finally:
                find_btn.configure(state="normal")

        threading.Thread(target=task, daemon=True).start()


    find_btn = ctk.CTkButton(left_panel, text="Start Scan", command=run_osint, height=40, width=200, corner_radius=10, fg_color="#4CAF50", hover_color="#45a049")
    find_btn.pack(pady=10)

    back_btn = ctk.CTkButton(left_panel, text="← Back", command=go_back_callback, height=40, width=200, corner_radius=10, fg_color="#f44336", hover_color="#e53935")
    back_btn.pack(pady=10)

    save_result_btn = ctk.CTkButton(left_panel, text="Save results", command=lambda: save_results(text_box.get("1.0", "end")), height=40, width=200, corner_radius=10, fg_color="#2196F3", hover_color="#1976D2")
    save_result_btn.pack(pady=10)

    keyboard = NormalKeyboard(bottom_right, entry_username)

    def set_keyboard_target(e):
        keyboard.target_entry = entry_username

    entry_username.bind("<FocusIn>", set_keyboard_target)
