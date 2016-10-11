from collections import namedtuple


Weapon = namedtuple('Weapon', [
    'dam',
    'crit',
    'range',
    'h_stat',
    'd_stat',
])


sml_unarmed = Weapon('1d2', 20, 0, 'str', 'str')
med_unarmed = Weapon('1d3', 20, 0, 'str', 'str')
lrg_unarmed = Weapon('1d4', 20, 0, 'str', 'str')
