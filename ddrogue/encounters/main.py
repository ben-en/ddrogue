import re

import pygame

from ..colors import GREEN, YELLOW, RED, BLUE
from .events import EncounterState, set_events
from .map import EncounterMap, create_map_matrix
from ..mechanics.classes import Fighter, Wizard
from ..mechanics.dice import roll
from ..mechanics.skills import SKILL_LIST
from ..mechanics.races import Human
from ..mechanics.weapons import Equipment
from .npc import Goblin
from .player import Character
from .ui import StatusBox, HUD


# TODO relative file paths
KEYMAP_FILE = './controls.json'
SAVE_DIR = './saves'
FONT_NAME = 'ubuntumono'
FONT_SIZE = 14

MOVEMENT_EVENTS = 'UP DOWN LEFT RIGHT'.split()

ALPHA_RE = re.compile("[a-zA-Z0-9]")

UI_SIZE = 400

ACTIONS = {}
SAVE_DIR = './saves'


def encounter_loop(screen, floor_plan, keymap_path, players, npcs=[]):
    set_events()
    s_width, s_height = screen.get_size()
    characters = npcs[:] + players[:]
    characters.sort(key=lambda x: roll('1d20+%s' % x.init))
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    m = EncounterMap(characters, floor_plan)
    hud = HUD(players, font, (s_width - UI_SIZE, 0), UI_SIZE, s_height)
    output = StatusBox(
        screen,
        font,
        (0, s_height - UI_SIZE / 2),
        s_width - UI_SIZE,
        UI_SIZE / 2
    )
    state = EncounterState(players, npcs, m, output, hud, keymap_path)
    while not state.quit:
        state.next_turn()


def init_encounter():
    screen = pygame.display.get_surface()
    m = EncounterMap([], create_map_matrix())
    goblin_img = m.create_tile(color=GREEN)
    goblin = Goblin(goblin_img)
    playera = Character(
        m.create_tile(color=RED),
        Human,
        [(Fighter, 1)],
        (roll('1d6') for x in range(6)),
        {'skill': 1 for skill in SKILL_LIST},
        Human.natural_weapons,
        name='Player A',
        features={
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        description="fighter player character",
        equipped=Equipment(r_h=0),
    )
    playerb = Character(
        m.create_tile(color=YELLOW),
        Human,
        [(Wizard, 2)],
        (roll('1d6') for x in range(6)),
        {'skill': 1 for skill in SKILL_LIST},
        Human.natural_weapons,
        name='Player B',
        features={
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        description="wizard player character",
        equipped=Equipment(r_h=0),
    )
    playerc = Character(
        m.create_tile(color=BLUE),
        Human,
        [(Fighter, 1), (Wizard, 2)],
        (roll('1d6') for x in range(6)),
        {'skill': 1 for skill in SKILL_LIST},
        Human.natural_weapons,
        name='Player C',
        features={
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        description="multiclass player character",
        equipped=Equipment(r_h=0),
    )
    playera.pos = [8, 1]
    playerb.pos = [8, 2]
    playerc.pos = [9, 1]
    players = [playera, playerb, playerc]
    goblin.pos = [1, 1]
    return screen, create_map_matrix(), KEYMAP_FILE, players, [goblin]
