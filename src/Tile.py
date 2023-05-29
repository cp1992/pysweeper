from tkinter import PhotoImage
import random

from utils import flatten


class Tile:

    unrevealed = True

    def __init__(self, coordinates, widget):
        self.coordinates = coordinates
        self.widget = widget
        self.generate_bomb()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({"coordinates": self.coordinates, "widget": self.widget, "bomb": self.bomb})

    # 10% chance of bomb
    def generate_bomb(self):
        self.bomb = random.randint(0, 9) == 0

    def reset(self):
        self.unrevealed = True
        self.set_image("assets/tile.png")
        self.generate_bomb()

    def set_image(self, image_path):
        image = PhotoImage(file=image_path)
        self.widget.config(image=image)
        self.widget.image = image
