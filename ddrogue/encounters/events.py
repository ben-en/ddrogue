import json
import shelve
import random

import pygame

from ..colors import BLACK, LIGHT_BLUE
from ..constants import UI_SIZE, SAVE_DIR, FONT_NAME, FONT_SIZE
from ..ui import menu
from ..mechanics.dice import roll
from .combat import move, move_to, charge
from .map import EncounterMap
from .ui import StatusBox, HUD


ACTIONS = {}


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
        state.quit = True
        return 'done'


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
    if not state.char.features['spells']:
        state._print('No spells known')
    spell_list = map(state.char.features['spells'], lambda x: x.__name__)
    spell = menu(state.screen, spell_list)
    res = state.char.features['spells'][spell_list.index(spell)]
    return res(state)


@action
def ability(state, event):
    """
    offer a list of abilities to activate
    """
    ability_list = map(lambda x: x.__name__, state.char.features['active'])
    ability = menu(pygame.display.get_surface(), ability_list,
                   xy=state.map.pixel_pos(state.map.size))
    if not ability:
        state._print('No event selected')
        return
    res = state.char.features['active'][ability_list.index(ability)]
    return res(state)


@action
def char_info(state, event):
    """
    display a character sheet loke view

    list:
        desc,
        stats,
        image
    """
    state._print('char_info not implemented')


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
    ability(state, event)


EVENT_MAP = {
    pygame.QUIT: quit,
    pygame.KEYUP: process_key_press,
    pygame.KEYDOWN: lambda x, y: None,
    pygame.MOUSEBUTTONUP: process_click,
}


def player_turn(state):
    done = 0
    while not done:
        # Wait for an event
        while 1:
            event = state.interact_with_user()
            if event:
                break
        print('found event', event)
        func = EVENT_MAP[event.type]
        res = func(state, event)
        if res == 'done':
            done = True


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
        self.map = EncounterMap(self.actors, floor_plan,
                                (self.screen.get_width() - UI_SIZE,
                                 self.screen.get_height() - UI_SIZE))
        self.hud = HUD(self, self.players, self.font, (s_width - UI_SIZE, 0),
                       UI_SIZE, s_height)
        self.output = StatusBox(self, self.screen, self.font,
                                (0, s_height - UI_SIZE / 2), s_width - UI_SIZE,
                                UI_SIZE / 2)
        # Assign _print method to self for easy access
        self._print = self.output._print
        self.ui = [self.map, self.hud, self.output]
        self.keymap = load_keymap(keymap_file)
        self.panel_areas = [pygame.rect.Rect(e.pos, e.img.get_size()) for e in
                            self.ui]
        self.selected_element = 0

        self.update_player_ui()

        # Set the selected player (if one exists)
        if self.actors[0] in self.players:
            self.hud.selected_player = self.hud.players.index(self.char)

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

    def interact_with_user(self):
        """
        Interact with the user (help dialogs etc) until a character acction
        occurs.
        """
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
                return
        elif event.type == pygame.QUIT:
            return event
        elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            for index in range(len(self.panel_areas)):
                if self.panel_areas[index].collidepoint(event.pos):
                    self.selected_element = index
                    return self.ui[index].event_handler(event)
        # Run the event handler on the event, if the event is returned
        # by the handler it is returned as the final event
        element = self.ui[self.selected_element]
        return element.event_handler(event)

    def next_turn(self):
        self._print('%s\'s turn' % self.char.s)
        if len(self.char.effects):
            for e in self.char.effects.pop[0]:
                e(self)
        if hasattr(self.char, 'ai'):
            ai_turn(self)
        else:
            player_turn(self)
        self.end_turn()

    def end_turn(self, *args, **kwargs):
        self.active_player += 1
        if self.active_player >= len(self.actors):
            self.turn += 1
            self.active_player = 0
        self.update_player_ui()
        # Reset actions
        self.char.moved = 0
        self.char.move_action = 1
        self.char.standard_action = 1
        self.char.swift_action = 1

    def update_player_ui(self):
        try:
            self.hud.selected_player = self.hud.players.index(self.char)
        except ValueError:
            # isn't a player
            pass


def set_events():
    """ Prevent events we aren't interested in from being used later """
    pygame.event.set_blocked([pygame.ACTIVEEVENT, pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONDOWN, ])
