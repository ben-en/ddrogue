import pygame
from pygame.rect import Rect
from pygame.transform import scale, chop

from .colors import BLACK, GREY
from .map import create_tile


class CharBox(object):
    def __init__(self, state):
        lambda x: create_tile(GREY, (390, 400))


def mini_map(state):
    """
    Scale the map to the width of the HUD, then chop off anything but the
    center 190 pixels
    """
    return chop(scale(state.map.image, (389, 389)), Rect((5, 150), (390, 190)))


class HUD(pygame.sprite.Sprite):
    """
    Ideals:
        character stats
        equipped weapons
        map
        tabbed interface containing inventory, spells, abilities, etc
        actions
    """
    def __init__(self, state, pos, x, y):
        self._state = state
        self.pos = pos
        self.width = x
        self.height = y
        self.image = create_tile(BLACK, [x, y])
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 18)

        self.elements = [
            (lambda x: self.font.render(
                '%s the level %s %s' % (x.player.name, x.player.level,
                                        x.player.cclass.name),
                False, (255, 255, 255)),
             (5, 5)),
            (mini_map, (5, 300)),
            (lambda x: create_tile(GREY, (389, 389)), (5, 500)),
        ]
        self.update()

    def update(self):
        self.image = create_tile(BLACK, [self.width, self.height])
        for e in self.elements:
            img = e[0](self._state)
            self.image.blit(img, e[1])


class StatusBox(pygame.sprite.Sprite):
    # TODO scroll as output is displayed
    def __init__(self, pos, x, y):
        self.pos = pos
        self.width = x
        self.height = y
        self.image = create_tile(BLACK, [x, y])
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 12)

        self.cursor = (5, 5)

    def _print(self, s):
        tmp = pygame.display.get_surface()
        x, y = self.cursor

        for l in s:
            render = self.font.render(l, False, (255, 255, 255))
            tmp.blit(render, (x, y))
            self.image.blit(render, (x, y))
            x += 10

            if (x > self.image.get_width()-5):
                x = self.rect.left+5
                y += 10
        x = 5
        y += 10  # CR
        self.cursor = (x, y)
