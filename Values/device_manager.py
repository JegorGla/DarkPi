import customtkinter as ctk 

def clear_frame(frame):
    """Очищает содержимое фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()

def device_manager_ui(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    wifi_manager = ctk.CTkButton(
        parent_frame, 
        text="Wi-Fi Manager", 
        command=lambda: print("Wi-Fi Manager clicked"),
        width=200)
    wifi_manager.pack(pady=10)

    bluetooth_manager = ctk.CTkButton(
        parent_frame,
        text="Bluetooth Manager",
        command=lambda: print("Bluetooth Manager clicked"),
        width=200)
    bluetooth_manager.pack(pady=10)

    mac_address_manager = ctk.CTkButton(
        parent_frame,
        text="MAC Address Manager",
        command=lambda: print("MAC Address Manager clicked"),
        width=200)
    mac_address_manager.pack(pady=10)

    task_manager = ctk.CTkButton(
        parent_frame,
        text="Task Manager",
        command=lambda: print("Task Manager clicked"),
        width=200)
    task_manager.pack(pady=10)
    go_back_button = ctk.CTkButton(
        parent_frame,
        text="Go Back",
        command=go_back_callback
        )
    go_back_button.pack(pady=10)