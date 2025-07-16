import platform
import subprocess
from setup import setup  # Импортируем функцию настройки
from Values.date_time_config import *
if should_check_update():
    setup()
    update_last_check_time()

#=============================Импортируем библиотеки=============================
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
#+++++++++++++++Import all UI+++++++++++++++
from Values.phishing_ui import create_main_phishing_ui
from Values.wifi_ui import create_main_wifi_ui
from Values.network_scan_ui import ns_ui  # Импортируем функцию создания интерфейса сканирования сети
from Values.bruteforce_ui import init_bruteforce_ui
from Values.game_ui import init_game_ui  # Импортируем функцию создания меню игр
from Values.greeting import show_greeting  # Импортируем функцию показа приветствия
from Values.DVD_ui import create_dvd_ui  # Импортируем функцию создания DVD анимации
from Values.settings_ui import init_settings_ui, selected_timeout  # Импортируем функцию создания настроек и выбранное время
from Values.ddos_ui import create_ddos_ui  # Импортируем функцию создания DDoS UI
from Values.see_files_ui import file_browser_ui  # Импортируем функцию создания файлового браузера
from Values.pi_helper_ui import pi_helper_ui
from Values.rat_ui import create_rat_ui
from Values.osint_ui import create_osint_ui
from Values.qr_code_ui import create_qr_code_ui
from Values.bad_ble import bad_ble_ui
from Values.scan_site_ui import scan_site_ui
from Values.proxy_ui import create_proxy_ui
from Values.task_sheduler import task_sheduler_ui  # Импортируем функцию создания интерфейса планировщика задач
from Values.terminal_ui import terminal_ui
from Values.virus_ui import create_gallery_ui as create_virus_ui
from Values.exit_Value import exit_values
from Values.topology_scaned_target import create_topology
from Values.device_manager import device_manager_ui  # Импортируем функцию создания интерфейса менеджера устройств
#-----Task Scheduler----------
from TaskScheduler.proxy_task import stop_flag
from TaskScheduler.Proxy import proxy
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from datetime import datetime
import datetime
import random
import socket
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
current_edition = None
alowed_animation = None
is_always_anim = None

image_button_current = None
image_button_next = None

last_proxy_update = 0  # глобальное время последнего обновления

ip_label = None
choise_ip = "N/A"
last_proxy_update = 0

start_x = 0  # Начальная позиция свайпа

theme_folder = "Theme/"
#===================================================================

def get_theme_from_settings():
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            return data.get("theme", "Dark")
    except (FileNotFoundError, json.JSONDecodeError):
        return "Dark"

def apply_theme_from_settings():
    theme = get_theme_from_settings()
    if theme == "Light":
        ctk.set_appearance_mode("Light")
    elif theme == "Dark":
        ctk.set_default_color_theme(f"{theme_folder}Dark_theme.json")
    elif theme == "Flipper Zero":
        ctk.set_default_color_theme(f"{theme_folder}Flipper_Zero_theme.json")
    elif theme == "Blackout":
        ctk.set_default_color_theme(f"{theme_folder}Blackout_theme.json")

    return theme

# ✅ Применяем ТЕМУ СРАЗУ перед созданием приложения
apply_theme_from_settings()


