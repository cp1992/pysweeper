from tkinter import PhotoImage

class Tile:

    def __init__(self, coordinates, widget, bomb=False):
        self.coordinates = coordinates
        self.widget = widget
        self.bomb = bomb

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({"coordinates": self.coordinates, "widget": self.widget, "bomb": self.bomb})
    
    def get_tile_above_left(self, tiles):
        x = self.coordinates[0] - 1
        y = self.coordinates[1] - 1

        if x >= 0 and y >= 0:
            return tiles[x][y]
        else:
            return None    

    def get_tile_above(self, tiles):
        x = self.coordinates[0]
        y = self.coordinates[1] - 1

        if y >= 0:
            return tiles[x][y]
        else:
            return None

    def get_tile_above_right(self, tiles):
        x = self.coordinates[0] + 1
        y = self.coordinates[1] - 1

        if x <= len(tiles) - 1 and y >= 0:
            return tiles[x][y]
        else:
            return None
        
    def get_tile_right(self, tiles):
        x = self.coordinates[0] + 1
        y = self.coordinates[1]

        if x <= len(tiles) - 1:
            return tiles[x][y]
        else:
            return None
        
    def get_tile_below_right(self, tiles):
        x = self.coordinates[0] + 1
        y = self.coordinates[1] + 1

        if x <= len(tiles) - 1 and y <= len(tiles) - 1:
            return tiles[x][y]
        else:
            return None
        
    def get_tile_below(self, tiles):
        x = self.coordinates[0]
        y = self.coordinates[1] + 1

        if y <= len(tiles) - 1:
            return tiles[x][y]
        else:
            return None
        
    def get_tile_below_left(self, tiles):
        x = self.coordinates[0] - 1
        y = self.coordinates[1] + 1

        if x >= 0 and y <= len(tiles) - 1:
            return tiles[x][y]
        else:
            return None

    def get_tile_left(self, tiles):
        x = self.coordinates[0] - 1
        y = self.coordinates[1]

        if x >= 0:
            return tiles[x][y]
        else:
            return None

    def get_adjacent_bomb_count(self, tiles):
        count = 0

        tile_above_left = self.get_tile_above_left(tiles)
        if tile_above_left and tile_above_left.bomb:
            count = count + 1

        tile_above = self.get_tile_above(tiles)
        if tile_above and tile_above.bomb:
            count = count + 1

        tile_above_right = self.get_tile_above_right(tiles)
        if tile_above_right and tile_above_right.bomb:
            count = count + 1

        tile_right = self.get_tile_right(tiles)
        if tile_right and tile_right.bomb:
            count = count + 1
        
        tile_below_right = self.get_tile_below_right(tiles)
        if tile_below_right and tile_below_right.bomb:
            count = count + 1

        tile_below = self.get_tile_below(tiles)
        if tile_below and tile_below.bomb:
            count = count + 1

        tile_below_left = self.get_tile_below_left(tiles)
        if tile_below_left and tile_below_left.bomb:
            count = count + 1

        tile_left = self.get_tile_left(tiles)
        if tile_left and tile_left.bomb:
            count = count + 1

        return count
    
    def set_image(self, image_path):
        image = PhotoImage(file=image_path)
        self.widget.config(image=image)
        self.widget.image = image