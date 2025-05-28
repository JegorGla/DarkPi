import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64
from bs4 import BeautifulSoup
import threading
import random
import customtkinter as ctk
import time
import json
from virtual_keyboard import NormalKeyboard

url_free_proxy_list = 'https://free-proxy-list.net/'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
]

def get_random_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://free-proxy-list.net/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def get_proxies_from_free_proxy_list():
    session = requests.Session()
    response = session.get(url_free_proxy_list, headers=get_random_headers(), timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    table = None
    for t in soup.find_all('table'):
        classes = t.get('class', [])
        if all(c in classes for c in ['table', 'table-striped', 'table-bordered']):
            table = t
            break

    proxies = []
    if table:
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append((f"{ip}:{port}", "free-proxy-list"))
    return proxies

def get_proxies_from_geonode():
    BASE_URL_GEONODE_API = "https://proxylist.geonode.com/api/proxy-list"
    LIMIT = 500
    MAX_PAGES = 20
    proxies = []
    for page in range(1, MAX_PAGES + 1):
        params = {
            "limit": LIMIT,
            "page": page,
            "sort_by": "lastChecked",
            "sort_type": "desc"
        }
        try:
            resp = requests.get(BASE_URL_GEONODE_API, params=params, headers=get_random_headers(), timeout=10)
            resp.raise_for_status()
            data = resp.json()
            print(f"Page {page} data keys: {data.keys()}")  # Отладка
            print(f"Sample data: {data.get('data', [])[:2]}")  # Вывести пару прокси
            for item in data.get("data", []):
                ip = item.get("ip")
                port = item.get("port")
                if ip and port:
                    proxies.append((f"{ip}:{port}", "geonode"))
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    return proxies


def get_proxies_from_proxyscrape():
    BASE_URL_PROXYSCRAPE_API = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    proxies = []
    try:
        resp = requests.get(BASE_URL_PROXYSCRAPE_API, headers=get_random_headers(), timeout=10)
        resp.raise_for_status()
        proxy_list = resp.text.splitlines()
        proxies = [(p.strip(), "proxyscrape") for p in proxy_list if p.strip()]
    except Exception:
        pass
    return proxies

def get_proxies_from_advanced_name(pages=5):
    BASE_URL = "https://advanced.name/freeproxy/"
    proxies = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}?page={page}"
        try:
            resp = requests.get(url, headers=get_random_headers(), timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, 'html.parser')
            table = soup.find('table', id='table_proxies')
            if not table:
                print(f"[!] Таблица не найдена на странице {page}")
                continue

            rows = table.find('tbody').find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue

                ip_encoded = cols[1].get("data-ip")
                port_encoded = cols[2].get("data-port")

                if not ip_encoded or not port_encoded:
                    continue

                try:
                    ip = base64.b64decode(ip_encoded).decode("utf-8")
                    port = base64.b64decode(port_encoded).decode("utf-8")
                    proxy = f"{ip}:{port}"
                    proxies.append((proxy, "advanced.name"))
                except Exception as e:
                    print(f"[!] Ошибка декодирования IP/порта: {e}")
                    continue

        except Exception as e:
            print(f"[!] Ошибка загрузки страницы {page}: {e}")
            continue

        time.sleep(1)  # не спамим сервер

    return proxies


