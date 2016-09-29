#!/bin/python

import pygame

from .event_management import EventHandler, State
from .player import Player
from .map import Map, create_map_matrix, create_tile
from .npc import Goblin


BLACK = 0, 0, 0
PURPLE = 255, 0, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
WHITE = 255, 255, 255

KEYMAP_FILE = './controls.json'


def game_loop(state, screen, event_handler):
    while not state.quit:
        # Write the map to screen
        screen.blit(state.map.image, [0, 0])

        # Add visible objects
        for obj in state.visible:
            screen.blit(obj.image, obj.pos)
            obj.rect.x, obj.rect.y = obj.pos

        # Flip the staging area to the display
        pygame.display.flip()

        # Wait for the next state
        state = event_handler.end_round(state)


def init_state():
    m = Map(create_map_matrix())
    goblin_image = create_tile(GREEN, [m.unit, m.unit])
    goblin = Goblin(goblin_image)
    state = State(m, Player(m.unit), npcs=[goblin])
    state.player.pos = [state.map.width/2 * state.map.unit,
                        state.map.height/2 * state.map.unit]
    state.npcs[0].pos = [state.player.pos[0] - state.map.unit * 2,
                         state.player.pos[1]]
    return state


def main():
    pygame.init()

    # Setup the initial game
    state = init_state()

    # Set up the screen
    screen = pygame.display.set_mode(state.map.pixel_size)

    # Initialize the event handler
    event_handler = EventHandler(state.player, KEYMAP_FILE)

    # Start the game
    game_loop(state, screen, event_handler)
