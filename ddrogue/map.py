import numpy
import pygame


BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 200, 200, 200
YELLOW = 255, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255

BLANK_MAP = [[0 for i in range(12)] for i in range(12)]

MAP = numpy.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
])


def create_map_matrix():
    """
    Placeholder function that returns a map matrix.
    ex:
        MAP = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
    """
    return MAP


def create_tile(color, xy):
    """ Takes a color and a height/width pair and returns a surface object """
    new_image = pygame.Surface(xy)
    new_image.fill(GREY)
    new_image.fill(color, rect=[1, 1, xy[0] - 2, xy[1] - 2])
    return new_image


class Map:
    """
    This class takes a floor plan and creates a completed map Image object that
    can be blitted onto the map as one object, as opposed to creating the map
    from all the tiles each turn.
    """
    def __init__(self, floorplan, tile_size=32):
        # Set up units, assumes rectangular matrix
        self.unit = tile_size
        self.pixel_width = len(floorplan[0]) * self.unit
        self.pixel_height = len(floorplan) * self.unit
        self.pixel_size = [self.pixel_width, self.pixel_height]
        self.width = len(floorplan[0])
        self.height = len(floorplan)
        self.size = [self.width, self.height]

        # Set up misc variables
        self.floor = floorplan
        self.floor_color = GREY
        self.wall_color = BLACK
        self.wall_tile = create_tile(BLACK, [self.unit, self.unit])
        self.wall_character = 1

        # Create the image
        self.walls = self.list_walls()
        self.image = self.assemble_map_image()
        self.rect = self.image.get_rect()

    def assemble_map_image(self):
        """
        Requires self to have the following properties:
            self.floor          Containing the floorplan matrix
            self.pixel_width    Containing the pixel width of the map
            self.pixel_height   Containing the pixel height of the map
            self.floor_color    Containing the color of the floor
            self.wall_tile      Containing an Image object with a wall tile
        """
        new_map = create_tile(self.floor_color,
                              [self.pixel_width, self.pixel_height])
        for wall_rect in self.walls:
            new_map.blit(self.wall_tile, wall_rect)
        return new_map

    def list_walls(self):
        print('assembling walls')
        walls = []
        y_val = 0
        for row in self.floor:
            y = y_val * self.unit
            x_val = 0
            for x_label in row:
                if x_label == self.wall_character:
                    x = x_val * self.unit
                    walls.append(pygame.Rect(
                        [x, y, self.unit, self.unit]))
                x_val += 1
            y_val += 1
        return walls

    def is_wall(self, pos):
        pos_rect = pygame.Rect(pos[0], pos[1], self.unit, self.unit)
        ret = pos_rect.collidelist(self.walls)
        if ret == -1:
            return False
        print('Is wall #%s in the list' % ret)
        print(pos_rect, self.walls[ret])
        print(self.walls[ret].colliderect(pos_rect))
        return True

    def grid_pos(self, pos):
        # print('pixel position', pos)
        # print('returned position', [((p / self.unit) + 0 if p % self.unit else
        #                            1) for p in pos])
        return [p / self.unit for p in pos]

    def pixel_pos(self, grid):
        # print('grid position', grid)
        # print('returned position', (grid[0] * self.unit, grid[1] * self.unit))
        return (grid[0] * self.unit, grid[1] * self.unit)

    def draw_grid(self, grid, color):
        """ Draws a grid of the chosen color.

        Example grid:
            [
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
            ]
        """
        total_x = len(grid[0]) * self.unit
        total_y = len(grid) * self.unit
        tile = create_tile(color, (self.unit, self.unit))
        new = create_tile(WHITE, (total_x, total_y))
        y = 0
        for row in grid:
            y += 1
            x = 0
            for point in row:
                x += 1
                if not point == 1:
                    continue
                rect = pygame.Rect([x, y, self.unit, self.unit])
                new.blit(tile, rect)
        return new
