from collections import namedtuple, OrderedDict


class Equipment(OrderedDict):
    def __init__(self, h=-1, c=-1, t=-1, l_a=-1, r_a=-1, l_h=-1, r_h=-1, l=-1,
                 f=-1):
        OrderedDict.__init__(self)
        self['head'] = h
        self['cloak'] = c
        self['torso'] = t
        self['l_arm'] = l_a
        self['r_arm'] = r_a
        self['l_hand'] = l_h
        self['r_hand'] = r_h
        self['legs'] = l
        self['feet'] = f


def simple_proficiency():
    """ can use any simple weapon """
    pass


def martial_proficiency():
    """ can use a martial weapon """
    pass


def shield_proficiency():
    """ can use any shield """
    pass


def light_armor_proficiency():
    """ can use any light armor """
    pass


def medium_armor_proficiency():
    """ can use any medium armor """
    pass


def heavy_armor_proficiency():
    """ can use any heavy armor """
    pass


def fighter_proficiency():
    """ can use any and all weapons (that aren't exotic) """
    pass


Weapon = namedtuple('Weapon', [
    's',
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
