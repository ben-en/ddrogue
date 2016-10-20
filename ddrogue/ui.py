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


def char_xp(state):
    """ Shows xp """
    next_level = 'na'
    current = state.player.xp
    image = state.font.render('XP: %s/%s' % (current, next_level), False,
                              (255, 255, 255))
    return image


def render_column(font, (x, y), rows, row_height=20):
    img = pygame.Surface([x, y])
    y = 0
    for field in rows:
        img.blit(font.render(field, False, (255, 255, 255)), (0, y))
        y += row_height
    return img


def str_bonus(val, just=3):
    """ Returns a justified stringed bonus. eg '3' returns ' +3' by default """
    if val >= 0:
        bonus = '+%s' % val
    else:
        bonus = str(val)
    return bonus.rjust(just)


def char_stats(state):
    rows = []
    for stat in 'str dex con int wis cha'.split():
        tup = state.player.stats[stat]
        val = tup[0]
        bonus = str_bonus(tup[1], just=2)
        rows.append('%s: [%s] (%s)' % (stat, str(val).rjust(2), bonus))
    return render_column(state.font, (120, 120), rows)


def char_defense(state):
    p = state.player
    rows = [
        'AC:    %s' % p.ac,
        'Touch: %s' % p.touch_ac,
        'Flat:  %s' % p.flat_ac
    ]
    return render_column(state.font, (65, 300), rows)


def char_offense(state):
    p = state.player
    rows = [
        'BAB:  %s' % p.bab,
        'CMB:    %s' % p.cmb,
        'CMD:    %s' % p.cmd
    ]
    return render_column(state.font, (65, 300), rows)


def char_saves(state):
    p = state.player
    rows = [
        'Ref:  %s' % str_bonus(p.ref),
        'Fort: %s' % str_bonus(p.fort),
        'Wis:  %s' % str_bonus(p.wis)
    ]
    return render_column(state.font, (65, 300), rows)


def char_misc(state):
    p = state.player
    rows = [
        'Init: %s' % str_bonus(p.init),
        'SR:     %s' % p.sr,
        'DR:     %s' % p.dr
    ]
    return render_column(state.font, (65, 300), rows)


def equipment(state):
    """ List equipped items """
    image = pygame.Surface([state.hud.element_width, 100])
    weapon = state.player.equipment[state.player.equipped]
    # TODO player armor
    from .mechanics.armor import leather_armor
    armor = leather_armor
    equip_strs = [
        'Weapon: %s' % weapon.name,
        'Armor: %s' % armor.name or 'none',
    ]
    y = 0
    for s in equip_strs:
        image.blit(state.font.render(s, False, (255, 255, 255)), (0, y))
        y += 12
    return image


class HUD(pygame.sprite.Sprite):
    """
    Ideals:
        equipped weapons
        map
        tabbed interface containing inventory, spells, abilities, etc
        actions


    TODOs:
        Spell resistance
        speed
        damage resistance
        action status (used actions, move points, etc)
        initiative (roll, bonus?)
    """
    def __init__(self, state, pos, x, y):
        self._state = state
        self.pos = pos
        self.width = x
        self.element_width = x - 6
        self.height = y
        self.image = create_tile(BLACK, [x, y])
        self.rect = self.image.get_rect()
        # TODO find a decent standard font
        self.font = state.font

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
            (char_xp, (285, 5)),
            (char_hp, (5, 32)),
            (char_stats, (5, 60)),
            (char_defense, (215, 60)),
            (char_offense, (215, 120)),
            (char_saves, (315, 60)),
            (char_misc, (315, 120)),
            (equipment, (5, 200)),
            # TODO finish mini map
            # (mini_map, (5, 300)),
            (lambda x: create_tile(GREY, (389, 389)), (5, 500)),
        ]

    def update(self):
        self.image = create_tile(BLACK, [self.width, self.height])
        for e in self.elements:
            img = e[0](self._state)
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
