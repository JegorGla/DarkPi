import subprocess

def install__python_package(file_path):
    """Install a package using pip."""
    subprocess.check_call(["python", "-m", "pip", "install", "-r", file_path])

def install_requirements():
    """Install the required packages."""
    try:
        install__python_package("requirements.txt")
        print("[INFO] Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install requirements: {e}")
    except FileNotFoundError:
        print("[ERROR] requirements.txt file not found. Please ensure it exists in the current directory.")

def install_evilwifi_dependencies():
    """Install required packages for EvilAP (Evil Wi-Fi) functionality."""
    packages = [
        "hostapd",      # Создание точки доступа
        "dnsmasq",      # DHCP и DNS-сервер
        "iptables",     # NAT и переадресация трафика
        "lighttpd"      # Лёгкий веб-сервер (можно заменить на Python HTTP сервер)
    ]

    print("[INFO] Installing EvilAP dependencies:")
    for pkg in packages:
        try:
            print(f"[*] Installing: {pkg}")
            subprocess.check_call(["sudo", "apt-get", "install", "-y", pkg])
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install {pkg}: {e}")
    print("[INFO] Installation complete.")


def setup():
    """Main setup function."""
    install_requirements()