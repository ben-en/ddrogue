from pygame.sprite import Sprite

from ..event_management import player_turn
from ..player import Character, PLAYER_COLOR
from ..ui import fullscreen_menu, str_bonus, create_tile
from .classes import CLASS_LIST
from .dice import roll, die_to_val
from .feats import FEAT_LIST
from .skills import SKILL_LIST
from .stats import StatBlock, Stat, stat_bonus
from .spells import bonus_spells
from .races import RACE_LIST


def chargen(screen):
    """ Go through chargen steps """
    # Name
    img = create_tile(PLAYER_COLOR, (32, 32))
    # Select stats
    stats = roll_stats(screen)
    print('stats', stats)
    # Select race
    race = select(screen, RACE_LIST)
    print('race', race)
    # Select class
    cclass = select(screen, CLASS_LIST)
    print('cclass', cclass)
    # Select skills
    skills = skill_select(screen)
    print('skills', skills)
    # Select feats
    feats = feat_select(screen)
    print('feats', feats)
    # Select spells
    # Select equipment
    return Character(img, race, cclass, abilities=stats, skill_ranks=skills)


def roll_stats(screen):
    """ Allow swapping values and rerolling """
    while 1:
        rows = ['reroll']
        stats = []
        for stat in 'str dex con int wis cha'.split():
            val = roll('3d6')
            bonus = str_bonus(stat_bonus(val), just=2)
            rows.append('%s: [%s] (%s)' % (stat, str(val).rjust(2), bonus))
            stats.append(val)
        if not fullscreen_menu(screen, rows) == 0:
            return stats


def select(screen, l):
    """ expects a list of objects with a `s` property which is a string """
    # Create a list of the strings the objects have
    str_l = [i.s for i in l]
    # Return the object with the selected string
    return l[fullscreen_menu(screen, str_l)]


def multi_select(screen, l, count):
    selected = []
    while len(selected) < count:
        index = fullscreen_menu(screen, l)
        selected.append(l.pop(index))
    return selected


def skill_select(screen):
    """ Should be list of ints that can be +/-'d """
    # TODO
    return {}


def feat_select(screen):
    f_names = [f.s for f in FEAT_LIST]
    picked = multi_select(screen, f_names, 2)
    return picked


class OldCharacter(Sprite):
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
