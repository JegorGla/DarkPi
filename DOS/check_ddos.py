import threading
import requests
import time
from statistics import mean
import argparse

results = {
    "success": 0,
    "fail": 0,
    "latencies": []
}

lock = threading.Lock()

def worker(target_url, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        start = time.time()
        try:
            response = requests.get(target_url, timeout=5)
            latency = time.time() - start
            with lock:
                if response.status_code == 200:
                    results["success"] += 1
                    results["latencies"].append(latency)
                else:
                    results["fail"] += 1
        except Exception:
            with lock:
                results["fail"] += 1

def main():
    parser = argparse.ArgumentParser(description="HTTP-нагрузочный тест")
    parser.add_argument("url", help="URL сервера, например http://127.0.0.1:8080")
    parser.add_argument("-c", "--clients", type=int, default=50, help="Количество параллельных клиентов")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Длительность теста (сек)")
    args = parser.parse_args()

    print(f"[~] Запуск теста: {args.clients} клиентов в течение {args.duration} секунд на {args.url}")
    threads = []

    for _ in range(args.clients):
        t = threading.Thread(target=worker, args=(args.url, args.duration))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n=== Результаты ===")
    print(f"Успешных запросов: {results['success']}")
    print(f"Неудачных запросов: {results['fail']}")
    if results["latencies"]:
        print(f"Средняя задержка: {round(mean(results['latencies'])*1000, 2)} мс")
        print(f"Макс: {round(max(results['latencies'])*1000, 2)} мс")
        print(f"Мин: {round(min(results['latencies'])*1000, 2)} мс")
    else:
        print("Нет успешных запросов — сервер не отвечает?")

if __name__ == "__main__":
    main()
