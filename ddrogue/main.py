#!/bin/python

import pygame

from .classes import Fighter
from .dice import roll
from .event_management import EventHandler
from .player import Player


TILE_SIZE = 32

SIZE = WIDTH, HEIGHT = 32 * TILE_SIZE, 24 * TILE_SIZE

BLACK = 0, 0, 0
WHITE = 255, 255, 255

KEYMAP_FILE = './controls.json'


def game_loop(screen, player, event_handler):
    while 1:
        # Blank the screen
        screen.fill(WHITE)

        # Add the character
        screen.blit(player.sprite.image, player.sprite.rect)

        # Flip the staging area to the display
        pygame.display.flip()

        if event_handler.end_round() == 'QUIT':
            break


def init_player():
    player = Player()
    player.sprite.rect.x = WIDTH/2 - player.width/2
    player.sprite.rect.y = HEIGHT/2 - player.height/2
    player._class = Fighter()
    player.bab = player._class.bab[player.level]
    player.saves = player._class.saves[player.level]
    player.hp = player.stats.con.bonus + sum(
        [roll(player._class.hd) for _ in xrange(0, player.level)]
    )
    return player


def main():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode(SIZE)

    # Set up the player
    player = init_player()

    # Initialize the event handler
    event_handler = EventHandler(player, KEYMAP_FILE)

    # Start the game
    game_loop(screen, player, event_handler)
