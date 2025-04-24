import customtkinter as ctk
import tkinter as tk

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def create_dvd_ui(parent_frame):
    clear_frame(parent_frame)  # Очищаем фрейм

    # Холст для анимации
    canvas = tk.Canvas(parent_frame, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Загружаем изображение логотипа DVD
    dvd_img = tk.PhotoImage(file="images/dvd_logo.png")  # ← замени на свой путь, если нужно

    # Начальные координаты
    x_pos = 100
    y_pos = 100
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
