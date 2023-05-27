import tkinter as tk
from tkinter import ttk

from utils import flatten
from Tile import Tile

# TODO: does this have to be a class? Can we convert it to script w/exported functions
class Game:

    # game data
    size = 5
    disable_input = False
    tiles = []
    bomb_count = 0

    # widgets
    root = None
    game_status_text = None
    new_game_button = None

    def __init__(self, root):
        self.root = root

    def start_game(self):
        self.disable_input = False
        ## build board ##

        # TODO: move into board object/build_board function
        # create tiles
        frame = ttk.Frame(self.root)
        frame.columnconfigure(self.size)
        frame.rowconfigure(self.size)

        tileImg = tk.PhotoImage(file="assets/tile.png")
        for x in range(0, self.size):
            col = []
            for y in range(0, self.size):
                tileWidget = ttk.Label(frame, image=tileImg)
                tileWidget.bind("<Button-1>", lambda _, x=x,
                                y=y: self.tile_clicked(x, y))
                tileWidget.bind("<Button-2>", lambda _, x=x, y=y: self.tile_right_clicked(x, y))
                tileWidget.grid(column=x, row=y)
                tile = Tile(coordinates=(x, y),
                                widget=tileWidget)
                self.bomb_count += tile.bomb # TODO: find more elegant way to accomplish this (refactor into create_tile method?)
                col.append(tile)
            self.tiles.append(col)

        frame.place(relx=.5, rely=.5, anchor="center")

        # create and game status text and new game button which will be added to a frame object
        self.gameStatusFrame = ttk.Frame(self.root)
        self.game_status_text = ttk.Label(
            self.gameStatusFrame, text="Lost Game!")
        self.new_game_button = ttk.Button(
            self.gameStatusFrame, text="New Game", command=self.new_game_clicked)
        self.gameStatusFrame.place(relx=.5, rely=.8, anchor="center")

        self.root.mainloop()

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

    # TODO: move to board
    # check tile
    # if bombs are nearby set the tile image and return false
    # otherwise tile is empty, check if tile not visited and return True
    def check_tile(self, tile, tiles, visited_tiles):
        if tile == None or tile.bomb:
            return False

        count = tile.get_adjacent_bomb_count(tiles)
        if count == 0:
            tile.set_image("assets/tileSafe.png")
            tile.unrevealed = False
            return tile not in visited_tiles

        tile.set_image(f"assets/tile{count}.png")
        tile.unrevealed = False
        return False

    def lose_game(self, clicked_tile, tiles):
        self.disable_input = True

        self.show_game_status('Lost game!')
        # go through tiles and show bombs
        for tile in flatten(tiles):
            if tile.coordinates == clicked_tile.coordinates:
                tile.set_image("assets/tileBombClicked.png")
            elif tile.bomb:
                tile.set_image("assets/tileBomb.png")

    def win_game(self):
        self.show_game_status('Won game!')
        self.disable_input = True

    def check_for_win_condition(self, tile, tiles):
        # get number of bombs
        # check number of unrevealed tiles
        # if unrevealed tiles == bombs
        # then win
        print(f"Bomb count => {self.bomb_count}, unrevealed tiles => {tile.get_unrevealed_tiles(tiles)}")
        if self.bomb_count == tile.get_unrevealed_tiles(tiles):
            self.win_game()

    def new_game_clicked(self):
        self.hide_game_status()
        self.reset_game()

        # reset tiles
        for tile in flatten(self.tiles):
            tile.reset()
            self.bomb_count += tile.bomb

        self.disable_input = False

    def tile_clicked(self, x, y):
        if (not self.disable_input):
            tile = self.tiles[x][y]
            if (tile.bomb):
                self.lose_game(tile, self.tiles)
            else:
                count = tile.get_adjacent_bomb_count(self.tiles)
                if count > 0:
                    tile.set_image(f"assets/tile{count}.png")
                    tile.unrevealed = False
                else:
                    tile.set_image("assets/tileSafe.png")
                    tile.unrevealed = False
                    # visit nearby tiles, and set their image if they have adjacent bombs
                    # if the tile is empty, add to emptyTiles list
                    # iterate through list, with same logic (set thir image, get empty tiles)
                    visited_tiles = []
                    empty_tiles = self.check_adjacent_tiles(
                        tile, self.tiles, visited_tiles)
                    while empty_tiles:
                        empty_tiles += self.check_adjacent_tiles(
                            empty_tiles.pop(), self.tiles, visited_tiles)
                        
            self.check_for_win_condition(tile, self.tiles)

    def tile_right_clicked(self, x, y):
        self.tiles[x][y].set_image("assets/tileFlag.png")

    def show_game_status(self, status):
        self.game_status_text.config(text=status)
        self.game_status_text.pack()
        self.new_game_button.pack()

    def hide_game_status(self):
        self.game_status_text.pack_forget()
        self.new_game_button.pack_forget()

    def reset_game(self):
        self.bomb_count = 0
