from time import sleep

import pygame
from pygame.rect import Rect

from ..colors import BLACK, GREY, WHITE, LIGHT_BLUE, DARK_GREY, RED
from ..ui import create_tile, navigable_loop, text_to_img, str_bonus


def grid_select(state, target, steps, end_pos_func=None, COLOR=LIGHT_BLUE):
    x, y = target.pos
    speed = steps
    speed_offset = speed/2 + (1 if (speed % 2) else 0)
    pos_list = []
    rect_list = []
    for i in range(speed + 1):
        for n in range(speed + 1):
            p = ((x + i - speed_offset), (y + n - speed_offset))
            pos_list.append(p)
            pixel_p = tuple(axis * state.map.unit for axis in p)
            rect_list.append(Rect(pixel_p, state.map.unit_t))
    state.draw()
    end_pos_found = False
    for i in range(len(pos_list)):
        p = pos_list[i]
        r = rect_list[i]
        if end_pos_func:
            if end_pos_func(p):
                pygame.draw.rect(state.screen, COLOR, r, 1)
                end_pos_found = True
        else:
            pygame.draw.rect(state.screen, COLOR, r, 1)
    pygame.display.flip()
    if end_pos_func and not end_pos_found:
        state._print('End position not found, cannot perform action')
        return
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == 27:  # esc
                return None
        if event.type == pygame.MOUSEBUTTONUP:
            r = Rect(event.pos, (1, 1))
            index = r.collidelist(rect_list)
            if not index == -1:
                return state.map.grid_pos(event.pos)


def mini_map(state):
    # TODO
    pass


def char_hp(player, font):
    """ Should show the HP for the currently selected character """
    # TODO add graphical bar
    total = player.max_hp
    current = player.hp
    img = font.render('HP: %s/%s' % (current, total), False, WHITE)
    return img


def char_xp(player, font):
    """ Shows xp """
    next_level = 'na'
    current = player.xp
    img = font.render('XP: %s/%s' % (current, next_level), False,
                      WHITE)
    return img


def render_column(font, (x, y), rows, row_height=20):
    img = pygame.Surface([x, y])
    y = 0
    for field in rows:
        img.blit(font.render(field, False, WHITE), (0, y))
        y += row_height
    return img


def char_stats(player, font):
    rows = []
    for stat in 'str dex con int wis cha'.split():
        tup = player.stats[stat]
        val = tup[0]
        bonus = str_bonus(tup[1], just=2)
        rows.append('%s: [%s] (%s)' % (stat, str(val).rjust(2), bonus))
    return render_column(font, (120, 120), rows)


def char_defense(player, font):
    p = player
    rows = [
        'AC:    %s' % p.ac,
        'Touch: %s' % p.touch_ac,
        'Flat:  %s' % p.flat_ac
    ]
    return render_column(font, (65, 300), rows)


def char_offense(player, font):
    # TODO fix negative number appearance
    p = player
    rows = [
        'BAB:  %s' % p.bab,
        'CMB:    %s' % p.cmb,
        'CMD:    %s' % p.cmd
    ]
    return render_column(font, (65, 300), rows)


def char_saves(player, font):
    p = player
    rows = [
        'Ref:  %s' % str_bonus(p.ref),
        'Fort: %s' % str_bonus(p.fort),
        'Will: %s' % str_bonus(p.will)
    ]
    return render_column(font, (65, 300), rows)


def char_misc(player, font):
    p = player
    rows = [
        'Init: %s' % str_bonus(p.init),
        'SR:     %s' % p.sr,
        'DR:     %s' % p.dr
    ]
    return render_column(font, (65, 300), rows)


def char_abilities(player, font):
    p = player
    rows = [a.__name__ for a in p.features['active']]
    return render_column(font, (100, 300), rows)


def equipment(player, font):
    """ List equipped items """
    # new body equip setup
    img = pygame.Surface([200, 200])
    equipped = player.equipped.items()
    equip_strs = []
    for slot, index in equipped:
        if index == -1:
            equip_strs.append(': '.join([slot, "unequipped"]))
            continue
        equip_strs.append(': '.join([slot, player.equipment[index].s]))
    y = 0
    for s in equip_strs:
        img.blit(font.render(s, False, WHITE), (0, y))
        y += 12
    return img


