from collections import OrderedDict
from copy import deepcopy
import json
from time import sleep
import re

import pygame

from .pathfinding import astar
from .menu import fullscreen_menu
from .mechanics.dice import roll


MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")

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


def move_to(state, char, pos, steps=-1):
    path = astar(state.map.floor.transpose(),
                 tuple(state.map.grid_pos(char.pos)),
                 tuple(state.map.grid_pos(pos)))
    path.reverse()
    for step in path[:steps]:
        char.pos = state.map.pixel_pos(step)
        state.draw()
        sleep(0.1)
    return state


# TODO: Logging really needs to be fixed
# TODO: How does duplicating an object work? for state
def process_key_press(state, event):
    print('Key pressed', event.key)
    try:
        func = state.keymap[event.key]
    except KeyError:
        print('Unknown key')
        return
    state = func(state, event)
    print('function executed', func.__name__)
    return state


def process_click(state, event):
    move_to(state, state.player, event.pos)
    return state


EVENT_MAP = {
    pygame.QUIT: quit,
    pygame.KEYDOWN: process_key_press,
    pygame.KEYUP: lambda x, y: None,
    pygame.MOUSEBUTTONUP: process_click,
}


def end_round(state):
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
class State:
    def __init__(self, screen, m, keymap_path, player, npcs=[]):
        set_events()  # TODO remove this
        self.screen = screen
        self.map = m
        self.keymap = load_keymap(keymap_path)
        self.player = player
        self.npcs = npcs
        self.characters = npcs[:] + [player]
        self.visible = self.characters
        self.quit = False

    def draw(self):
        # Write the map to screen
        self.screen.blit(self.map.image, [0, 0])

        # Write the text box to screen
        self.screen.blit(self.output.image, [0, self.map.pixel_height])

        # Add visible objects
        for obj in self.visible:
            self.screen.blit(obj.image, obj.pos)
            obj.rect.x, obj.rect.y = obj.pos

        # Flip the staging area to the display
        pygame.display.flip()

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
