import tkinter as tk
from tkinter import ttk
import random

from utils import flatten

from Tile import Tile

# TODO: consider moving these into a 'Game' object? 
# Then pass that around as needed to provide required references
root = tk.Tk()
lost_game = False
tiles = []

def start_game():

    # set window height/width, position, and title
    window_width = 800
    window_height = 600
    center_coordinates = get_center(root, window_width, window_height)

    root.geometry(f'{window_width}x{window_height}+{center_coordinates}')
    root.resizable(False, False)
    root.title("pysweeper")

    # build board
    size = 10
    frame = ttk.Frame(root)
    frame.columnconfigure(10)
    frame.rowconfigure(10)

    tileImg = tk.PhotoImage(file="assets/tile.png")
    for x in range(0, size):
        col = []
        for y in range(0, size):
            tileWidget = ttk.Label(frame, image=tileImg)
            tileWidget.bind("<Button-1>", lambda _, x=x, y=y: button_clicked(x, y))
            tileWidget.grid(column=x, row=y)
            col.append(Tile(coordinates=(x, y),
                    widget=tileWidget, bomb=generate_bomb()))
        tiles.append(col)

    frame.place(relx=.5, rely=.5, anchor="center")

    root.mainloop()

def get_center(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    return f'{center_x}+{center_y}'


def button_clicked(x, y):
    if (not lost_game):
        tile = tiles[x][y]
        if (tile.bomb):
            lose_game(tile, tiles)
        else:
            count = tile.get_adjacent_bomb_count(tiles)
            if count > 0:
                tile.set_image(f"assets/tile{count}.png")
            else:
                tile.set_image("assets/tileSafe.png")
                # visit nearby tiles, and set their image if they have adjacent bombs
                # if the tile is empty, add to emptyTiles list
                # iterate through list, with same logic (set thir image, get empty tiles)
                visited_tiles = []
                empty_tiles = check_adjacent_tiles(tile, tiles, visited_tiles)
                while empty_tiles:
                    empty_tiles += check_adjacent_tiles(
                        empty_tiles.pop(), tiles, visited_tiles)


def lose_game(clicked_tile, tiles):
    print("Lost game!")

    # TODO: poopy, find better way to control state
    # prevents buttons from being clicked
    global lost_game
    lost_game = True

    # go through tiles and show bombs
    for tile in flatten(tiles):
        if tile.coordinates == clicked_tile.coordinates:
            tile.set_image("assets/tileBombClicked.png")
        elif tile.bomb:
            tile.set_image("assets/tileBomb.png")

    # show lost game text
    lostGameText = ttk.Label(root, text="Lost Game!")
    lostGameText.pack(side="bottom", pady=80)

# 10% chance of bomb


def generate_bomb():
    return random.randint(0, 9) == 0

# visit nearby tiles and set count on each
# if nearby tile is an empty tile, and tile has not been visited, return it


def check_adjacent_tiles(tile, tiles, visited_tiles=[]):

    empty_tiles = []

    tile_above_left = tile.get_tile_above_left(tiles)
    if check_tile(tile_above_left, tiles, visited_tiles):
        empty_tiles.append(tile_above_left)

    tile_above = tile.get_tile_above(tiles)
    if check_tile(tile_above, tiles, visited_tiles):
        empty_tiles.append(tile_above)

    tile_above_right = tile.get_tile_above_right(tiles)
    if check_tile(tile_above_right, tiles, visited_tiles):
        empty_tiles.append(tile_above_right)

    tile_right = tile.get_tile_right(tiles)
    if check_tile(tile_right, tiles, visited_tiles):
        empty_tiles.append(tile_right)

    tile_below_right = tile.get_tile_below_right(tiles)
    if check_tile(tile_below_right, tiles, visited_tiles):
        empty_tiles.append(tile_below_right)

    tile_below = tile.get_tile_below(tiles)
    if check_tile(tile_below, tiles, visited_tiles):
        empty_tiles.append(tile_below)

    tile_below_left = tile.get_tile_below_left(tiles)
    if check_tile(tile_below_left, tiles, visited_tiles):
        empty_tiles.append(tile_below)

    tile_left = tile.get_tile_left(tiles)
    if check_tile(tile_left, tiles, visited_tiles):
        empty_tiles.append(tile_left)

    visited_tiles.append(tile)

    return empty_tiles

# check tile
# if bombs are nearby set the tile image and return false
# otherwise tile is empty, check if tile not visited and return True


def check_tile(tile, tiles, visited_tiles):
    if tile == None:
        return False

    count = tile.get_adjacent_bomb_count(tiles)
    if count == 0:
        tile.set_image("assets/tileSafe.png")
        return tile not in visited_tiles

    tile.set_image(f"assets/tile{count}.png")
    return False

start_game()
