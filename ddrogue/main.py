import pygame

from .game import main_menu


def main():
    pygame.init()
    pygame.font.init()

    # Set up the screen
    # TODO use pygame.display.get_surface
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Start the main menu
    # new_game(screen)
    main_menu(screen)
