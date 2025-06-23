import customtkinter as ctk
import math
import json
import random
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "127.0.0.1"

has_visible_inf_pnl = False

class DraggableCanvas(ctk.CTkCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<MouseWheel>", self.on_zoom)

        self.drag_start = None

        # Словарь для хранения id текста и их начальных размеров шрифта
        self.text_items = {}

    def on_start_drag(self, event):
        self.drag_start = (event.x, event.y)

    def on_drag(self, event):
        dx = event.x - self.drag_start[0]
        dy = event.y - self.drag_start[1]
        self.drag_start = (event.x, event.y)

        self.offset_x += dx
        self.offset_y += dy
        self.move("all", dx, dy)

    def on_zoom(self, event):
        zoom = 1.1 if event.delta > 0 else 0.9
        self.scale("all", self.winfo_width() / 2, self.winfo_height() / 2, zoom, zoom)
        # Масштабируем размер шрифта для текста
        self.current_scale *= zoom

        for text_id, (base_font_size, font_name) in self.text_items.items():
            new_size = max(1, int(base_font_size * self.current_scale))
            self.itemconfig(text_id, font=(font_name, new_size))
        
        self.scale_canvas(zoom)

    def scale_canvas(self, zoom):
        # Масштабируем все объекты (круги, линии и т.п.)
        self.scale("all", self.winfo_width() / 2, self.winfo_height() / 2, zoom, zoom)

        # Масштабируем размер шрифта для текста
        for text_id, (base_font_size, font_name) in self.text_items.items():
            new_size = max(1, int(base_font_size * self.current_scale))
            self.itemconfig(text_id, font=(font_name, new_size))

    def create_text_scaled(self, x, y, text, font_name="Arial", font_size=12, **kwargs):
        text_id = self.create_text(x, y, text=text, font=(font_name, font_size), **kwargs)
        self.text_items[text_id] = (font_size, font_name)
        return text_id

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def draw_network_topology(canvas, nodes, edges, local_ip, localhost, localhost_ip, on_node_click=None):
    node_positions = {}
    # Словарь для сопоставления id овала и ip
    node_items = {}

    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    # Центральный (локальный) IP только текстом
    node_positions[local_ip] = (center_x, center_y)

    oval_id = canvas.create_oval(center_x - 25, center_y - 25, center_x + 25, center_y + 25,
                                fill="green",  width=2)
    text_id = canvas.create_text_scaled(center_x, center_y, text=local_ip, fill="white", font_size=14)

    node_items[oval_id] = local_ip
    node_items[text_id] = local_ip


    # localhost всегда под локальным IP (смещение только по Y вниз)
    distance_down = 90  # расстояние вниз от центра локального IP
    lx = center_x
    ly = center_y + distance_down
    node_positions[localhost] = (lx, ly)
    oval_id = canvas.create_oval(lx - 20, ly - 20, lx + 20, ly + 20, fill="gray")
    text_id = canvas.create_text_scaled(lx, ly, text="localhost", fill="white", font_size=12)
    node_items[oval_id] = localhost
    node_items[text_id] = localhost


    # Остальные узлы
    idx = 0
    new_locations_added = False

    for node in nodes:
        if node == localhost_ip:
            continue
        
        node_data = ip_info.get(node, {})
        location = node_data.get("location")
        if isinstance(location, list) and len(location) == 2:
            x, y = location
        else:
            max_attempts = 100
            attempt = 0
            node_radius = 20  # радиус кружка
            forbidden_radius = 150

            while attempt < max_attempts:
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(forbidden_radius + 10, node_radius)
                x = center_x + distance * math.cos(angle)
                y = center_y + distance * math.sin(angle)

                # Проверка на пересечение с другими узлами
                too_close = False
                for other_x, other_y in node_positions.values():
                    dist = math.hypot(x - other_x, y - other_y)
                    if dist < node_radius * 2 + 10:  # добавим немного отступа
                        too_close = True
                        break

                if not too_close:
                    break
                attempt += 1

            # Если нашли допустимое место — сохраняем
            if node != local_ip:
                ip_info.setdefault(node, {})["location"] = [x, y]
                new_locations_added = True
            new_locations_added = True

        node_positions[node] = (x, y)
        oval_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="#1E3A8A", outline="#1E3A8A")
        text_id = canvas.create_text_scaled(x, y, text=node, fill="white", font_size=12)
        node_items[oval_id] = node
        node_items[text_id] = node

    # Лямбда-обработчик клика по канвасу
    def on_click(event):
        # Получаем id элемента по координатам клика
        clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in clicked_items:
            if item in node_items:
                ip = node_items[item]
                if on_node_click:
                    on_node_click(ip)
                    has_visible_inf_pnl = True
                break

    canvas.tag_bind("all", "<Button-1>", on_click)
    # или canvas.bind("<Button-1>", on_click) - но тогда надо фильтровать

    # Рисуем связи
    for edge in edges:
        if edge[0] in node_positions and edge[1] in node_positions:
            x1, y1 = node_positions[edge[0]]
            x2, y2 = node_positions[edge[1]]
            canvas.create_line(x1, y1, x2, y2, fill="white", width=1, arrow="last")

