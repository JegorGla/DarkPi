import requests
import customtkinter as ctk
import json
import os

current_proxy = None

def clear_frame(frame):
    """Очищает все виджеты внутри переданного фрейма."""
    for widget in frame.winfo_children():
        widget.destroy()

def get_current_proxy():
    """Получаем текущий прокси из файла."""
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            proxy = f.read().strip()
            if proxy:
                current_proxy = {"current_proxy": proxy}
    except FileNotFoundError:
        print("Proxy file not found. Using direct connection.")
    return None

def get_ip_info(ip):
    """Получаем информацию о IP-адресе с помощью ipinfo.io API."""
    try:
        url = f"https://ipinfo.io/{ip}/json"
        proxy = current_proxy or get_current_proxy()
        response = requests.get(url, proxies=proxy, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Error fetching IP info: {e}")
        return None

def get_ip_from_json_file():
    try:
        with open("IPMapper/ip.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
def render_ip_info(ip_info, frame):
    clear_frame(frame)

    if not ip_info:
        ctk.CTkLabel(frame, text="Error fetching IP information.").pack(pady=5)
        return None  # Нечего возвращать

    fields = {
        "IP": ip_info.get("ip", "Unavailable"),
        "City": ip_info.get("city", "Unavailable"),
        "Region": ip_info.get("region", "Unavailable"),
        "Country": ip_info.get("country", "Unavailable"),
        "Location": ip_info.get("loc", "Unavailable"),
        "Organization": ip_info.get("org", "Unavailable"),
        "Timezone": ip_info.get("timezone", "Unavailable"),
        "Hostname": ip_info.get("hostname", "Unavailable")
    }

    for label, value in fields.items():
        ctk.CTkLabel(frame, text=f"{label}: {value}").pack(pady=3)

    # Entry для заметки пользователя
    additional_entry = ctk.CTkEntry(
        frame,
        placeholder_text="Дополнительная информация",
        width=300
    )
    additional_entry.pack(pady=10)

    # Если уже была сохранена ранее заметка — подставим её
    if "note" in ip_info:
        additional_entry.insert(0, ip_info["note"])

    return additional_entry  # Возвращаем для дальнейшего использования

def fetch_and_update_ip_data(ip, scrollable_frame, tab2):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            new_data = response.json()
        else:
            new_data = {}
    except Exception as e:
        print(f"Ошибка при запросе IP info: {e}")
        new_data = {}

    file_path = "IPMapper/ip.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    old_data = data.get(ip, {})

    updated_entry = {
        "ip": ip,
        "country": new_data.get("country", old_data.get("country", "Unavailable")),
        "city": new_data.get("city", old_data.get("city", "Unavailable")),
        "hostname": new_data.get("hostname", old_data.get("hostname", "Unavailable")),
        "os": old_data.get("os", "Unavailable"),
        "open_ports": old_data.get("open_ports", []),
        "last_checked": old_data.get("last_checked", "")
    }

    data[ip] = updated_entry
    os.makedirs("IPMapper", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    show_ip_info(updated_entry, scrollable_frame, tab2)

def show_ip_info(ip_info, scrollable_frame, tab2):
    clear_frame(scrollable_frame)

    # Отображаем информацию и получаем ссылку на Entry
    note_entry = render_ip_info(ip_info, scrollable_frame)

    def go_back():
        # Получаем текущий текст из поля
        user_note = note_entry.get() if note_entry else ""

        # Читаем существующий файл
        file_path = "IPMapper/ip.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        ip = ip_info.get("ip")
        if ip:
            if ip in data:
                data[ip]["note"] = user_note
            else:
                data[ip] = {**ip_info, "note": user_note}

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        clear_frame(scrollable_frame)
        show_ip_buttons(scrollable_frame, tab2)

    # Кнопка "Назад"
    back_btn = ctk.CTkButton(scrollable_frame, text="← Назад", command=go_back)
    back_btn.pack(pady=10)

def show_ip_buttons(scrollable_frame, tab2):
    clear_frame(scrollable_frame)

    ip_data = get_ip_from_json_file()
    if not ip_data:
        ctk.CTkLabel(scrollable_frame, text="Файл IPMapper/ip.json пуст или не найден").pack(pady=20)
        return

    for ip_key in ip_data.keys():
        ip_info = ip_data[ip_key]
        unavailable_count = sum(1 for v in ip_info.values() if v == "Unavailable")
        status_text = " (not checked)" if unavailable_count >= 2 else " (checked)"
        text_color = "#ff0000" if unavailable_count >= 2 else "#00ff1f"

        btn = ctk.CTkButton(
            scrollable_frame,
            text=f"{ip_key}{status_text}",
            text_color=text_color,
            command=lambda ip=ip_key: fetch_and_update_ip_data(ip, scrollable_frame, tab2)
        )
        btn.pack(pady=5)


def display_ip_info(frame, go_back_callback):
    clear_frame(frame)

    tabs = ctk.CTkTabview(frame)
    tabs.pack(expand=True, fill="both", padx=20, pady=20)

    tab1 = tabs.add("Scan Normal IP")
    tab2 = tabs.add("Get IP Info from File")

    # --- Вкладка 1 ---
    # Ввод IP сверху
    ip_entry = ctk.CTkEntry(tab1, placeholder_text="Enter IP Address")
    ip_entry.pack(fill="x", padx=10, pady=(10, 5))  # сверху и снизу отступы

    # Контейнер для textbox и кнопок (горизонтально)
    controls_frame = ctk.CTkFrame(tab1)
    controls_frame.pack(fill="both", padx=10, pady=5, expand=True)

    # Textbox справа и занимает всё оставшееся пространство
    result_frame = ctk.CTkTextbox(controls_frame)
    result_frame.pack(side="left", expand=True, fill="both")
    result_frame.configure(state="disabled")

    def on_find_ip():
        ip = ip_entry.get()
        info = get_ip_info(ip)
        render_ip_info(info, result_frame)

    # Кнопки слева
    find_btn = ctk.CTkButton(controls_frame, text="Find IP", command=on_find_ip)
    find_btn.pack(padx=10, pady=5)

    go_back_button = ctk.CTkButton(controls_frame, text="← Go Back", command=go_back_callback)
    go_back_button.pack(padx=10, pady=5)

    
    # --- Вкладка 2 ---
    scrollable_frame = ctk.CTkScrollableFrame(tab2)
    scrollable_frame.pack(fill="both", expand=True, pady=10)

    show_ip_buttons(scrollable_frame, tab2)
