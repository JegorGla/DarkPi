import customtkinter as ctk
from PIL import Image, ImageTk
from bruteforce_ui import init_bruteforce_ui
from settings_ui import init_settings_ui
from theme_utils import apply_theme_colors
import time

# Создаем окно
app = ctk.CTk()


# Глобальная переменная для метки времени и основного контейнера
time_label = None
content_frame = None  # Контейнер для смены интерфейсов

# Инициализация панели с временем
def init_time_panel(parent_frame):
    global time_label
    if time_label is None:  # Создаем панель времени только один раз
        time_label = ctk.CTkLabel(parent_frame, text="", font=("Arial", 16), fg_color="black", text_color="white")
        time_label.place(relx=0.5, rely=0.05, anchor="center")  # Размещаем в верхней части экрана

# Обновление времени каждую секунду
def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату и время
    if time_label:  # Проверяем, что метка времени была инициализирована
        time_label.configure(text=current_time)  # Обновляем метку времени
    app.after(1000, update_time)  # Обновляем время каждую секунду

# Функция для очистки контента в content_frame
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_main_ui():
    clear_content()  # Очищаем только содержимое content_frame
    init_main_ui(content_frame)

def show_settings_ui():
    clear_content()  # Очищаем только содержимое content_frame
    init_settings_ui(content_frame, show_main_ui)

# Инициализация основного интерфейса
def init_main_ui(parent_frame):
    global image_button, label_text, prev_button, next_button
    
    # Центр: кнопка с картинкой
    image_button = ctk.CTkButton(parent_frame, text="", command=on_image_click, width=400, height=300, fg_color="#000000", hover_color="#000000")
    image_button.place(relx=0.5, rely=0.4, anchor="center")

    # Подпись под изображением
    label_text = ctk.CTkLabel(parent_frame, text="", font=("Arial", 20))
    label_text.place(relx=0.5, rely=0.75, anchor="center")

    # Левая стрелка
    prev_button = ctk.CTkButton(parent_frame, text="←", width=50, command=prev_slide, font=("Arial", 24))
    prev_button.place(relx=0.1, rely=0.4, anchor="center")

    # Правая стрелка
    next_button = ctk.CTkButton(parent_frame, text="→", width=50, command=next_slide, font=("Arial", 24))
    next_button.place(relx=0.9, rely=0.4, anchor="center")

    # Загрузить первый слайд
    load_slide(current_index)

# Создаем контейнер для панели с временем и контента
def init_app_layout():
    global content_frame
    # Панель с временем
    init_time_panel(app)

    # Контейнер для смены интерфейсов
    content_frame = ctk.CTkFrame(app, fg_color="#000000")
    content_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=1, relheight=0.9)

# Слайды: список словарей с путями к изображениям и подписями
slides = [
    {"image": "images/DDoS_image.png", "text": "DDOS attack", "action": "ddos_action"},
    {"image": "images/Wifi.png", "text": "Wifi", "action": "wifi_action"},
    {"image": "images/Bruteforce.png", "text": "Bruteforce", "action": "bruteforce_action"},
    {"image": "images/Phishing.png", "text": "Phishing", "action": "phishing_action"},
    {"image": "images/Settings.png", "text": "Settings", "action": "settings_action"},
]

current_index = 0  # текущий слайд

# ===== ФУНКЦИИ =====

def load_slide(index):
    global current_index
    current_index = index % len(slides)

    slide = slides[current_index]
    img = Image.open(slide["image"])
    img = img.resize((400, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    image_button.configure(image=photo, text="", width=400, height=300)
    image_button.image = photo  # важно сохранить ссылку!
    label_text.configure(text=slide["text"])

def next_slide():
    load_slide(current_index + 1)

def prev_slide():
    load_slide(current_index - 1)

def on_image_click():
    # Действие в зависимости от текущего слайда
    action = slides[current_index]["action"]
    
    if action == "ddos_action":
        ddos_action()
    elif action == "wifi_action":
        wifi_action()
    elif action == "bruteforce_action":
        bruteforce_action()
    elif action == "phishing_action":
        phishing_action()
    elif action == "settings_action":
        show_settings_ui()

def ddos_action():
    print("Запуск атаки DDOS!")

def wifi_action():
    print("Подключение к Wifi!")

def bruteforce_action():
    print("Запуск Bruteforce атаки!")
    init_bruteforce_ui(app, show_main_ui)  # Переход на интерфейс Bruteforce

def phishing_action():
    print("Запуск фишинговой атаки!")

# Инициализация приложения
init_app_layout()
update_time()  # Запуск обновления времени
show_main_ui()  # Отображение главного интерфейса
apply_theme_colors(app)  # Или content_frame, если хочешь локально

# ========== APP configuration ==========
if ctk.get_appearance_mode() == "Dark":
    app.configure(fg_color="#000000")
else:
    app.configure(fg_color="#FFFFFF")
    
app.title("Слайдер")
app.geometry("800x480")

# Запуск приложения
app.mainloop()