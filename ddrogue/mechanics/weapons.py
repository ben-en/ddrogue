from collections import namedtuple


Weapon = namedtuple('Weapon', [
    'cost',
    'dmg',
    'crit_r',
    'crit_m',
    'range',
    'weight',
    'hands',
    'type',
    'tags'
])

bolas = Weapon(
    5,
    '1d4',
    20,
    2,
    10,
    2,
    2,
    'b',
    'ranged nonlethal trip'.split()
)

quarterstaff = Weapon(
    0,
    ['1d6', '1d6'],
    20,
    2,
    0,
    4,
    2
    'b',
    'double monk'.split()
)

longspear = Weapon(
    5,
    '1d8',
    20,
    3,
    0,
    9,
    2,
    'p',
    'brace reach'.split()
)
