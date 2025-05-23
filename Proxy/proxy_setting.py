import customtkinter as ctk
import json

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_proxy_setting_frame(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # input_frame содержит Label и ComboBox
    input_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    input_frame.pack(pady=10)

    label = ctk.CTkLabel(input_frame, text="Select timeout in", font=("Arial", 14))
    label.grid(row=0, column=0, padx=(0, 10))

    unit_combobox = ctk.CTkComboBox(input_frame, values=["minutes", "seconds"], width=100)
    unit_combobox.set("minutes")
    unit_combobox.grid(row=0, column=1)

    # timeout_entry лежит отдельно в parent_frame, рядом с input_frame
    timeout_entry = ctk.CTkEntry(parent_frame, width=100, font=("Arial", 14))
    timeout_entry.pack(pady=10)

    def save_proxy_settings():
        number = timeout_entry.get()
        unit = unit_combobox.get()

        if not number.isdigit():
            print("[ERROR] Please enter a valid number")
            return

        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            settings = {}

        # Сохраняем как словарь с числом и единицей
        settings["proxy_rechoice_interval"] = {
            "value": int(number),
            "unit": unit
        }

        try:
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            print(f"[INFO] proxy_rechoice_interval saved as {number} {unit}")
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")


    save_btn = ctk.CTkButton(parent_frame, text="Save", command=save_proxy_settings)
    save_btn.pack(pady=10)

    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback)
    back_btn.pack(pady=10)
