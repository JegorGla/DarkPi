import customtkinter as ctk
import tkinter as tk
import random

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_dvd_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)  # Очищаем фрейм

    # Холст для анимации
    canvas = tk.Canvas(parent_frame, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Загружаем изображение логотипа DVD
    dvd_img = tk.PhotoImage(file="images/dvd_logo.png")  # ← замени на свой путь, если нужно

    # Начальные координаты
    canvas.pack(fill="both", expand=True)
    canvas.update_idletasks()  # Убедимся, что размеры обновлены

    x_pos = random.randint(0, canvas.winfo_width() - dvd_img.width())
    y_pos = random.randint(0, canvas.winfo_height() - dvd_img.height())

    x_speed = 4
    y_speed = 3

    # Добавляем изображение на холст
    dvd_logo = canvas.create_image(x_pos, y_pos, image=dvd_img, anchor="nw")

    # Анимация
    def animate_dvd():
        nonlocal x_pos, y_pos, x_speed, y_speed

        x_pos += x_speed
        y_pos += y_speed

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        img_width = dvd_img.width()
        img_height = dvd_img.height()

        # Проверка на границы
        if x_pos <= 0 or x_pos + img_width >= canvas_width:
            x_speed = -x_speed
        if y_pos <= 0 or y_pos + img_height >= canvas_height:
            y_speed = -y_speed

        canvas.coords(dvd_logo, x_pos, y_pos)

        parent_frame.after(20, animate_dvd)

    animate_dvd()

    # Храним ссылку, чтобы изображение не исчезло
    canvas.image = dvd_img

    # ==== ЛОГИКА СВАЙПА ДЛЯ ВОЗВРАТА НАЗАД ====
    start_x = [None]  # Используем список, чтобы модифицировать внутри функций

    def on_swipe_start(event):
        start_x[0] = event.x

    def on_swipe_end(event):
        if start_x[0] is None:
            return

        delta = event.x - start_x[0]
        width = canvas.winfo_width()

        if start_x[0] > width * 0.7 and delta < -50:  # свайп влево в правой части
            if go_back_callback:
                go_back_callback()

        start_x[0] = None

    canvas.bind("<ButtonPress-1>", on_swipe_start)
    canvas.bind("<ButtonRelease-1>", on_swipe_end)