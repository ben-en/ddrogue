from collections import OrderedDict
import json
import shelve
from time import sleep
import re
import random

import pygame
from pygame.rect import Rect

from ..colors import BLACK
from ..pathfinding import astar
from ..ui import menu


FONT_NAME = 'ubuntumono'
FONT_SIZE = 14

MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")

UI_SIZE = 400

ACTIONS = {}
SAVE_DIR = './saves'


def save_game(state, filename=None):
    """ write game to file """
    if not filename:
        filename = state.char.name + '.save'
    f = shelve.open(SAVE_DIR + filename, 'n')
    f['foo'] = 'saves aren\'t functional yet'
    f.close


def action(func):
    ACTIONS[func.__name__] = func
    return func


@action
def quit(state, event):
    """ Tell the state to exit after user dialog """
    save_game(state)
    # TODO user dialog
    options = OrderedDict()
    options['Yes'] = lambda x: True
    options['No'] = lambda x: False
    if menu(pygame.display.get_surface(), options):
        return 'quit'


@action
def debug(state, event):
    """ drop into ipdb to debug an unknown event. """
    print('Entered debug')
    print('nothing here')


# TODO assign keys to spell, ability, and char info
@action
def spell(state, event):
    """
    offer a list of abilities to activate
    """
    ability_list = state.char.features['spells'].keys()
    index = menu(pygame.display.get_surface(), ability_list)
    import ipdb
    ipdb.set_trace()
    res = state.char.features['spells'][ability_list[index]]()
    return res


@action
def ability(state, event):
    """
    offer a list of abilities to activate
    """
    ability_list = state.char.features['active'].keys()
    index = menu(pygame.display.get_surface(), ability_list)
    import ipdb
    ipdb.set_trace()
    res = state.char.features['active'][ability_list[index]]()
    return res


@action
def char_info(state, event):
    """
    display a character sheet loke view
    """
    print('not implemented')


@action
def move_down(state, event):
    """ Move the player down by adding one unit to its y value.
    """
    state.char.pos = (state.char.pos[0], state.char.pos[1] + 1)
    return 'done'


@action
def move_up(state, event):
    """ Move the player up by subracting one unit from its y value.
    """
    state.char.pos = (state.char.pos[0], state.char.pos[1] - 1)
    return 'done'


@action
def move_left(state, event):
    """ Move the player left by subracting one unit from its x value.
    """
    state.char.pos = (state.char.pos[0] - 1, state.char.pos[1])
    return 'done'


@action
def move_right(state, event):
    """ Move the player right by adding one unit to its x value.
    """
    state.char.pos = (state.char.pos[0] + 1, state.char.pos[1])
    return 'done'


def move_to(state, char, pos, steps=None):
    """
    Using state's access to the map, move given `char` to `pos`, max `steps`
    """
    state._print('character trying to move from %s to %s' % (tuple(char.pos),
                                                             tuple(pos)))
    path = astar(state.map.floor.transpose(), tuple(char.pos), tuple(pos))
    # For some reason astar figures the path backwards. Dunno why,
    path.reverse()
    if steps:
        path = path[:steps]
    state._print(', '.join([str(p) for p in path]))
    for step in path:
        char.pos = step
        state._print(str(char.pos))
        state._print(str(state.char.pos))
        state.draw()
        sleep(0.1)


def process_key_press(state, event):
    # print('Key pressed', event.key)
    try:
        func = state.keymap[event.key]
    except KeyError:
        print('Unknown key')
        print(event.key, event.unicode)
        return
    res = func(state, event)
    return res
    # print('function executed', func.__name__)


def process_click(state, event):
    move_to(state, state.char, state.map.grid_pos(event.pos))
    return 'done'


EVENT_MAP = {
    pygame.QUIT: quit,
    pygame.KEYDOWN: process_key_press,
    pygame.KEYUP: lambda x, y: None,
    pygame.MOUSEBUTTONUP: process_click,
}


def player_turn(state, event):
    """
    Wait for an event, try to execute a command and return True to quit.
    """
    # Wait for an event
    func = EVENT_MAP[event.type]
    return func(state, event)


def ai_turn(state):
    """ Do something with a given npc """
    npc = state.char
    move_to(state, state.char, random.choice(state.players).pos,
            steps=npc.speed)


def load_keymap(file_path):
    """
    Loads a json file from the file path then tries to match all provided
    key mappings to known functions
    """
    skel = {}
    with open(file_path, 'r') as json_file:
        for key, value in json.load(json_file).items():
                # JSON requires key names to be strings
                key = int(key)
                print(key, value)
                skel[key] = ACTIONS[value.lower()]
    return skel


# TODO: State should duplicate itself and store its history somewhere whenever
# something changes, without events having to do something themselves.
class EncounterState:
    def __init__(self, players, npcs, m, output, hud, keymap_file):
        """
        Keeps track of turns and object state in an encounter
        """
        # TODO font should be global
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        # screen might do well as a global too
        self.screen = pygame.display.get_surface()

        self.output = output
        # Assign _print method to self for easy access
        self._print = self.output._print
        self.hud = hud
        self.map = m
        self.ui = [self.output, self.hud, self.map]
        self.keymap = load_keymap(keymap_file)
        self.panel_areas = [Rect(e.pos, e.img.get_size()) for e in self.ui]
        self.selected_element = 0

        self.players = players
        self.npcs = npcs
        self.actors = players + npcs
        self.active_player = 0
        self.turn = 0

        self.quit = 0

    @property
    def char(self):
        return self.actors[self.active_player]

    def draw(self):
        self.screen.fill(BLACK)
        # Draw the panels on the screen
        for e in self.ui:
            e.update()
            self._print(str(e.__class__) + str(e.pos))
            self.screen.blit(e.img, e.pos)
        pygame.display.flip()

    def interact_until_action(self):
        """
        Interact with the user (help dialogs etc) until a character acction
        occurs.
        """
        while 1:
            # Draw the frame
            self.draw()
            # Wait for an event
            event = pygame.event.wait()
            if event.type == pygame.KEYUP:
                print('keycode: ', event.key)
                print('key: ', chr(event.key))
                if event.key == 27:  # esc
                    # break out returning a quit event
                    break
                elif event.key == ord('\t'):
                    # If tab, switch to the next ui element
                    self.selected_element += 1
                    if self.selected_element >= len(self.ui):
                        self.selected_element = 0
                    elif self.selected_element < 0:
                        self.selected_element = len(self.ui) - 1
                    continue
            elif event.type == pygame.QUIT:
                break
            elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                for index in range(len(self.panel_areas)):
                    if self.panel_areas[index].collidepoint(event.pos):
                        area = index
                        self.ui[index].event_handler(event)
                        continue
            self.ui[area].event_handler(event)
        return event

    def next_turn(self):
        self._print('%s\'s turn' % self.char.name)
        if hasattr(self.char, 'ai'):
            ai_turn(self)
        else:
            while 1:
                self.hud.selected = self.hud.players.index(self.char)
                self._print('player loop start')
                event = self.interact_until_action()
                res = player_turn(self, event)
                self._print(res)
                if res == 'quit':
                    self.quit = True
                    break
                elif res == 'done':
                    break
        # End turn
        self.active_player += 1
        if self.active_player >= len(self.actors):
            self.turn += 1
            self.active_player = 0


def set_events():
    """ Prevent events we aren't interested in from being used later """
    pygame.event.set_blocked([pygame.ACTIVEEVENT, pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONDOWN, ])
