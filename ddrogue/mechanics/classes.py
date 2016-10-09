from collections import namedtuple

from .bab import HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves


BaseClass = namedtuple('BaseClass', [
    'hd',
    'bab',
    'saves',
    'skills',
    'knowledges',
    'sp',
    'gold',
    'features'
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
    [{} for x in range(20)]
)
