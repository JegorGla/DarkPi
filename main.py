import customtkinter as ctk
from PIL import Image, ImageTk
from bruteforce_ui import init_bruteforce_ui

# Слайды: список словарей с путями к изображениям и подписями
slides = [
    {"image": "images/DDoS_image.png", "text": "DDOS attack", "action": "ddos_action"},
    {"image": "images/Wifi.png", "text": "Wifi", "action": "wifi_action"},
    {"image": "images/Bruteforce.png", "text": "Bruteforce", "action": "bruteforce_action"},
    {"image": "images/Phishing.png", "text": "Phishing", "action": "phishing_action"}
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

def ddos_action():
    print("Запуск атаки DDOS!")

def wifi_action():
    print("Подключение к Wifi!")

def bruteforce_action():
    print("Запуск Bruteforce атаки!")
    init_bruteforce_ui(app, show_main_ui)  # Переход на интерфейс Bruteforce

def phishing_action():
    print("Запуск фишинговой атаки!")

def show_main_ui():
    # Очищаем текущие виджеты
    for widget in app.winfo_children():
        widget.destroy()

    # Перезагружаем элементы главного интерфейса
    init_main_ui(app)

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

# ===== UI ЭЛЕМЕНТЫ =====

# Создаем окно
app = ctk.CTk()

# Инициализация основного интерфейса
init_main_ui(app)

# ========== APP configuration ========== 
app.configure(fg_color="#000000")  # Цвет фона приложения
app.title("Слайдер")
app.geometry("800x480")

# Запуск приложения
app.mainloop()