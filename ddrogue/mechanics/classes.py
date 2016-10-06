from collections import namedtuple

from .bab import HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves


class Character(object):
    def __init__(self, name, cclass, race, stats, interactive=False):
        self.name = name
        self.cclass = cclass
        self.race = race
        self.stats = stats

        # Setup null attributes with appropriate typed info
        self.hp = 0
        self.bab = [0]
        self.saves = 0, 0, 0
        self.initiative = 0
        self.ac = (10, 10, 10)
        self.sr = 0
        self.cmb = 0
        self.cmd = 0
        self.stats = StatBlock(*(Stat((10, 0)) for x in range(6)))
        self.skills = SkillBlock(*(0 for x in SKILL_LIST))
        self.feats = {
            'levelup': [],
            'combat': [],
            'free': [],
            'persistent': [],
        }

        self.abilities = {
            'levelup': [],
            'combat': [],
            'free': [],
            'persistent': [],
        }
        self.abilities.extend(race.abilities)
        self.equipment = []
        self.backpack = []
        self.gold = 0

        self.level = 0
        self = self.levelup(interactive=interactive)

    def levelup(self, interactive=False):
        """ level the character up and return a new Character object """
        new = self.copy()
        new.level += 1
        new.hp += (roll(self.cclass.hd) + self.stats.con.bonus)
        new.bab = self.cclass.bab[new.level]
        new.abilities += self.cclass.features[new.level]
        return new


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
