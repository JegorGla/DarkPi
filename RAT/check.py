import asyncio
from bleak import BleakScanner

async def run():
    scanner = BleakScanner()
    devices = await scanner.discover()  # Используем Scanner для обнаружения
    
    # Печатаем список устройств
    for i, device in enumerate(devices):
        print(f"{i+1}. Устройство найдено: {device.name} - {device.address}")
    
    # Ввод индекса устройства
    choice = int(input("Введите номер устройства для подключения: ")) - 1
    
    if choice >= 0 and choice < len(devices):
        device = devices[choice]
        print(f"Вы выбрали устройство: {device.name} - {device.address}")
        
        # Подключение к выбранному устройству
        await connect_to_device(device.address)
    else:
        print("Неверный номер устройства!")

async def connect_to_device(device_address):
    from bleak import BleakClient

    async with BleakClient(device_address) as client:
        print(f"Подключено к устройству: {device_address}")
        # Здесь можно добавить код для работы с устройством (чтение данных и т.д.)

# Запуск основного кода
asyncio.run(run())
