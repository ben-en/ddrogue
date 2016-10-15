from collections import OrderedDict

import pygame

from .game import new_game, settings, guide, legal, quit
from .menu import fullscreen_menu


def main_menu(screen):
    options = OrderedDict()
    options["New Game"] = new_game
    options["Settings"] = settings
    options["Guide"] = guide
    options["Legal"] = legal
    options["Exit"] = quit
    fullscreen_menu(screen, options)


def main():
    pygame.init()
    pygame.font.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0))

    # Start the main menu
    new_game(screen)
    # main_menu(screen)
