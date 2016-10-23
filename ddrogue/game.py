from collections import OrderedDict
import sys

from .colors import GREEN
from .map import Map, create_map_matrix, create_tile
from .menu import fullscreen_menu
from .npc import Goblin
from .event_management import State
from .ui import render_text

from .mechanics.classes import Fighter
from .mechanics.dice import roll
from .mechanics.skills import SKILL_LIST
from .mechanics.chargen import Character, PlainCharacter
from .mechanics.races import Human

PLAYER_COLOR = 255, 255, 100

# TODO relative file paths
KEYMAP_FILE = './controls.json'


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
    m = Map(create_map_matrix())
    goblin_image = create_tile(GREEN, [m.unit, m.unit])
    goblin = Goblin(goblin_image)
    player_image = create_tile(PLAYER_COLOR, [m.unit, m.unit])
    player = PlainCharacter(
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
    state = State(screen, m, KEYMAP_FILE, player, npcs=[goblin])
    state.player.pos = [state.map.width/2 * state.map.unit,
                        state.map.height/2 * state.map.unit]
    state.npcs[0].pos = [state.player.pos[0] - state.map.unit * 2,
                         state.player.pos[1]]
    return state


def new_game(screen):
    """ Create a state object and start a game loop with it """
    # Setup the initial game
    state = init_state(screen)

    # Start the game
    game_loop(state)


def main_menu(screen):
    options = OrderedDict()
    options["New Game"] = new_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    fullscreen_menu(screen, options)
