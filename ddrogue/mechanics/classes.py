from collections import namedtuple

from .bab import HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves


BaseClass = namedtuple('BaseClass', [
    'hd',           # hit dice rolled for HP each level
    'bab',          # base attack bonus for the class
    'saves',        # saves to be used for a given level (under dev)
    'skills',       # list of class skills
    'knowledges',   # list of knowledges if character has knowledge skill
    'sp',           # skill points gained per level
    'gold',         # initial gold
    'equipment',    # initial equipment, if any
    'features',     # features gained at each level
    'desc'          # description of the class
])


Fighter = BaseClass(
    '1d10',
    HIGH_BAB,
    compile_saves(GOOD_SAVE, BAD_SAVE, BAD_SAVE),
    ('climb craft handle animal intimidate knowledge profession ride survival'
     'swim').split(),
    'dungeoneering engineering'.split(),
    2,  # implies intelligence + 2 skill progression
    '5d6',
    [],
    [
        {
            'active': [],
            'passive': [],
        } for x in range(20)
    ],
    'Fighter character class description'
)
