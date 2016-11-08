from collections import namedtuple

from ..ogc.loader import load_file, prep_section


Armor = namedtuple('Armor', [
    's',
    'cost',
    'bonus',
    'max_dex',
    'check_pen',
    'spell_fail',
    'speed_pen',
    'slot',
    'weight'
])


PREP = [
    str,    # s
    int,    # cost
    int,    # bonus
    int,    # max_dex
    int,    # check_pen
    int,    # spell_fail
    int,    # speed_pen
    str,    # slot
    int     # weight
]


def load_armor():
    config = load_file('ogc/armor.ini')
    armor = {
        k: Armor(*prep_section(v.values(), PREP)) for k, v in config.items()
    }
    return armor
