import pygame

from ..colors import BLACK, GREY, WHITE

from ..ui import create_tile, navigable_loop, text_to_img, str_bonus


def mini_map(state):
    # TODO
    pass


def char_hp(player, font):
    """ Should show the HP for the currently selected character """
    # TODO add graphical bar
    total = player.max_hp
    current = player.hp
    img = font.render('HP: %s/%s' % (current, total), False, (255, 255, 255))
    return img


def char_xp(player, font):
    """ Shows xp """
    next_level = 'na'
    current = player.xp
    img = font.render('XP: %s/%s' % (current, next_level), False,
                      (255, 255, 255))
    return img


def render_column(font, (x, y), rows, row_height=20):
    img = pygame.Surface([x, y])
    y = 0
    for field in rows:
        img.blit(font.render(field, False, (255, 255, 255)), (0, y))
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
        img.blit(font.render(s, False, (255, 255, 255)), (0, y))
        y += 12
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
    def __init__(self, players, font, pos, x, y):
        self.players = players
        self.selected = 0
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
                                     player.name,
                                     sum([l for c, l in player.clevel]),
                                     player.race.s,
                                     '/'.join([c.s for c, l in player.clevel])
                                 ), False, (255, 255, 255)),
                (5, 40)
            ),
            (char_xp, (285, 40)),
            (char_hp, (5, 62)),
            (char_stats, (5, 90)),
            (char_defense, (215, 90)),
            (char_offense, (215, 150)),
            (char_saves, (315, 90)),
            (char_misc, (315, 150)),
            (equipment, (5, 230)),
            # TODO finish mini map
            # (mini_map, (5, 300)),
            (lambda x, y: create_tile(GREY, (389, 389)), (5, 500)),
        ]
        self.update()

    def update(self):
        self.img = create_tile(BLACK, [self.width, self.height])
        x, y = 5, 5
        for icon in self.header:
            self.img.blit(icon, (x, y))
            x += icon.get_width() + 5
        for e in self.elements:
            img = e[0](self.players[self.selected], self.font)
            self.img.blit(img, e[1])

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            print('clicked on the hud', event.pos)


class StatusBox(pygame.sprite.Sprite):
    # TODO on click, run navigable_loop on statusbox img starting at bottom
    # TODO scroll as output is displayed
    def __init__(self, screen, font, pos, x, y):
        self.screen = screen
        self.pos = pos
        self.width = x
        self.height = y
        self.img = create_tile(BLACK, [x, y])
        self.rect = self.img.get_rect()
        self.font = font
        self.lines = []

        self.cursor = (5, 5)

    def update(self):
        pass

    def _print(self, s):
        self.lines.append(s)
        tmp = pygame.display.get_surface()
        x, y = self.cursor

        for l in s:
            render = self.font.render(l, False, (255, 255, 255))
            tmp.blit(render, (x, y))
            self.img.blit(render, (x, y))
            x += 10

            if (x > self.width - 5):
                x = self.rect.left+5
                if (y > self.height - 5):
                    self.img.scroll(0, 10)
                    y -= 10
                else:
                    y += 10
        x = 5
        y += 10  # CR
        self.cursor = (x, y)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.fullscreen()
        elif event.type == pygame.KEYUP:
            if event.key == 32:  # TODO space
                self.fullscreen()

    def fullscreen(self):
        # TODO find out why you have to hit esc twice
        self.screen.fill(BLACK)
        navigable_loop(
            self.screen,
            text_to_img(self.screen.get_width(), self.lines),
            start_pos=-1
        )
