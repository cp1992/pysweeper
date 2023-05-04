import tkinter as tk
from tkinter import ttk

from Game import Game

def get_center(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    return f'{center_x}+{center_y}'

##################
###### MAIN ######
##################

root = tk.Tk()

# set window height/width, position, and title
window_width = 800
window_height = 600
center_coordinates = get_center(root, window_width, window_height)

root.geometry(
    f'{window_width}x{window_height}+{center_coordinates}')
root.resizable(False, False)
root.title("pysweeper")

game = Game(root)
game.start_game()