#=============================Слайды=============================
slides = [
    {"image": "images/DDoS_image.png", "text": "DDOS attack\n (site test)", "action": "ddos_action"},
    {"image": "images/Wifi.png", "text": "Wifi", "action": "wifi_action"},
    {"image": "images/NetworkScan.png", "text": "Network Scan", "action": "network_scan_action"},
    {"image": "images/site_scan.png", "text": "Site Scan", "action": "site_scan_action"},
    {"image": "images/Qr_code_gen.png", "text": "QRCode Generation", "action": "qr_coder_action"},
    {"image": "images/Terminal.png", "text":"Terminal", "action": "terminal_action"},
    {"image": "images/EvilAP.png", "text": "EvilAp", "action": "evilap_action"},
    {"image": "images/Virus.png", "text": "Virus", "action": "virus_action"},
    {"image": "images/Bruteforce.png", "text": "Bruteforce", "action": "bruteforce_action"},
    {"image": "images/Phishing.png", "text": "Phishing", "action": "phishing_action"},
    {"image": "images/BadBLE.png", "text": "BadBLE", "action": "bad_ble_action"},
    {"image": "images/Scaned_target.png", "text": f"Scaned target\nMap", "action": "scaned_target_action"},
    {"image": "images/Osint.png", "text": "Osint", "action": "osint_action"},
    {"image": "images/scheduled-task-configuration.png", "text": "Task\nScheduler", "action": "task_scheduler_action"},
    {"image": "images/Games.png", "text": "Games", "action": "games_action"},
    {"image": "images/Folder.png", "text": "See files", "action": "files_action"},
    {"image": "images/Proxy.png", "text": "Proxy", "action": "proxy_action"},
    {"image": "images/Settings.png", "text": "Settings", "action": "settings_action"},
    {"image": "images/pi_helper.png", "text": "Pi-helper", "action": "pi_helper_action"},
    {"image": "images/device_mngr.png", "text": "Device Manager", "action": "device_manager_action"}
]

# Инициализация окна
app = ctk.CTk()

def dvd_button():
    def on_dvd_click():
        global alowed_gif_animation
        alowed_gif_animation = False  # Отключаем анимацию GIF.
        
        def go_back():
            global alowed_swipe, alowed_gif_animation
            alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
            alowed_gif_animation = True
            init_main_ui(content_frame)

        # Переход в DVD UI с логикой свайпа-назад
        create_dvd_ui(content_frame, go_back_callback=go_back)

    # Кнопка DVD
    dvd_btn = ctk.CTkButton(app, text="DVD", font=("Arial", 20), command=on_dvd_click, hover_color="#272727", fg_color="#242424", text_color="white")
    dvd_btn.place(relx=0, rely=0, x=10, y=10, anchor="nw")

def IP_Label():
    global ip_label
    if ip_label is None:
        ip_label = ctk.CTkLabel(app, text=f"IP:{choise_ip}", font=("Arial", 15), fg_color="#242424", text_color="#A30031")
        ip_label.place(relx=0.62, rely=0.023)
    else:
        ip_label.configure(text=f"IP:{choise_ip}")

