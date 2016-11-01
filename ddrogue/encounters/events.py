import json
import shelve
import re
import random

import pygame

from ..colors import BLACK, LIGHT_BLUE
from ..ui import menu, func_to_str
from ..mechanics.dice import roll
from .combat import move, move_to
from .map import EncounterMap
from .ui import StatusBox, HUD


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
        filename = state.char.s + '.save'
    f = shelve.open(SAVE_DIR + filename, 'n')
    f['foo'] = 'saves aren\'t functional yet'
    f.close


def action(func):
    ACTIONS[func.__name__] = func
    return func


@action
def quit(state, _):
    """ Tell the state to exit after user dialog """
    save_game(state)
    if state.output.ask('Would you like to quit?'):
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
    ability_list = func_to_str(state.char.features['spells'])
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
    ability_list = func_to_str(state.char.features['active'])
    index = menu(pygame.display.get_surface(), ability_list)
    import ipdb
    ipdb.set_trace()
    res = state.char.features['active'][index]()
    return res


@action
def char_info(state, event):
    """
    display a character sheet loke view

    list:
        desc,
        stats,
        image
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


def process_key_press(state, event):
    # print('Key pressed', event.key)
    try:
        func = state.keymap[event.key]
    except KeyError:
        print('Unknown key')
        return
    res = func(state, event)
    return res
    # print('function executed', func.__name__)


def process_click(state, event):
    move(state)


EVENT_MAP = {
    pygame.QUIT: quit,
    pygame.KEYUP: process_key_press,
    pygame.KEYDOWN: lambda x, y: None,
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
                skel[key] = ACTIONS[value.lower()]
    return skel


# TODO: State should duplicate itself and store its history somewhere whenever
# something changes, without events having to do something themselves.
class EncounterState:
    def __init__(self, players, npcs, floor_plan, keymap_file):
        """
        Keeps track of turns and object state in an encounter
        """
        # Characters
        self.players = players
        self.npcs = npcs
        self.actors = players + npcs
        # Initiative order
        self.actors.sort(key=lambda x: roll('1d20+%s' % x.init))
        self.active_player = 0
        self.turn = 0
        # When true, exit the game
        self.quit = 0
        # UI
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.screen = pygame.display.get_surface()
        set_events()
        s_width, s_height = self.screen.get_size()
        self.map = EncounterMap(self.actors, floor_plan)
        self.hud = HUD(self, self.players, self.font, (s_width - UI_SIZE, 0),
                       UI_SIZE, s_height)
        self.output = StatusBox(self, self.screen, self.font,
                                (0, s_height - UI_SIZE / 2), s_width - UI_SIZE,
                                UI_SIZE / 2)
        # Assign _print method to self for easy access
        self._print = self.output._print
        self.ui = [self.map, self.output, self.hud]
        self.keymap = load_keymap(keymap_file)
        self.panel_areas = [pygame.rect.Rect(e.pos, e.img.get_size()) for e in
                            self.ui]
        self.selected_element = 0

    @property
    def char(self):
        return self.actors[self.active_player]

    def draw(self):
        self.screen.fill(BLACK)
        # Draw the panels on the screen
        for e in self.ui:
            e.update()
            self.screen.blit(e.img, e.pos)
        selected_element = self.ui[self.selected_element]
        pygame.draw.rect(
            self.screen, LIGHT_BLUE,
            (selected_element.pos, selected_element.img.get_size()), 1
        )
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
                try:
                    print('key: ', chr(event.key))
                except ValueError:
                    print('non-alphanumeric key')
                if event.key == 27:  # esc
                    # break out returning a quit event
                    return event
                elif event.key == ord('\t'):
                    # If tab, switch to the next ui element
                    self.selected_element += 1
                    if self.selected_element >= len(self.ui):
                        self.selected_element = 0
                    elif self.selected_element < 0:
                        self.selected_element = len(self.ui) - 1
                    continue
            elif event.type == pygame.QUIT:
                return 'quit'
            elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
                for index in range(len(self.panel_areas)):
                    if self.panel_areas[index].collidepoint(event.pos):
                        self.selected_element = index
                        self.ui[index].event_handler(event)
                        continue
            # Run the event handler on the event, if the event is returned by
            # the handler it is returned as the final event
            element = self.ui[self.selected_element]
            returned_event = element.event_handler(event)
            if returned_event:
                break
        return event

    def next_turn(self):
        self._print('%s\'s turn' % self.char.s)
        if len(self.char.effects):
            for e in self.char.effects.pop[0]:
                e(self)
        if hasattr(self.char, 'ai'):
            ai_turn(self)
        else:
            # [0] is whether a 5ft step is available (any move action negates)
            # [1] is whether a move action is available
            # [2] is whether a standard action is available
            # a move action plus a standard action equals a full round action,
            # and as they're typically stationary you still get a free 5ft step
            # [3] is whether a swift action is available
            self.actions = [1, 1, 1, 1]
            while 1:
                self.hud.selected = self.hud.players.index(self.char)
                self._print('player loop start')
                event = self.interact_until_action()
                res = player_turn(self, event)
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