def load_ip_data():
    try:
        with open("IPMapper/ip.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Ошибка загрузки IP]: {e}")
        return {}

abbreviated_countries = {
    "US": "United States of America",
    "HU": "Hungary",
    "AE": "United Arab Emirates",
    "FR": "France",
    "GB": "United Kingdom",
    "DE": "Germany",
    "IT": "Italy",
    "ES": "Spain",
    "CN": "China",
    "JP": "Japan",
    "RU": "Russia",
    "IN": "India",
    "BR": "Brazil",
    "CA": "Canada",
    "AU": "Australia",
    "MX": "Mexico",
    "KR": "South Korea",
    "NL": "Netherlands",
    "SE": "Sweden",
    "CH": "Switzerland",
    "NO": "Norway",
    "PL": "Poland",
    "BE": "Belgium",
    "AT": "Austria",
    "DK": "Denmark",
    "FI": "Finland",
    "IE": "Ireland",
    "PT": "Portugal",
    "ZA": "South Africa",
    "NZ": "New Zealand",
    "SG": "Singapore",
    "IL": "Israel",
    "SA": "Saudi Arabia",
    "TR": "Turkey",
    "CZ": "Czech Republic",
    "GR": "Greece",
    "RO": "Romania",
    "HU": "Hungary",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "LT": "Lithuania",
    "LV": "Latvia",
    "EE": "Estonia",
    "UA": "Ukraine",
    "BY": "Belarus",
    "EG": "Egypt",
    "NG": "Nigeria",
    "KE": "Kenya"
}   

def country_from_ip():
    with open("IPMapper/ip.json", "r", encoding="utf-8") as f:
        ip_data = json.load(f)
    country_data = {}
    for ip, data in ip_data.items():
        if isinstance(data, dict) and "country" in data:
            short_country = data["country"]
            # Замена кода на полное имя, если есть, иначе оставить как есть
            full_country = abbreviated_countries.get(short_country, short_country)
            if full_country not in country_data:
                country_data[full_country] = []
            country_data[full_country].append(ip)
    return country_data

