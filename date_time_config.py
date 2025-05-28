from datetime import datetime, timedelta
import json

def update_last_check_time():
    """Сохраняем дату последней проверки обновлений."""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    data["last_update_check"] = datetime.now().strftime("%Y-%m-%d")

    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)
    print("[INFO] Обновлена дата последней проверки обновлений")

def should_check_update():
    """Возвращает True, если пора запустить setup() на основе интервала из настроек."""
    try:
        with open("settings.json", "r") as f:
            data = json.load(f)
    except:
        print("[INFO] Не удалось прочитать settings.json, запускаем setup по умолчанию.")
        return True  # если нет файла — запускаем setup

    interval = data.get("Time to check update", "1 day").lower().strip()
    last_check = data.get("last_update_check")

    # если никогда не запускали setup — запускаем
    if not last_check:
        return True

    try:
        last_date = datetime.strptime(last_check, "%Y-%m-%d")
    except ValueError:
        return True  # неправильная дата — обновляем

    days_map = {
        "1 day": 1,
        "5 day": 5,
        "1 month": 30,
        "1 year": 365,
        "never": float("inf"),
    }

    days = days_map.get(interval, 1)  # по умолчанию 1 день

    due = datetime.now() - last_date >= timedelta(days=days)
    print(f"[INFO] Проверка обновлений: прошло {datetime.now() - last_date}. Надо запускать? {due}")
    return due
