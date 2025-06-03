import socket
import cv2
import pickle
import struct

# Настройки сервера
HOST = '0.0.0.0'  # Принимать соединения на всех интерфейсах
PORT = 12345       # Убедись, что порт совпадает с тем, что ты публикуешь через ngrok/localtonet

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"🚀 Сервер запущен на порту {PORT}. Ожидание подключения клиента...")

    conn, addr = server_socket.accept()
    print(f"✅ Клиент подключён: {addr}")

    data = b""
    payload_size = struct.calcsize("!I")

    try:
        while True:
            # Получаем размер
            while len(data) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Клиент отключился")
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("!I", packed_msg_size)[0]

            # Получаем данные изображения
            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Декодируем и отображаем
            frame = pickle.loads(frame_data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            cv2.imshow("📹 Видеопоток от клиента", frame)
            if cv2.waitKey(1) == 27:  # Esc — выход
                break
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()
        server_socket.close()
        cv2.destroyAllWindows()
        print("🛑 Сервер остановлен.")

if __name__ == "__main__":
    start_server()
