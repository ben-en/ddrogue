from collections import OrderedDict
import os
import shelve
import re

from .encounters.main import encounter_loop
from .ui import render_text, menu

# TODO relative file paths
KEYMAP_FILE = './controls.json'
SAVE_DIR = './saves'
FONT_NAME = 'ubuntumono'
FONT_SIZE = 14

MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")

UI_SIZE = 400

ACTIONS = {}
SAVE_DIR = './saves'


def settings(screen):
    """ Simple things like fullscreen/windowed, keybinding """
    pass


def guide(screen):
    """
    Load the help interface

    Will be a loop that will navigate similarly to dungeon crawl: stone soup.
    Specifically, there will be function keys for things like searching help
    files, description texts of characters, races, or other features of the
    game.
    """
    # TODO relative file paths
    render_text(screen, './ogc/mechanics.txt')


def legal(screen):
    """ Loads legal text """
    # TODO relative file paths
    render_text(screen, './ogc/license.txt')


def quit(_):
    """ Hard quit, takes one argument that is ignored """
    return


def load_game(_):
    """ Offer a selection of files that exist that are loadable """
    import ipdb
    ipdb.set_trace()
    load_dir = SAVE_DIR
    loadable_files = [os.basename(f) for f in os.path.walk(load_dir)]
    index = menu(loadable_files)
    with shelve.open(loadable_files[index], 'r') as f:
        encounter_loop(f['state'])


def debug(screen):
    """ drop into ipdb to debug an unknown event. """
    print('Entered debug')
    from .mechanics.chargen import chargen
    player = chargen(screen)
    print(player)
    # import ipdb
    # ipdb.set_trace()


def new_game(screen):
    """ Create a state object and start a game loop with it """
    encounter_loop()


def main_menu(screen):
    options = OrderedDict()
    options["New Game"] = new_game
    options["debug"] = debug
    options["Load Game"] = load_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    func = options[menu(screen, options)]
    func(screen)
