import customtkinter as ctk
import psutil
import socket
import threading

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_process_name(pid):
    try:
        return psutil.Process(pid).name()
    except Exception:
        return "N/A"

def get_connections_info():
    connections = psutil.net_connections(kind='inet')  # TCP + UDP
    data = []
    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
        status = conn.status
        pid = conn.pid or 0
        pname = get_process_name(pid)
        proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
        data.append((proto, laddr, raddr, status, pid, pname))
    return data

def port_monitoring_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    # Заголовочный фрейм
    header_frame = ctk.CTkFrame(parent_frame)
    header_frame.pack(fill="x", pady=10, padx=10)

    # Заголовок (слева)
    title_label = ctk.CTkLabel(header_frame, text="🔍 Port Monitoring", font=("Arial", 20))
    title_label.pack(side="left", padx=5)

    # Кнопка Назад (справа)
    if go_back_callback:
        back_button = ctk.CTkButton(header_frame, text="← Назад", command=go_back_callback, width=100, height=30)
        back_button.pack(side="right", padx=5)

    # Scrollable frame
    scrollable_frame = ctk.CTkScrollableFrame(parent_frame, width=800, height=400)
    scrollable_frame.pack(pady=10)

    # Header
    header = ctk.CTkLabel(scrollable_frame, text="Proto | Local Address        | Remote Address       | Status       | PID   | Process",
                          font=("Courier", 14, "bold"))
    header.pack(anchor="w")

    entry_labels = []

    def update_ports():
        for label in entry_labels:
            label.destroy()
        entry_labels.clear()

        conn_data = get_connections_info()
        for conn in conn_data:
            proto, laddr, raddr, status, pid, pname = conn
            text = f"{proto:<5} | {laddr:<20} | {raddr:<20} | {status:<12} | {pid:<5} | {pname}"
            label = ctk.CTkLabel(scrollable_frame, text=text, font=("Courier", 12))
            label.pack(anchor="w")
            entry_labels.append(label)

        # Автообновление
        #parent_frame.after(3000, update_ports)  # обновлять каждые 3 секунды

    update_ports()

    # Назад
    if go_back_callback:
        back_btn = ctk.CTkButton(parent_frame, text="← Назад", command=go_back_callback)
        back_btn.pack(pady=10)
