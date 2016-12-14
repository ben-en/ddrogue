from collections import OrderedDict

from pygame.sprite import Sprite

from ..mechanics.dice import die_to_val
from ..mechanics.stats import Stat, StatBlock, stat_bonus
from ..mechanics.skills import SKILL_LIST


# The charaxter class will be a wrapper around the data that makes up the core
# of rhe character, such as attributes, abilities, spells known and per day,
# feats and so on.
# methods it should have onclude a method to export the core info, properties,
# a way for accessing skills with a calculated bonus, management for effects on
# the character, perhaps equipment managementas well.
# active abilities should specify how much time they take to accomplish.
# generic combat actions are being added to combat module
class Character(Sprite):
    """
    TODO:
        armor check penaltty
        body based equipment
    """
    def __init__(
        self,
        img,
        race,
        char_levels,
        abilities,
        skill_ranks,
        equipment,
        features={
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
            'levelup': [],
        },
        name='foo',
        description='',
        gold=0,
        equipped=None,
    ):
        # img related
        Sprite.__init__(self)
        self.groups = []
        self.hostile = 0
        self.img = img
        self.rect = self.img.get_rect()

        self.race = race
        self.clevel = char_levels
        self.speed = race.speed

        self.desc = description or 'missing unique description'
        self.s = name or 'No Name'

        self.equipment = equipment
        self.equipped = equipped or sorted(self.equipment,
                                           key=lambda x: die_to_val(x.dmg))[0]

        self.stats = StatBlock([Stat(i, stat_bonus(i)) for i in abilities])
        self.skill_ranks = skill_ranks
        self.features = features
        self.effects = []

        self._fort_mods = [0]
        self._ref_mods = [0]
        self._will_mods = [0]
        self._init_mods = [0]
        self._ac_mods = [0]
        self._hp_mods = [0]
        self._speed_mods = [0]

        self._stat_mods = {}
        for stat in self.stats:
            self._stat_mods[stat] = [0]

        self._skill_mods = {}
        for skill in self.skill_ranks:
            self._skill_mods[skill] = [0]

        self.sr = 0
        self.dr = 0
        self.level = 0
        self.xp = 0
        self._rolled_hd = 0
        self.hp = self.max_hp
        self.bab = self.clevel[0][0].bab[self.clevel[0][1]]

        self.moved = 0
        self.move_action = 1
        self.standard_action = 1
        self.swift_action = 1
        self.prone = 0

    @property
    def ac(self):
        return 10 + self.stats['dex'].bonus + sum(self._ac_mods)

    @property
    def touch_ac(self):
        return 10 + self.stats['dex'].bonus + sum(self._ac_mods)

    @property
    def flat_ac(self):
        return 10 + sum(self._ac_mods)

    @property
    def init(self):
        return self.stats['dex'].bonus + sum(self._init_mods)

    @property
    def cmb(self):
        return int(self.bab[0] + self.stats['str'].bonus)

    @property
    def cmd(self):
        return self.bab[0] + self.stats['str'].bonus + self.stats['dex'].bonus

    @property
    def ref(self):
        return self.stats['dex'].bonus + sum(self._ref_mods)

    @property
    def fort(self):
        return self.stats['con'].bonus + sum(self._fort_mods)

    @property
    def will(self):
        return self.stats['wis'].bonus + sum(self._will_mods)

    @property
    def max_hp(self):
        return self._rolled_hd + (self.stats['con'].bonus * self.level)

    @property
    def skills(self):
        skills = OrderedDict
        for skill, attr, check in SKILL_LIST:
            skills[skill] = sum((
                self._skill_ranks[skill],
                self._skill_mods[skill],
                self.stats[attr].bonus,
                self.check_penalty if check else 0
            ))
        return skills
