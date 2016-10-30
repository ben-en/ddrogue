import pygame
from pygame.rect import Rect

from ..colors import WHITE, BLUE, GREY
from ..game import FONT_NAME, FONT_SIZE
from ..ui import menu, str_bonus, create_tile, multi_panel_ui
from .classes import CLASS_LIST, Fighter, Wizard
from .dice import roll
from .feats import FEAT_LIST
from .skills import SKILL_LIST
from .stats import stat_bonus
from .races import RACE_LIST, Human


# active features should probably activate using similar mechanisms to casting
# a spell.
# passive features should apply at object creation, directly to the character
# object. Perhaps characters should maintain a list of effects that affect them
# each phase or turn
blank_char_info = {
    'img': create_tile(BLUE, (16, 16)),
    'race': Human,
    'char_levels': ((Fighter, 5), (Wizard, 5)),
    'abilities': (roll('3d6') for x in range(6)),
    'skill_ranks': {'skill': 0 for skill in SKILL_LIST},
    'features': {
            # All the abilities that would be gained from the class, processed
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
    'name': 'foo',
    'description': None,
    'gold': 0,
    'equipment': Human.natural_weapons,  # Should be all of the racial weapons
    'equipped': {
        'head': -1,
        'cloak': -1,
        'torso': -1,
        'l_arm': -1,
        'r_arm': -1,
        'l_hand': -1,
        'r_hand': -1,
        'legs': -1,
        'feet': -1,
    },
    'xp': 0,
    'hp': 29
}


def chargen(screen):
    """ Go through chargen steps and create level 1 character """
    name, attributes, race, cclass = first_step(screen)
    print(name, attributes, race, cclass)
    feat_list = [r.s for r in FEAT_LIST]
    print('stats', attributes)
    print('race', race)
    print('cclass', cclass)
    # print('skills', skill_ranks)
    # print('feats', feats)


def first_step(screen):
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    race_list = [r.s for r in RACE_LIST]
    race_list += 'Elf Orc Dwarf Gnome'.split()
    class_list = [r.s for r in CLASS_LIST]
    panels = [
        NamePanel(font, (10, 10), (400, 40)),
        AttributeRoller(font, (10, 60)),
        SelectPanel(race_list, (150, 60), (140, 400), font=font),
        SelectPanel(class_list, (300, 60), (140, 400), font=font),
    ]
    return multi_panel_ui(screen, panels)


class NamePanel(object):
    def __init__(self, font, pos, xy):
        self.font = font or pygame.font.Font(None, 24)
        self.pos = pos
        self.xy = xy
        self.name = ''
        self.draw_img()
        self.desc = ('The name for your character; alpha characters and spaces'
                     'only.')

    def draw_img(self):
        txt_img = self.font.render('Name: ' + self.name, False, WHITE)
        self.img = pygame.surface.Surface(self.xy)
        self.img.blit(txt_img, (10, 10))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            print(event)
            if event.key == 8:
                self.name = self.name[:-1]
            elif hasattr(event, 'unicode'):
                self.name += event.unicode
            self.draw_img()

    def resolve(self):
        return self.name


class AttributeRoller(object):
    """ Allow swapping values and rerolling """
    def __init__(self, font, xy):
        self.pos = xy
        self.xy = (120, 110)
        self.font = font
        self.roll()

    def roll(self):
        rows = []
        self.stats = []
        for stat in 'str dex con int wis cha'.split():
            val = roll('3d6')
            bonus = str_bonus(stat_bonus(val), just=2)
            rows.append('%s: [%s] (%s)' % (stat, str(val).rjust(2), bonus))
            self.stats.append(val)

        self.img = pygame.surface.Surface(self.xy)
        x, y = 10, 10
        for t in rows:
            self.img.blit(self.font.render(t, False, (255, 255, 255)), (x, y))
            y += 15

    def event_handler(self, event):
        if event.type == pygame.KEYUP:
            if event.key == 114:  # r
                self.roll()

    def resolve(self):
        return self.stats


class SelectPanel(object):
    def __init__(self, options, pos, xy, font=None, text_color=WHITE,
                 select_color=BLUE):
        self.font = font or pygame.font.Font(None, 24)
        self.xy = xy
        self.pos = pos
        # Create a blank surface to draw the menu on
        self.menu_img = pygame.surface.Surface(self.xy)
        # Create imgs for each option provided
        imgs = [self.font.render(x, False, text_color) for x in options]
        cursor_start = (10, 10)
        self.selected = 0
        self.hovered = 0
        self.positions = []  # Empty list to hold rects of the imgs
        self.highlight_positions = []  # Empty list to hold highlight rect
        x, y = cursor_start
        # Get img positions and blit options onto menu
        for i in imgs:
            size = i.get_size()
            size = (size[0] + 10, size[1] + 4)
            self.highlight_positions.append(Rect(
                (x - 5, y - 2), size)
            )
            self.positions.append(Rect((pos[0] + x, pos[1] + y), size))
            self.menu_img.blit(i, (x, y))
            y += 20
        self.draw_img()

    def draw_img(self):
        self.img = pygame.surface.Surface(self.xy)
        self.img.blit(self.menu_img, (0, 0))
        pygame.draw.rect(self.img, GREY,
                         self.highlight_positions[self.hovered], 1)
        pygame.draw.rect(self.img, BLUE,
                         self.highlight_positions[self.selected], 2)

    def event_handler(self, event):
        if event.type in [pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            found = False
            for i in self.positions:
                if i.collidepoint(event.pos):
                    index = self.positions.index(i)
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.selected = index
                    else:
                        self.hovered = index
                    found = True
            self.draw_img()
            if not found:
                self.hovered = self.selected
        elif event.type == pygame.KEYUP:
            if event.key == 273:  # up
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.positions) - 1
            elif event.key == 274:  # down
                self.selected += 1
                if self.selected >= len(self.positions):
                    self.selected = 0
            self.hovered = self.selected
            self.draw_img()

    def resolve(self):
        return self.options[self.selected]


def multi_select(screen, l, count):
    selected = []
    while len(selected) < count:
        index = menu(screen, l)
        selected.append(l.pop(index))
    return selected


def old_feat_select(screen):
    f_names = [f.s for f in FEAT_LIST]
    picked = multi_select(screen, f_names, 2)
    return picked
