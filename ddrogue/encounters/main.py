from ..constants import KEYMAP_FILE
from .combat import COMBAT_ACTIONS
from .events import EncounterState
from .map import create_map_matrix
from ..mechanics.classes import Fighter, Wizard
from ..mechanics.dice import roll
from ..mechanics.skills import SKILL_LIST
from ..mechanics.races import Human
from ..mechanics.weapons import Equipment
from .npc import Goblin
from .player import Character
from ..ui import load_tile


ACTIONS = {}


def encounter_loop():
    players, npcs, floor_plan, keymap_path = init_encounter()
    state = EncounterState(players, npcs, floor_plan, keymap_path)
    while not state.quit:
        state.next_turn()


def init_encounter():
    goblin = Goblin(load_tile('goblin'))
    playera = Character(
        load_tile('fighter'),
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
        load_tile('wizard'),
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
    #     load_tile('wizard'),
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
