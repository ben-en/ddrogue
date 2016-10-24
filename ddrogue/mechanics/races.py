from collections import namedtuple

from .sizes import medium
from .weapons import med_unarmed


Race = namedtuple('Race', [
    'size',
    'speed',        # movement speed in feet per turn
    'ab_mod',       # ability modifiers, if any
    'features',     # any racial features
    'base_langs',   # free languages, probably unused at first
    'natural_weapons',      # natural weapons (must be iterable)
    's',            # race as a string
    'desc'          # description
])


def start_stat_bonus():
    """ Gives +2 to the stat of the user's choice """
    pass


def free_start_feat():
    """ Add one feat to the starting selection """
    pass


def skilled():
    """ Free skill point every level, including first """
    pass


Human = Race(
    medium,       # size
    '30',           # speed in feet per turn
    {},             # ability modifiers
    {               # racial features
     'creation': [
        start_stat_bonus,
        free_start_feat,
        skilled,
     ],
     'active': []
    },
    [],             # racial languages
    [med_unarmed],
    'Human',
    'Human racial description'
)


Halfling = Race(
    small,       # size
    '20',           # speed in feet per turn
    {'dex': 2,'cha': 2, 'str': -2},             # ability modifiers
    {               # racial features
     'persistent': [
        fearless,
        halfling_luck,
        keen_senses,
        sure_footes,
     ],
     'creation': [halfing_proficiency],
     'active': []
    },
    [halfling],             # racial languages
    [sml_unarmed],
    'Halfling',
    'Halfling racial description'
)


RACE_LIST = [Human]
