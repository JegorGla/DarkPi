import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
from wifi_ui import create_wifi_ui
from bruteforce_ui import init_bruteforce_ui
from game_ui import init_game_ui  # Импортируем функцию создания меню игр
import time

# Глобальные переменные
time_label = None
content_frame = None
last_activity_time = time.time()  # Время последнего действия
inactivity_timeout = 5  # Время в секундах до бездействия (например, 5 секунд)
current_index = 0  # текущий слайд

gif_label = None
gif_frames = []
gif_durations = []
gif_animation_running = False
gif_visible = False

# Слайды
slides = [
    {"image": "images/DDoS_image.png", "text": "DDOS attack", "action": "ddos_action"},
    {"image": "images/Wifi.png", "text": "Wifi", "action": "wifi_action"},
    {"image": "images/Bruteforce.png", "text": "Bruteforce", "action": "bruteforce_action"},
    {"image": "images/Phishing.png", "text": "Phishing", "action": "phishing_action"},
    {"image": "images/Games.png", "text": "Games", "action": "games_action"}
]

# Инициализация окна
app = ctk.CTk()

# Функция инициализации панели времени
def init_time_panel(parent_frame):
    global time_label
    if time_label is None:  # Создаем панель времени только один раз
        time_label = ctk.CTkLabel(parent_frame, text="", font=("Arial", 16), fg_color="#252525", text_color="white")
        time_label.place(relx=0.5, rely=0.05, anchor="center")

# Обновление времени каждую секунду
def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату и время
    if time_label:  # Проверяем, что метка времени была инициализирована
        time_label.configure(text=current_time)  # Обновляем метку времени
    app.after(1000, update_time)  # Обновляем время каждую секунду

# Функция для очистки контента
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Функция для загрузки слайда
def load_slide(index):
    global current_index
    current_index = index % len(slides)
    slide = slides[current_index]
    img = Image.open(slide["image"])
    img = img.resize((400, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_button.configure(image=photo, text="", width=400, height=300)
    image_button.image = photo  # Важно сохранить ссылку!
    label_text.configure(text=slide["text"])

# Функции перехода между слайдами
def next_slide():
    load_slide(current_index + 1)

def prev_slide():
    load_slide(current_index - 1)

# Сброс таймера активности
def reset_inactivity_timer(event=None):
    global last_activity_time
    last_activity_time = time.time()  # Сброс таймера
    #print(last_activity_time)  # Для отладки
    hide_gif_animation()  # Останавливаем отображение GIF при активности

# Проверка на бездействие
def check_inactivity():
    if time.time() - last_activity_time > inactivity_timeout:
        show_gif_animation()  # Показываем анимацию GIF при бездействии
    else:
        hide_gif_animation()  # Скрываем GIF при активности

    app.after(1000, check_inactivity)  # Проверка каждую секунду

# Функция для показа GIF анимации
def show_gif_animation():
    global gif_label, gif_frames, gif_durations, gif_animation_running, gif_visible

    if gif_visible:
        return  # уже отображается — ничего не делаем

    gif_visible = True  # начинаем показывать

    if gif_label is None:
        gif_label = ctk.CTkLabel(app, text="", fg_color="transparent")
        gif_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
    else:
        gif_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    if not gif_frames:
        gif = Image.open("images/EvilEye.gif")
        for frame in ImageSequence.Iterator(gif):
            resized = frame.resize((app.winfo_width(), app.winfo_height()), Image.Resampling.LANCZOS)
            gif_frames.append(ImageTk.PhotoImage(resized))
            gif_durations.append(frame.info.get('duration', 100))

    if not gif_animation_running:
        gif_animation_running = True

        def update_gif(index=0):
            if not gif_visible:
                return  # остановим цикл, если гиф скрыта
            gif_label.configure(image=gif_frames[index])
            gif_label.image = gif_frames[index]
            next_index = (index + 1) % len(gif_frames)
            app.after(gif_durations[index], update_gif, next_index)

        update_gif()


def hide_gif_animation():
    global gif_visible, gif_animation_running

    if gif_visible:
        gif_visible = False
        gif_animation_running = False  # остановим цикл анимации

        if gif_label is not None:
            gif_label.place_forget()  # скрываем, но не уничтожаем


# Инициализация интерфейса
def init_main_ui(parent_frame):
    clear_content()  # очищаем перед загрузкой UI
    global image_button, label_text, prev_button, next_button
    
    # Кнопка с картинкой
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

# Инициализация основного интерфейса
def init_app_layout():
    global content_frame
    # Панель с временем
    init_time_panel(app)

    # Контейнер для смены интерфейсов
    content_frame = ctk.CTkFrame(app, fg_color="#000000")
    content_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=1, relheight=0.9)

# Действия для слайдов
def on_image_click():
    action = slides[current_index]["action"]
    if action == "ddos_action":
        ddos_action()
    elif action == "wifi_action":
        create_wifi_ui(content_frame, go_back_callback=lambda: init_main_ui(content_frame))
    elif action == "bruteforce_action":
        bruteforce_action()
    elif action == "phishing_action":
        phishing_action()
    elif action == "games_action":
        init_game_ui(content_frame, go_back_callback=lambda: init_main_ui(content_frame))
def ddos_action():
    print("Запуск атаки DDOS!")

def wifi_action():
    print("Подключение к Wifi!")

def bruteforce_action():
    init_bruteforce_ui(content_frame, go_back_callback=lambda: init_main_ui(content_frame))
def phishing_action():
    print("Запуск фишинговой атаки!")

# Инициализация приложения
init_app_layout()
update_time()  # Запуск обновления времени
check_inactivity()  # Запуск проверки бездействия
init_main_ui(content_frame)  # Отображение главного интерфейса

# ========== Настройки приложения ==========
ctk.set_appearance_mode("Dark")  # Темная тема
app.title("Слайдер")
app.geometry("800x480")

app.bind_all("<Button>", reset_inactivity_timer)   # любое нажатие мыши
app.bind_all("<Key>", reset_inactivity_timer)      # любое нажатие клавиши
app.bind_all("<Motion>", reset_inactivity_timer)  # любое движение мыши

# Запуск приложения
app.mainloop()
