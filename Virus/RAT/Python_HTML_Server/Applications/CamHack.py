import cv2
import socket
import struct
import pickle
import requests
import time
from urllib.parse import urlparse

# === 1. Получаем данные с Firebase через REST API ===
FIREBASE_URL = "https://ngrokservers-2e669-default-rtdb.europe-west1.firebasedatabase.app/serverInfo.json"

def get_ngrok_info():
    try:
        response = requests.get(FIREBASE_URL)
        data = response.json()
        ngrok_url = data['ngrok_url']
        ngrok_port = int(data['ngrok_port'])

        print(f"✅ Получен сервер: {ngrok_url}:{ngrok_port}")
        return ngrok_url, ngrok_port
    except Exception as e:
        print(f"❌ Ошибка при получении данных Firebase: {e}")
        return None, None

# === 2. Подключаемся к серверу ===
def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("🔌 Подключено к серверу.")
    return client_socket

# === 3. Захват видео с камеры и отправка ===
def stream_camera(sock):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Камера не найдена.")
        return

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            # Сжатие кадра
            data = pickle.dumps(cv2.imencode('.jpg', frame)[1])
            size = struct.pack("!I", len(data))

            # Отправляем размер + данные
            sock.sendall(size + data)

            time.sleep(0.1)  # ограничим частоту кадров
    except Exception as e:
        print(f"⚠ Ошибка: {e}")
    finally:
        cam.release()
        sock.close()
        print("📴 Поток завершён.")

# === Запуск ===
if __name__ == "__main__":
    host, port = get_ngrok_info()

    if host and port:
        # ngrok_url может быть в формате https://xxxx.ngrok-free.app
        parsed = urlparse(host)
        hostname = parsed.hostname or host
        sock = connect_to_server(hostname, port)
        stream_camera(sock)
