from pygame import image, Rect


def load_tileset(path, tile_size=(32, 32)):
    i = image.load(path).convert()
    x, y = tile_size
    i_x, i_y = i.get_size()
    tileset = []
    if (i_x % x or i_y % y):
        # If not an even division
        raise Exception('tileset doesn\'t fit evenly into tiles\n'
                        'x remainder: %d, y remainder: %d' %
                        (i_x % x, i_y % y))
    for tile_y in range(0, i_y, y):
        line = []
        for tile_x in range(0, i_x, x):
            line.append(i.subsurface(Rect((tile_x, tile_y), tile_size)))
        tileset.append(line)
    return tileset


def select_tile(tile_set, pos):
    return tile_set[pos[0]][pos[1]]
