from pygame.sprite import Sprite

from .dice import roll
from .classes import Fighter
from .mechanics.stats import Stat, StatBlock
from .mechanics.skills import SKILL_LIST
from .mechanics.sizes import Medium
from .mechanics.weapons import Fist
from .map import create_tile


PLAYER_COLOR = 255, 255, 100


def init_player(tile_size):
    """ Returns a player object """
    player_image = create_tile(PLAYER_COLOR, [tile_size, tile_size])
    player = Player(player_image)

    # TODO add races
    # player.set_race(Human)
    player.size = Medium()
    player.set_class(Fighter)

    player.init_stats(interactive=True)

    player.add_weapon(Fist)
    player.equip(0)

    return player


class Player(Sprite):
    def __init__(self, image):
        Sprite.__init__(self)
        self.groups = []
        self.image = image
        self.rect = self.image.get_rect()

        self.level = 1
        self.weapons = []
        self.equipped = -1

    def init_stats(self, interactive=False):
        if interactive:
            print('tough luck buddy')
        self.stats = StatBlock(
            str=Stat(17, 3), dex=Stat(13, 1), con=Stat(14, 2), int=Stat(9, -1),
            wis=Stat(10, 0), cha=Stat(12, 1),
        )
        self.hp = self.stats.con.bonus + sum(
            [roll(self._class.hd or self.race.hd) for _ in
                xrange(0, self.level)]
        )

    def levelup(self, level=-1):
        """ Levels the character up to kwarg level, default current level +1
        """
        if level == -1:
            level = self.level + 1
        for i in xrange(self.level, level):
            self._levelup()
        pass

    def _levelup(self):
        self.level += 1

    def set_class(self, _class):
        self._class = Fighter()
        self.bab = self._class.bab[self.level - 1]
        print(self.bab)
        self.base_saves = self._class.saves[self.level]

    def add_weapon(self, weapon):
        self.weapons.append(Fist(self))

    def equip(self, weapon):
        self.equipped = weapon

    def setup_skills(self):
        self.skills = {}
        for skill in SKILL_LIST:
            self.skill[skill] = [0, 0]  # [ranks, bonus]
