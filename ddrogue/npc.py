from pygame.sprite import Sprite, Group

from .mechanics.dice import roll
from .mechanics.stats import Stat, StatBlock
from .mechanics.sizes import small
from .mechanics.weapons import sml_unarmed


BLACK = 0, 0, 0
BLUE = 0, 255, 0

WIDTH = HEIGHT = 32  # TODO only define this once


class Goblin(Sprite):
    def __init__(self, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.stats = self.init_stats()
        self.hp = roll('1d4') + self.stats.con.bonus
        self.ac = 10 + self.stats.dex.bonus
        self.bab = 1
        self.size = small
        self.weapons = [sml_unarmed]
        self.equipped = 0
        # TODO add armor and size values

    def init_stats(self):
        stats = StatBlock(
            str=Stat(13, 1),
            dex=Stat(14, 2),
            con=Stat(12, 1),
            int=Stat(11, 0),
            wis=Stat(8, -1),
            cha=Stat(9, -1),
        )
        return stats


class MonsterGroup(Group):
    pass
