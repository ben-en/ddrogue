from os import getcwd
from os.path import realpath, join, dirname

import pygame


pygame.init()
pygame.font.init()


# Set up the screen
# TODO make full screen optional
# SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN = pygame.display.set_mode((0, 0))

FONT_NAME = 'ubuntumono'
FONT_SIZE = 14
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# TODO make relative to screen size
UI_SIZE = 400

__location__ = realpath(join(getcwd(), dirname(__file__)))
KEYMAP_FILE = join(__location__, 'controls.json')
TILES_DIR = join(__location__, 'tiles')
SAVE_DIR = join(__location__, 'saves')
OGC_DIR = join(__location__, 'ogc')
