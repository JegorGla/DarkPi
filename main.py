#=============================Импортируем библиотеки=============================
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
#+++++++++++++++Import all UI+++++++++++++++
from phishing_ui import create_main_phishing_ui
from wifi_ui import create_main_wifi_ui
from network_scan_ui import ns_ui  # Импортируем функцию создания интерфейса сканирования сети
from bruteforce_ui import init_bruteforce_ui
from game_ui import init_game_ui  # Импортируем функцию создания меню игр
from greeting import show_greeting  # Импортируем функцию показа приветствия
from DVD_ui import create_dvd_ui  # Импортируем функцию создания DVD анимации
from settings_ui import init_settings_ui, selected_timeout  # Импортируем функцию создания настроек и выбранное время
from ddos_ui import create_ddos_ui  # Импортируем функцию создания DDoS UI
from see_files_ui import file_browser_ui  # Импортируем функцию создания файлового браузера
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import time
import pywifi
import logging
import json
#====================================================================


#=============================Пременные=============================
time_label = None
content_frame = None
wifi_znak_label = None
alowed_gif_animation = True  # Разрешаем анимацию GIF
swipe_enabled = True
alowed_swipe = True  # Разрешаем свайп
last_activity_time = time.time()  # Время последнего действия
inactivity_timeout = 5  # Время в секундах до бездействия (например, 5 секунд)
current_index = 0  # текущий слайд

gif_label = None
gif_frames = []
gif_durations = []
gif_animation_running = False
gif_visible = False

image_button_current = None
image_button_next = None

start_x = 0  # Начальная позиция свайпа
#===================================================================

logging.getLogger("pywifi").setLevel(logging.CRITICAL)

#=============================Слайды=============================
slides = [
    {"image": "images/DDoS_image.png", "text": "DDOS attack\n (site test)", "action": "ddos_action"},
    {"image": "images/Wifi.png", "text": "Wifi", "action": "wifi_action"},
    {"image": "images/NetworkScan.png", "text": "Network Scan", "action": "network_scan_action"},
    {"image": "images/Bruteforce.png", "text": "Bruteforce", "action": "bruteforce_action"},
    {"image": "images/Phishing.png", "text": "Phishing", "action": "phishing_action"},
    {"image": "images/Games.png", "text": "Games", "action": "games_action"},
    {"image": "images/Folder.png", "text": "See files", "action": "files_action"},
    {"image": "images/Settings.png", "text": "Settings", "action": "settings_action"},
]

# Инициализация окна
app = ctk.CTk()

def dvd_button():
    def on_dvd_click():
        global alowed_gif_animation
        alowed_gif_animation = False  # Отключаем анимацию GIF

        # Переход в DVD UI с логикой свайпа-назад
        create_dvd_ui(content_frame, go_back_callback=lambda: init_main_ui(content_frame))

    # Кнопка DVD
    dvd_btn = ctk.CTkButton(app, text="DVD", font=("Arial", 20), command=on_dvd_click, hover_color="#272727", fg_color="#242424", text_color="white")
    dvd_btn.place(relx=0, rely=0, x=10, y=10, anchor="nw")

def exit_btn():
    def exit_app():
        app.quit()
    
    logout_img = Image.open("images/Logout.png")  # Загружаем изображение
    logout_img = logout_img.resize((50, 50))  # Измените размер изображения по необходимости
    logout_img = ImageTk.PhotoImage(logout_img)  # Преобразуем в PhotoImage

    exit_button = ctk.CTkButton(app, text="", image=logout_img, font=("Arial", 20), command=exit_app, hover_color="#272727", fg_color="#242424", text_color="white", width=40, height=40)
    exit_button.place(relx=1, rely=0.01, anchor="ne")  # Размещение в правом верхнем углу

# Функция инициализации панели времени
def init_time_panel(parent_frame):
    global time_label
    if time_label is None:  # Создаем панель времени только один раз
        time_label = ctk.CTkLabel(parent_frame, text="", font=("Arial", 16), fg_color="#242424", text_color="white")
        time_label.place(relx=0.5, rely=0.05, anchor="center")

def init_wifi_znak_with_texture(parent_frame):
    global wifi_znak_label
    if wifi_znak_label is None:  # Создаем панель только один раз
        # Загружаем изображение для текстуры
        texture_image = Image.open("images/WifiDisconnected.png")  # Изображение для не подключенного состояния
        texture_image = texture_image.resize((50, 50))  # Измените размер изображения по необходимости
        texture_photo = ImageTk.PhotoImage(texture_image)

        # Создаем метку с фоновым изображением
        wifi_znak_label = ctk.CTkButton(parent_frame, image=texture_photo, text="", font=("Arial", 16), fg_color="#242424", hover_color="#272727", text_color="white", width=50, height=50, command=show_connected_network)
        wifi_znak_label.image = texture_photo  # Сохраняем ссылку на изображение, чтобы оно не удалялось сборщиком мусора

        # Размещаем в правом верхнем углу
        wifi_znak_label.place(relx=0.92, rely=0.01, anchor="ne")  # Размещение в правом верхнем углу

        # Проверяем состояние подключения и обновляем изображение
        update_wifi_icon()

