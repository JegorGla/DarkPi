import subprocess
import platform
import customtkinter as ctk

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def nslookup_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Поле ввода сайта
    site_entry = ctk.CTkEntry(parent_frame, placeholder_text="Введите домен", width=400, height=40)
    site_entry.pack(pady=10)

    # Функция запуска nslookup
    def run_nslookup():
        site = site_entry.get()
        if not site:
            return
        
        cmd = ["nslookup", site]
        try:
            output = subprocess.check_output(cmd, text=True)
        except subprocess.CalledProcessError as e:
            output = e.output

        # Вывод результата
        result_box.configure(state="normal")
        result_box.delete("1.0", "end")
        result_box.insert("1.0", output)
        result_box.configure(state="disabled")

    # Кнопка запуска
    run_button = ctk.CTkButton(parent_frame, text="Запустить nslookup", command=run_nslookup)
    run_button.pack(pady=10)

    # Текстовое поле вывода
    result_box = ctk.CTkTextbox(parent_frame, width=600, height=300)
    result_box.pack(pady=10)
    result_box.configure(state="disabled")

    # Назад
    if go_back_callback:
        back_button = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
        back_button.pack(pady=10)
