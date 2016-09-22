import pygame
from pygame.sprite import Sprite, Group


BLACK = 0, 0, 0


class Player(object):
    """
    Creates a player sprite and group, and attaches them to itself.
    """
    def __init__(self):
        self.width = self.height = 32
        self.group = PlayerGroup()
        self.sprite = PlayerSprite(self.width, self.height,
                                   groups=[self.group])
        self.rect = self.sprite.rect
        self.image = self.sprite.image


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
        self.image.fill(BLACK)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x
        # and rect.y
        self.rect = self.image.get_rect()


class PlayerGroup(Group):
    pass
