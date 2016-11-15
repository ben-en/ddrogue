import re

from ..colors import GREEN, YELLOW, RED, BLUE
from .combat import COMBAT_ACTIONS
from .events import EncounterState
from .map import EncounterMap, create_map_matrix
from ..mechanics.classes import Fighter, Wizard
from ..mechanics.dice import roll
from ..mechanics.skills import SKILL_LIST
from ..mechanics.races import Human
from ..mechanics.weapons import Equipment
from .npc import Goblin
from .player import Character


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


def encounter_loop():
    players, npcs, floor_plan, keymap_path = init_encounter()
    state = EncounterState(players, npcs, floor_plan, keymap_path)
    while not state.quit:
        state.next_turn()


def init_encounter():
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
            'active': COMBAT_ACTIONS.values(),
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        description="fighter player character",
        equipped=Equipment(r_h=0),
    )
    playera.pos = [8, 1]
    playerb = Character(
        m.create_tile(color=YELLOW),
        Human,
        [(Wizard, 2)],
        (roll('1d6') for x in range(6)),
        {'skill': 1 for skill in SKILL_LIST},
        Human.natural_weapons,
        name='Player B',
        features={
            'active': COMBAT_ACTIONS.values(),
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        description="wizard player character",
        equipped=Equipment(r_h=0),
    )
    playerb.pos = [8, 2]
    # playerc = Character(
    #     m.create_tile(color=BLUE),
    #     Human,
    #     [(Fighter, 1), (Wizard, 2)],
    #     (roll('1d6') for x in range(6)),
    #     {'skill': 1 for skill in SKILL_LIST},
    #     Human.natural_weapons,
    #     name='Player C',
    #     features={
    #         'active': COMBAT_ACTIONS.values(),
    #         'passive': [],
    #         'spells': [],
    #         'spd': [],
    #         'feats_known': [],
    #     },
    #     description="multiclass player character",
    #     equipped=Equipment(r_h=0),
    # )
    # playerc.pos = [9, 1]
    # players = [playera, playerb, playerc]
    players = [playera, playerb]
    goblin.pos = [1, 1]
    return players, [goblin], create_map_matrix(), KEYMAP_FILE
