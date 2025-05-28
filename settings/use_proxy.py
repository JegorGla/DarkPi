from stem import Signal
from stem.control import Controller
import requests

# Функция для получения нового IP через Tor
def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Аутентификация с паролем (по умолчанию нет пароля)
        controller.signal(Signal.NEWNYM)  # Отправка сигнала для нового IP

# Функция для получения IP через Tor
def get_ip():
    session = requests.Session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    response = session.get('https://ifconfig.me/')  # Получение вашего IP через Tor
    print(response.json())

# Пример использования
if __name__ == "__main__":
    get_ip()  # Получить текущий IP
    change_ip()  # Изменить IP
    get_ip()  # Проверить новый IP