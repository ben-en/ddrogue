import re
import json

import pygame


MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")


def set_events():
    """ Prevent events we aren't interested in from being used later """
    pygame.event.set_blocked([pygame.ACTIVEEVENT, pygame.MOUSEMOTION,
                              pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, ])


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
        self.unit = player.height  # Tiles are all the same size
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

    def end_round(self):
        """
        Wait for an event, try to execute a command and return True to quit.
        """
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return self.quit()
        elif event.type == pygame.KEYDOWN:
            return self.key_pressed(event)
        elif event.type == pygame.KEYUP:
            # As this is turn based, it is possible we don't care so much about
            # this
            return
        else:
            print('Unknown event')
            print(event)
            print(dir(event))
            import ipdb; ipdb.set_trace()

    def key_pressed(self, event):
        # TODO: Logging really needs to be fixed
        print('Key pressed')
        print('unicode: ', event.unicode, bool(event.unicode))
        print('keycode: ', event.key)
        try:
            action = self.get_action(event)
            print('action taken: ', action.__name__)
            return action()
        except KeyError:
            print('Unknown key')

    def get_action(self, event):
        if event.unicode and ALPHA_RE.match(event.unicode):
            return self.keymap['unicode'][event.unicode]
        else:
            return self.keymap['keycode'][event.key]

    def load_keymap(self, file_path):
        """
        Loads a json file from the file path then tries to match all provided
        key mappings to known functions
        """
        print("Loading keymap...")
        skel = {
            'keycode': {},
            'unicode': {}
        }
        with open(file_path, 'r') as json_file:
            control_dict = json.load(json_file)
        for name, d in control_dict.items():
            for key, value in d.items():
                if name == 'keycode':
                    # JSON requires key names to be strings
                    key = int(key)
                action_func = self.player_actions[value.lower()]
                skel[name][key] = action_func
        print(skel)
        return skel

    #####################
    #  Event Functions  #
    #####################
    def quit(self):
        print('Got quit signal')
        return 'QUIT'

    def move_down(self):
        """ Move the player down by adding one unit to its y value.
        """
        self.player.rect.y += self.unit

    def move_up(self):
        """ Move the player up by subracting one unit from its y value.
        """
        self.player.rect.y -= self.unit

    def move_left(self):
        """ Move the player left by subracting one unit from its x value.
        """
        self.player.rect.x -= self.unit

    def move_right(self):
        """ Move the player right by adding one unit to its x value.
        """
        self.player.rect.x += self.unit
