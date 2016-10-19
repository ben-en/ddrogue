from collections import OrderedDict
import sys
from textwrap import wrap

import pygame

from .colors import GREEN
from .map import Map, create_map_matrix, create_tile
from .menu import fullscreen_menu
from .npc import Goblin
from .event_management import State

from .mechanics.classes import Fighter
from .mechanics.dice import roll
from .mechanics.skills import SKILL_LIST
from .mechanics.chargen import Character
from .mechanics.races import Human

PLAYER_COLOR = 255, 255, 100

# TODO relative file paths
KEYMAP_FILE = './controls.json'


def load_text(screen, text_file):
    """ Render the text file on the screen in a readable format """
    # Initialize the font
    text_font = pygame.font.Font(None, 18)
    # Calculate the number of characters that can be shown on one row
    characters = (screen.get_width() - 10) / 7

    # Attach a header that shows the path of the text file so the user can look
    # it up for manual inspection at their discretion
    text = ['loaded from: %s' % text_file, '']
    # Open and read the text file into a list of rows
    with open(text_file, 'r') as input:
        for l in input.readlines():
            text += wrap(l, characters)
            text += ['']

    # Create an image the size of the text
    image = pygame.surface.Surface((screen.get_width(), len(text) * 15))

    # Write the text onto the image
    x, y = 0, 0
    for t in text:
        image.blit(text_font.render(t, False, (255, 255, 255)), (x, y))
        y += 15

    # Disply the image
    x, y = 5, 5
    bottom = image.get_height() - screen.get_height()
    while 1:
        screen.blit(image, (x, y))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key in [27, 13]:
                break
            if event.key == 273:
                y += 30
                if y >= 0:
                    # If you're trying to scroll too high, reset to 0
                    y = 0
            if event.key == 274:
                y -= 30
                if y <= - bottom:
                    # If you're trying to scroll to low, reset to bottom
                    y = - bottom


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
    load_text(screen, './ogc/mechanics.txt')


def legal(screen):
    """ Loads legal text """
    # TODO relative file paths
    load_text(screen, './ogc/license.txt')


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
    player = Character(
                 player_image,
                 Human,
                 abilities=(roll('4d6') for x in range(6)),
                 cclass=Fighter,
                 skills={'skill': 1 for skill in SKILL_LIST},
                 features={
                     'active': [],
                     'passive': [],
                     'feats_known': [],
                 },
                 description=None)
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
