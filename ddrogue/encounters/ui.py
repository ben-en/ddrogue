from time import sleep

import pygame
from pygame.rect import Rect

from ..colors import BLACK, GREY, WHITE, DARK_GREY, RED
from ..constants import SCREEN, FONT
from ..ui import create_tile, navigable_loop, text_to_img, str_bonus


class StatusBox(pygame.sprite.Sprite):
    def __init__(self, state, pos, x, y):
        self.state = state
        self.pos = pos
        self.size = self.width, self.height = x, y
        self.img = pygame.Surface(self.size)
        self.rect = self.img.get_rect()
        self.area_rect = Rect(pos, self.size)
        self.lines = []

    def cr(self, y, incr=20):
        y += incr
        self.img.scroll(0, -incr)
        return 5, y

    # TODO find a better name than _print
    def _print(self, s):
        """ write given string to output box """
        # Put the text into the list of lines for fullscreen status
        self.lines.append(s)
        tmp = pygame.Surface(self.size)
        x = 5
        y = 0

        # Print each character
        for l in s:
            if l == '\n':
                x, y = self.cr(y)
                self.img.blit(tmp, (1, self.height - 20))
                continue
            # Render the character
            render = FONT.render(l, False, WHITE)
            # Blit the character on the temporary surface
            tmp.blit(render, (x, y))
            # Adjust the cursor to the right
            x += 10

            # If the cursor is 5px to the edge of the surface, carriage return
            if (x > self.width - 5):
                x, y = self.cr(y)
                self.img.blit(tmp, (1, self.height - 20))

        x, y = self.cr(y)
        self.img.blit(tmp, (0, self.height - 20))
        # After writing text, carriage return.
        # Set cursor property

    def fullscreen(self):
        # TODO find out why you have to hit esc twice
        SCREEN.fill(BLACK)
        navigable_loop(
            text_to_img(SCREEN.get_width(), self.lines),
            start_pos=-1
        )

    def ask(self, str):
        self._print(str + ' (Y or n)')
        sleep(0.1)
        while 1:
            self.state.draw()
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.KEYUP:
                if not hasattr(event, 'key'):
                    continue
                if event.key == ord('y'):
                    if event.mod == 1:  # TODO add right shift compatibility
                        return True
                    else:
                        self._print("shift and y, to mimize accidents")
                        continue
                if event.key == ord('n'):
                    self._print('aborting')
                    return False
                else:
                    self._print("'n' or 'Y' only")


# HUD
def current_turn(state, player):
    rows = [
        'T:%s' % str(state.turn + 1).rjust(6),
        'P:     %s' % state.active_player,
    ]
    return render_column((60, 40), rows)


def mini_map(state, player):
    # TODO
    pass


def char_hp(state, player):
    """ Should show the HP for the currently selected character """
    # TODO add graphical bar
    total = player.max_hp
    current = player.hp
    img = FONT.render('HP: %s/%s' % (current, total), False, WHITE)
    return img


def char_xp(state, player):
    """ Shows xp """
    next_level = 'na'
    current = player.xp
    img = FONT.render('XP: %s/%s' % (current, next_level), False,
                      WHITE)
    return img


def render_column((x, y), rows, row_height=20):
    img = pygame.Surface([x, y])
    y = 0
    for field in rows:
        img.blit(FONT.render(field, False, WHITE), (0, y))
        y += row_height
    return img


def char_stats(state, player):
    rows = []
    for stat in 'str dex con int wis cha'.split():
        tup = player.stats[stat]
        val = tup[0]
        bonus = str_bonus(tup[1], just=2)
        rows.append('%s: [%s] (%s)' % (stat, str(val).rjust(2), bonus))
    return render_column((120, 120), rows)


def char_defense(state, player):
    p = player
    rows = [
        'AC:    %s' % p.ac,
        'Touch: %s' % p.touch_ac,
        'Flat:  %s' % p.flat_ac
    ]
    return render_column((65, 300), rows)


def char_offense(state, player):
    # TODO fix negative number appearance
    p = player
    rows = [
        'BAB:  %s' % p.bab,
        'CMB:    %s' % p.cmb,
        'CMD:    %s' % p.cmd
    ]
    return render_column((65, 300), rows)


def char_saves(state, player):
    p = player
    rows = [
        'Ref:  %s' % str_bonus(p.ref),
        'Fort: %s' % str_bonus(p.fort),
        'Will: %s' % str_bonus(p.will)
    ]
    return render_column((65, 300), rows)


