from textwrap import wrap

import pygame
from pygame.rect import Rect
from pygame.transform import scale, chop

from .colors import BLACK, GREY
from .map import create_tile


def render_text(screen, text_file):
    """ Render the text file on the screen in a readable format """
    # Initialize the font
    text_font = pygame.font.Font(None, 18)
    # Calculate the number of characters that can be shown on one row
    characters = (screen.get_width() - 10) / 7

    # Add a header that shows the path of the text file so the user can look it
    # up for manual inspection at their discretion
    text = ['loaded from: %s' % text_file, '']
    # Open and read the text file into a list of rows
    with open(text_file, 'r') as input:
        for l in input.readlines():
            text += wrap(l, characters)
            # Add an extra space to clearly show a new line in the file
            text += ['']

    # Create an image the size of the text
    image = pygame.surface.Surface((screen.get_width(), len(text) * 15))

    # Write the text onto the image
    x, y = 0, 0
    for t in text:
        image.blit(text_font.render(t, False, (255, 255, 255)), (x, y))
        y += 15

    navigable_loop(screen, image)


def navigable_loop(screen, image):
    # Disply the image
    x, y = 5, 5
    bottom = image.get_height() - screen.get_height()
    while 1:
        screen.blit(image, (x, y))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            # Esc key or ??
            # TODO figure out keycode 13
            if event.key in [27, 13]:
                break
            # Arrow keys
            if event.key == 273:
                y += 30
                if y >= 0:
                    # If you're trying to scroll too high, reset to 0
                    y = 0
            if event.key == 274:
                y -= 30
                if y <= - bottom:
                    # If you're trying to scroll to low, reset to bottom
                    y = - bottom


class CharBox(object):
    def __init__(self, state):
        lambda x: create_tile(GREY, (390, 400))


def mini_map(state):
    #TODO
    pass


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
    full_image = create_tile(BLACK, [state.hud.width, 30])
    full_image.blit(state.font.render(top, False, (255, 255, 255)), (0, 0))
    full_image.blit(state.font.render(mid, False, (255, 255, 255)), (0, 10))
    full_image.blit(state.font.render(bot, False, (255, 255, 255)), (0, 20))
    return full_image


def equipment(state):
    item = state.player.equipment[state.player.equipped]
    image = state.font.render('Weapon: %s' % item.name, False, (255, 255, 255))
    return image


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
        # TODO find a decent standard font
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
            # TODO finish mini map
            # (mini_map, (5, 300)),
            (lambda x: create_tile(GREY, (389, 389)), (5, 500)),
        ]

    def update(self):
        self.image = create_tile(BLACK, [self.width, self.height])
        for e in self.elements:
            img = e[0](self._state)
            print(e[1])
            self.image.blit(img, e[1])


class StatusBox(pygame.sprite.Sprite):
    # TODO on click, run navigable_loop on statusbox image starting at bottom
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
