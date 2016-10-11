from collections import OrderedDict

import pygame

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

    from .game import new_game
    new_game(screen)

    # Start the main menu
    #main_menu(screen)
