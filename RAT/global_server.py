import customtkinter as ctk
import webbrowser

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def server(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Основной контейнер
    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Левый блок (для формы входа)
    left_frame = ctk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="both", padx=10, pady=10)

    # Правый блок (можно оставить пустым или использовать под информацию)
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Информационный текст
    info_label = ctk.CTkLabel(left_frame, text="Will open the browser, you need to start the server on port 12345", font=ctk.CTkFont(size=14))
    info_label.pack(pady=(10, 20))

    # Кнопка входа
    login_and_open_btn = ctk.CTkButton(left_frame, text="Войти", command=lambda: open_browser())
    login_and_open_btn.pack(pady=10)

    # Кнопка Назад

    if go_back_callback:
        back_btn = ctk.CTkButton(left_frame, text="Назад", command=go_back_callback)
        back_btn.pack(side="bottom", pady=10)


    def open_browser():
        url = 'https://localtonet.com/tunnel/tcpudp'
        # Открыть URL в браузере по умолчанию
        webbrowser.open(url)