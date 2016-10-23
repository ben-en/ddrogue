from collections import OrderedDict
import os
import shelve
import sys

from .colors import GREEN
from .map import EncounterMap, create_map_matrix
from .npc import Goblin
from .event_management import EncounterState
from .ui import render_text, pick, fullscreen_menu

from .mechanics.classes import Fighter
from .mechanics.dice import roll
from .mechanics.skills import SKILL_LIST
from .mechanics.races import Human
from .player import Character

PLAYER_COLOR = 255, 255, 100

# TODO relative file paths
KEYMAP_FILE = './controls.json'
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
    sys.exit()


def game_loop(state):
    while not state.quit:
        state.output._print('loaded new frame')

        state.draw()

        for char in state.characters:
            char.act(state)


def init_state(screen):
    m = EncounterMap(create_map_matrix())
    goblin_image = m.create_tile(color=GREEN)
    goblin = Goblin(goblin_image)
    player_image = m.create_tile(color=PLAYER_COLOR)
    player = Character(
        player_image,
        Human,
        Fighter,
        abilities=(roll('1d6') for x in range(6)),
        skill_ranks={'skill': 1 for skill in SKILL_LIST},
        features={
            'active': [],
            'passive': [],
            'feats_known': [],
        },
        description="player character"
    )
    state = EncounterState(screen, m, KEYMAP_FILE, player, npcs=[goblin])
    state.player.pos = [state.map.width/2,
                        state.map.height/2]
    state.npcs[0].pos = [state.player.pos[0] - 2,
                         state.player.pos[1]]
    return state


def new_game(screen):
    """ Create a state object and start a game loop with it """
    # Setup the initial game
    state = init_state(screen)

    # Start the game
    game_loop(state)


def load_game(_):
    """ Offer a selection of files that exist that are loadable """
    import ipdb
    ipdb.set_trace()
    load_dir = SAVE_DIR
    loadable_files = [os.basename(f) for f in os.path.walk(load_dir)]
    index = pick(loadable_files)
    with shelve.open(loadable_files[index], 'r') as f:
        game_loop(f['state'])


def debug(screen):
    """ drop into ipdb to debug an unknown event. """
    print('Entered debug')
    from .mechanics.chargen import chargen
    player = chargen(screen)
    print(player)
    import ipdb
    ipdb.set_trace()


def main_menu(screen):
    options = OrderedDict()
    options["debug"] = debug
    options["New Game"] = new_game
    options["Load Game"] = load_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    index = fullscreen_menu(screen, options)
    print('index is', index)
    func = options.values()[index]
    print('func is', func.__name__)
    func(screen)
