from collections import OrderedDict

from pygame.sprite import Sprite

from .event_management import player_turn
from .mechanics.dice import roll, die_to_val
from .mechanics.stats import Stat, StatBlock, stat_bonus
from .mechanics.skills import SKILL_LIST


PLAYER_COLOR = 255, 255, 100


# active features should probably activate using similar mechanisms to casting
# a spell.
# passive features should apply at object creation, directly to the cha4acter
# object. perhaps  haracters should maintain a list of effects that affect them
# each phase or turn
blank_char_info = {
    'image': create_tile(BLUE, (16, 16)),
    'race': Human,
    'char_levels': ((Fighter, 5), (Wizard, 5)),
    'abilities': (roll('3d6') for x in range(6)),
    'skill_ranks': {'skill': 0 for skill in SKILL_LIST},
    'features': {
            # All the abilities that would be gained from the class, processed
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
    'name': 'foo',
    'description': None,
    'gold': 0,
    'equipment': race_weapons,
    'equipped': {
        'hand': 0
    },
    'xp': 0,
    'hp': 29
}



# The charaxter class will be a wrapper around the data that makes up the core
# of rhe character, such as attributes, abilities, spells known and per day,
# feats and so on.
# methods it should have onclude a method to export the core info, properties,
# a way for accessing skills with a calculated bonus, management for effects on
# the character, perhaps equipment managementas well.
class Character(Sprite):
    """
    TODO:
        armor check penaltty
        body based equipment
    """
    def __init__(
        self,
        image,
        race,
        char_levels,
        abilities=(roll('3d6') for x in range(6)),
        skill_ranks={'skill': 0 for skill in SKILL_LIST},
        features={
            'active': [],
            'passive': [],
            'spells': [],
            'spd': [],
            'feats_known': [],
        },
        name='foo',
        description=None,
        gold=None,
        equipment=None,
        equipped=None,
    ):
        """ Creates a character object """
        # Image related
        Sprite.__init__(self)
        self.groups = []
        self.image = image
        self.rect = self.image.get_rect()

        self.race = race
        self.cclass = cclass
        self.speed = race.speed

        self.desc = (
            (description or 'missing unique description') + '\n\n\n' +
            cclass.desc + '\n\n\n' + race.desc
        )
        self.name = name

        self.gold = gold or roll(cclass.gold) * 10
        self.equipment = equipment or cclass.equipment + race.natural_weapons
        self.equipped = equipped or self.equipment.index(
            sorted(self.equipment, key=lambda x: die_to_val(x.dmg))[0]
        )

        self.stats = StatBlock([Stat(i, stat_bonus(i)) for i in abilities])
        self.skill_ranks = skill_ranks
        self.features = features

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
        self.bab = self.cclass.bab[self.level]

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

    def act(self, state):
        # TODO void any kepresses while rendering
        state = player_turn(state)
        return state
