import json
import customtkinter as ctk

from settings.about_device import about_device_ui  # Импортируем функцию очистки фрейма из about_device.py

def clear_frame(frame):
    """Очистить все виджеты в переданном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

selected_timeout = None  # Глобальная переменная для хранения значения времени

# Функция для сохранения значения в файл
def save_timeout_setting():
    """Сохранение выбранного времени в файл JSON."""
    if selected_timeout:
        with open("settings.json", "w") as f:
            json.dump({"timeout": selected_timeout}, f)

# Функция для загрузки сохраненного значения из файла
def load_timeout_setting():
    """Загрузка сохраненного значения из файла JSON, если оно есть."""
    global selected_timeout
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            selected_timeout = data.get("timeout", None)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_timeout = None  # Если файл не найден или его содержимое повреждено

def set_gif_timeout(event):
    """Функция для обработки выбранного времени."""
    global selected_timeout
    selected_timeout = timeout_combo.get()  # Сохраняем выбранное значение
    print(f"GIF Timeout set to: {selected_timeout}")  # Для проверки, можно заменить на сохранение в файл
    save_timeout_setting()  # Сохраняем настройку в файл

def init_settings_ui(parent_frame, go_back_callback):
    """Функция для инициализации UI настроек."""
    clear_frame(parent_frame)

    # Заголовок
    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 24))
    title.place(relx=0.5, rely=0.1, anchor="center")

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(parent_frame, text="← Back", command=go_back_callback)
    back_btn.place(relx=0.01, rely=0.01, anchor="nw")

    # ==== Блок Use Proxies ====  
    setting_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    setting_frame.place(relx=0.5, rely=0.25, anchor="center", relwidth=0.9)

    setting_label = ctk.CTkLabel(setting_frame, text="Use proxies", anchor="w", font=("Arial", 16))
    setting_label.pack(side="left", fill="x", expand=True)

    use_proxies_var = ctk.BooleanVar()
    checkbox = ctk.CTkCheckBox(setting_frame, variable=use_proxies_var, text="")
    checkbox.pack(side="right")

    # ==================== About Device ====================
    about_device_btn = ctk.CTkButton(
        parent_frame, 
        text="About Device", 
        command=lambda: about_device_ui(parent_frame, go_back_callback), 
        font=("Arial", 16)
    )
    about_device_btn.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.9)

    # =====================================================

    # Настройка времени для GIF-анимации
    global timeout_combo  # Делаем ComboBox глобальным для доступа из других функций
    timeout_combo = ctk.CTkComboBox(
        parent_frame, 
        values=["5 seconds", "10 seconds", "30 seconds", "1 minute", "5 minutes"],
        font=("Arial", 16), 
        state="readonly",
    )
    timeout_combo.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9)

    timeout_combo.set(selected_timeout if selected_timeout else "Select timeout")  # Загружаем ранее сохранённое значение
    timeout_combo.bind("<<ComboboxSelected>>", set_gif_timeout)  # Привязка события

    # Горизонтальная линия
    separator = ctk.CTkFrame(parent_frame, height=1, fg_color="#444444")
    separator.place(relx=0.05, rely=0.3, relwidth=0.9)

# Загружаем сохранённую настройку при запуске
load_timeout_setting()