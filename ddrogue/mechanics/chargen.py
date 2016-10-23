from collections import OrderedDict

from pygame.sprite import Sprite

from ..event_management import player_turn
from .dice import roll, die_to_val
from .skills import SKILL_LIST
from .stats import StatBlock, Stat, stat_bonus
from .spells import bonus_spells


class PlainCharacter(Sprite):
    def __init__(
        self,
        image,
        race,
        cclass,
        abilities=(roll('3d6') for x in range(6)),
        skill_ranks={'skill': 0 for skill in SKILL_LIST},
        features={
            'active': [],
            'passive': [],
            'spells': [],
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


class Character(Sprite):
    """
    Object that handles recalculating saves when attributes are modified,
    recalculating AC when armor is un/equipped, calculating weapon stats when
    equipped, and keeping track of generic things like current HP, ability
    usage, and spells per day.

    Requirements for a combat-capable player character are:
        [x] stats
        [ ] hp
        [ ] damage resistance
        [ ] land/fly/swim/climb/burrow speeds
        [x] size
        [ ] initiative
        [ ] ac/touch ac/flat footed ac
        [ ] fort/ref/will
        [x] bab
        [ ] spell resistance
        [ ] cmb/cmd
        [ ] skills
        [ ] languages
        [ ] feats (list of all known feats)
        [ ] usable abilities (activated on command, but not spells)
        [ ] spells/domains/spells per day (if applicable)
        [ ] equipped weapons/armor
        [ ] backpack items
        [ ] weight
        [ ] money
        [ ] xp/rate of leveling


    property functions to do:
        fort
        ref
        wis
        cmb
        cmd
    """

    def __init__(self,
                 image,
                 race,
                 abilities=(roll('3d6') for x in range(6)),
                 cclass=None,
                 skills={'skill': 0 for skill in SKILL_LIST},
                 features={
                     'active': [],
                     'passive': [],
                     'spells': [],
                     'feats_known': [],
                 },
                 name='foo',
                 description=None):
        """
        initializes a level one character

        + race
        + ability scores
        + class - monsters don't have these typically.
        + skills
        + features - from race, class, or feats
        + description - optional, for unique characters
        """
        Sprite.__init__(self)
        self.groups = []
        self.image = image
        self.rect = self.image.get_rect()

        self.stats = StatBlock([Stat(i, stat_bonus(i)) for i in abilities])
        self.race = race
        self.cclass = cclass
        self.speed = race.speed

        self.desc = (
            (description or 'missing unique description') + '\n\n\n' +
            cclass.desc + '\n\n\n' + race.desc
        )
        self.name = name

        self.gold = roll(cclass.gold) * 10
        self.equipment = cclass.equipment + race.natural_weapons
        self.equipped = self.equipment.index(
            sorted(self.equipment, key=lambda x: die_to_val(x.dmg))[0]
        )

        self._fort = 0
        self._ref = 0
        self._will = 0

        self.sr = 0
        self.dr = 0
        self.level = 0
        self.xp = 0
        self.rolled_hp = 0
        self.skill_ranks = {'skill': 0 for skill in SKILL_LIST}
        self.abilities = race.features['active']
        self.features = race.features['passive']
        self.level_up(self.cclass)

    def level_up(self, cclass):
        """ Increase a character's level by one with the given class """
        f, r, w = cclass.saves[self.level]
        self._fort += f
        self._ref += r
        self._will += w
        self.level += 1
        index = self.level - 1  # because indices start at 0
        self.rolled_hp += roll(cclass.hd)
        self.hp = self.max_hp
        self.bab = cclass.bab[index]
        self.speed = self.race.speed
        self.skill_ranks.update(self.skill_up())

        features = cclass.features

        self.abilities += features[index].get('active', [])
        new_features = features[index].get('passive', [])
        # Apply new features to the character
        for func in new_features:
            self = func(self)
        self.features += new_features

        if features[index].get('spells', False):
            self.add_spells()
        else:
            print('no spells known')
            self.spells = None
            self.spd = None

    def skill_up(self, interactive=False):
        """ Returns a dictionary of updated skills """
        if interactive:
            import ipdb
            ipdb.set_trace()
            print('nothing here')
        # TODO determine method for AI to level up, or select skills?
        # TODO create skill menu that can be used for initial skills as well as
        # updating skills
        return {}

    def add_spells(self, cclass, interactive=False):
        """ Adds spells and spells per day in place if applicable """
        # TODO make level based
        # TODO make spellbook/spell known based
        self.spells = cclass.features['spells']['known']

        spd = cclass.features['spells']['per_day']
        index = self.level - 1
        bonus = self.stats[cclass.features['spells']['attr']].bonus
        self.spd = [(spd[index] + bonus_spells(bonus, i)) for i in range(10)]

    @property
    def ac(self):
        return 10

    @property
    def touch_ac(self):
        return 10

    @property
    def flat_ac(self):
        return 10

    @property
    def init(self):
        return self.stats['dex'].bonus

    @property
    def cmb(self):
        return self.stats['str'].bonus

    @property
    def ref(self):
        return self.stats['dex'].bonus + self._ref

    @property
    def fort(self):
        return self.stats['con'].bonus + self._fort

    @property
    def will(self):
        return self.stats['wis'].bonus + self._will

    @property
    def cmd(self):
        return self.stats['str'].bonus

    @property
    def max_hp(self):
        return self.rolled_hp + (self.stats['con'].bonus * self.level)

    def act(self, state):
        # TODO void any kepresses while rendering
        state = player_turn(state)
        return state
