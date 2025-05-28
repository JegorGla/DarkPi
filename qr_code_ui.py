import qrcode
import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_qr_code_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Настройка фона (оставляем тему управлять этим)
    parent_frame.configure(fg_color="transparent")

    # Вложенная панель с цветом (в центре окна)
    panel_frame = ctk.CTkFrame(parent_frame, fg_color="#2E1A47", corner_radius=15)
    panel_frame.pack(padx=15, pady=15, fill="both", expand=True)

    # Заголовок
    title_label = ctk.CTkLabel(panel_frame, text="🎯 QR Code Generator", 
                               font=("Helvetica", 24, "bold"), text_color="#E0C3FC")
    title_label.pack(pady=(30, 20))

    # Поля ввода
    site_entry = ctk.CTkEntry(panel_frame, placeholder_text="Enter website URL",
                              width=300, height=40, corner_radius=10)
    site_entry.pack(pady=10)

    filename_entry = ctk.CTkEntry(panel_frame, placeholder_text="Save as (e.g., my_qr.png)",
                                  width=300, height=40, corner_radius=10)
    filename_entry.pack(pady=10)

    status_label = ctk.CTkLabel(panel_frame, text="", text_color="#A8E6CF")
    status_label.pack(pady=5)

    # Панель бокового меню
    sidebar_frame = ctk.CTkFrame(panel_frame, width=220, fg_color="#1B1B2F", corner_radius=10)
    sidebar_visible = False  # Флаг

    # Метка для QR-кода
    qr_image_label = ctk.CTkLabel(sidebar_frame, text="QR will appear here", text_color="#ffffff")
    qr_image_label.pack(pady=20, padx=10)

    is_animation = False

    # Функция для анимации панели (плавное появление)
    def toggle_sidebar():
        nonlocal sidebar_visible
        if sidebar_visible:
            animate_sidebar_close(sidebar_frame)  # Скрыть панель плавно
            sidebar_visible = False
        else:
            sidebar_frame.place(relx=1.0, rely=0.0, anchor="ne", relheight=0)  # Начальный размер 0
            animate_sidebar_open(sidebar_frame)  # Показать панель плавно
            sidebar_visible = True

    # Анимация появления
    def animate_sidebar_open(frame, current_height=0, is_animation=True):
        if is_animation and current_height < 1.0:
            new_height = current_height + 0.05
            frame.place_configure(relheight=new_height)
            parent_frame.after(20, animate_sidebar_open, frame, new_height, is_animation)
        else:
            frame.place_configure(relheight=1.0)


    def animate_sidebar_close(frame, current_height=1.0):
        if current_height > 0:
            new_height = current_height - 0.05
            frame.place_configure(relheight=new_height)
            parent_frame.after(20, animate_sidebar_close, frame, new_height)
        else:
            frame.place_forget()  # Убирает панель из окна, когда она полностью исчезнет


    # Кнопка гамбургер
    hamburger_btn = ctk.CTkButton(
        panel_frame,
        text="☰",  # Символ гамбургера
        width=40,   # Ширина
        height=40,  # Высота
        font=("Helvetica", 20, "bold"),  # Шрифт для текста
        command=toggle_sidebar,
        fg_color="#6A0572",  # Цвет фона кнопки
        hover_color="#AB83A1",  # Цвет при наведении
        corner_radius=20,  # Круглые углы
        text_color="#E0C3FC",  # Цвет текста
        border_width=2,  # Ширина границы
        border_color="#FFFFFF"  # Цвет границы
    )
    hamburger_btn.place(relx=0.1, rely=0.05, anchor="ne")

    # Функция генерации QR-кода
    def create_qr():
        data = site_entry.get().strip()
        filename = filename_entry.get().strip()

        if not data:
            status_label.configure(text="⚠️ Please enter a URL.")
            return

        if not filename:
            filename = "qr_code"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "Qr_Codes/" + filename + ".png"
        img.save(img_path)

        status_label.configure(text=f"✅ QR saved as {img_path}")

        # Загружаем и отображаем изображение QR
        qr_pil_img = Image.open(img_path)  # Загружаем картинку
        qr_pil_img = qr_pil_img.resize((200, 200))  # Масштабируем картинку
        qr_img = ImageTk.PhotoImage(qr_pil_img)  # Конвертируем в формат, поддерживаемый tkinter

        # Обновляем label с QR изображением
        qr_image_label.configure(image=qr_img, text="")
        qr_image_label.image = qr_img  # Сохраняем ссылку на изображение, чтобы оно не исчезло

        # Обновить кнопку
        start_button.configure(text="🔁 Regenerate QR Code", command=create_qr)

    # Кнопка генерации QR-кода
    start_button = ctk.CTkButton(panel_frame, text="⚡ Generate QR Code", 
                                 command=create_qr, corner_radius=8, fg_color="#6A0572", hover_color="#AB83A1")
    start_button.pack(pady=20)

    if go_back_callback:
        back_btn = ctk.CTkButton(panel_frame, text="← Go Back", command=go_back_callback,
                                 fg_color="#44475A", hover_color="#6272A4")
        back_btn.pack(pady=(10, 30))
