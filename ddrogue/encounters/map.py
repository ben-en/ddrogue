import numpy
import pygame
from pygame import Rect
from pygame.transform import scale

from ..colors import BLACK, WHITE, LIGHT_GREY, GREY
from ..ui import load_tile

BLANK_MAP = [[0 for i in range(12)] for i in range(12)]

MAP = numpy.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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


def points_around(point):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1),
                 (-1, 1), (-1, -1)]
    x, y = point
    return [((x + n_x), (y + n_y)) for n_x, n_y in neighbors]


# TODO: centering
class EncounterMap:
    """
    This class takes a floor plan and creates a completed map Image object that
    can be blitted onto the map as one object, as opposed to creating the map
    from all the tiles each turn.
    """
    def __init__(self, objects, floorplan, ui_size, tile_size=32):
        # Set up units, assumes rectangular matrix
        self.pos = (0, 0)
        self.unit = tile_size
        self.unit_t = (tile_size, tile_size)
        self.pixel_width = len(floorplan[0]) * self.unit
        self.pixel_height = len(floorplan) * self.unit
        self.pixel_size = [self.pixel_width, self.pixel_height]
        self.width = len(floorplan[0])
        self.height = len(floorplan)
        self.size = [self.width, self.height]
        self.ui_size = ui_size

        # Set up misc variables
        self.floor = floorplan
        self.floor_color = LIGHT_GREY
        self.wall_color = BLACK
        self.wall_tile = load_tile('wall')
        self.wall_character = 1

        # Create the img
        self.walls = self.list_walls()
        self.bg_img = self.assemble_map_img()
        self.rect = self.bg_img.get_rect()

        self.objects = objects
        self.update((0, 0))

    def assemble_map_img(self):
        """
        Requires self to have the following properties:
            self.floor          Containing the floorplan matrix
            self.pixel_width    Containing the pixel width of the map
            self.pixel_height   Containing the pixel height of the map
            self.floor_color    Containing the color of the floor
            self.wall_tile      Containing an Image object with a wall tile
        """
        new_map = self.create_tile(color=self.floor_color,
                                   xy=[self.pixel_width, self.pixel_height])
        for wall_rect in self.walls:
            new_map.blit(self.wall_tile, wall_rect)
        return new_map

    def list_walls(self):
        walls = []
        y_val = 0
        for row in self.floor:
            y = y_val * self.unit
            x_val = 0
            for x_label in row:
                if x_label == self.wall_character:
                    x = x_val * self.unit
                    walls.append(Rect(
                        [x, y, self.unit, self.unit]))
                x_val += 1
            y_val += 1
        return walls

    def is_wall(self, pos):
        ret = Rect(pos, (1, 1)).collidelist(self.walls)
        if ret == -1:
            return False
        return True

    def grid_pos(self, pos):
        """ Takes pixel coordinates and returns grid coordinates """
        new_pos = [
            (p / self.unit) + (0 if p % self.unit else 1) for p in pos
        ]
        return new_pos

    def pixel_pos(self, grid):
        """ Takes grid coordinates and returns pixel coordinates """
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
        tile = self.create_tile(color=color)
        new = self.create_tile(color=WHITE, xy=(total_x, total_y))
        y = 0
        for row in grid:
            y += 1
            x = 0
            for point in row:
                x += 1
                if not point == 1:
                    continue
                rect = Rect([x, y, self.unit, self.unit])
                new.blit(tile, rect)
        return new

    def create_tile(self, color=BLACK, edge_color=GREY, img=None, xy=None):
        """
        Creates a tile default the size of one grid square
        """
        if not xy:
            xy = (self.unit, self.unit)
        if img:
            # If an img for the tile, shrink it to the size of a tile
            return scale(img, xy)
        new_img = pygame.Surface(xy)
        new_img.fill(edge_color)
        new_img.fill(color, rect=[1, 1, xy[0] - 2, xy[1] - 2])
        return new_img

    def update(self, pos):
        self.full_img = self.bg_img.copy()
        for obj in self.objects:
            self.full_img.blit(obj.img, self.pixel_pos(obj.pos))
        self.img = pygame.Surface(self.ui_size)
        offset_pos = self.center(pos)
        self.img.blit(self.full_img, (0, 0), Rect(offset_pos, self.ui_size))

    def center(self, pos):
        p_pos = self.pixel_pos(pos)
        return (p_pos[0] - (self.ui_size[0] / 2),
                p_pos[1] - (self.ui_size[1] / 2))

    def obj_at(self, pos):
        """ return the object at the given position, if any """
        object_pos = [tuple(o.pos) for o in self.objects]
        if pos in object_pos:
            return self.objects[object_pos.index(pos)]
        return None

    def is_occupied(self, pos):
        return bool(self.obj_at(pos))

    def enemy_adjacent(self, grid_pos):
        """
        return true only if given position is adjacent to an enemy or object
        """
        possible_locations = []
        for enemy_position in [
            e.pos for e in self.objects if hasattr(e, 'ai') and e.hostile
        ]:
            x, y = enemy_position
            possible_locations.append(enemy_position)
            for i in range(3):
                for n in range(3):
                    offset_pos = (x + (i - 1), y + (n - 1))
                    possible_locations.append(offset_pos)
        if grid_pos in possible_locations:
            return True
        else:
            return False

    def visible_area(self, start, area):
        x, y = start
        area_list = []
        potentials = [(p, 1) for p in points_around(start)]
        while potentials:
            pos, steps = potentials.pop(0)
            if steps >= area:
                continue
            if self.is_wall(self.pixel_pos(pos)):
                continue
            new_potentials = [p for p in points_around(pos) if
                              p not in area_list]
            potentials.extend([(p, steps + 1) for p in new_potentials])
            area_list.append(pos)
        return area_list

    def movable_area(self, start, speed):
        x, y = start
        area_list = []
        potentials = [(p, 1) for p in points_around(start)]
        while potentials:
            pos, steps = potentials.pop(0)
            if steps >= speed:
                continue
            if self.is_occupied(pos) and self.obj_at(pos).hostile:
                continue
            if self.is_wall(self.pixel_pos(pos)):
                continue
            new_potentials = [p for p in points_around(pos) if
                              p not in area_list]
            potentials.extend([(p, steps + 1) for p in new_potentials])
            area_list.append(pos)
        return area_list