def update_wifi_icon():
    """Обновляет иконку в зависимости от состояния подключения к Wi-Fi."""
    if is_wifi_connected():
        # Если Wi-Fi подключен, загружаем изображение для подключенного состояния
        texture_image = Image.open("images/WifiConnected.png")
    else:
        # Если Wi-Fi не подключен, загружаем изображение для отключенного состояния
        texture_image = Image.open("images/WifiDisconnected.png")
    
    # Меняем размер изображения
    texture_image = texture_image.resize((50, 50))
    texture_photo = ImageTk.PhotoImage(texture_image)

    # Обновляем метку
    wifi_znak_label.configure(image=texture_photo)
    wifi_znak_label.image = texture_photo  # Сохраняем ссылку на изображение, чтобы оно не удалялось сборщиком мусора

# Обновление времени каждую секунду
def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Форматируем дату и время
    if time_label:  # Проверяем, что метка времени была инициализирована
        time_label.configure(text=current_time)  # Обновляем метку времени
    app.after(1000, update_time)  # Обновляем время каждую секунду

def is_wifi_connected():
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # Получаем первый доступный интерфейс
        return iface.status() == pywifi.const.IFACE_CONNECTED
    except Exception as e:
        pass

def show_connected_network():
    """Отображает название подключенной сети."""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            ssid = data.get("ssid", None)
            if ssid:
                wifi_znak_label.configure(text=f"{ssid}")
                app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Скрываем текст через 2 секунды
            else:
                wifi_znak_label.configure(text="No connected")
                app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Скрываем текст через 2 секунды
    except FileNotFoundError:
        wifi_znak_label.configure(text="Файл с данными сети не найден.")

def check_and_update_wifi_status():
    """Периодическая проверка состояния Wi-Fi и обновление иконки."""
    update_wifi_icon()  # Обновляем иконку в зависимости от состояния подключения к Wi-Fi
    app.after(1000, check_and_update_wifi_status)  # Проверка каждую секунду (1000 мс)

