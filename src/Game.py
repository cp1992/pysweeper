import tkinter as tk
from tkinter import ttk
import random

from utils import flatten
from Tile import Tile

class Game:

    def __init__(self, root):
        self.size = 10
        self.lost_game = False
        self.tiles = []

        self.root = root

    def start_game(self):
        # restart
        if self.lost_game:
            self.lost_game = False

        ## build board ##

        # create tiles
        frame = ttk.Frame(self.root)
        frame.columnconfigure(10)
        frame.rowconfigure(10)

        tileImg = tk.PhotoImage(file="assets/tile.png")
        for x in range(0, self.size):
            col = []
            for y in range(0, self.size):
                tileWidget = ttk.Label(frame, image=tileImg)
                tileWidget.bind("<Button-1>", lambda _, x=x,
                                y=y: self.button_clicked(x, y))
                tileWidget.grid(column=x, row=y)
                col.append(Tile(coordinates=(x, y),
                        widget=tileWidget, bomb=self.generate_bomb()))
            self.tiles.append(col)

        frame.place(relx=.5, rely=.5, anchor="center")

        # create and game status text and new game button which will be added to a frame object
        self.gameStatusFrame = ttk.Frame(self.root)
        self.gameStatusText = ttk.Label(self.gameStatusFrame, text="Lost Game!")
        self.newGameButton = ttk.Button(self.gameStatusFrame, text="New Game", command=self.new_game)
        self.gameStatusFrame.place(relx=.5, rely=.8, anchor="center")
        
        self.root.mainloop()

    def show_game_status(self, status):
        self.gameStatusText.config(text = status)
        self.gameStatusText.pack()
        self.newGameButton.pack()

    def hide_game_status(self):
        self.gameStatusText.pack_forget()
        self.newGameButton.pack_forget()

    # 10% chance of bomb
    def generate_bomb(self):
        return random.randint(0, 9) == 0
    
    def button_clicked(self, x, y):
        if (not self.lost_game):
            tile = self.tiles[x][y]
            if (tile.bomb):
                self.lose_game(tile, self.tiles)
            else:
                count = tile.get_adjacent_bomb_count(self.tiles)
                if count > 0:
                    tile.set_image(f"assets/tile{count}.png")
                else:
                    tile.set_image("assets/tileSafe.png")
                    # visit nearby tiles, and set their image if they have adjacent bombs
                    # if the tile is empty, add to emptyTiles list
                    # iterate through list, with same logic (set thir image, get empty tiles)
                    visited_tiles = []
                    empty_tiles = self.check_adjacent_tiles(tile, self.tiles, visited_tiles)
                    while empty_tiles:
                        empty_tiles += self.check_adjacent_tiles(
                            empty_tiles.pop(), self.tiles, visited_tiles)
                        
    # visit nearby tiles and set count on each
    # if nearby tile is an empty tile, and tile has not been visited, return it
    def check_adjacent_tiles(self, tile, tiles, visited_tiles=[]):

        empty_tiles = []

        tile_above_left = tile.get_tile_above_left(tiles)
        if self.check_tile(tile_above_left, tiles, visited_tiles):
            empty_tiles.append(tile_above_left)

        tile_above = tile.get_tile_above(tiles)
        if self.check_tile(tile_above, tiles, visited_tiles):
            empty_tiles.append(tile_above)

        tile_above_right = tile.get_tile_above_right(tiles)
        if self.check_tile(tile_above_right, tiles, visited_tiles):
            empty_tiles.append(tile_above_right)

        tile_right = tile.get_tile_right(tiles)
        if self.check_tile(tile_right, tiles, visited_tiles):
            empty_tiles.append(tile_right)

        tile_below_right = tile.get_tile_below_right(tiles)
        if self.check_tile(tile_below_right, tiles, visited_tiles):
            empty_tiles.append(tile_below_right)

        tile_below = tile.get_tile_below(tiles)
        if self.check_tile(tile_below, tiles, visited_tiles):
            empty_tiles.append(tile_below)

        tile_below_left = tile.get_tile_below_left(tiles)
        if self.check_tile(tile_below_left, tiles, visited_tiles):
            empty_tiles.append(tile_below)

        tile_left = tile.get_tile_left(tiles)
        if self.check_tile(tile_left, tiles, visited_tiles):
            empty_tiles.append(tile_left)

        visited_tiles.append(tile)

        return empty_tiles

    # check tile
    # if bombs are nearby set the tile image and return false
    # otherwise tile is empty, check if tile not visited and return True
    def check_tile(self, tile, tiles, visited_tiles):
        if tile == None or tile.bomb:
            return False

        count = tile.get_adjacent_bomb_count(tiles)
        if count == 0:
            tile.set_image("assets/tileSafe.png")
            return tile not in visited_tiles

        tile.set_image(f"assets/tile{count}.png")
        return False

    def lose_game(self, clicked_tile, tiles):
        self.lost_game = True

        self.show_game_status('Lost game!')
        # go through tiles and show bombs
        for tile in flatten(tiles):
            if tile.coordinates == clicked_tile.coordinates:
                tile.set_image("assets/tileBombClicked.png")
            elif tile.bomb:
                tile.set_image("assets/tileBomb.png")


    def new_game(self):
        self.hide_game_status()

        # reset tiles
        for tile in flatten(self.tiles):
            tile.set_image("assets/tile.png")
            tile.bomb = self.generate_bomb()

        self.lost_game = False
                



