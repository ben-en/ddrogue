import pygame

from .colors import WHITE, GREEN
from .map import Map, create_map_matrix, create_tile
from .npc import Goblin
from .player import Player
from .event_management import EventHandler, State

from .mechanics.classes import Fighter
from .mechanics.dice import roll
from .mechanics.skills import SKILL_LIST
from .mechanics.chargen import Character
from .mechanics.races import Human


PLAYER_COLOR = 255, 255, 100

KEYMAP_FILE = './controls.json'


class StatusBox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.width = x
        self.height = y
        self.image = create_tile(WHITE, [x, y])
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 12)

        self.cursor = (5, 5)

    def _print(self, s):
        tmp = pygame.display.get_surface()
        x, y = self.cursor

        for l in s:
            render = self.font.render(l, False, (0, 0, 0))
            tmp.blit(render, (x, y))
            self.image.blit(render, (x, y))
            x += 10

            if (x > self.image.get_width()-5):
                x = self.rect.left+5
                y += 10
        x = 5
        y += 10  # CR
        self.cursor = (x, y)


def game_loop(state, screen, event_handler):
    while not state.quit:
        state.output._print('loaded new frame')

        # Write the map to screen
        screen.blit(state.map.image, [0, 0])

        # Write the text box to screen
        screen.blit(state.output.image, [0, state.map.pixel_height])

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
    player_image = create_tile(PLAYER_COLOR, [m.unit, m.unit])
    player = Character(
                 player_image,
                 Human,
                 abilities=(roll('4d6') for x in range(6)),
                 char_class=Fighter,
                 skills={'skill': 1 for skill in SKILL_LIST},
                 features={
                     'active': [],
                     'passive': [],
                     'feats_known': [],
                 },
                 description=None)
    state = State(m, player, npcs=[goblin])
    state.player.pos = [state.map.width/2 * state.map.unit,
                        state.map.height/2 * state.map.unit]
    state.npcs[0].pos = [state.player.pos[0] - state.map.unit * 2,
                         state.player.pos[1]]
    state.output = StatusBox(state.map.pixel_width, 100)
    return state


def new_game(screen):
    # Setup the initial game
    state = init_state()

    # Initialize the event handler
    event_handler = EventHandler(state.player, KEYMAP_FILE)

    # Start the game
    game_loop(state, screen, event_handler)
