import pygame
from pygame.sprite import Sprite, Group

from .mechanics import Stat, StatBlock


PLAYER_COLOR = 255, 255, 100


class Player(object):
    """
    Creates a player sprite and group, and attaches them to itself.
    """
    def __init__(self):
        self.width = self.height = 32  # TODO only define this once
        self.group = PlayerGroup()
        self.sprite = PlayerSprite(self.width, self.height,
                                   groups=[self.group])
        self.rect = self.sprite.rect
        self.image = self.sprite.image
        self.level = 1
        self.stats = self.init_stats()

    def init_stats(self):
        stats = StatBlock(
            str=Stat(17, 3), dex=Stat(13, 1), con=Stat(14, 2), int=Stat(9, -1),
            wis=Stat(10, 0), cha=Stat(12, 1),
        )
        return stats


class PlayerSprite(Sprite):
    """
    Player sprite, expects an image object and a width/height assignment
    """
    def __init__(self, width, height, groups=[]):
        # Call the parent class (Sprite) constructor which takes no arguments
        Sprite.__init__(self, groups)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(PLAYER_COLOR)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x
        # and rect.y
        self.rect = self.image.get_rect()


class PlayerGroup(Group):
    pass
