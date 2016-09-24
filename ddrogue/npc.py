import pygame
from pygame.sprite import Sprite, Group

from .dice import roll
from .mechanics import stat_bonus, Stat


BLACK = 0, 0, 0
BLUE = 0, 255, 0

WIDTH = HEIGHT = 32  # TODO only define this once


class NonPlayerCharacter:
    """
    Creates a player sprite and group, and attaches them to itself.
    """
    def __init__(self):
        self.width = self.height = 32  # TODO only define this once
        self.group = NonPlayerGroup()
        self.sprite = NonPlayerSprite(self.width, self.height,
                                      groups=[self.group])


class NonPlayerSprite(Sprite):
    """
    NonPlayer sprite, expects an image object and a width/height assignment
    """
    def __init__(self, image, groups=[]):
        # Call the parent class (Sprite) constructor which takes no arguments
        Sprite.__init__(self, groups)

        self.image = image

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Update the position of this object by setting the values of rect.x
        # and rect.y


class NonPlayerGroup(Group):
    pass


class Goblin(NonPlayerCharacter):
    def __init__(self):
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.groups = [NonPlayerGroup(), MonsterGroup()]
        self.sprite = NonPlayerSprite(pygame.Surface([WIDTH, HEIGHT]),
                                      groups=self.group)
        self.sprite.image.fill(BLUE)
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
