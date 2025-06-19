import customtkinter as ctk
from TaskScheduler.proxy_task import proxy_task_ui
from TaskScheduler.setting_task_scheduler import create_setting_task_scheduler
import json

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()
    
def task_sheduler_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    Proxy_btn = ctk.CTkButton(
        parent_frame,
        text="Proxy",
        command=lambda: proxy_task_ui(parent_frame, go_back_callback),  # Placeholder for actual functionality
        font=("Arial", 16),
        width=parent_frame.winfo_width() * 0.7,
        height=40
    )
    Proxy_btn.pack(pady=10)
    #=================Proxy button====================

    setting_btn = ctk.CTkButton(parent_frame, text="Setting Task Scheduler", command=lambda: create_setting_task_scheduler(parent_frame, go_back_callback))
    setting_btn.pack(pady=10)
    #===============Setting Button===================

    back_btn = ctk.CTkButton(parent_frame, command=go_back_callback, text="Back", width=parent_frame.winfo_width() * 0.7, height=40)
    back_btn.pack(pady=10)
    #================Back button======================