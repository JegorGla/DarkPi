import customtkinter as ctk
import subprocess

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def execute_command():
    command = command_entry.get()
    if not command.strip():
        return
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.stdout else result.stderr
    except Exception as e:
        output = str(e)

    output_box.configure(state="normal")
    output_box.insert("end", f">>> {command}\n{output}\n")
    output_box.configure(state="disabled")
    output_box.see("end")
    command_entry.delete(0, "end")

def create_normal_terminal_ui(parent_frame, go_back_callback=None):
    clear_frame(parent_frame)

    global command_entry, output_box

    # Output window
    output_box = ctk.CTkTextbox(parent_frame, width=600, height=parent_frame.winfo_height() * 0.7)
    output_box.pack(padx=10, pady=10)
    output_box.configure(state="disabled")

    # Command entry
    command_entry = ctk.CTkEntry(parent_frame, width=600)
    command_entry.pack(padx=10, pady=(0, 10))
    command_entry.bind("<Return>", lambda event: execute_command())

    # Optional back button
    if go_back_callback:
        back_button = ctk.CTkButton(parent_frame, text="Back", command=go_back_callback)
        back_button.pack(pady=5)
