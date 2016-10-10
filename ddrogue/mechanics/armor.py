from collections import namedtuple


Armor = namedtuple('Armor', [
    'cost',
    'bonus',
    'max_dex',
    'check_pen',
    'spell_fail',
    'speed_pen',
    'slot',
    'weight'
])

leather_armor = Armor(5, 2, 6, 0, 10, 0, 'body', 15)
buckler = Armor(5, 1, None, -1, 5, 0, 'arm', 5)