def get_ip_proxy_from_file():
    global ip_label, choise_ip, last_proxy_update
    IP_Label()

    # Загружаем настройки
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
        interval_obj = settings.get("proxy_rechoice_interval", {"value": 10, "unit": "minutes"})

        # Проверяем что interval_obj - словарь с нужными ключами
        if isinstance(interval_obj, dict):
            value = int(interval_obj.get("value", 10))
            unit = interval_obj.get("unit", "minutes").lower()

            if unit == "minutes":
                interval_seconds = value * 60
            elif unit == "seconds":
                interval_seconds = value
            else:
                interval_seconds = 10 * 60  # дефолт 10 минут в секундах
        else:
            # Если вдруг старый формат (просто число)
            interval_seconds = int(interval_obj) * 60

        use_proxy = settings.get("use_proxy", "No") == "Yes"
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        interval_seconds = 10 * 60  # дефолт 10 минут в секундах
        use_proxy = False
        settings = {}

    # Отладочная печать: сколько секунд и в каких единицах хранится интервал
    # print(f"[DEBUG] Proxy rechoice interval: {value} {unit} ({interval_seconds} seconds)")

    # Если прокси выключен — скрыть метку и выйти
    if not use_proxy:
        if ip_label is not None:
            ip_label.destroy()
            ip_label = None
        app.after(1000, get_ip_proxy_from_file)
        return

    # Загружаем список прокси
    try:
        with open("working_proxies.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        lines = []

    current_time = time.time()

    # Время, оставшееся до следующей смены прокси
    time_since_update = current_time - last_proxy_update
    time_left = max(0, interval_seconds - time_since_update)

    # Отладочная печать, сколько осталось до смены прокси
    if unit == "minutes":
        pass
        # print(f"[DEBUG] Next proxy change in approximately: {time_left / 60:.1f} minutes")
    else:
        pass
        # print(f"[DEBUG] Next proxy change in approximately: {time_left:.0f} seconds")

    if lines:
        if time_since_update > interval_seconds:
            choise_ip = random.choice(lines)
            last_proxy_update = current_time
            # print(f"[INFO] Proxy changed to: {choise_ip}")
        else:
            pass
            #print(f"[INFO] Proxy not changed yet: {choise_ip}")
    else:
        choise_ip = "No proxy available"

    # Обновление или создание метки
    if ip_label is None:
        ip_label = ctk.CTkLabel(app, text=f"IP: {choise_ip}", font=("Arial", 15), fg_color="#242424", text_color="white")
        ip_label.place(relx=0.63, rely=0.023, anchor="nw")
    else:
        ip_label.configure(text=f"IP: {choise_ip}")

    # Обновление JSON
    settings["current_proxy"] = choise_ip
    try:
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        pass
        #print(f"[ERROR] Ошибка при сохранении settings.json: {e}")

    # Повторный вызов каждые 5 секунд
    app.after(500, get_ip_proxy_from_file)  # можно менять интервал обновления

get_ip_proxy_from_file()

def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    test_urls = [
        "https://httpbin.org/ip",
        "https://www.google.com",
        "https://www.github.com",
        "https://www.wikipedia.org",
        "https://api.ipify.org?format=json",
        "https://icanhazip.com/",
        "https://ifconfig.me/ip"
    ]

    
    try:
        test_url = random.choice(test_urls)
        print(test_url)  # выбираем случайный URL при каждом вызове
        response = requests.get(test_url, proxies=proxies, timeout=10)
        return response.status_code == 200
    except:
        return False


def start_proxy_validator_loop(settings_path="settings.json", proxy_file="working_proxies.txt"):
    def validator_loop():
        # Загрузка настроек
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                interval_value = settings["proxy_rechoice_interval"]["value"]
                interval_unit = settings["proxy_rechoice_interval"]["unit"]
        except Exception as e:
            #print(f"[!] Ошибка чтения настроек: {e}")
            return

        # Перевод в секунды
        multiplier = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600
        }.get(interval_unit.lower(), 60)

        interval_seconds = interval_value * multiplier

        while True:
            try:
                # Чтение текущих прокси
                with open(proxy_file, "r", encoding="utf-8") as f:
                    proxies = [line.strip() for line in f if line.strip()]
                
                valid_proxies = []

                # Проверка прокси с многопоточностью
                with ThreadPoolExecutor(max_workers=30) as executor:
                    futures = {executor.submit(check_proxy, p): p for p in proxies}
                    for future in as_completed(futures):
                        proxy = futures[future]
                        try:
                            if future.result():
                                valid_proxies.append(proxy)
                        except Exception:
                            continue

                # Обновление файла только с валидными прокси
                with open(proxy_file, "w", encoding="utf-8") as f:
                    for proxy in valid_proxies:
                        f.write(proxy + "\n")

                #print(f"[✓] Проверено: {len(proxies)} | Осталось рабочих: {len(valid_proxies)}")
            except Exception as e:
                #print(f"[!] Ошибка в цикле проверки прокси: {e}")
                pass

            # Ожидание до следующей итерации
            time.sleep(interval_seconds)

    # Запуск в фоне
    threading.Thread(target=validator_loop, daemon=True).start()

# start_proxy_validator_loop()

def exit_btn():
    def exit_app():
        global alowed_swipe
        alowed_swipe = False

        def go_back():
            global alowed_swipe
            alowed_swipe = True
            init_main_ui(content_frame)
        
        exit_values(content_frame, go_back_callback=go_back)
    
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
        # print("[INFO] Wi-Fi is connected.")
        # Если Wi-Fi подключен, загружаем изображение для подключенного состояния
        texture_image = Image.open("images/WifiConnected.png")
    else:
        # print("[INFO] Wi-Fi is disconnected.")
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
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 53))
        return True
    except socket.error:
        return False

