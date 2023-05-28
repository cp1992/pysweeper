from utils import flatten

class TilesService:
    
    def get_unrevealed_tiles_count(self, tiles):
        count = 0
        for tile in flatten(tiles):
            if tile.unrevealed:
                count += 1
        return count
    
    def get_bomb_tiles_count(self, tiles):
        count = 0
        for tile in flatten(tiles):
            if (tile.bomb):
                count += 1
        return count