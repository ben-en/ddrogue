import re
import json

import pygame

from .mechanics.dice import roll


MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")


def set_events():
    """ Prevent events we aren't interested in from being used later """
    pygame.event.set_blocked([pygame.ACTIVEEVENT, pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, ])


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


class State:
    def __init__(self, m, player, npcs=[]):
        self.map = m
        self.player = player
        self.npcs = npcs
        self.characters = npcs[:] + [player]
        self.visible = self.characters
        self.quit = False


class EventHandler(object):
    """
    EventHandler is a class that requires a `Player` object as the first
    argumet, see the `player.py` file for details, and a file path to the
    the keymap json file as the second argument. The keymap dict is a work in
    progress. For now it will map unicode and keymap codes separately. Example
    of a json file contents:
        {
            "keycode": {
                "273": "move_up",
                "274": "move_down",
                "275": "move_right",
                "276": "move_left",
                "27": "quit"
            },
            "unicode": {
                "h": "move_left",
                "k": "move_down",
                "j": "move_up",
                "l": "move_right"
            }
        }
    """

    def __init__(self, player, keymap_file):
        set_events()
        self.player = player
        self.unit = player.rect[2]  # Tiles are all the same size
        self.event_types = [self.quit, self.move_up, self.move_down,
                            self.move_left, self.move_right]
        self.player_actions = {
            'quit': self.quit,
            'move_up': self.move_up,
            'move_down': self.move_down,
            'move_left': self.move_left,
            'move_right': self.move_right,
        }
        self.keymap = self.load_keymap(keymap_file)

    def end_round(self, state):
        """
        Wait for an event, try to execute a command and return True to quit.
        """
        self.state = state
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.process_key_press(event)
        elif event.type == pygame.KEYUP:
            # As this is turn based, it is possible we don't care so much about
            # this
            pass
        else:
            print('Unknown event')
            print(event)
            print(dir(event))
            import ipdb; ipdb.set_trace()
        return self.state

    def process_key_press(self, event):
        # TODO: Logging really needs to be fixed
        key_pressed = self.get_key_pressed(event)
        print('Key pressed', key_pressed)
        try:
            action = self.keymap[key_pressed]
        except KeyError:
            print('Unknown key')
            return
        if action.__name__[0:4] == "move":
            self.move_character_to(self.state.player,
                                   action(self.state.player.pos))
        else:
            action()
        print('action taken: ', action.__name__)

    def get_key_pressed(self, event):
        if event.unicode and ALPHA_RE.match(event.unicode):
            print('unicode: ', event.unicode, bool(event.unicode))
            return event.unicode
        else:
            print('keycode: ', event.key)
            return event.key

    def load_keymap(self, file_path):
        """
        Loads a json file from the file path then tries to match all provided
        key mappings to known functions
        """
        print("Loading keymap...")
        skel = {}
        with open(file_path, 'r') as json_file:
            control_dict = json.load(json_file)
        for name, d in control_dict.items():
            for key, value in d.items():
                if name == 'keycode':
                    # JSON requires key names to be strings
                    key = int(key)
                action_func = self.player_actions[value.lower()]
                skel[key] = action_func
        return skel

    #####################
    #  Event Functions  #
    #####################
    def move_character_to(self, mover, new_pos):
        print('trying to move to', new_pos)
        move_ok = True
        if self.state.map.is_wall(new_pos):
            return
        for character in self.state.characters:
            if character.rect.collidepoint(new_pos):
                # Attack returns whether the defender was destroyed
                move_ok = attack(mover, character)
        if move_ok:
            mover.pos = new_pos
            print('move success')

    def quit(self):
        self.state.quit = True

    def move_down(self, pos):
        """ Move the player down by adding one unit to its y value.
        """
        return (pos[0], pos[1] + self.unit)

    def move_up(self, pos):
        """ Move the player up by subracting one unit from its y value.
        """
        return (pos[0], pos[1] - self.unit)

    def move_left(self, pos):
        """ Move the player left by subracting one unit from its x value.
        """
        return (pos[0] - self.unit, pos[1])

    def move_right(self, pos):
        """ Move the player right by adding one unit to its x value.
        """
        return (pos[0] + self.unit, pos[1])
