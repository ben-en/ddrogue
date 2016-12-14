import json
import shelve
import random
from time import sleep

import pygame
from pygame import draw
from pygame import Rect

from ..colors import BLACK, LIGHT_BLUE, GREY
from ..constants import UI_SIZE, SAVE_DIR, SCREEN
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
    spell = menu(spell_list)
    res = state.char.features['spells'][spell_list.index(spell)]
    return res(state)


@action
def all_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    action_groups = (('Free Actions', FREE_ACTIONS),
                     ('Swift Actions', SWIFT_ACTIONS),
                     ('Move Actions', MOVE_ACTIONS),
                     ('Standard Actions', STANDARD_ACTIONS),
                     ('Full Round Actions', FULL_ROUND_ACTIONS))
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    for s, d in action_groups:
        final_img.blit(FONT.render(s, False, WHITE), (x, y))
        y += 20
        imgs = [FONT.render(k, False, WHITE) for k in d]
        for i in imgs:
            select_box = Rect((x - 4, y - 4), i.get_size())
            img_positions.append(select_box)
            final_img.blit(i, (x, y))
            y += 20
        y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    for s, d in action_groups:
        if index > len(d):
            index -= len(d)
            continue
        return d.values()[index](state)


@action
def free_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    s, d = ('Free Actions', FREE_ACTIONS)
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    final_img.blit(FONT.render(s, False, WHITE), (x, y))
    y += 20
    imgs = [FONT.render(k, False, WHITE) for k in d]
    for i in imgs:
        select_box = Rect((x - 4, y - 4), i.get_size())
        img_positions.append(select_box)
        final_img.blit(i, (x, y))
        y += 20
    y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    return d.values()[index](state)


@action
def swift_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    s, d = ('Swift Actions', SWIFT_ACTIONS)
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    final_img.blit(FONT.render(s, False, WHITE), (x, y))
    y += 20
    imgs = [FONT.render(k, False, WHITE) for k in d]
    for i in imgs:
        select_box = Rect((x - 4, y - 4), i.get_size())
        img_positions.append(select_box)
        final_img.blit(i, (x, y))
        y += 20
    y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    return d.values()[index](state)


@action
def move_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    s, d = ('Move Actions', MOVE_ACTIONS)
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    final_img.blit(FONT.render(s, False, WHITE), (x, y))
    y += 20
    imgs = [FONT.render(k, False, WHITE) for k in d]
    for i in imgs:
        select_box = Rect((x - 4, y - 4), i.get_size())
        img_positions.append(select_box)
        final_img.blit(i, (x, y))
        y += 20
    y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    return d.values()[index](state)


@action
def full_round_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    s, d = ('Full Round Actions', FULL_ROUND_ACTIONS)
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    final_img.blit(FONT.render(s, False, WHITE), (x, y))
    y += 20
    imgs = [FONT.render(k, False, WHITE) for k in d]
    for i in imgs:
        select_box = Rect((x - 4, y - 4), i.get_size())
        img_positions.append(select_box)
        final_img.blit(i, (x, y))
        y += 20
    y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    return d.values()[index](state)


@action
def standard_actions(state, event):
    """
    offer a list of combat actions available to all characters
    """
    s, d = ('Standard Actions', STANDARD_ACTIONS)
    x, y = 5, 5
    img_positions = []
    final_img = pygame.surface.Surface(state.map.ui_size)
    final_img.fill(BLACK)
    final_img.blit(FONT.render(s, False, WHITE), (x, y))
    y += 20
    imgs = [FONT.render(k, False, WHITE) for k in d]
    for i in imgs:
        select_box = Rect((x - 4, y - 4), i.get_size())
        img_positions.append(select_box)
        final_img.blit(i, (x, y))
        y += 20
    y += 20
    selectable = Selectable(final_img, img_positions)
    index = select_loop(selectable)
    if not index:
        state._print('No action selected')
        return
    return d.values()[index](state)


@action
def ability(state, event):
    """
    offer a list of abilities to activate
    """
    ability_list = map(lambda x: x.__name__, state.char.features['active'])
    ability = menu(ability_list, xy=state.map.ui_size)
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
    all_actions(state, event)


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
        if event == 'done':
            done = 1
            continue
        print('found event', event)
        func = EVENT_MAP[event.type]
        res = func(state, event)
        if res == 'done':
            done = 1


def ai_turn(state):
    """ Do something with a given npc """
    npc = state.char
    move_to(state, state.char, random.choice(state.players).pos,
            steps=npc.speed)
    sleep(0.2)


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
        set_events()
        s_width, s_height = SCREEN.get_size()
        self.map = EncounterMap(self.actors, floor_plan,
                                (s_width - UI_SIZE, s_height - UI_SIZE / 2))
        self.hud = HUD(self, self.players, (s_width - UI_SIZE, 0),
                       UI_SIZE, s_height)
        self.output = StatusBox(self,
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
        SCREEN.fill(BLACK)
        # Draw the panels on the screen
        self.map.update(self.char.pos)
        self.hud.update()
        for e in self.ui:
            SCREEN.blit(e.img, e.pos)
        draw.rect(SCREEN, GREY, Rect((0, 0), self.map.ui_size), 2)
        selected_element = self.ui[self.selected_element]
        pygame.draw.rect(
            SCREEN, LIGHT_BLUE,
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
            except ValueError as e:
                print(e)
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
            elif event.key in [ord(c) for c in '\n ']:
                self.output.fullscreen()
            elif event.key == 275:
                self.hud.adjust_selected_player(1)
            elif event.key == 276:
                self.hud.adjust_selected_player(-1)
        elif event.type == pygame.QUIT:
            return event
        elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            if self.output.area_rect.collidepoint(event.pos):
                print('output box collision', self.output.rect)
                self.output.fullscreen()
            elif self.hud.area_rect.collidepoint(event.pos):
                print('hud collision', self.hud.rect)
                for index in range(len(self.hud.elements)):
                    if self.hud.element_areas[index].collidepoint(event.pos):
                        print('clicked on ', index)
                        self.hud.selected_element = index
                        func = self.hud.element_functions.get(index, None)
                        if func:
                            return func(self, event)
            else:
                # Pass the mouse event back if it was on the map
                return event
            # Don't return the even tif it was in the hud or output
            return
        return event

    def next_turn(self):
        self.draw()
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
