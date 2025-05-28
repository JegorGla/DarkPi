import subprocess
import platform
import time
import sys
import select

list_of_linux_package = [
    "lolcat",
    "figlet"
]

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
            subprocess.check_call(["figlet", "-f", "slant", "-c", "DONE", "|", "lolcat"])
            time.sleep(3)
        else:
            print("[INFO] Python-зависимости успешно установлены.")
            time.sleep(3)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Ошибка установки зависимостей: {e}")
    except FileNotFoundError:
        print("[ERROR] Файл requirements.txt не найден. Убедитесь, что он находится в текущей директории.")

def setup():
    """Главная функция настройки окружения."""
    if platform.system() != "Windows":
        install_linux_package()
    install_requirements()
    if platform.system() != "Windows":
        subprocess.call("clear", shell=True)
    else:
        subprocess.call("cls", shell=True)
    