def show_connected_network():
    """Отображает название подключенной сети."""
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(
                "netsh wlan show interfaces",
                shell=True,
                encoding="cp866"  # Ключевой момент: правильная кодировка консоли
            )
            for line in output.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":", 1)[1].strip()
                    wifi_znak_label.configure(text=ssid)  # Обновляем текст метки
                    app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Сбрасываем текст через 2 секунды
        except subprocess.CalledProcessError:
            wifi_znak_label.configure(text="No connection")
            app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Сбрасываем текст через 2 секунды
    elif platform.system() == "Linux":
        try:
            output = subprocess.check_output("iwgetid -r", shell=True, text=True)
            ssid = output.strip()
            wifi_znak_label.configure(text=ssid)  # Обновляем текст метки
            app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Сбрасываем текст через 2 секунды
        except subprocess.CalledProcessError:
            wifi_znak_label.configure(text="No connection")
            app.after(2000, lambda: wifi_znak_label.configure(text=""))  # Сбрасываем текст через 2 секунды


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

    sign = -1 if direction == "left" else 1

    # Создаем временный лейбл для нового текста (он будет сдвигаться вместе с кнопкой)
    temp_label = ctk.CTkLabel(content_frame, text=new_text, font=("Arial", 20))
    temp_label.place(relx=0.5 - sign * total_shift, rely=0.75, anchor="center")
    temp_label.lower()  # Скрываем под текущим текстом, пока не будет момент замены

    def slide_out(step=0):
        if not image_button or not image_button.winfo_exists():
            return

        progress = step / steps
        offset = sign * progress * total_shift

        # Двигаем кнопку и текущий текст вместе вправо/влево
        image_button.place_configure(relx=0.5 + offset)
        label_text.place_configure(relx=0.5 + offset)

        if step < steps:
            app.after(delay, slide_out, step + 1)
        else:
            # Когда старые элементы "ушли", меняем содержимое
            image_button.configure(image=new_photo)
            image_button.image = new_photo

            label_text.configure(text=new_text)
            label_text.place_configure(relx=0.5 - sign * total_shift)

            temp_label.destroy()  # Удаляем временный лейбл

            slide_in()

    def slide_in(step=0):
        progress = step / steps
        offset = -sign * (1 - progress) * total_shift

        # Появляем кнопку и текст вместе
        image_button.place_configure(relx=0.5 + offset)
        label_text.place_configure(relx=0.5 + offset)

        if step < steps:
            app.after(delay, slide_in, step + 1)
        else:
            image_button.place_configure(relx=0.5)
            label_text.place_configure(relx=0.5)

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

def get_current_edition():
    """Функция для загрузки актуальной редакции из settings.json."""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            edition = data.get("edition", "Evil eye")  # Значение по умолчанию
            #print(f"[INFO] Loaded edition from settings: {edition}")
            return edition
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[ERROR] {e}. Returning default edition 'Normal edition'.")
        return "Evil eye"  # Возвращаем дефолтное значение

def get_allowed_anim():
    global alowed_animation, is_always_anim
    try:
        with open("settings.json", "r") as f:
            setting = json.load(f)
            alowed_animation = setting.get("allowed_anim", True)
            is_always_anim = setting.get("always_show_anim", False)
    except Exception:
        alowed_animation = True  # если файл отсутствует или ошибка
        is_always_anim =  False

def set_allowed_anim(value: bool):
    try:
        settings = {}

        # Если файл существует, загрузить его содержимое
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                settings = json.load(f)

        # Обновляем или добавляем ключ
        settings["allowed_anim"] = value

        # Записываем обратно обновлённый словарь
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    except Exception as e:
        print("Ошибка при записи файла:", e)


