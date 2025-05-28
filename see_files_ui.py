import customtkinter as ctk
import os

def file_browser_ui(parent_frame, go_back_callback=None):
    """Файловый браузер с просмотром содержимого файлов."""
    clear_frame(parent_frame)

    # Текущая папка
    current_path = [os.getcwd()]  # Обертка в список, чтобы менять внутри функций

    # Заголовок пути
    label_path = ctk.CTkLabel(parent_frame, text=current_path[0], font=("Arial", 16))
    label_path.pack(pady=5)

    # Фрейм для кнопок файлов и папок
    files_frame = ctk.CTkScrollableFrame(parent_frame, width=parent_frame.winfo_width() * 0.7, height=parent_frame.winfo_height() * 0.1)
    files_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Фрейм для управления
    button_frame = ctk.CTkFrame(parent_frame)
    button_frame.pack(pady=10)

    up_button = ctk.CTkButton(button_frame, text="Up", width=100, command=lambda: go_up())
    up_button.grid(row=0, column=0, padx=5)

    back_button = ctk.CTkButton(button_frame, text="← Back", width=100, command=lambda: go_back_callback() if go_back_callback else None)
    back_button.grid(row=0, column=1, padx=5)

    # Фрейм для содержимого файла
    file_viewer = ctk.CTkTextbox(parent_frame, height=300, font=("Arial", 14))
    file_viewer.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def update_list():
        """Обновляет список файлов и папок."""
        for widget in files_frame.winfo_children():
            widget.destroy()

        label_path.configure(text=current_path[0])
        file_viewer.delete("1.0", "end")  # Очищаем просмотр при переходе

        try:
            items = os.listdir(current_path[0])
            items.sort()
            for item in items:
                full_path = os.path.join(current_path[0], item)

                if os.path.isdir(full_path):
                    btn = ctk.CTkButton(files_frame, text=f"[DIR] {item}", anchor="w",
                                        command=lambda p=full_path: open_folder(p))
                    btn.pack(fill="x", pady=2)
                else:
                    btn = ctk.CTkButton(files_frame, text=item, anchor="w", fg_color="transparent",
                                        hover_color="#333333", command=lambda p=full_path: open_file(p))
                    btn.pack(fill="x", pady=2)
        except Exception as e:
            error_label = ctk.CTkLabel(files_frame, text=f"Error: {str(e)}", text_color="red")
            error_label.pack()

    def open_folder(path):
        """Открыть папку."""
        current_path[0] = path
        update_list()

    def open_file(path):
        """Открыть файл и показать его содержимое."""
        file_viewer.delete("1.0", "end")
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                file_viewer.insert("1.0", content)
        except Exception as e:
            file_viewer.insert("1.0", f"Cannot open file:\n{str(e)}")

    def go_up():
        """Подняться на уровень вверх."""
        current_path[0] = os.path.dirname(current_path[0])
        update_list()

    update_list()

def clear_frame(frame):
    """Очищает все виджеты в указанном фрейме."""
    for widget in frame.winfo_children():
        widget.destroy()
