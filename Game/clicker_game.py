from tkinter import messagebox
import customtkinter as ctk

class ClickerGame:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.score = 0
        self.create_ui()

    def create_ui(self):
        # Очищаем фрейм
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Заголовок
        label_title = ctk.CTkLabel(self.parent_frame, text="Кликер", font=("Arial", 24))
        label_title.pack(pady=20)

        # Счет
        self.score_label = ctk.CTkLabel(self.parent_frame, text=f"Счет: {self.score}", font=("Arial", 20))
        self.score_label.pack(pady=10)

        # Кнопка для кликов
        click_button = ctk.CTkButton(
            self.parent_frame, text="Click me!", font=("Arial", 16),
            command=self.increment_score
        )
        click_button.pack(pady=20)

        # Кнопка завершения игры
        finish_button = ctk.CTkButton(
            self.parent_frame, text="End", font=("Arial", 16),
            command=self.finish_game
        )
        finish_button.pack(pady=20)

    def increment_score(self):
        self.score += 1
        self.score_label.configure(text=f"Score: {self.score}")

    def finish_game(self):
        messagebox.showinfo("Clicker", f"Game over! Your score: {self.score}")
        for widget in self.parent_frame.winfo_children():
            widget.destroy()