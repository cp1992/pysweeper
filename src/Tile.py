from tkinter import PhotoImage


class Tile:

    def __init__(self, coordinates, widget):
        self.coordinates = coordinates
        self.widget = widget
        self.bomb = False
        self.unrevealed = True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({"coordinates": self.coordinates, "widget": self.widget, "bomb": self.bomb})

    def reset(self):
        self.unrevealed = True
        self.set_image("assets/tile.png")
        self.bomb = False

    def set_image(self, image_path):
        image = PhotoImage(file=image_path)
        self.widget.config(image=image)
        self.widget.image = image
