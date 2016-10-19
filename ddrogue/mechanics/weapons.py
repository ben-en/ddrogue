from collections import namedtuple


Weapon = namedtuple('Weapon', [
    'name',
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

sml_unarmed = Weapon('Unarmed', 0, '1d2', 20, 2, 0, 0, 1, 'b', ['nonlethal'])
med_unarmed = Weapon('Unarmed', 0, '1d3', 20, 2, 0, 0, 1, 'b', ['nonlethal'])
lrg_unarmed = Weapon('Unarmed', 0, '1d4', 20, 2, 0, 0, 1, 'b', ['nonlethal'])

bolas = Weapon(
    'Bolas',
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
    'Quarterstaff',
    0,
    ['1d6', '1d6'],
    20,
    2,
    0,
    4,
    2,
    'b',
    'double monk'.split()
)

longspear = Weapon(
    'Longspear',
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
