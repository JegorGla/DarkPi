import customtkinter as ctk
import subprocess
import platform
import asyncio
from bleak import BleakScanner
import threading
import pyperclip  # Для копирования в буфер обмена

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

    # Создаем главный контейнер для двух колонок
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Левая колонка
    left_frame = ctk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=10)

    # Правая колонка
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10)

    output_box = ctk.CTkTextbox(left_frame, width=500, height=250)
    output_box.pack(pady=10)
    output_box.configure(state="disabled")

    write_to_output(output_box, "[INFO] Начинаем сканирование Bluetooth-устройств...")

    system = platform.system()

    def scan_linux():
        try:
            result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True)
            if result.stdout.strip():
                write_to_output(output_box, "[RESULT]\n" + result.stdout.strip())
            else:
                write_to_output(output_box, "[INFO] Устройства не найдены.")
        except Exception as e:
            write_to_output(output_box, f"[ERROR] Ошибка при запуске bluetoothctl: {e}")

    async def scan_ble():
        try:
            devices = await BleakScanner.discover(timeout=5.0)
            if devices:
                for d in devices:
                    # Для каждого устройства создаём отдельный лейбл и кнопку в правой части
                    device_label = ctk.CTkLabel(right_frame, text=f"{d.name or 'Unknown'} - {d.address}")
                    device_label.pack(pady=5)
                    
                    copy_button = ctk.CTkButton(right_frame, text="Копировать SSID", command=lambda addr=d.address: copy_to_clipboard(addr))
                    copy_button.pack(pady=5)

            else:
                write_to_output(output_box, "[INFO] BLE-устройства не найдены.")
        except Exception as e:
            write_to_output(output_box, f"[ERROR] Ошибка BLE-сканирования: {e}")

    def run_ble_scan():
        asyncio.run(scan_ble())

    def copy_to_clipboard(ssid):
        # Копируем адрес в буфер обмена
        pyperclip.copy(ssid)
        write_to_output(output_box, f"[INFO] SSID {ssid} скопирован в буфер обмена.")

    def run_linux_scan():
        threading.Thread(target=scan_linux).start()
        threading.Thread(target=run_ble_scan).start()

    def run_windows_scan():
        threading.Thread(target=run_ble_scan).start()

    # Выбираем метод сканирования
    if system == "Linux":
        run_linux_scan()
    elif system == "Windows":
        run_windows_scan()
    else:
        write_to_output(output_box, "[ERROR] Операционная система не поддерживается.")

    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="Назад", command=go_back_callback)
        back_btn.pack(pady=10)