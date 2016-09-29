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

    player.stats = player.init_stats()
    player.size = Medium()
    player._class = Fighter()
    player.levelup(level=1)

    player.bab = player._class.bab[player.level]
    print(player.bab)
    print(player._class.bab)
    player.base_saves = player._class.saves[player.level]
    player.hp = player.stats.con.bonus + sum(
        [roll(player._class.hd) for _ in xrange(0, player.level)]
    )

    player.weapons = [Fist(player)]
    player.equipped = 0

    return player


class Player(Sprite):
    def __init__(self, image):
        Sprite.__init__(self)
        self.groups = []
        self.image = image
        self.rect = self.image.get_rect()

        self.level = 0

    def init_stats(self):
        stats = StatBlock(
            str=Stat(17, 3), dex=Stat(13, 1), con=Stat(14, 2), int=Stat(9, -1),
            wis=Stat(10, 0), cha=Stat(12, 1),
        )
        return stats

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

    def setup_skills(self):
        self.skills = {}
        for skill in SKILL_LIST:
            self.skill[skill] = [0, 0]  # [ranks, bonus]
