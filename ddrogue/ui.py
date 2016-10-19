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


def char_hp(state):
    """ Should show the HP for the currently selected character """
    # TODO add graphical bar
    total = state.player.max_hp
    current = state.player.hp
    image = state.font.render('HP: %s/%s' % (current, total), False,
                              (255, 255, 255))
    return image


def char_saves(state):
    p = state.player
    top = 'AC: %s\tTouch: %s\tFlat: %s' % (p.ac, p.touch_ac, p.flat_ac)
    mid = 'BAB: %s\tCMB: %s\tCMD: %s' % (p.bab, p.cmb, p.cmd)
    bot = 'Ref: %s\tFort: %s\tWis: %s' % (p.ref, p.fort, p.wis)
    full_image = create_tile(BLACK, [30, state.hud.width])
    full_image.blit(state.font.render(top, False, (255, 255, 255)), (0, 0))
    full_image.blit(state.font.render(mid, False, (255, 255, 255)), (10, 0))
    full_image.blit(state.font.render(bot, False, (255, 255, 255)), (20, 0))
    return full_image


def equipment(state):
    return state.font.render(state.player.equipped, False, (255, 255, 255))


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
            (
                lambda x:
                self.font.render('%s the level %s %s %s' % (
                                     x.player.name,
                                     x.player.level,
                                     x.player.race.name,
                                     x.player.cclass.name
                                 ), False, (255, 255, 255)),
                (5, 5)
            ),
            (char_saves, (5, 20)),
            (equipment, (5, 50)),
            (mini_map, (5, 300)),
            (lambda x: create_tile(GREY, (389, 389)), (5, 500)),
        ]

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

    def update(self):
        pass

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
