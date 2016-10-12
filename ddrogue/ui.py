import pygame

from .colors import WHITE, GREEN
from .map import create_tile


class HUD(pygame.sprite.Sprite):
    """
    Ideals:
        character stats
        equipped weapons
        map
        tabbed interface containing inventory, spells, abilities, etc
        actions
    """
    def __init__(self, pos, x, y):
        self.pos = pos
        self.width = x
        self.height = y
        self.image = create_tile(GREEN, [x, y])
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 12)


class StatusBox(pygame.sprite.Sprite):
    def __init__(self, pos, x, y):
        self.pos = pos
        self.width = x
        self.height = y
        self.image = create_tile(WHITE, [x, y])
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 12)

        self.cursor = (5, 5)

    def _print(self, s):
        tmp = pygame.display.get_surface()
        x, y = self.cursor

        for l in s:
            render = self.font.render(l, False, (0, 0, 0))
            tmp.blit(render, (x, y))
            self.image.blit(render, (x, y))
            x += 10

            if (x > self.image.get_width()-5):
                x = self.rect.left+5
                y += 10
        x = 5
        y += 10  # CR
        self.cursor = (x, y)
