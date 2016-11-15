from os import getcwd
from os.path import realpath, join, dirname
import re

import pygame


pygame.init()
pygame.font.init()


# Set up the screen
# SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN = pygame.display.set_mode((0, 0))

FONT_NAME = 'ubuntumono'
FONT_SIZE = 14
FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

UI_SIZE = 400

# TODO relative file paths
__location__ = realpath(join(getcwd(), dirname(__file__)))
KEYMAP_FILE = join(__location__, 'controls.json')
SAVE_DIR = join(__location__, 'saves')

# Unused
MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")
