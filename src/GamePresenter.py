from utils import flatten

import tile_service
import tiles_service


class GamePresenter:
    # constants
    difficulties = {
        'easy': {'size': 10, 'bombs': 12},
        'medium': {'size': 15, 'bombs': 40},
        'hard': {'size': 25, 'bombs': 99}
    }

    # defaults
    size = difficulties["easy"]["size"]
    bomb_count = difficulties["easy"]["bombs"]

    tiles = []
    disable_input = False

    def __init__(self, game_view):
        self.game_view = game_view
        self.__create_ui()

    def __create_ui(self):
        self.game_view.create_window()
        self.game_view.create_menu(self.difficulty_changed, self.set_custom_game, self.size, self.bomb_count)
        self.tiles = self.game_view.create_board(
            self.size, self.tile_clicked, self.tile_right_clicked)
        self.game_view.create_game_status_frame(
            self.bomb_count, self.new_game_clicked)

    def start_game(self):
        self.disable_input = False
        tiles_service.generate_bomb_tiles(self.tiles, self.size, self.bomb_count)
        self.game_view.window.mainloop()

    def win_game(self):
        self.disable_input = True
        self.game_view.show_game_status("Won game!")

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
        if self.bomb_count == tiles_service.get_unrevealed_tiles_count(tiles):
            self.win_game()

    def reset_game(self):
        # reset tiles
        for tile in flatten(self.tiles):
            tile.reset()

        # regenerate bombs
        tiles_service.generate_bomb_tiles(self.tiles, self.size, self.bomb_count)

        # re-enable input
        self.disable_input = False

    # visit nearby tiles and set count on each
    # if nearby tile is an empty tile, and tile has not been visited, return it
    def check_adjacent_tiles(self, tile, tiles, visited_tiles):

        empty_tiles = []

        tile_above_left = tile_service.get_tile_above_left(tile, tiles)
        if self.check_tile(tile_above_left, tiles, visited_tiles):
            empty_tiles.append(tile_above_left)

        tile_above = tile_service.get_tile_above(tile, tiles)
        if self.check_tile(tile_above, tiles, visited_tiles):
            empty_tiles.append(tile_above)

        tile_above_right = tile_service.get_tile_above_right(tile, tiles)
        if self.check_tile(tile_above_right, tiles, visited_tiles):
            empty_tiles.append(tile_above_right)

        tile_right = tile_service.get_tile_right(tile, tiles)
        if self.check_tile(tile_right, tiles, visited_tiles):
            empty_tiles.append(tile_right)

        tile_below_right = tile_service.get_tile_below_right(tile, tiles)
        if self.check_tile(tile_below_right, tiles, visited_tiles):
            empty_tiles.append(tile_below_right)

        tile_below = tile_service.get_tile_below(tile, tiles)
        if self.check_tile(tile_below, tiles, visited_tiles):
            empty_tiles.append(tile_below)

        tile_below_left = tile_service.get_tile_below_left(tile, tiles)
        if self.check_tile(tile_below_left, tiles, visited_tiles):
            empty_tiles.append(tile_below)

        tile_left = tile_service.get_tile_left(tile, tiles)
        if self.check_tile(tile_left, tiles, visited_tiles):
            empty_tiles.append(tile_left)

        visited_tiles.append(tile)

        return empty_tiles

    # check tile
    # if bombs are nearby set the tile image and return false
    # otherwise tile is empty, check if tile not visited and return True
    def check_tile(self, tile, tiles, visited_tiles):
        if tile is None or tile.bomb:
            return False

        count = tile_service.get_adjacent_bomb_count(tile, tiles)
        if count == 0:
            tile.set_image("assets/tileSafe.png")
            tile.unrevealed = False
            return tile not in visited_tiles

        tile.set_image(f"assets/tile{count}.png")
        tile.unrevealed = False
        return False

    ## Listeners ##

    def tile_clicked(self, x, y):
        if not self.disable_input:
            tile = self.tiles[x][y]
            if tile.bomb:
                self.lose_game(tile, self.tiles)
            else:
                count = tile_service.get_adjacent_bomb_count(
                    tile, self.tiles)
                if count > 0:
                    tile.set_image(f"assets/tile{count}.png")
                    tile.unrevealed = False
                else:
                    tile.set_image("assets/tileSafe.png")
                    tile.unrevealed = False
                    # visit nearby tiles, and set their image if they have adjacent bombs
                    # if the tile is empty, add to emptyTiles list
                    # iterate through list, with same logic (set their image, get empty tiles)
                    visited_tiles = []
                    empty_tiles = self.check_adjacent_tiles(
                        tile, self.tiles, visited_tiles)
                    while empty_tiles:
                        empty_tiles += self.check_adjacent_tiles(
                            empty_tiles.pop(), self.tiles, visited_tiles)

            self.check_for_win_condition(self.tiles)

    def tile_right_clicked(self, x, y):
        if not self.disable_input:
            self.tiles[x][y].set_image("assets/tileFlag.png")

    def new_game_clicked(self):
        self.game_view.hide_game_status()
        self.reset_game()

    def difficulty_changed(self, difficulty):
        self.size = self.difficulties[difficulty]["size"]
        self.bomb_count = self.difficulties[difficulty]["bombs"]

        self.game_view.destroy_tiles(self.tiles)
        self.tiles = self.game_view.create_board(
            self.size, self.tile_clicked, self.tile_right_clicked)
        tiles_service.generate_bomb_tiles(self.tiles, self.size, self.bomb_count)
        self.game_view.set_bomb_count(self.bomb_count)

    def set_custom_game(self, size, bomb_count):
        self.size = size
        self.bomb_count = bomb_count

        self.game_view.destroy_tiles(self.tiles)
        self.tiles = self.game_view.create_board(
            self.size, self.tile_clicked, self.tile_right_clicked)
        tiles_service.generate_bomb_tiles(self.tiles, self.size, self.bomb_count)
        self.game_view.set_bomb_count(self.bomb_count)