def show_gif_animation():
    global gif_label, gif_frames, gif_durations, gif_animation_running, gif_visible, current_edition, alowed_animation, is_always_anim

    get_allowed_anim()  # обновим значение из файла

    edition = get_current_edition()  # Получаем актуальное значение редакции

    # Проверка на смену редакции
    if edition != current_edition:
        current_edition = edition
        gif_frames = []
        gif_durations = []
        gif_animation_running = False

    # Определение нужного GIF
    try:
        gif_path = None
        if edition == "Evil eye":
            gif_path = "images/gif_animation/EvilEye.gif"
        elif edition == "P Diddy":
            gif_path = "images/gif_animation/P_ddidy.gif"
        elif edition == "Smile ascii":
            gif_path = "images/gif_animation/ascii_smile.gif"
        elif edition == "Matrix":
            gif_path = "images/gif_animation/hacker_matrix.gif"
        elif edition == "Boom":
            gif_path = "images/gif_animation/ascii_boom_correct_order.gif"
        elif edition == "Car":
            gif_path = "images/gif_animation/car.gif"
        elif edition == "Space warp":
            gif_path = "images/gif_animation/space_warp_loop.gif"
        elif edition == "Earth":
            gif_path = "images/gif_animation/earth.gif"

        if not gif_path or not os.path.exists(gif_path):
            raise FileNotFoundError("GIF file not found for selected edition.")

        gif = Image.open(gif_path)

    except (FileNotFoundError, Exception) as e:
        print(f"[ERROR] {e}")
        return

    if not alowed_animation and not is_always_anim:
        return

    if gif_visible:
        return  # если уже видна — не запускаем повторно

    gif_visible = True

    if gif_label is None:
        gif_label = ctk.CTkLabel(app, text="", fg_color="transparent")
    gif_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

    if not gif_frames:
        for frame in ImageSequence.Iterator(gif):
            resized = frame.resize((app.winfo_width(), app.winfo_height()), Image.Resampling.LANCZOS)
            gif_frames.append(ImageTk.PhotoImage(resized))
            gif_durations.append(frame.info.get('duration', 100))

    if not gif_animation_running:
        gif_animation_running = True

        def update_gif(index=0):
            if not gif_visible:
                return
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
    image_button = ctk.CTkButton(parent_frame, text="", command=on_image_click, width=400, height=300)
    image_button.place(relx=0.5, rely=0.4, anchor="center")
    
    if apply_theme_from_settings() == "Blackout" or apply_theme_from_settings() == "Dark":
        print("YEAH! Blackout theme applied")
        image_button.configure(fg_color="#000000", hover_color="#000000", border_color="#000000")

    # Подпись под изображением
    label_text = ctk.CTkLabel(parent_frame, text="", font=("Arial", 20))
    label_text.place(relx=0.5, rely=0.75, anchor="center")

    # Левая стрелка
    prev_button = ctk.CTkButton(parent_frame, text="←", width=50, height=50, command=prev_slide, font=("Arial", 24))
    prev_button.place(relx=0.1, rely=0.4, anchor="center")

    # Правая стрелка
    next_button = ctk.CTkButton(parent_frame, text="→", width=50, height=50, command=next_slide, font=("Arial", 24))
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
    content_frame = ctk.CTkFrame(app)
    content_frame.place(relx=0.5, rely=0.55, anchor="center", relwidth=1, relheight=0.9)

# Действия для слайдов
#=============================Главные действия=============================
def on_image_click():
    disable_swipe_temporarily(1)  # 🔒 Отключаем свайп на 2 секунды после нажатия
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
    elif action == "osint_action":
        osint_action()
    elif action == "games_action":
        games_action()
    elif action == "files_action":
        files_action()
    elif action == "pi_helper_action":
        pi_helper_action()
    elif action == "rat_action":
        rat_action()
    elif action == "qr_coder_action":
        qr_coder_action()
    elif action == "bad_ble_action":
        bad_ble_action()
    elif action == "site_scan_action":
        site_scan_action()
    elif action == "proxy_action":
        proxy_action()
    elif action == "task_scheduler_action":
        task_scheduler_action()
    elif action == "terminal_action":
        terminal_action()
    elif action == "virus_action":
        virus_action()
    elif action == "scaned_target_action":
        scaned_target_action()
#========
def ddos_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        set_allowed_anim(True)
        init_main_ui(content_frame)

    create_ddos_ui(content_frame, go_back_callback=go_back)
