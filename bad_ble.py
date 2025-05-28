import customtkinter as ctk
import os
import platform

from BadBLE.scan_ble import bluetooth_scan_action
from BadBLE.connect_to_ble import connect_to_ble_ui

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def bad_ble_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    ctk.CTkLabel(parent_frame, text="Bad BLE Tools", font=("Arial", 20)).pack(pady=10)

    Bluetooth_Scan = ctk.CTkButton(parent_frame, text="Bluetooth Scan", command=lambda: bluetooth_scan_action(parent_frame, go_back_callback))
    Bluetooth_Scan.pack(pady=10)

    connect_to_ble_btn = ctk.CTkButton(parent_frame, text="Connect to BLE", command=lambda: connect_to_ble_ui(parent_frame, go_back_callback))
    connect_to_ble_btn.pack(pady=10)

    # Проверка, что не Windows (то есть скорее всего Linux)
    if platform.system() != "Windows":
        BLE_spoof = ctk.CTkButton(parent_frame, text="BLE Spoof", command=lambda: print("Имитация BLE..."))
        BLE_spoof.pack(pady=10)
    else:
        ctk.CTkLabel(parent_frame, text="BLE Spoof не поддерживается на Windows", text_color="red").pack(pady=5)

    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
        back_btn.pack(pady=10)