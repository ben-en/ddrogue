from ..constants import KEYMAP_FILE
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


def encounter_loop():
    players, npcs, floor_plan, keymap_path = init_encounter()
    state = EncounterState(players, npcs, floor_plan, keymap_path)
    while not state.quit:
        state.next_turn()


def init_encounter():
    goblin1 = Goblin(load_tile('goblin'))
    goblin2 = Goblin(load_tile('goblin'))
    goblin3 = Goblin(load_tile('goblin'))
    goblin4 = Goblin(load_tile('goblin'))
    goblin1.pos = [1, 1]
    goblin2.pos = [1, 2]
    goblin3.pos = [19, 1]
    goblin4.pos = [8, 10]
    playera = Character(
        load_tile('fighter'),
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
    playera.pos = [18, 1]
    playerb = Character(
        load_tile('wizard'),
        Human,
        [(Wizard, 2)],
        (roll('4d6') for x in range(6)),
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
    playerb.pos = [8, 12]
    # playerc = Character(
    #     load_tile('wizard'),
    #     Human,
    #     [(Fighter, 1), (Wizard, 2)],
    #     (roll('1d6') for x in range(6)),
    #     {'skill': 1 for skill in SKILL_LIST},
    #     Human.natural_weapons,
    #     name='Player C',
    #     features={
    #         'active': [],
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
    npcs = [goblin1, goblin2, goblin3, goblin4]
    return players, npcs, create_map_matrix(), KEYMAP_FILE
