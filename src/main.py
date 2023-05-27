# TODO: Would like to split game into Model-View-Controller
# Model/Controller 
#   - Game: stores all information/functionality needed by the game
#   - Tile: stores all information/functionality for tile
# View
#   - main: initial creation of UI, setups root
#   - Board: creates UI for representing game   


import tkinter as tk

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

# TODO: should all GUI setup logic go here? Then pass relevant 
game = Game(root)
game.start_game()
