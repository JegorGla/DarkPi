import customtkinter as ctk
import os
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberFormat
from virtual_keyboard import PhoneNumber_Keyboard

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_PN_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)
    
    # Главный контейнер
    container = ctk.CTkFrame(parent_frame)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    # Верхняя секция: input + результаты
    top_frame = ctk.CTkFrame(container)
    top_frame.pack(side="top", fill="both", expand=True)

    # Нижняя секция: клавиатура
    bottom_frame = ctk.CTkFrame(container)
    bottom_frame.pack(side="bottom", fill="x")

    # Левая панель — кнопки, entry
    left_panel = ctk.CTkFrame(top_frame, width=250)
    left_panel.pack(side="left", fill="y", padx=10, pady=10)

    # Правая часть (делим на верх и низ)
    right_panel = ctk.CTkFrame(top_frame)
    right_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    top_right = ctk.CTkFrame(right_panel)
    top_right.pack(side="top", fill="both", expand=True)

    bottom_right = ctk.CTkFrame(right_panel)
    bottom_right.pack(side="bottom", fill="x")

    # Entry
    entry_phone_number = ctk.CTkEntry(left_panel, placeholder_text="Enter phone number", height=40)
    entry_phone_number.pack(pady=10)

    # Кнопка "Start Scan"
    find_btn = ctk.CTkButton(left_panel, text="Start Scan", command=lambda: check_PN(text_box), height=40, width=200, corner_radius=10, fg_color="#4CAF50", hover_color="#45a049")
    find_btn.pack(pady=10)

    # Кнопка "Back"
    back_btn = ctk.CTkButton(left_panel, text="← Back", command=go_back_callback, height=40, width=200, corner_radius=10, fg_color="#f44336", hover_color="#e53935")
    back_btn.pack(pady=10)

    # TextBox
    text_box = ctk.CTkTextbox(top_right)
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    keyboard = PhoneNumber_Keyboard(bottom_right, entry_phone_number)

    def set_keyboard_target(e):
        keyboard.target_entry = entry_phone_number

    entry_phone_number.bind("<FocusIn>", set_keyboard_target)

    def check_PN(text_box):
        number = entry_phone_number.get()
        text_box.delete("1.0", "end")

        try:
            parsed_number = phonenumbers.parse(number, None)

            if phonenumbers.is_valid_number(parsed_number):
                # Основные данные
                local_format = phonenumbers.format_number(parsed_number, PhoneNumberFormat.NATIONAL)
                intl_format = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                country_code = str(parsed_number.country_code)
                country_name = geocoder.description_for_number(parsed_number, 'en')
                location = geocoder.description_for_number(parsed_number, 'en')
                operator_name = carrier.name_for_number(parsed_number, 'en')
                timezones = timezone.time_zones_for_number(parsed_number)

                # Определение типа номера
                num_type = phonenumbers.number_type(parsed_number)
                if num_type == phonenumbers.PhoneNumberType.MOBILE:
                    line_type = "mobile"
                elif num_type == phonenumbers.PhoneNumberType.FIXED_LINE:
                    line_type = "landline"
                elif num_type == phonenumbers.PhoneNumberType.VOIP:
                    line_type = "voip"
                else:
                    line_type = "unknown"

                # Форматированный вывод
                result = {
                    "valid": True,
                    "local_format": local_format,
                    "intl_format": intl_format,
                    "country_code": country_code,
                    "country_name": country_name,
                    "location": location,
                    "carrier": operator_name,
                    "line_type": line_type,
                    "timezones": list(timezones)
                }

                # Вывод как JSON-подобная структура
                for k, v in result.items():
                    text_box.insert("end", f"{k}: {v}\n")

            else:
                text_box.insert("end", "valid: false\nerror: Invalid phone number.\n")

        except Exception as e:
            text_box.insert("end", f"valid: false\nerror: {e}\n")

     # Кнопка "Save results"
    save_result_btn = ctk.CTkButton(left_panel, text="Save results", command=lambda: save_results(text_box.get("1.0", "end")), height=40, width=200, corner_radius=10, fg_color="#2196F3", hover_color="#1976D2")
    save_result_btn.pack(pady=10)

    def save_results(results):
        """Save results to a file."""
        if not os.path.exists("results"):
            os.makedirs("results")
        with open(f"results/{entry_phone_number.get()}_results.txt", "w") as f:
            f.write(results)
        text_box.insert("end", "Results saved successfully!\n")
        text_box.yview("end")