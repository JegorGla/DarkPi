import customtkinter as ctk
import subprocess
import platform

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def write_to_output(output_widget: ctk.CTkTextbox, text: str):
    output_widget.configure(state="normal")
    output_widget.insert("end", text + "\n")
    output_widget.see("end")
    output_widget.configure(state="disabled")

def bluetooth_scan_action(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="Bluetooth Scanner", font=("Arial", 20))
    title.pack(pady=10)

    output_box = ctk.CTkTextbox(parent_frame, width=500, height=250)
    output_box.pack(pady=10)
    output_box.configure(state="disabled")

    write_to_output(output_box, "[INFO] Начинаем сканирование Bluetooth-устройств...")

    if platform.system() == "Linux":
        try:
            result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True)
            if result.stdout.strip():
                write_to_output(output_box, "[RESULT]\n" + result.stdout.strip())
            else:
                write_to_output(output_box, "[INFO] Устройства не найдены.")
        except Exception as e:
            write_to_output(output_box, f"[ERROR] Ошибка при запуске bluetoothctl: {e}")
    else:
        write_to_output(output_box, "[ERROR] Сканирование Bluetooth поддерживается только на Linux.")

    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="Назад", command=go_back_callback)
        back_btn.pack(pady=10)