def end_turn(_, font):
    img = pygame.Surface((400, 40))
    img.fill(DARK_GREY)
    img.blit(font.render('End Player Turn', False, RED), (100, 10))
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
    def __init__(self, state, players, font, pos, x, y):
        self.state = state
        self.players = players
        self.selected_player = 0
        self.pos = pos
        self.width = x
        self.element_width = x - 6
        self.height = y
        self.img = create_tile(BLACK, [x, y])
        self.rect = self.img.get_rect()
        # TODO find a decent standard font
        self.font = font

        self.header = [font.render('Party: ', False, WHITE)]
        self.header += [p.img for p in players]

        self.elements = [
            (
                lambda player, font:
                font.render('%s the level %s %s %s' % (
                                     player.s,
                                     sum([l for c, l in player.clevel]),
                                     player.race.s,
                                     '/'.join([c.s for c, l in player.clevel])
                                 ), False, WHITE),
                (5, 40)
            ),
            (char_xp, (285, 40)),
            (char_hp, (5, 62)),
            (char_stats, (5, 90)),
            (char_defense, (215, 90)),
            (char_offense, (215, 150)),
            (char_saves, (315, 90)),
            (char_misc, (315, 150)),
            (char_abilities, (5, 230)),
            (equipment, (5, 530)),
            # TODO finish mini map
            # (mini_map, (5, 300)),
            # (lambda x, y: create_tile(GREY, (389, 389)), (5, 500)),
            (end_turn, (0, self.height - 40)),
        ]
        self.selected_element = -1
        self.update()
        self.element_areas = [
            Rect(p, e.get_size()) for e, p in self.compiled
        ]

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
            img = e(self.players[self.selected_player], self.font)
            self.img.blit(img, pos)
            self.compiled.append((img, pos))
        if self.selected_element >= 0:
            pygame.draw.rect(
                self.img, WHITE, self.element_areas[self.selected_element], 5
            )

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for index in range(len(self.elements)):
                if self.element_areas[index].collidepoint(event.pos):
                    self.selected_element = index
                    func = self.element_functions.get(index, None)
                    if func:
                        func(event)
                    continue
            return
        elif event.type == pygame.KEYUP:
            if event.key == 275:
                self.adjust_selected_player(1)
            if event.key == 276:
                self.adjust_selected_player(-1)
            self.update()
            return
        return event

    def adjust_selected_player(self, val):
        self.selected_player += val
        # TODO find method that only steps in the list and
        # automatically resets if out of range
        if self.selected_player < 0:
            self.selected_player = len(self.players) - 1
        elif self.selected_player == len(self.players):
            self.selected_player = 0
        self.update()


class StatusBox(pygame.sprite.Sprite):
    def __init__(self, state, screen, font, pos, x, y):
        self.state = state
        self.screen = screen
        self.pos = pos
        self.size = self.width, self.height = x, y
        self.img = pygame.Surface(self.size)
        self.rect = self.img.get_rect()
        self.font = font
        self.lines = []

    def update(self):
        pygame.draw.rect(self.img, GREY,
                         pygame.rect.Rect((0, 0), (self.width + 20,
                                                   self.height + 20)), 1)

    def cr(self, y, incr=20):
        y += incr
        self.img.scroll(0, -incr)
        return 5, y

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
            render = self.font.render(l, False, WHITE)
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
        self.update()
        # After writing text, carriage return.
        # Set cursor property

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.fullscreen()
        elif event.type == pygame.KEYUP:
            if event.key in [ord(c) for c in '\n ']:
                self.fullscreen()

    def fullscreen(self):
        # TODO find out why you have to hit esc twice
        self.screen.fill(BLACK)
        navigable_loop(
            self.screen,
            text_to_img(self.screen.get_width(), self.lines),
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
                    if event.mod == 1:
                        return True
                    else:
                        self._print("shift and y, to mimize accidents")
                        continue
                if event.key == ord('n'):
                    return False
                else:
                    self._print("'n' or 'Y' only")