# Функция для очистки контента
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Функция для загрузки слайда
def load_slide(index, animate=False, direction="left"):
    global current_index
    current_index = index % len(slides)
    slide = slides[current_index]

    img = Image.open(slide["image"])
    img = img.resize((400, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    if animate:
        animate_slide(photo, slide["text"], direction)
    else:
        image_button.configure(image=photo, text="", width=400, height=300)
        image_button.image = photo
        label_text.configure(text=slide["text"])


def animate_slide(new_photo, new_text, direction):
    steps = 15
    delay = 10  # мс
    total_shift = 0.5  # относительное смещение (1 = ширина окна)

    if direction == "left":
        sign = -1
    else:
        sign = 1

    # Создаем временный лейбл для нового текста
    temp_label = ctk.CTkLabel(content_frame, text=new_text, font=("Arial", 20))
    temp_label.place(relx=0.5 - sign * total_shift, rely=0.75, anchor="center")

    def slide_out(step=0):
        if not image_button or not image_button.winfo_exists():  # Проверяем, что виджет существует
            return

        progress = step / steps
        offset = sign * progress * total_shift

        # Двигаем кнопку с изображением
        image_button.place_configure(relx=0.5 + offset)

        # Двигаем текущий текст
        label_text.place_configure(relx=0.5 + offset)

        # Двигаем новый текст синхронно, но с противоположной стороны
        temp_label.place_configure(relx=0.5 - sign * (1 - progress) * total_shift)

        if step < steps:
            app.after(delay, slide_out, step + 1)
        else:
            # Финальное состояние
            image_button.configure(image=new_photo)
            image_button.image = new_photo

            # Удаляем старый лейбл, заменяем на новый
            label_text.configure(text=new_text)
            label_text.place_configure(relx=0.5)
            temp_label.destroy()

            # Подготовка кнопки к финальной анимации
            image_button.place_configure(relx=0.5 - sign * total_shift)
            slide_in()

    def slide_in(step=0):
        progress = step / steps
        offset = -sign * (1 - progress) * total_shift
        image_button.place_configure(relx=0.5 + offset)

        if step < steps:
            app.after(delay, slide_in, step + 1)
        else:
            image_button.place_configure(relx=0.5)

    slide_out()

# Функции перехода между слайдами
def next_slide():
    load_slide(current_index + 1, animate=True, direction="left")

def prev_slide():
    load_slide(current_index - 1, animate=True, direction="right")


def show_loading(callback=None):
    loading_label = ctk.CTkLabel(
        app,
        text="Loading...",
        font=("Arial", 20),
        text_color="#000000",
        fg_color="black"
    )
    loading_label.place(relx=0.5, rely=0.5, anchor="center")

    # Переменные для анимации точек
    dot_position = 0  # Начальная позиция для точек
    max_position = 10  # Максимальное смещение точек
    dot_direction = 1  # Направление движения (1 - вверх, -1 - вниз)

    def animate_dots():
        nonlocal dot_position, dot_direction

        # Смена позиции точек
        dot_position += dot_direction

        # Перевернуть направление, если мы достигли максимального смещения
        if dot_position >= max_position or dot_position <= 0:
            dot_direction *= -1

        # Генерация текста с анимацией точек
        dots = '.' * (dot_position % 4)
        loading_label.configure(text=f"Loading{dots}")

        # Повторить анимацию
        app.after(200, animate_dots)

    def fade(widget, start, end, step, delay, on_complete=None):
        def _fade(opacity=start):
            if (step > 0 and opacity <= end) or (step < 0 and opacity >= end):
                val = int(255 * opacity)
                color = f"#{val:02x}{val:02x}{val:02x}"
                widget.configure(text_color=color)
                app.after(delay, _fade, opacity + step)
            else:
                if on_complete:
                    on_complete()

        _fade()

    def done():
        loading_label.destroy()
        if callback:
            callback()

    # Плавный вход и выход
    fade(loading_label, 0, 1, 0.05, 30, on_complete=lambda:
        app.after(1500, lambda: fade(loading_label, 1, 0, -0.05, 30, on_complete=done)))

    # Запуск анимации точек
    animate_dots()

# Сброс таймера активности
def reset_inactivity_timer(event=None):
    global last_activity_time
    last_activity_time = time.time()  # Сброс таймера
    #print(last_activity_time)  # Для отладки
    hide_gif_animation()  # Останавливаем отображение GIF при активности

def load_timeout_setting():
    """Загрузка сохраненного значения времени из файла JSON."""
    global selected_timeout
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            selected_timeout = data.get("timeout", None)
    except (FileNotFoundError, json.JSONDecodeError):
        selected_timeout = None  # Если файл не найден или поврежден

# Проверка на бездействие
def check_inactivity():
    # Загрузка настроек при старте программы
    load_timeout_setting()
    """Проверка на бездействие."""
    global inactivity_timeout

    # Преобразуем текстовое значение `selected_timeout` в секунды
    if selected_timeout:  # Если значение выбрано
        timeout_mapping = {
            "5 seconds": 5,
            "10 seconds": 10,
            "30 seconds": 30,
            "1 minute": 60,
            "5 minutes": 300,
        }
        inactivity_timeout = timeout_mapping.get(selected_timeout, 5)  # Значение по умолчанию — 5 секунд

    # Проверяем, прошло ли время бездействия
    if time.time() - last_activity_time > inactivity_timeout:
        show_gif_animation()  # Показываем анимацию GIF при бездействии
    else:
        hide_gif_animation()  # Скрываем GIF при активности

    app.after(1000, check_inactivity)  # Проверка каждую секунду

# Функция для показа GIF анимации
def show_gif_animation():
    global gif_label, gif_frames, gif_durations, gif_animation_running, gif_visible

    if not alowed_gif_animation:
        return

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
    check_and_update_wifi_status()  # Важно вызвать это здесь, чтобы началась периодическая проверка

# Инициализация основного интерфейса
def init_app_layout():
    global content_frame
    # Панель с временем
    init_time_panel(app)

    # Контейнер для смены интерфейсов
    content_frame = ctk.CTkFrame(app, fg_color="#000000")
    content_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=1, relheight=0.9)

# Действия для слайдов
#=============================Главные действия=============================
def on_image_click():
    disable_swipe_temporarily(0.5)  # 🔒 Отключаем свайп на 2 секунды после нажатия
    action = slides[current_index]["action"]
    if action == "ddos_action":
        ddos_action()
    elif action == "wifi_action":
        wifi_action()
    elif action == "network_scan_action":
        network_scan_action()
    elif action == "bruteforce_action":
        bruteforce_action()
    elif action == "phishing_action":
        phishing_action()
    elif action == "settings_action":
        settings_action()
    elif action == "games_action":
        games_action()
    elif action == "files_action":
        files_action()
        
#========
def ddos_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    create_ddos_ui(content_frame, go_back_callback=go_back)

def bruteforce_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе
    def go_back():
        global alowed_swipe
        alowed_swipe = True
        init_main_ui(content_frame)
    init_bruteforce_ui(content_frame, go_back_callback=go_back)
#=======
def wifi_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе
    def go_back():
        global alowed_swipe
        alowed_swipe = True
        init_main_ui(content_frame)
    
    create_main_wifi_ui(content_frame, go_back_callback=go_back)  # Создаем интерфейс Wi-Fi
#==========
def network_scan_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    ns_ui(content_frame, go_back_callback=go_back)  # Создаем интерфейс сканирования сети

#=========
def phishing_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе
    def go_back():
        global alowed_swipe
        alowed_swipe = True
        init_main_ui(content_frame)
    create_main_phishing_ui(content_frame, go_back_callback=go_back)
#==========

def games_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    init_game_ui(content_frame, go_back_callback=go_back)  # Инициализация интерфейса игр
#==========
def files_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    file_browser_ui(content_frame, go_back_callback=go_back)  # Инициализация интерфейса файлового браузера
#==========
def settings_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    init_settings_ui(content_frame, go_back_callback=go_back)
#===========================================================================

# События свайпа
def on_swipe_start(event):
    global start_x, swipe_enabled, alowed_swipe

    if not alowed_swipe:
        print("[SWIPE START] Свайп отключён — ничего не делаем.")
        start_x = None
        return

    if not swipe_enabled:
        print("[SWIPE START] Свайп отключён — ничего не делаем.")
        start_x = None
        return
    # Получаем корневое окно
    root = event.widget._root()

    # Получаем настоящий объект
    try:
        widget = root.nametowidget(str(event.widget))
    except Exception as e:
        print(f"[SWIPE START] Ошибка при получении виджета: {e}")
        widget = event.widget

    print(f"[SWIPE START] Widget: {widget}, Type: {type(widget)}")

    # Проверяем, если свайп начался на кнопке или её потомке — отменяем
    parent = widget
    while parent:
        if isinstance(parent, ctk.CTkButton):
            print("[SWIPE START] Свайп отключён — начался на кнопке.")
            start_x = None
            return
        try:
            parent = parent.master
        except AttributeError:
            break

    # Проверка — разрешён ли свайп только на определённом виджете
    if not isinstance(widget, ctk.CTkCanvas):
        print("[SWIPE START] Свайп запрещён — не на Canvas.")
        start_x = None
        return

    # Всё ок — активируем свайп
    start_x = event.x
    print(f"[SWIPE START] Свайп активирован. start_x = {start_x}")


def on_swipe_end(event):
    global start_x

    if start_x is None:
        print("[SWIPE END] Свайп был отключён — ничего не делаем.")
        return

    end_x = event.x
    delta = end_x - start_x
    print(f"[SWIPE END] end_x = {end_x}, delta = {delta}")

    if abs(delta) > 50:
        if delta > 0:
            print("[SWIPE] Свайп вправо")
            prev_slide()
        else:
            print("[SWIPE] Свайп влево")
            next_slide()
    else:
        print("[SWIPE] Слишком маленькое смещение — свайп проигнорирован.")

def disable_swipe_temporarily(seconds=0.5):
    global swipe_enabled
    swipe_enabled = False
    print(f"[SWIPE] Свайп временно отключён на {seconds} сек")
    app.after(int(seconds * 1000), enable_swipe)

def enable_swipe():
    global swipe_enabled
    swipe_enabled = True
    print("[SWIPE] Свайп снова разрешён")


# Привязка событий к окну
app.bind("<ButtonPress-1>", on_swipe_start)  # Начало свайпа
app.bind("<ButtonRelease-1>", on_swipe_end)  # Конец свайпа

# Инициализация приложения
init_wifi_znak_with_texture(content_frame)
dvd_button()  # Кнопка DVD
exit_btn()  # Кнопка выхода
init_app_layout()
update_time()  # Запуск обновления времени
check_inactivity()  # Запуск проверки бездействия
#init_main_ui(content_frame)  # Отображение главного интерфейса

show_greeting(app, callback=lambda: show_loading(callback=lambda: init_main_ui(content_frame)))

# ========== Настройки приложения ==========
ctk.set_appearance_mode("Dark")  # Темная тема
app.title("Слайдер")
app.geometry("800x480")

app.bind_all("<Button>", reset_inactivity_timer)   # любое нажатие мыши
app.bind_all("<Key>", reset_inactivity_timer)      # любое нажатие клавиши
app.bind_all("<Motion>", reset_inactivity_timer)  # любое движение мыши

# fade_out_label(animation_label, 1)  # Скрываем анимацию при запуске приложения

# Запуск приложения
app.mainloop()