#========
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
        enable_fullscreen(app)

    init_settings_ui(content_frame, go_back_callback=go_back)
#========
def pi_helper_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)
    pi_helper_ui(content_frame, go_back_callback=go_back)
#=======
def rat_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)
    create_rat_ui(content_frame, go_back_callback=go_back)
#========
def osint_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)
    create_osint_ui(content_frame, go_back_callback=go_back)
#========
def qr_coder_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_app_layout()
        init_main_ui(content_frame)

    create_qr_code_ui(content_frame, go_back_callback=go_back)
#========
def bad_ble_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_app_layout()
        init_main_ui(content_frame)

    bad_ble_ui(content_frame, go_back_callback=go_back)
#=========
def site_scan_action():
    global alowed_swipe
    alowed_swipe = False

    def go_back():
        global alowed_swipe
        alowed_swipe = True
        init_app_layout()
        init_main_ui(content_frame)
    scan_site_ui(content_frame, go_back_callback=go_back)
#=========
def proxy_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)
    create_proxy_ui(content_frame, go_back_callback=go_back)
#=========
def task_scheduler_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True
        init_main_ui(content_frame)
    
    task_sheduler_ui(content_frame, go_back_callback=go_back)  # Инициализация интерфейса планировщика задач
#=========
def terminal_action():
    global alowed_swipe
    alowed_swipe = True

    def go_back():
        global alowed_swipe
        alowed_swipe = False
        init_main_ui(content_frame)

    terminal_ui(parent_frame=content_frame, go_back_callback=go_back)
#=========
def virus_action():
    global alowed_swipe
    alowed_swipe = True

    def go_back():
        global alowed_swipe
        alowed_swipe = False
        init_main_ui(content_frame)

    create_virus_ui(content_frame, go_back)
#==========
def scaned_target_action():
    global alowed_swipe
    alowed_swipe = True

    def go_back():
        global alowed_swipe
        alowed_swipe = False
        init_main_ui(content_frame)

    create_topology(content_frame, go_back_callback=go_back)

def device_manager_action():
    global alowed_swipe
    alowed_swipe = False  # Отключаем свайп при заходе

    def go_back():
        global alowed_swipe
        alowed_swipe = True  # ВКЛЮЧАЕМ свайп при возврате
        init_main_ui(content_frame)

    device_manager_ui(content_frame, go_back_callback=go_back)  # Инициализация интерфейса менеджера устройств
#===========================================================================

# События свайпа
def on_swipe_start(event):
    global start_x, swipe_enabled, alowed_swipe

    if not alowed_swipe:
        #print("[SWIPE START] Свайп отключён — ничего не делаем.")
        start_x = None
        return

    if not swipe_enabled:
        #print("[SWIPE START] Свайп отключён — ничего не делаем.")
        start_x = None
        return
    # Получаем корневое окно
    root = event.widget._root()

    # Получаем настоящий объект
    try:
        widget = root.nametowidget(str(event.widget))
    except Exception as e:
        #print(f"[SWIPE START] Ошибка при получении виджета: {e}")
        widget = event.widget

    #print(f"[SWIPE START] Widget: {widget}, Type: {type(widget)}")

    # Проверяем, если свайп начался на кнопке или её потомке — отменяем
    parent = widget
    while parent:
        if isinstance(parent, ctk.CTkButton):
            #print("[SWIPE START] Свайп отключён — начался на кнопке.")
            start_x = None
            return
        try:
            parent = parent.master
        except AttributeError:
            break

    # Проверка — разрешён ли свайп только на определённом виджете
    if not isinstance(widget, ctk.CTkCanvas):
        #print("[SWIPE START] Свайп запрещён — не на Canvas.")
        start_x = None
        return

    # Всё ок — активируем свайп
    start_x = event.x
    #print(f"[SWIPE START] Свайп активирован. start_x = {start_x}")