def get_proxies_from_free_porxy_cz(pages=70):
    proxies = []

    for page in range(1, pages + 1):
        url = f"http://free-proxy.cz/en/proxylist/main/{page}"
        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            print(f"[!] Ошибка загрузки страницы {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="proxy_list")
        if not table:
            print(f"[!] Не найдена таблица на странице {page}")
            continue

        rows = table.find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            script = cols[0].find("script")
            if not script or "Base64.decode" not in script.text:
                continue

            try:
                encoded_ip = script.string.split("Base64.decode(\"")[1].split("\")")[0]
                ip = base64.b64decode(encoded_ip).decode("utf-8")
                port = cols[1].text.strip()
                proxy = f"{ip}:{port}"
                proxies.append((proxy, "free-proxy.cz"))  # ✅ нужно так
            except Exception as e:
                print(f"[!] Ошибка декодирования IP: {e}")
                continue

        time.sleep(1)  # Не спамим сервер

    return proxies

def check_proxy(proxy):
    proxies = {
        'http': f"http://{proxy}",
        'https': f"http://{proxy}",
    }
    test_url = 'https://google.com/'  # URL для проверки прокси
    # test_url = 'https://httpbin.org/ip'  # Альтернативный URL для проверки прокси
    try:
        resp = requests.get(test_url, proxies=proxies, timeout=5)
        if resp.status_code == 200:
            return (proxy, True, None)
        else:
            return (proxy, False, f"Status code: {resp.status_code}")
    except Exception as e:
        return (proxy, False, str(e))

def validate_existing_proxies(file_path="working_proxies.txt"):
    valid_proxies = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []  # Файл не найден — возвращаем пустой список

    with ThreadPoolExecutor(max_workers=70) as executor:
        futures = [executor.submit(check_proxy, proxy) for proxy in proxies]
        for future in as_completed(futures):
            proxy, status, _ = future.result()
            if status:
                valid_proxies.append(proxy)
    
    # Перезаписываем файл только рабочими
    with open(file_path, "w", encoding="utf-8") as f:
        for proxy in valid_proxies:
            f.write(proxy + "\n")

    return valid_proxies


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_get_proxy_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)
    
    # Основной вертикальный layout
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Верх: entry для URL и интервал
    top_frame = ctk.CTkFrame(main_frame)
    top_frame.pack(fill="x", pady=5)

    url_label = ctk.CTkLabel(top_frame, text="URL for proxy check:")
    url_label.pack(side="left", padx=(0, 5))

    url_entry = ctk.CTkEntry(top_frame)
    url_entry.pack(side="left", fill="x", expand=True)
    url_entry.insert(0, "https://google.com/")

    proxies_text = ctk.CTkTextbox(main_frame, height=300)
    proxies_text.pack(fill="both", expand=True, pady=10)
    
    # Центр: кнопки
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(fill="x", pady=10)

    bottom_frame = ctk.CTkFrame(main_frame)
    bottom_frame.pack(fill="x", pady=10)

    close_keyboard_button = ctk.CTkButton(
        bottom_frame,
        text="X",
        font=("Arial", 25),
        command=lambda: hide_keyboard(),
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        width=50,
        height=50,
        border_width=2
    )
    close_keyboard_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    # Функция для загрузки и проверки прокси с обновлением UI и сохранением в файл
    def load_and_check_proxies():
        #print(("Starting...")
        proxies_text.insert("end", "Validating existing proxies...\n")
        parent_frame.update_idletasks()

        valid_existing = validate_existing_proxies()

        if valid_existing:
            proxies_text.insert("end", f"✓ {len(valid_existing)} existing proxies are still valid.\n")
        else:
            proxies_text.insert("end", "No existing proxies were valid. Loading new proxies...\n")


        proxies_text.delete("0.0", "end")
        proxies_text.insert("end", "Loading proxy...\n")
        parent_frame.update_idletasks()

        proxies3 = get_proxies_from_free_proxy_list()
        proxies4 = get_proxies_from_geonode()
        proxies2 = get_proxies_from_proxyscrape()
        proxies1 = get_proxies_from_advanced_name()
        proxies5 = get_proxies_from_free_porxy_cz()
        proxies = proxies1 + proxies2 + proxies3 + proxies4 + proxies5

        working_proxies = []
        lock = threading.Lock()

        test_url = url_entry.get().strip() or "https://google.com/"

        def check_proxy_local(proxy, source, stop_event):
            if stop_event.is_set():
                return (proxy, False, source)

            proxies_dict = {
                'http': f"http://{proxy}",
                'https': f"http://{proxy}",
            }
            try:
                resp = requests.get(test_url, proxies=proxies_dict, timeout=5)
                if stop_event.is_set():
                    return (proxy, False, source)
                if resp.status_code == 200:
                    return (proxy, True, source)
                else:
                    return (proxy, False, source)
            except Exception:
                return (proxy, False, source)


        total = len(proxies)
        checked = 0

        with open("working_proxies.txt", "a", encoding="utf-8") as f:
            with ThreadPoolExecutor(max_workers=70) as executor:
                futures = [executor.submit(check_proxy_local, p[0], p[1], stop_auto_update) for p in proxies]
                for future in as_completed(futures):
                    if stop_auto_update.is_set():
                        break  # Прерываем цикл, не проверяем больше
                    proxy, status, source = future.result()
                    with lock:
                        checked += 1
                        if status:
                            working_proxies.append(proxy)
                            f.write(proxy + "\n")
                            f.flush()
                            msg = f"[+] Worked proxy: {proxy} from {source}"
                        else:
                            msg = f"[-] Proxy not working: {proxy} from {source}"

                        # Обновление UI для каждого результата
                        def update_ui():
                            proxies_text.insert("end", msg + "\n")
                            proxies_text.insert("end", f"Checked: {checked}/{total} | Workers: {len(working_proxies)}\n")
                            proxies_text.see("end")
                            parent_frame.update_idletasks()
                        proxies_text.after(0, update_ui)

                # Обновляем UI только из главного потока
                def update_ui():
                    proxies_text.insert("end", msg + "\n")
                    proxies_text.see("end")
                    progress_msg = f"Cheked proxy: {checked}/{total} | Workers: {len(working_proxies)}"
                    proxies_text.insert("end", progress_msg + "\n")
                    parent_frame.update_idletasks()
                proxies_text.after(0, update_ui)

        if not working_proxies:
            def show_no_proxies():
                proxies_text.delete("0.0", "end")
                msg = "No working proxies found.\n"
                proxies_text.insert("end", msg)
                #print((msg)
            proxies_text.after(0, show_no_proxies)

    # Кнопка Change IP
    def on_change_ip_click():
        nonlocal auto_thread
        if auto_thread is None or not auto_thread.is_alive():
            stop_auto_update.clear()  # <== сбрасываем
            auto_thread = threading.Thread(target=auto_update_loop, daemon=True)
            auto_thread.start()
            proxies_text.insert("end", "Auto update started.\n")

    change_ip_button = ctk.CTkButton(
        button_frame,
        text="Change IP",
        fg_color="#000000",
        border_color="#8d33ff",
        hover_color="#FF6A00",
        border_width=2,
        command=on_change_ip_click
    )
    change_ip_button.pack(side="left", padx=10)

    # Кнопка Stop
    def on_stop_click():
        nonlocal auto_thread, proxies_text
        if auto_thread is not None and auto_thread.is_alive():
            stop_auto_update.set()
            try:
                auto_thread.join(timeout=10)  # ждем максимум 10 секунд
            except RuntimeError:
                pass
            auto_thread = None
            proxies_text.insert("end", "Auto update stopped.\n")
            parent_frame.update_idletasks()
            #print(("Auto-update stopped.")


    stop_btn = ctk.CTkButton(
        button_frame,
        command=on_stop_click,
        text="Stop",
        fg_color="#FF6A00",
        hover_color="#FF6A00",
        border_color="#8d33ff",
        border_width=2
    )
    stop_btn.pack(side="left", padx=10)

    back_btn = ctk.CTkButton(
        button_frame,
        text="← Back",
        command=go_back_callback,
        fg_color="#f44336",
        hover_color="#e53935"
    )
    back_btn.pack(side="left", padx=10)

    
    # Автообновление по таймеру
    stop_auto_update = threading.Event()
    

    def auto_update_loop():
        while not stop_auto_update.is_set():

            interval = 10

            load_and_check_proxies()

            # Ждем указанное время в минутах
            for _ in range(interval * 60):
                if stop_auto_update.is_set():
                    break
                time.sleep(1)
    
    auto_thread = None  # Объявим переменную, но не запускаем поток
    
    # Переменная для хранения активного поля
    active_entry = None
    def set_target_entry(entry, name):
        nonlocal active_entry
        active_entry = entry
        keyboard.target_entry = entry
        #print(f"[DEBUG] Активное поле ввода: {name}")

    # Виртуальная клавиатура в нижнем фрейме
    keyboard = None  # Клавиатура будет создана позже


    # Привязка клавиатуры к полям ввода
    url_entry.bind("<FocusIn>", lambda e: [set_target_entry(url_entry, "Target (IP/Domain)"), show_keyboard()])

    keyboard_visible = False

    def slide_keyboard(target_y, step=10):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2

        current_y = bottom_frame.winfo_y()
        if abs(current_y - target_y) < step:
            bottom_frame.place_configure(x=x_pos, y=target_y, width=keyboard_width, height=keyboard_height)
            return
        direction = 1 if target_y > current_y else -1
        next_y = current_y + direction * step
        bottom_frame.place_configure(x=x_pos, y=next_y, width=keyboard_width, height=keyboard_height)
        parent_frame.after(10, lambda: slide_keyboard(target_y, step))


    def show_keyboard():
        nonlocal keyboard_visible, keyboard
        if keyboard_visible:
            return

        if keyboard is None:
            keyboard = NormalKeyboard(bottom_frame, url_entry)
            # Привязка только при первом создании:
            url_entry.bind("<FocusIn>", lambda e: [set_target_entry(url_entry, "Target (IP/Domain)"), show_keyboard()])

        keyboard_visible = True
        slide_keyboard(target_y=parent_frame.winfo_height() - 300)


    def hide_keyboard():
        nonlocal keyboard_visible
        if not keyboard_visible:
            return
        keyboard_visible = False
        slide_keyboard(target_y=parent_frame.winfo_height())

    def toggle_keyboard():
        if keyboard_visible:
            hide_keyboard()
        else:
            show_keyboard()

    toggle_button = ctk.CTkButton(
        button_frame,
        text="⌨ Клавиатура",
        command=toggle_keyboard,
        fg_color="#3b3b3b",
        border_color="#8d33ff",
        hover_color="#444444",
        border_width=2
    )
    toggle_button.pack(side="left", padx=10)


    # Изначально клавиатура скрыта (сдвигаем за пределы контейнера)
    keyboard_width = 750
    keyboard_height = 300

    def place_keyboard_at(y_pos):
        parent_frame.update()
        parent_frame_width = parent_frame.winfo_width()
        x_pos = (parent_frame_width - keyboard_width) // 2
        bottom_frame.place(in_=parent_frame, x=x_pos, y=y_pos, width=keyboard_width, height=keyboard_height)

    # Изначально скрываем клавиатуру
    place_keyboard_at(parent_frame.winfo_height())