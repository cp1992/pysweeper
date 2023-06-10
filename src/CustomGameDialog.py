import tkinter as tk
from tkinter import ttk

from utils import get_screen_horizontal_center

width = 330
height = 155


class CustomGameDialog:

    def __init__(self, parent, listener, current_size, current_bomb_count):
        self.listener = listener

        # create dialog
        self.top = tk.Toplevel(parent)
        self.top.resizable(False, False)
        self.top.title("Custom Game")
        self.top.geometry(f"{width}x{height}+{get_screen_horizontal_center(parent, width)}+100")

        # add labels/fields
        ttk.Label(self.top, text=f"Size ({current_size * current_size} Tiles):").place(x=20, y=20)
        self.size_text_field = ttk.Entry(self.top)
        self.size_text_field.insert(0, str(current_size))
        self.size_text_field.place(x=130, y=15)

        ttk.Label(self.top, text="Bomb Count:").place(x=20, y=50)
        self.bomb_count_text_field = ttk.Entry(self.top)
        self.bomb_count_text_field.insert(0, str(current_bomb_count))
        self.bomb_count_text_field.place(x=130, y=45)

        self.error = ttk.Label(self.top, foreground="red", wraplength=300)
        self.error.place(x=20, y=85)

        # add button
        ttk.Button(self.top, text="Create", command=self.on_create_clicked).place(x=208, y=115)

    def on_create_clicked(self):
        # validate size

        try:
            size = int(self.size_text_field.get())
            bomb_count = int(self.bomb_count_text_field.get())
            if self.validate(size=size, bomb_count=bomb_count, error_widget=self.error):
                self.listener(size, bomb_count)
                self.top.destroy()
        except ValueError:
            self.error.config(text="Please enter valid values")

    @staticmethod
    def validate(size, bomb_count, error_widget):
        if size == 0:
            error_widget.config(text="Size must have value")
            return False

        if bomb_count == 0:
            error_widget.config(text="Bomb count must have value")
            return False

        if bomb_count >= size ** 2:
            error_widget.config(text=f"Bomb count must be less than number of tiles ({size ** 2})")
            return False

        if size > 30:
            error_widget.config(text=f"Max size is 30 ({30 ** 2} tiles)")
            return False

        return True
