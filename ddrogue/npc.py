from pygame.sprite import Sprite, Group

from .dice import roll
from .mechanics.stats import Stat


BLACK = 0, 0, 0
BLUE = 0, 255, 0

WIDTH = HEIGHT = 32  # TODO only define this once


class Goblin:
    def __init__(self, image):
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = image
        self.rect = image.get_rect()
        self.stats = self.init_stats()
        self.hp = roll('1d4') + self.stats['con'].bonus
        self.ac = 10 + self.stats['dex'].bonus
        # TODO add armor and size values

    def init_stats(self):
        stats = {
            'str': Stat(13, 1),
            'dex': Stat(14, 2),
            'con': Stat(12, 1),
            'wis': Stat(11, 0),
            'cha': Stat(8, -1),
            'int': Stat(9, -1),
        }
        return stats


class MonsterGroup(Group):
    pass
