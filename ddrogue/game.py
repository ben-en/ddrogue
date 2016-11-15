from collections import OrderedDict
import os
import shelve

from .constants import SAVE_DIR, OGC_DIR
from .encounters.main import encounter_loop
from .ui import render_text, menu


def settings():
    """ Simple things like fullscreen/windowed, keybinding """
    pass


def guide():
    """
    Load the help interface

    Will be a loop that will navigate similarly to dungeon crawl: stone soup.
    Specifically, there will be function keys for things like searching help
    files, description texts of characters, races, or other features of the
    game.
    """
    render_text(os.path.join(OGC_DIR, 'mechanics.txt'))


def legal():
    """ Loads legal text """
    render_text(os.path.join(OGC_DIR, 'license.txt'))


def quit(_):
    """ Quit, takes one argument that is ignored """
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


def debug():
    """ drop into ipdb to debug an unknown event. """
    print('Entered debug')
    from .mechanics.chargen import chargen
    player = chargen()
    print(player)
    # import ipdb
    # ipdb.set_trace()


def new_game():
    """ Create a state object and start a game loop with it """
    encounter_loop()


def main_menu():
    options = OrderedDict()
    options["New Game"] = new_game
    options["debug"] = debug
    options["Load Game"] = load_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    func = options[menu(options)]
    func()
