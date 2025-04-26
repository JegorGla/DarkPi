import customtkinter as ctk

class NormalKeyboard:
    def __init__(self, parent_frame, target_entry):
        self.parent_frame = parent_frame
        self.target_entry = target_entry  # Изначально целевое поле
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = ctk.CTkFrame(self.parent_frame)
        keyboard_frame.pack(pady=10)

        keys = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['←', ' ', 'OK']
        ]

        for row in keys:
            row_frame = ctk.CTkFrame(keyboard_frame)
            row_frame.pack()

            for key in row:
                button = ctk.CTkButton(
                    row_frame, text=key, width=50, height=50,
                    command=lambda k=key: self.on_key_press(k)
                )
                button.pack(side="left", padx=5)

    def on_key_press(self, key):
        if key == '←':  # Удалить последний символ
            current_text = self.target_entry.get()
            self.target_entry.delete(0, "end")
            self.target_entry.insert(0, current_text[:-1])
        elif key == 'OK':  # Завершить ввод
            self.target_entry.event_generate("<Return>")
        elif key == ' ':  # Добавить пробел
            self.target_entry.insert("end", " ")
        else:  # Добавить символ
            self.target_entry.insert("end", key)

class NumericKeyboard:
    def __init__(self, parent_frame, target_entry):
        self.parent_frame = parent_frame
        self.target_entry = target_entry  # Изначально целевое поле
        self.create_keyboard()

    def create_keyboard(self):
        keyboard_frame = ctk.CTkFrame(self.parent_frame)
        keyboard_frame.pack(pady=10)

        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['←', ' ', '.', ',', '-', 'OK']
        ]

        for row in keys:
            row_frame = ctk.CTkFrame(keyboard_frame)
            row_frame.pack()

            for key in row:
                button = ctk.CTkButton(
                    row_frame, text=key, width=50, height=50,
                    command=lambda k=key: self.on_key_press(k)
                )
                button.pack(side="left", padx=1)

    def on_key_press(self, key):
        if key == '←':  # Удалить последний символ
            current_text = self.target_entry.get()
            self.target_entry.delete(0, "end")
            self.target_entry.insert(0, current_text[:-1])
        else:  # Добавить символ
            self.target_entry.insert("end", key)