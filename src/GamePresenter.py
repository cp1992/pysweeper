from utils import flatten

from Tile import Tile
from TilesService import TilesService

class GamePresenter():
    
    # constants
    size = 10

    # game logic
    tiles = []
    bomb_count = 0
    disable_input = False
    
    def __init__(self, game_view):
        self.game_view = game_view
        self.tiles_service = TilesService()
        self.__create_ui()

    def __create_ui(self):
      self.game_view.create_window()
      self.tiles = self.game_view.create_board(self.size, self.tile_clicked, self.tile_right_clicked)
      self.game_view.create_game_status_frame(self.new_game_clicked)
      self.game_view.root.mainloop()
    
    def start_game(self):
       self.disable_input = False
       self.bomb_count = self.tiles_service.get_bomb_tiles_count(self.tiles)

    def win_game(self):
        self.disable_input = True
        self.game_view.show_game_status('Won game!')

    def lose_game(self, clicked_tile, tiles):
        self.disable_input = True

        self.game_view.show_game_status('Lost game!')
        # go through tiles and show bombs
        for tile in flatten(tiles):
            if tile.coordinates == clicked_tile.coordinates:
                tile.set_image("assets/tileBombClicked.png")
            elif tile.bomb:
                tile.set_image("assets/tileBomb.png")

    def check_for_win_condition(self, tiles):
        # get number of bombs
        # check number of unrevealed tiles
        # if unrevealed tiles == bombs
        # then win
        print(f"Bomb count => {self.bomb_count}, unrevealed tiles => {self.tiles_service.get_unrevealed_tiles_count(tiles)}")
        if self.bomb_count == self.tiles_service.get_unrevealed_tiles_count(tiles):
            self.win_game()

    def reset_game(self):
        self.bomb_count = 0

    # TODO: move to TileService
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

    # TODO: move to tile_service
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

    ## Listeners ##

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
                        
            self.check_for_win_condition(self.tiles)

    def tile_right_clicked(self, x, y):
        self.tiles[x][y].set_image("assets/tileFlag.png")

    def new_game_clicked(self):
        self.game_view.hide_game_status()
        self.reset_game()

        # reset tiles
        for tile in flatten(self.tiles):
            tile.reset()
            self.bomb_count += tile.bomb

        self.disable_input = False