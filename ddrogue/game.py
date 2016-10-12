from collections import OrderedDict
import sys
from textwrap import wrap

import pygame

from .colors import WHITE, GREEN
from .map import Map, create_map_matrix, create_tile
from .menu import fullscreen_menu
from .npc import Goblin
from .event_management import State, end_round

from .mechanics.classes import Fighter
from .mechanics.dice import roll
from .mechanics.skills import SKILL_LIST
from .mechanics.chargen import Character
from .mechanics.races import Human

PLAYER_COLOR = 255, 255, 100

KEYMAP_FILE = './controls.json'


def load_text(screen, text_file):
    text_font = pygame.font.Font(None, 18)
    characters = (screen.get_width() - 10) / 7

    text = ['loaded from: %s' % text_file, '']
    with open(text_file, 'r') as input:
        for l in input.readlines():
            text += wrap(l, characters)
            text += ['']

    image = pygame.surface.Surface((screen.get_width(), len(text) * 15))

    x, y = 0, 0
    for t in text:
        image.blit(text_font.render(t, False, (255, 255, 255)), (x, y))
        y += 15

    x, y = cursor = 5, 5
    bottom = image.get_height() - screen.get_height()
    while 1:
        screen.blit(image, (x, y))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key in [27, 13]:
                break
            if event.key == 273:
                y += 30
                if y >= 0:
                    y = cursor[0]
            if event.key == 274:
                y -= 30
                if y <= - bottom:
                    y = - (bottom + 5)


def settings(screen):
    pass


def guide(screen):
    load_text(screen, './ogc/mechanics.txt')


def legal(screen):
    """ Loads legal text """
    load_text(screen, './ogc/license.txt')


def quit(_):
    sys.exit()


class StatusBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
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


def game_loop(state):
    while not state.quit:
        state.output._print('loaded new frame')

        state.draw()

        # TODO void any kepresses while rendering
        # Wait for the next state
        while not end_round(state):
            pass


def init_state(screen):
    m = Map(create_map_matrix())
    goblin_image = create_tile(GREEN, [m.unit, m.unit])
    goblin = Goblin(goblin_image)
    player_image = create_tile(PLAYER_COLOR, [m.unit, m.unit])
    player = Character(
                 player_image,
                 Human,
                 abilities=(roll('4d6') for x in range(6)),
                 char_class=Fighter,
                 skills={'skill': 1 for skill in SKILL_LIST},
                 features={
                     'active': [],
                     'passive': [],
                     'feats_known': [],
                 },
                 description=None)
    state = State(screen, m, KEYMAP_FILE, player, npcs=[goblin])
    state.player.pos = [state.map.width/2 * state.map.unit,
                        state.map.height/2 * state.map.unit]
    state.npcs[0].pos = [state.player.pos[0] - state.map.unit * 2,
                         state.player.pos[1]]
    state.output = StatusBox(state.map.pixel_width, 100)
    return state


def new_game(screen):
    # Setup the initial game
    state = init_state(screen)

    # Start the game
    game_loop(state)


def main_menu(screen):
    options = OrderedDict()
    options["New Game"] = new_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    fullscreen_menu(screen, options)
