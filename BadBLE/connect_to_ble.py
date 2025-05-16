import customtkinter as ctk
import asyncio
from bleak import BleakClient
import threading

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def write_to_output(output_widget: ctk.CTkTextbox, text: str):
    output_widget.configure(state="normal")
    output_widget.insert("end", text + "\n")
    output_widget.see("end")
    output_widget.configure(state="disabled")

def connect_to_ble_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="BLE Подключение", font=("Arial", 20))
    title.pack(pady=10)

    addr_entry = ctk.CTkEntry(parent_frame, placeholder_text="Введите BLE-адрес", width=400)
    addr_entry.pack(pady=10)
 
    output_box = ctk.CTkTextbox(parent_frame, width=500, height=250)
    output_box.pack(pady=10)
    output_box.configure(state="disabled")

    def attempt_connection():
        address = addr_entry.get().strip()
        if not address:
            write_to_output(output_box, "[ERROR] Адрес устройства не указан.")
            return

        async def connect():
            try:
                write_to_output(output_box, f"[INFO] Подключение к {address}...")
                async with BleakClient(address) as client:
                    if await client.is_connected():
                        write_to_output(output_box, f"[SUCCESS] Устройство {address} подключено.")
                    else:
                        write_to_output(output_box, f"[FAIL] Не удалось подключиться к {address}")
            except Exception as e:
                write_to_output(output_box, f"[ERROR] {e}")

        threading.Thread(target=lambda: asyncio.run(connect())).start()

    connect_button = ctk.CTkButton(parent_frame, text="Подключиться", command=attempt_connection)
    connect_button.pack(pady=5)

    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="Назад", command=go_back_callback)
        back_btn.pack(pady=10)