def char_misc(state, player):
    p = player
    rows = [
        'Init: %s' % str_bonus(p.init),
        'SR:     %s' % p.sr,
        'DR:     %s' % p.dr
    ]
    return render_column((65, 300), rows)


def char_abilities(state, player):
    p = player
    rows = [a.__name__ for a in p.features['active']]
    return render_column((100, 300), rows)


def equipment(state, player):
    """ List equipped items """
    # new body equip setup
    img = pygame.Surface([160, 160])
    equipped = player.equipped.items()
    equip_strs = ['Equipment Slots']
    for slot, index in equipped:
        if index == -1:
            equip_strs.append(': '.join([slot, "unequipped"]))
            continue
        equip_strs.append(': '.join([slot, player.equipment[index].s]))
    y = 0
    for s in equip_strs:
        img.blit(FONT.render(s, False, WHITE), (0, y))
        y += 12
    return img


def turn_ui(state, player):
    p = player
    rows = [
        'Available actions',
        'Move action:     %s' % bool(p.move_action),
        'Standard Action: %s' % bool(p.standard_action),
        'Swift Action:    %s' % bool(p.swift_action),
        'Has moved:       %s' % bool(p.moved),
    ]
    first_column = render_column((200, 100), rows)
    # Show initiative order because actors is sorted
    rows = ['Initiative order']
    rows += ['%s:\t%s' % (i + 1, state.actors[i].s)
             for i in range(len(state.actors))]
    second_column = render_column((120, 100), rows)
    tmp = pygame.Surface([360, 100])
    tmp.blit(first_column, (0, 0))
    tmp.blit(second_column, (200, 0))
    return tmp


def end_turn_func(state, *args):
    if (state.char.standard_action or state.char.move_action or
            state.char.swift_action):
        state._print('%s still has actions available.' % state.char.s)
        if state.output.ask('Are you sure you want to end the turn?'):
            return state.end_turn()


def end_turn(_, x):
    img = pygame.Surface((400, 40))
    img.fill(DARK_GREY)
    img.blit(FONT.render('End Player Turn', False, RED), (100, 10))
    return img


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
    def __init__(self, state, players, pos, x, y):
        self.state = state
        self.players = players
        self.selected_player = 0
        self.pos = pos
        self.size = self.width, self.height = x, y
        self.element_width = x - 6
        self.img = create_tile(BLACK, [x, y])
        self.rect = self.img.get_rect()
        self.area_rect = Rect(pos, self.size)

        self.header = [FONT.render('Party: ', False, WHITE)]
        self.header += [p.img for p in players]

        self.elements = (
            (current_turn, (335, 5)),
            (
                lambda state, player:
                FONT.render('%s the level %s %s %s' % (
                                     player.s,
                                     sum([l for c, l in player.clevel]),
                                     player.race.s,
                                     '/'.join([c.s for c, l in player.clevel])
                                 ), False, WHITE),
                (60, 45)
            ),
            (char_xp, (10, 65)),
            (char_hp, (10, 85)),
            (char_stats, (20, 110)),
            (char_defense, (200, 110)),
            (char_offense, (200, 170)),
            (char_saves, (310, 110)),
            (char_misc, (310, 170)),
            (equipment, (20, 280)),
            # TODO finish mini map
            # (mini_map, (5, 300)),
            (turn_ui, (20, 460)),
            (end_turn, (0, self.height - 40)),
        )
        self.selected_element = -1
        self.update()
        self.element_areas = [
            Rect((p[0] + pos[0], p[1] + pos[1]), e.get_size()) for e, p in
            self.compiled
        ]
        self.element_functions = {
            11: end_turn_func
        }

    def update(self):
        self.img = create_tile(BLACK, [self.width, self.height])
        x, y = 5, 5
        for icon in self.header:
            self.img.blit(icon, (x, y))
            if self.header.index(icon) == self.selected_player + 1:
                pygame.draw.rect(
                    self.img,
                    WHITE,
                    pygame.rect.Rect((x, y), icon.get_size()),
                    5
                )
            x += icon.get_width() + 5
        self.compiled = []
        for e, pos in self.elements:
            img = e(self.state, self.players[self.selected_player])
            self.img.blit(img, pos)
            self.compiled.append((img, pos))
        if self.selected_element >= 0:
            pygame.draw.rect(
                self.img, WHITE, self.element_areas[self.selected_element], 5
            )

    def adjust_selected_player(self, val):
        self.selected_player += val
        # TODO find method that only steps in the list and
        # automatically resets if out of range
        if self.selected_player < 0:
            self.selected_player = len(self.players) - 1
        elif self.selected_player == len(self.players):
            self.selected_player = 0
