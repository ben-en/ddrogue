from pygame.sprite import Sprite

from ..colors import BLUE
from ..event_management import player_turn
from .dice import roll, die_to_val
from .skills import SKILL_LIST
from .stats import StatBlock, Stat, stat_bonus
from .spells import bonus_spells


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
            sorted(self.equipment, key=lambda x: die_to_val(x.dam))[0]
        )

        self.level = 0
        self.rolled_hp = 0
        self.skill_ranks = {'skill': 0 for skill in SKILL_LIST}
        self.abilities = race.features['active']
        self.features = race.features['passive']
        self.level_up()

    def level_up(self):
        """ Increase a character's level by one """
        self.level += 1
        index = self.level - 1  # because indices start at 0
        self.rolled_hp += roll(self.cclass.hd)
        self.bab = self.cclass.bab[index]
        self.fort, self.ref, self.wis = self.cclass.saves[0]
        self.speed = self.race.speed
        self.skill_ranks.update(self.skill_up())

        features = self.cclass.features

        print(features)

        try:
            self.abilities += features[index]['active']
        except KeyError:
            pass
        try:
            new_features = features[index]['passive']
            # Apply new features to the character
            for func in new_features:
                self = func(self)
            self.features += new_features
        except KeyError:
            pass

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

    def add_spells(self, interactive=False):
        """ Adds spells and spells per day in place if applicable """
        # TODO make level based
        # TODO make spellbook/spell known based
        self.spells = self.cclass.features['spells']['known']

        spd = self.cclass.features['spells']['per_day']
        index = self.level - 1
        bonus = self.stats[self.cclass.features['spells']['attr']].bonus
        self.spd = [(spd[index] + bonus_spells(bonus, i)) for i in range(10)]

    def combat_ready(self):
        """ Compute initial values for combat variables """
        # TODO add current state (standing/prone etc)
        self.ac = self.compute_ac()
        self.hp = self.compute_hp()
        self.init = self.compute_init()
        self.fort, self.ref, self.wis = self.compute_saves()
        self.cmb, self.cmd = self.compute_cms()

    def act(self, state):
        # TODO void any kepresses while rendering
        state = player_turn(state)
        return state
