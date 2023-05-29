import random

from utils import flatten


class TilesService:

    def get_unrevealed_tiles_count(self, tiles):
        count = 0
        for tile in flatten(tiles):
            if tile.unrevealed:
                count += 1
        return count

    def generate_bomb_tiles(self, tiles, bomb_count):
        bomb_tiles = []
        while len(bomb_tiles) < bomb_count:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            bomb_tile = tiles[x][y]
            if bomb_tile not in bomb_tiles:
                bomb_tile.bomb = True
                bomb_tiles.append(bomb_tile)