def on_swipe_end(event):
    global start_x

    if start_x is None:
        #print("[SWIPE END] Свайп был отключён — ничего не делаем.")
        return

    end_x = event.x
    delta = end_x - start_x
    #print(f"[SWIPE END] end_x = {end_x}, delta = {delta}")

    if abs(delta) > 50:
        if delta > 0:
            #print("[SWIPE] Свайп вправо")
            prev_slide()
        else:
            #print("[SWIPE] Свайп влево")
            next_slide()
    else:
        pass  # Игнорируем свайп, если смещение слишком маленькое
        #print("[SWIPE] Слишком маленькое смещение — свайп проигнорирован.")

def disable_swipe_temporarily(seconds=0.5):
    global swipe_enabled
    swipe_enabled = False
    #print(f"[SWIPE] Свайп временно отключён на {seconds} сек")
    app.after(int(seconds * 1000), enable_swipe)

def enable_swipe():
    global swipe_enabled
    swipe_enabled = True
    #print("[SWIPE] Свайп снова разрешён")

def enable_fullscreen(app):
    """Применяет полноэкранный режим к окну в зависимости от настроек."""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
            fullscreen = data.get("fullscreen", "No")
            app.attributes("-fullscreen", fullscreen == "Yes")
    except FileNotFoundError:
        print("[WARNING] settings.json not found — fullscreen not applied.")
    except Exception as e:
        print(f"[ERROR] Failed to apply fullscreen setting: {e}")

def load_scheduler_setting():
    global task_settings, tool_value, time_value, every_day_value
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)

        # Достаём вложенные значения
        task_settings = settings.get("task_scheduler", {})
        tool_value = task_settings.get("tool", "")
        time_value = task_settings.get("time", "")
        every_day_value = task_settings.get("every_day", False)

    except FileNotFoundError:
        print("settings.json not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")

    app.after(1000, load_scheduler_setting)

def schedule_checker():
    global task_settings, tool_value, time_value, every_day_value

    now = datetime.datetime.now()

    try:
        if every_day_value:
            # Ожидаем формат HH:MM
            target_time = datetime.datetime.strptime(time_value, "%H:%M").time()

            if now.hour == target_time.hour and now.minute == target_time.minute:
                run_scheduled_task()
        else:
            # Ожидаем формат YYYY-MM-DD HH:MM
            target_datetime = datetime.datetime.strptime(time_value, "%Y-%m-%d %H:%M")

            if now.strftime("%Y-%m-%d %H:%M") == target_datetime.strftime("%Y-%m-%d %H:%M"):
                run_scheduled_task()

    except ValueError:
        print("Неверный формат времени в настройках")

    # Проверяем каждую минуту
    app.after(60 * 1000, schedule_checker)

def run_scheduled_task():
    print(f"🚀 Выполняем задачу: {tool_value}")
    if tool_value == "Proxy":
        def task():
            stop_flag = threading.Event()
            proxy.main(quantity=None, stop_flag=stop_flag)

        thread = threading.Thread(target=task)
        thread.daemon = True  # завершится с закрытием программы
        thread.start()

def start_tor_for_proxy():
    def run_tor():
        # Запуск команды через shell=True, чтобы работала systemctl
        subprocess.run("systemctl start tor", shell=True)

    thread = threading.Thread(target=run_tor, daemon=True)
    thread.start()


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
enable_fullscreen(app)
#init_main_ui(content_frame)  # Отображение главного интерфейса

show_greeting(app, callback=lambda: show_loading(callback=lambda: init_main_ui(content_frame)))

load_scheduler_setting()
load_scheduler_setting()
schedule_checker()
if platform.system() != "Windows":
    start_tor_for_proxy()

# ========== Настройки приложения ==========
app.geometry("800x480")

app.bind_all("<Button>", reset_inactivity_timer)   # любое нажатие мыши
app.bind_all("<Key>", reset_inactivity_timer)      # любое нажатие клавиши
app.bind_all("<Motion>", reset_inactivity_timer)  # любое движение мыши

# fade_out_label(animation_label, 1)  # Скрываем анимацию при запуске приложения

# Запуск приложения
app.mainloop()