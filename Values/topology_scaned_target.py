import customtkinter as ctk
import math
import json

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
        for text_id, (base_font_size, font_name) in self.text_items.items():
            new_size = max(1, int(base_font_size * self.current_scale))
            self.itemconfig(text_id, font=(font_name, new_size))
        self.current_scale *= zoom
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

def draw_network_topology(canvas, nodes, edges, localhost_ip, on_node_click=None):
    node_positions = {}
    # Словарь для сопоставления id овала и ip
    node_items = {}

    center_x = canvas.winfo_width() / 2
    center_y = canvas.winfo_height() / 2

    localhost_radius = 25
    forbidden_radius = 150
    nodes_radius = forbidden_radius + 30

    total_nodes = len(nodes) - 1
    angle_step = (2 * math.pi) / total_nodes if total_nodes > 0 else 0

    # Локалхост
    node_positions[localhost_ip] = (center_x, center_y)
    oval_id = canvas.create_oval(center_x - localhost_radius, center_y - localhost_radius,
                       center_x + localhost_radius, center_y + localhost_radius,
                       fill="green", outline="black")
    text_id = canvas.create_text_scaled(center_x, center_y, text=localhost_ip, fill="white", font_size=14)
    node_items[oval_id] = localhost_ip
    node_items[text_id] = localhost_ip

    # Остальные узлы
    idx = 0
    for node in nodes:
        if node == localhost_ip:
            continue
        angle = idx * angle_step
        x = center_x + nodes_radius * math.cos(angle)
        y = center_y + nodes_radius * math.sin(angle)
        node_positions[node] = (x, y)
        oval_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="skyblue", outline="black")
        text_id = canvas.create_text_scaled(x, y, text=node, font_size=12)
        node_items[oval_id] = node
        node_items[text_id] = node
        idx += 1

    # Лямбда-обработчик клика по канвасу
    def on_click(event):
        # Получаем id элемента по координатам клика
        clicked_items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in clicked_items:
            if item in node_items:
                ip = node_items[item]
                if on_node_click:
                    on_node_click(ip)
                break

    canvas.tag_bind("all", "<Button-1>", on_click)
    # или canvas.bind("<Button-1>", on_click) - но тогда надо фильтровать

    # Рисуем связи
    for edge in edges:
        if edge[0] in node_positions and edge[1] in node_positions:
            x1, y1 = node_positions[edge[0]]
            x2, y2 = node_positions[edge[1]]
            canvas.create_line(x1, y1, x2, y2, fill="black", width=3, arrow="last")

def load_ip_data():
    try:
        with open("IPMapper/ip.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Ошибка загрузки IP]: {e}")
        return {}


def create_topology(parent_frame, go_back_callback):
    clear_frame(parent_frame)

    topology_frame = ctk.CTkFrame(parent_frame)
    topology_frame.pack(fill="both", expand=True)

    # Верхняя панель управления
    control_frame = ctk.CTkFrame(topology_frame, height=40)
    control_frame.pack(fill="x", side="top", padx=10, pady=5)

    # Основная область: Canvas + инфо-панель
    main_area = ctk.CTkFrame(topology_frame)
    main_area.pack(fill="both", expand=True)

    # Canvas
    canvas = DraggableCanvas(main_area, bg="white")
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Информационная панель
    info_panel = ctk.CTkFrame(main_area, width=300)
    info_panel.pack(side="right", fill="y", padx=10, pady=10)
    info_label = ctk.CTkLabel(info_panel, text="Выберите узел...", justify="left", anchor="nw", wraplength=280)
    info_label.pack(fill="both", expand=True, padx=5, pady=5)

    # Зум-кнопки
    zoom_in_btn = ctk.CTkButton(control_frame, text="+", width=30, command=lambda: canvas.scale_canvas(1.1))
    zoom_in_btn.pack(side="left", padx=5)
    zoom_out_btn = ctk.CTkButton(control_frame, text="−", width=30, command=lambda: canvas.scale_canvas(0.9))
    zoom_out_btn.pack(side="left", padx=5)

    # Загрузка IP-данных
    global ip_info
    ip_info = load_ip_data()

    localhost = "127.0.0.1"
    nodes = list(ip_info.keys()) if ip_info else [localhost]
    if localhost not in nodes:
        nodes.insert(0, localhost)
    edges = [("127.0.0.1", ip) for ip in nodes if ip != "127.0.0.1"]

    # Функция при клике по узлу
    def on_node_click(ip):
        ip_data = ip_info.get(ip)
        if ip_data:
            info = (
                f"IP: {ip}\n"
                f"Страна: {ip_data.get('country', '-')}\n"
                f"Город: {ip_data.get('city', '-')}\n"
                f"Хостнейм: {ip_data.get('hostname', '-')}\n"
                f"ОС: {ip_data.get('os', '-')}\n"
                f"Порты: {', '.join(map(str, ip_data.get('open_ports', [])))}\n"
                f"Последняя проверка: {ip_data.get('last_checked', '-')}"
            )
        else:
            info = f"Нет данных по IP {ip}"
        info_label.configure(text=info)

    canvas.after(100, lambda: draw_network_topology(canvas, nodes, edges, localhost, on_node_click))
