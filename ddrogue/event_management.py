from collections import OrderedDict
from copy import deepcopy
import json
from time import sleep
import re

import pygame

from .pathfinding import astar
from .menu import fullscreen_menu
from .mechanics.dice import roll
from .ui import StatusBox, HUD


FONT_NAME = 'ubuntumono'
FONT_SIZE = 14

MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")

UI_SIZE = 400

ACTIONS = {}


def action(func):
    ACTIONS[func.__name__] = func
    return func


@action
def quit(state, event):
    """ Tell the state to exit after user dialog """
    state.quit = True
    return state
    # TODO user dialog
    options = OrderedDict()
    options['Yes'] = lambda x: True
    options['No'] = lambda x: False
    if fullscreen_menu(state.screen, options):
        state.quit = True
    return state


@action
def debug(state, event):
    """ drop into ipdb to debug an unknown event. """
    print('Unknown event')
    print(event)
    print(dir(event))
    import ipdb
    ipdb.set_trace()


@action
def move_down(state, event):
    """ Move the player down by adding one unit to its y value.
    """
    state.player.pos = (state.player.pos[0],
                        state.player.pos[1] + state.map.unit)
    return state


@action
def move_up(state, event):
    """ Move the player up by subracting one unit from its y value.
    """
    state.player.pos = (state.player.pos[0],
                        state.player.pos[1] - state.map.unit)
    return state


@action
def move_left(state, event):
    """ Move the player left by subracting one unit from its x value.
    """
    state.player.pos = (state.player.pos[0] - state.map.unit,
                        state.player.pos[1])
    return state


@action
def move_right(state, event):
    """ Move the player right by adding one unit to its x value.
    """
    state.player.pos = (state.player.pos[0] + state.map.unit,
                        state.player.pos[1])
    return state


def move_to(state, char, pos, steps=None):
    """
    Using state's access to the map, move given `char` to `pos`, max `steps`
    """
    path = astar(state.map.floor.transpose(), tuple(char.pos), tuple(pos))
    # For some reason astar figures the path backwards. Dunno why,
    path.reverse()
    if steps:
        path = path[:steps]
    for step in path:
        char.pos = step
        state.draw()
        sleep(0.1)
    # TODO don't return state, you're modifying in place.
    return state


# TODO: Logging really needs to be fixed
# TODO: How does duplicating an object work? for state
def process_key_press(state, event):
    # print('Key pressed', event.key)
    try:
        func = state.keymap[event.key]
    except KeyError:
        print('Unknown key')
        return
    state = func(state, event)
    # print('function executed', func.__name__)
    return state


def process_click(state, event):
    move_to(state, state.player, state.map.grid_pos(event.pos))
    return state


EVENT_MAP = {
    pygame.QUIT: quit,
    pygame.KEYDOWN: process_key_press,
    pygame.KEYUP: lambda x, y: None,
    pygame.MOUSEBUTTONUP: process_click,
}


def player_turn(state):
    """
    Wait for an event, try to execute a command and return True to quit.
    """
    # Wait for an event
    event = pygame.event.wait()
    func = EVENT_MAP[event.type]
    return func(state, event)


def load_keymap(file_path):
    """
    Loads a json file from the file path then tries to match all provided
    key mappings to known functions
    """
    print("Loading keymap...")
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
class CombatState:
    def __init__(self, screen, m, keymap_path, player, npcs=[]):
        """
        Has properties necessery to complete an encounter.

        Properties include screen, map, screen width and height, a key map of
        keys to functions, the player object, a list of npcs, a list of
        characters, a list of visible objects, whether the player has chosen to
        quit or  not, a font object from pygame, a text status box, and a heads
        up display for things like player hitpoints and experience.

        Some of these properties are redundant, it kind of got away from me and
        i didn't plan it so much as slap stuff on as i wanted it.
        """
        set_events()  # TODO remove this
        self.screen = screen
        self.map = m
        s_width, s_height = screen.get_width(), screen.get_height()
        self.keymap = load_keymap(keymap_path)
        self.player = player
        self.npcs = npcs
        self.characters = npcs[:] + [player]
        self.visible = self.characters
        self.quit = False
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.output = StatusBox((0, s_height - UI_SIZE / 2), s_width - UI_SIZE,
                                UI_SIZE / 2)
        # Assign _print method to self for easy access
        self._print = self.output._print

        # initialize UI second, as HUD depends on access to attributes through
        # state
        self.hud = HUD(self, (s_width - UI_SIZE, 0), UI_SIZE, s_height)
        self.ui = [self.output, self.hud]

    def draw(self):
        print(self.player.pos)
        offset = (
            self.player.pos[0],
            self.player.pos[1]
        )
        offset = (self.map.image.get_width() / 2,
                  self.map.image.get_height() / 2)
        # Write the map to screen
        self.screen.blit(self.map.image,
                         self.map.image.get_rect(
                             center=(offset)))

        # Write the text box to screen
        for ui in self.ui:
            ui.update()
            self.screen.blit(ui.image, ui.pos)

        # Add visible objects
        for obj in self.visible:
            self.screen.blit(obj.image, self.map.pixel_pos(obj.pos))

        # Flip the staging area to the display
        pygame.display.flip()

        # TODO Handle end of round in state.
        # Reasoning is that click events can be checked against HUD, statusbox,
        # and map areas. If on map, then the active character does something
        # with that click.

    def copy(self):
        return deepcopy(self)


def set_events():
    """ Prevent events we aren't interested in from being used later """
    pygame.event.set_blocked([pygame.ACTIVEEVENT, pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONDOWN, ])


def attack(attacker, defender):
    """ Runs one _attack() for every attack bonus in attacker.bab """
    print('attacker', attacker)
    print('defender', defender)
    weapon = attacker.weapons[attacker.equipped]

    print('attacker base attack bonus', attacker.bab)
    for bab in attacker.bab:
        print('rolling to hit')
        attack_bonus = bab + weapon.attack_bonus
        if not attempt_hit(attack_bonus, defender.ac):
            print('attack missed')
            continue
        if resolve_damage(attacker, defender):
            return True  # Destroyed the monster


def attempt_hit(bonus, ac):
    return (roll('1d20') + bonus) > ac


def resolve_damage(weapon, defender):
    print('rolling damage')
    base_dmg = roll(weapon.damage)
    print('base', base_dmg)
    total_dmg = base_dmg + weapon.dmg_bonus
    print('total', total_dmg)
    print('initial hp', defender.hp)
    defender.hp -= total_dmg
    print('remaining hp', defender.hp)
    return defender.hp <= 0  # Whether defender was destroyed
