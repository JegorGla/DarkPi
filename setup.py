import subprocess
import platform
import time
import sys
import select
import os

list_of_linux_package = [
    "lolcat",
    "figlet",
    "tor",
    "proxychains"
]

def setup_proxychains_config():
    import shutil

    global_path = "/etc/proxychains.conf"
    user_path = os.path.expanduser("~/.proxychains/proxychains.conf")

    target_path = None
    if os.path.isfile(global_path) and os.access(global_path, os.W_OK):
        target_path = global_path
    else:
        os.makedirs(os.path.dirname(user_path), exist_ok=True)
        target_path = user_path

    proxy_lines = [
        "http 127.0.0.1 8080\n",
        "https 127.0.0.1 8080\n",
        "socks4 127.0.0.1 9050\n",
        "socks5 127.0.0.1 9050\n",
    ]

    # Считаем файл или создаём минимальный шаблон
    if os.path.isfile(target_path):
        with open(target_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = [
            "strict_chain\n",
            "proxy_dns\n",
            "remote_dns_subnet 224\n",
            "tcp_read_time_out 15000\n",
            "tcp_connect_time_out 8000\n",
            "\n",
            "[ProxyList]\n"
        ]

    # Найдём индекс [ProxyList]
    try:
        idx = lines.index("[ProxyList]\n")
    except ValueError:
        lines.append("\n[ProxyList]\n")
        idx = len(lines) - 1

    # Удаляем все прокси-строки после [ProxyList]
    new_lines = lines[:idx+1]  # до и включая [ProxyList]

    for line in lines[idx+1:]:
        if not line.strip().startswith(("socks5", "socks4", "http", "https")):
            new_lines.append(line)

    # Добавляем наши строки в конец секции ProxyList
    new_lines.extend(proxy_lines)

    # Резервное копирование перед записью (рекомендуется)
    try:
        if os.path.isfile(target_path):
            shutil.copy(target_path, target_path + ".bak")
    except Exception as e:
        print(f"[WARNING] Не удалось создать резервную копию: {e}")

    # Записываем обновлённый конфиг
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"[INFO] Proxychains config обновлен: {target_path}")
    except PermissionError:
        print(f"[ERROR] Нет прав для записи в {target_path}. Запустите с sudo или настройте вручную.")

def countdown(seconds=5):
    print("Вы можете остановить обновление в любой момент, нажав 's'!")
    for n in range(seconds, 0, -1):
        print(f"Начнётся через {n} сек...")
        time.sleep(1)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            if sys.stdin.read(1).lower() == 's':
                print("Нажато s!")
                if platform.system() != "Windows":
                    subprocess.run('echo -e "\\033[31m$(figlet -f slant -c CANCELED)\\033[0m"', shell=True)
                else:
                    print("Обновление отменено пользователем.")
                return False
    return True

def install_linux_package():
    if not countdown():
        return

    print("[INFO] Обновление и апгрейд системы...")
    try:
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "upgrade", "-y"])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Ошибка при обновлении системы: {e}")
        return

    for package in list_of_linux_package:
        try:
            print(f"[INFO] Установка пакета: {package}")
            subprocess.check_call(["sudo", "apt", "install", "-y", package])
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Не удалось установить {package}: {e}")

def install_python_package(file_path):
    """Установить Python-зависимости из файла."""
    if platform.system() == "Windows":
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])
    elif platform.system() == "Linux":
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path, "--break-system-package"])
        
def install_requirements():
    """Установить зависимости из requirements.txt."""
    try:
        install_python_package("requests.txt")
        if platform.system() != "Windows":
            subprocess.run("figlet -f slant -c DONE, INSTALED REQUESTS! | lolcat", shell=True)
            time.sleep(3)
        else:
            import pyfiglet
            from pyfiglet import Figlet
            f = pyfiglet.figlet_format("DONE, INSTALED REQUESTS!", font="Slant")
            print(f)
            time.sleep(3)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Ошибка установки зависимостей: {e}")
    except FileNotFoundError:
        print("[ERROR] Файл requirements.txt не найден. Убедитесь, что он находится в текущей директории.")

def install_localonet():
    import urllib.request
    import zipfile
    if platform.system() == "Linux":
        localonet_binary = "./localtonet"
        zip_url = "https://localtonet.com/download/localtonet-linux-x64.zip"
        zip_filename = "localtonet-linux-x64.zip"

        if os.path.isfile(localonet_binary):
            print("[INFO] localtonet уже установлен, пропускаем установку.")
            return

        try:
            print("[INFO] Скачиваем localtonet...")
            urllib.request.urlretrieve(zip_url, zip_filename)
            print("[INFO] Распаковываем архив...")
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("[INFO] Устанавливаем права на выполнение...")
            subprocess.run(["chmod", "+x", localonet_binary], check=True)
            print("[SUCCESS] localtonet успешно установлен.")
            os.remove(zip_filename)  # удаляем архив после установки
        except Exception as e:
            print(f"[ERROR] Ошибка при установке localtonet: {e}")


def install_ngrok():
    import urllib.request
    import zipfile
    if platform.system() == "Linux":
        ngrok_binary = "./ngrok"
        zip_filename = "ngrok-stable-linux-amd64.zip"
        zip_url = "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip"

        if os.path.isfile(ngrok_binary):
            print("[INFO] ngrok уже установлен, пропускаем установку.")
            return

        try:
            print("[INFO] Скачиваем ngrok...")
            urllib.request.urlretrieve(zip_url, zip_filename)
            print("[INFO] Распаковываем архив...")
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(".")
            print("[INFO] Устанавливаем права на выполнение...")
            subprocess.run(["chmod", "+x", ngrok_binary], check=True)
            print("[SUCCESS] ngrok успешно установлен.")
            os.remove(zip_filename)  # удаляем архив после установки
        except Exception as e:
            print(f"[ERROR] Ошибка при установке ngrok: {e}")

def setup():
    """Главная функция настройки окружения."""
    if platform.system() != "Windows":
        install_linux_package()
        setup_proxychains_config()
    install_requirements()
    install_localonet()
    install_ngrok()
    if platform.system() != "Windows":
        subprocess.call("clear", shell=True)
    else:
        subprocess.call("cls", shell=True)
    