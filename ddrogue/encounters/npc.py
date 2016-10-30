from pygame.sprite import Sprite

from ..mechanics.dice import roll
from ..mechanics.stats import Stat, StatBlock
from ..mechanics.sizes import small
from ..mechanics.weapons import sml_unarmed


class Goblin(Sprite):
    def __init__(self, img):
        Sprite.__init__(self)
        self.name = 'Goblin'
        self.img = img
        self.rect = img.get_rect()
        self.stats = self.init_stats()
        self.hp = roll('1d4') + self.stats.con.bonus
        self.ac = 10 + self.stats.dex.bonus
        self.bab = 1
        self.init = 1
        self.size = small
        self.speed = 4
        self.weapons = [sml_unarmed]
        self.equipped = 0
        # TODO add armor and size values
        self.ai = 1

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

    def act(self):
        print('Goblin\'s turn')
        print('Goblin can\'t do anything')
