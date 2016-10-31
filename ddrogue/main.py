import pygame

from .game import main_menu


def main():
    pygame.init()
    pygame.font.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Start the main menu
    main_menu(screen)
