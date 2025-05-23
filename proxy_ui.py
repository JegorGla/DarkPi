import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import random
import customtkinter as ctk
import time
import json

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

    from bs4 import BeautifulSoup
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
            for item in data.get("data", []):
                ip = item.get("ip")
                port = item.get("port")
                if ip and port:
                    proxies.append((f"{ip}:{port}", "geonode"))
        except Exception:
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

def get_proxies_from_advanced_name():
    BASE_URL_ADVANCED_NAME_API = "https://advanced.name/freeproxy/682aea68553f3"
    proxies = []
    try:
        resp = requests.get(BASE_URL_ADVANCED_NAME_API, headers=get_random_headers(), timeout=10)
        resp.raise_for_status()
        proxy_list = resp.text.splitlines()
        proxies = [(p.strip(), "advanced.name") for p in proxy_list if p.strip()]
    except Exception:
        pass
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

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_proxy_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)
    
    # Основной вертикальный layout
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Верх: entry для URL и интервал
    top_frame = ctk.CTkFrame(main_frame)
    top_frame.pack(fill="x", pady=5)

    url_label = ctk.CTkLabel(top_frame, text="URL для проверки прокси:")
    url_label.pack(side="left", padx=(0, 5))

    url_entry = ctk.CTkEntry(top_frame)
    url_entry.pack(side="left", fill="x", expand=True)
    url_entry.insert(0, "https://google.com/")

    proxies_text = ctk.CTkTextbox(main_frame, height=300)
    proxies_text.pack(fill="both", expand=True, pady=10)

    # Интервал обновления
    interval_label = ctk.CTkLabel(top_frame, text="Интервал (мин):")
    interval_label.pack(side="left", padx=(10, 5))

    interval_entry = ctk.CTkEntry(top_frame, width=50)
    interval_entry.pack(side="left")
    interval_entry.insert(0, "10")

    # Центр: кнопки
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(fill="x", pady=10)

    # Функция для загрузки и проверки прокси с обновлением UI и сохранением в файл
    def load_and_check_proxies():
        print("Starting...")
        proxies_text.delete("0.0", "end")
        proxies_text.insert("end", "Загрузка прокси...\n")
        parent_frame.update_idletasks()

        proxies3 = get_proxies_from_free_proxy_list()
        proxies2 = get_proxies_from_geonode()
        proxies4 = get_proxies_from_proxyscrape()
        proxies1 = get_proxies_from_advanced_name()
        proxies = proxies1 + proxies2 + proxies3 + proxies4

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

        with open("working_proxies.txt", "w", encoding="utf-8") as f:
            with ThreadPoolExecutor(max_workers=50) as executor:
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
                            msg = f"[+] Рабочий прокси: {proxy} from {source}"
                        else:
                            msg = f"[-] Не работает прокси: {proxy} from {source}"

                        # Обновление UI для каждого результата
                        def update_ui():
                            proxies_text.insert("end", msg + "\n")
                            proxies_text.insert("end", f"Проверено: {checked}/{total} | Рабочих: {len(working_proxies)}\n")
                            proxies_text.see("end")
                            parent_frame.update_idletasks()
                        proxies_text.after(0, update_ui)

                # Обновляем UI только из главного потока
                def update_ui():
                    proxies_text.insert("end", msg + "\n")
                    proxies_text.see("end")
                    progress_msg = f"Проверено прокси: {checked}/{total} | Рабочих: {len(working_proxies)}"
                    proxies_text.insert("end", progress_msg + "\n")
                    parent_frame.update_idletasks()
                proxies_text.after(0, update_ui)

                print(msg)
                print(f"Проверено прокси: {checked}/{total} | Рабочих: {len(working_proxies)}")

        if not working_proxies:
            def show_no_proxies():
                proxies_text.delete("0.0", "end")
                msg = "Рабочих прокси не найдено.\n"
                proxies_text.insert("end", msg)
                print(msg)
            proxies_text.after(0, show_no_proxies)

    # Кнопка Change IP
    def on_change_ip_click():
        nonlocal auto_thread
        if auto_thread is None or not auto_thread.is_alive():
            stop_auto_update.clear()  # <== сбрасываем
            auto_thread = threading.Thread(target=auto_update_loop, daemon=True)
            auto_thread.start()
            proxies_text.insert("end", "Автообновление запущено.\n")

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
                auto_thread.join(timeout=1)  # ждем максимум 10 секунд
            except RuntimeError:
                pass
            auto_thread = None
            proxies_text.insert("end", "Автообновление остановлено.\n")
            parent_frame.update_idletasks()
            print("Auto-update stopped.")


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
            try:
                interval = int(interval_entry.get())
            except ValueError:
                interval = 10  # дефолт 10 мин
            load_and_check_proxies()
            # Ждем указанное время в минутах
            for _ in range(interval * 60):
                if stop_auto_update.is_set():
                    break
                time.sleep(1)

    def save_rechoise_proxy_interval(minutes: int):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data["proxy_rechoice_interval"] = minutes

        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    interval = int(interval_entry.get())
    save_rechoise_proxy_interval(interval)

    auto_thread = None  # Объявим переменную, но не запускаем поток

    # Вернем функцию для остановки автообновления (если понадобится)
    return stop_auto_update.set