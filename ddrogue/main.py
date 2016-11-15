import pygame

from .game import main_menu


def main():
    pygame.init()
    pygame.font.init()

    # Start the main menu
    main_menu()
