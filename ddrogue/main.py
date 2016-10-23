import pygame

from .game import new_game, main_menu


def main():
    pygame.init()
    pygame.font.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0))

    # Start the main menu
    # new_game(screen)
    main_menu(screen)
