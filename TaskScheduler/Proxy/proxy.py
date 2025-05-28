import requests
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, as_completed
from colorama import init, Fore
import threading
import random

init(autoreset=True)  # Инициализация colorama

url_free_proxy_list = 'https://free-proxy-list.net/'

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
    # добавь ещё варианты по желанию
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
    response = session.get(url_free_proxy_list, headers=get_random_headers())
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
                proxy = f"{ip}:{port}"
                proxies.append((proxy, "free-proxy-list"))
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
            print(Fore.CYAN + f"Загружено прокси со страницы {page}: {len(proxies)}")
        except Exception as e:
            print(Fore.RED + f"Ошибка при загрузке страницы {page}: {e}")
            break
    return proxies

def get_proxies_from_proxyscrape():
    BASE_URL_PROXYSCRAPE_API = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    proxies = []
    try:
        resp = requests.get(BASE_URL_PROXYSCRAPE_API, headers=get_random_headers(), timeout=10)
        resp.raise_for_status()
        proxy_list = resp.text.splitlines()
        # Удаляем пустые строки и формируем кортежи с источником
        proxies = [(p.strip(), "proxyscrape") for p in proxy_list if p.strip()]
        print(Fore.CYAN + f"Загружено прокси с Proxyscrape: {len(proxies)}")
    except Exception as e:
        print(Fore.RED + f"Ошибка при загрузке прокси с Proxyscrape: {e}")
    return proxies

def get_proxie_from_advanced_name():
    BASE_URL_ADVANCED_NAME_API = "https://advanced.name/freeproxy/682aea68553f3"
    proxies = []
    try:
        resp = requests.get(BASE_URL_ADVANCED_NAME_API, headers=get_random_headers(), timeout=10)
        resp.raise_for_status()
        proxy_list = resp.text.splitlines()
        # Удаляем пустые строки и формируем кортежи с источником
        proxies = [(p.strip(), "advanced.name") for p in proxy_list if p.strip()]
        print(Fore.CYAN + f"Загружено прокси с advanced.name: {len(proxies)}")
    except Exception as e:
        print(Fore.RED + f"Ошибка при загрузке прокси с advanced.name: {e}")
    return proxies

def check_proxy(proxy):
    proxies = {
        'http': f"http://{proxy}",
        'https': f"http://{proxy}",
    }
    test_url = 'https://httpbin.org/ip'  # URL для проверки работоспособности прокси
    try:
        resp = requests.get(test_url, proxies=proxies, timeout=5)
        if resp.status_code == 200:
            return (proxy, True, None)
        else:
            return (proxy, False, f"Status code: {resp.status_code}")
    except Exception as e:
        return (proxy, False, str(e))


def main(quantity, stop_flag):
    checked_proxies = set()
    working_proxies = set()
    lock = threading.Lock()

    def save_proxy(proxy):
        with lock:
            with open("working_proxies.txt", "a") as f:
                f.write(f"{proxy}\n")
                f.flush()

    def load_working_proxies():
        try:
            with open("working_proxies.txt", "r") as f:
                return set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            return set()

    sources = [
        get_proxie_from_advanced_name,
        get_proxies_from_geonode,
        get_proxies_from_proxyscrape,
        get_proxies_from_free_proxy_list,
    ]

    while True:
        if stop_flag.is_set():
            print("⛔ Задача остановлена пользователем.")
            return

        current_working = load_working_proxies()
        if quantity is not None and len(current_working) >= quantity:
            print(Fore.YELLOW + f"[✓] Достигнуто необходимое количество рабочих прокси: {len(current_working)}")
            break

        for source_func in sources:
            if stop_flag.is_set():
                print("⛔ Задача остановлена пользователем (во время обхода источников).")
                return

            new_proxies = source_func()
            new_proxies = [p for p in new_proxies if p[0] not in checked_proxies]

            print(Fore.CYAN + f"[{source_func.__name__}] Получено новых прокси: {len(new_proxies)}")

            proxy_sources = {p: src for p, src in new_proxies}

            with ThreadPoolExecutor(max_workers=50) as executor:
                futures = {executor.submit(check_proxy, p[0]): p[0] for p in new_proxies}
                
                while futures:
                    done, _ = wait(futures, timeout=0.1, return_when=FIRST_COMPLETED)
                    
                    for future in done:
                        if stop_flag.is_set():
                            print("⛔ Задача остановлена — прерывание ожидания результатов.")
                            return

                        proxy, status, error = future.result()
                        proxy_str = futures.pop(future)
                        checked_proxies.add(proxy_str)
                        source = proxy_sources.get(proxy_str, "unknown")

                        if status:
                            if proxy_str not in current_working:
                                print(Fore.GREEN + f"[Рабочий] {proxy_str} from {source}")
                                save_proxy(proxy_str)
                                working_proxies.add(proxy_str)
                        else:
                            print(Fore.RED + f"[Не работает] {proxy_str} from {source}, error: {error}")


            current_working = load_working_proxies()
            if quantity is not None and len(current_working) >= quantity:
                break

    print(Fore.GREEN + f"✅ Всего рабочих прокси: {len(load_working_proxies())}")