def create_topology(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    topology_frame = ctk.CTkFrame(parent_frame)
    topology_frame.pack(fill="both", expand=True)

    control_frame = ctk.CTkFrame(topology_frame, height=40)
    control_frame.pack(fill="x", side="top", padx=10, pady=5)

    hamburger_menu = ctk.CTkFrame(parent_frame, width=700, corner_radius=10)

    countries = ["Все"] + list(country_from_ip().keys())
    filters = ctk.CTkComboBox(hamburger_menu, values=countries, height=30, state="readonly")
    filters.set("Все")  # Значение по умолчанию — показать всех
    filters.place(x=10, y=10, relwidth=0.8, relheight=0.1)

    main_area = ctk.CTkFrame(topology_frame)
    main_area.pack(fill="both", expand=True)

    canvas = DraggableCanvas(main_area, bg="black")
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Создаём info_panel и info_label всегда
    info_panel = ctk.CTkFrame(main_area, width=300)
    # info_panel.pack(side="right", fill="y", padx=10, pady=10)

    info_label = ctk.CTkLabel(info_panel, text="Выберите узел...", justify="left", anchor="nw", wraplength=280)
    info_label.pack(fill="both", expand=True, padx=5, pady=5)

    has_visible_inf_pnl = True  # локальная переменная в функции

    def destroy_inf_pnl():
        nonlocal has_visible_inf_pnl
        info_panel.pack_forget()
        has_visible_inf_pnl = False

    close_btn_on_inf_pnl = ctk.CTkButton(info_panel, text="❌", command=destroy_inf_pnl, width=40, height=40)
    close_btn_on_inf_pnl.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

    zoom_in_btn = ctk.CTkButton(control_frame, text="+", width=30, command=lambda: canvas.scale_canvas(1.1))
    zoom_in_btn.pack(side="left", padx=5)
    zoom_out_btn = ctk.CTkButton(control_frame, text="−", width=30, command=lambda: canvas.scale_canvas(0.9))
    zoom_out_btn.pack(side="left", padx=5)

    back_btn = ctk.CTkButton(control_frame, text="Back", command=go_back_callback, width=30)
    back_btn.pack(side="left", padx=5)

    # --- Функции для обработки плохих данных ---

    def parse_brace_block(text: str) -> dict:
        """Простой парсер текстового блока в фигурных скобках"""
        data = {}
        lines = text.strip().strip("{}").splitlines()
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace(" ", "_")
                value = value.strip()
                if "," in value:
                    parts = [v.strip() for v in value.split(",")]
                    try:
                        value = [int(v) if v.isdigit() else v for v in parts]
                    except:
                        pass
                data[key] = value
        return data

    def normalize_keys(data: dict) -> dict:
        """Исправляет опечатки и приводит ключи к нужному виду"""
        mapping = {
            "coutry": "country",
            "open_pons": "open_ports",
            "last_chckd": "last_checked",
        }
        normalized = {}
        for k, v in data.items():
            normalized[mapping.get(k, k)] = v
        return normalized

    # Загрузка IP-данных
    global ip_info
    ip_info = load_ip_data()

    localhost = "localhost\n127.0.0.1"
    local_ip = get_local_ip()

    nodes = list(set(ip_info.keys()) | {localhost})
    if local_ip in nodes:
        nodes.remove(local_ip)  # Убираем локальный IP из общего списка узлов

    edges = []

    # Связи: все к локальному IP
    for ip in nodes:
        if ip != local_ip:
            edges.append((local_ip, ip))

    # Функция при клике по узлу
    def on_node_click(ip):
        ip_data = ip_info.get(ip)

        # Парсим строку в фигурных скобках, если нужно
        if isinstance(ip_data, str) and ip_data.strip().startswith("{"):
            ip_data = parse_brace_block(ip_data)

        if isinstance(ip_data, dict):
            ip_data = normalize_keys(ip_data)
            info = (
                f"IP: {ip}\n"
                f"Country: {ip_data.get('country', '-')}\n"
                f"City: {ip_data.get('city', '-')}\n"
                f"Hostname: {ip_data.get('hostname', '-')}\n"
                f"OS: {ip_data.get('os', '-')}\n"
                f"Open Ports: {', '.join(map(str, ip_data.get('open_ports', [])))}\n"
                f"Last checked: {ip_data.get('last_checked', '-')}.\n"
                f"Note about IP: {ip_data.get('note', '-')}"
            )
        else:
            info = f"Нет данных по IP {ip}"

        info_label.configure(text=info)
        if not info_label.winfo_ismapped():
            info_panel.pack(side="right",  fill="y", padx=10, pady=10)

    def render_topology():
        draw_network_topology(canvas, nodes, edges, local_ip, localhost, localhost, on_node_click)

        # Сохраняем ip_info, если появились новые координаты
        try:
            # Удаляем локальный IP перед сохранением
            data_to_save = {ip: data for ip, data in ip_info.items() if ip != local_ip}

            with open("IPMapper/ip.json", "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"[Ошибка сохранения координат]: {e}")

    canvas.after(100, render_topology)

    #======Hamburger menu======

    sidebar_visible = False  # Флаг
    
    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            animate_sidebar_close(hamburger_menu)
            # sidebar_visible = False  <- убираем отсюда
        else:
            control_frame.update_idletasks()
            start_x = control_frame.winfo_width()
            target_x = start_x - 900
            hamburger_menu.place(x=start_x, y=0, relheight=1.0)
            animate_sidebar_open(hamburger_menu, target_x)
            sidebar_visible = True

    
    # Анимация появления
    def animate_sidebar_open(frame, target_x, step=20):
        current_x = control_frame.winfo_width()
        def slide():
            nonlocal current_x
            if current_x > target_x:
                current_x -= step
                frame.place(x=current_x, y=0)  # НЕ меняем width/height!
                control_frame.after(10, slide)
            else:
                frame.place(x=target_x, y=0)
        slide()

    def animate_sidebar_close(frame, step=20):
        current_x = frame.winfo_x()
        target_x = control_frame.winfo_width()

        def slide():
            nonlocal current_x
            if current_x < target_x:
                current_x += step
                frame.place(x=current_x, y=0)  # НЕ меняем width/height!
                control_frame.after(10, slide)
            else:
                frame.place_forget()
                nonlocal sidebar_visible
                sidebar_visible = False
        slide()


    close_menu = ctk.CTkButton(hamburger_menu, text="❌", width=50, height=50, command=lambda: animate_sidebar_close(hamburger_menu))
    close_menu.place(relx=0.99, rely=0.05, anchor="ne")
    close_menu.lift()

    hamburger_btn = ctk.CTkButton(control_frame, text="☰", width=40, height=40, command=toggle_sidebar)
    hamburger_btn.pack(side="left", padx=10, pady=5)
    hamburger_btn.lift()

    def update_topology_for_country(country):
        nonlocal nodes, edges

        if country == "Все":
            nodes = list(set(ip_info.keys()) | {localhost})
            if local_ip in nodes:
                nodes.remove(local_ip)
        else:
            filtered_ips = country_from_ip().get(country, [])
            nodes = list(set(filtered_ips))
        
        edges = []
        for ip in nodes:
            if ip != local_ip:
                edges.append((local_ip, ip))

        canvas.delete("all")
        render_topology()


    def on_filter_change(choice):
        nonlocal nodes, edges  # добавить nonlocal

        if choice == "Все":
            nodes = list(set(ip_info.keys()) | {localhost})
            if local_ip in nodes:
                nodes.remove(local_ip)
            edges = [(local_ip, ip) for ip in nodes if ip != local_ip]
        else:
            update_topology_for_country(choice)

        canvas.delete("all")
        render_topology()


    filters.set("Выберите страну")  # Установка значения по умолчанию
    filters.configure(command=on_filter_change)  # Привязка обработчика
