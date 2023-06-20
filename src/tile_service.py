def get_adjacent_bomb_count(tile, tiles):
    count = 0

    tile_above_left = get_tile_above_left(tile, tiles)
    if tile_above_left and tile_above_left.bomb:
        count = count + 1

    tile_above = get_tile_above(tile, tiles)
    if tile_above and tile_above.bomb:
        count = count + 1

    tile_above_right = get_tile_above_right(tile, tiles)
    if tile_above_right and tile_above_right.bomb:
        count = count + 1

    tile_right = get_tile_right(tile, tiles)
    if tile_right and tile_right.bomb:
        count = count + 1

    tile_below_right = get_tile_below_right(tile, tiles)
    if tile_below_right and tile_below_right.bomb:
        count = count + 1

    tile_below = get_tile_below(tile, tiles)
    if tile_below and tile_below.bomb:
        count = count + 1

    tile_below_left = get_tile_below_left(tile, tiles)
    if tile_below_left and tile_below_left.bomb:
        count = count + 1

    tile_left = get_tile_left(tile, tiles)
    if tile_left and tile_left.bomb:
        count = count + 1

    return count


def get_tile_above_left(tile, tiles):
    x = tile.coordinates[0] - 1
    y = tile.coordinates[1] - 1

    if x >= 0 and y >= 0:
        return tiles[x][y]
    else:
        return None


def get_tile_above(tile, tiles):
    x = tile.coordinates[0]
    y = tile.coordinates[1] - 1

    if y >= 0:
        return tiles[x][y]
    else:
        return None


def get_tile_above_right(tile, tiles):
    x = tile.coordinates[0] + 1
    y = tile.coordinates[1] - 1

    if x <= len(tiles) - 1 and y >= 0:
        return tiles[x][y]
    else:
        return None


def get_tile_right(tile, tiles):
    x = tile.coordinates[0] + 1
    y = tile.coordinates[1]

    if x <= len(tiles) - 1:
        return tiles[x][y]
    else:
        return None


def get_tile_below_right(tile, tiles):
    x = tile.coordinates[0] + 1
    y = tile.coordinates[1] + 1

    if x <= len(tiles) - 1 and y <= len(tiles) - 1:
        return tiles[x][y]
    else:
        return None


def get_tile_below(tile, tiles):
    x = tile.coordinates[0]
    y = tile.coordinates[1] + 1

    if y <= len(tiles) - 1:
        return tiles[x][y]
    else:
        return None


def get_tile_below_left(tile, tiles):
    x = tile.coordinates[0] - 1
    y = tile.coordinates[1] + 1

    if x >= 0 and y <= len(tiles) - 1:
        return tiles[x][y]
    else:
        return None


def get_tile_left(tile, tiles):
    x = tile.coordinates[0] - 1
    y = tile.coordinates[1]

    if x >= 0:
        return tiles[x][y]
    else:
        return None
