from collections import namedtuple


Size = namedtuple('Size', ['name', 'ac', 'atk', 'cmb', 'cmd', 'skills'])
medium = Size('medium', 0, 0, 0, 0, {})
small = Size('small', 1, 1, -1, -1, {'stealth': 4})
