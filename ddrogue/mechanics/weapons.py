

class Unarmed:
    def __init__(self, char):
        """ Expects a character as the first argument """
        self.damages = {
            'small': '1d2',
            'medium': '1d3',
            'large': '1d4'
        }
        self.crit = '20'
        self.range = 0
        self.hit_stat = 'str'
        self.dmg_stat = 'str'
        self.calculate_bonuses(char)

    def calculate_bonuses(self, char):
        self.damage = self.damages[char.size.name]
        self.hit_bonus = char.stats[self.hit_stat].bonus + char.size.atk_bonus
        self.dmg_bonus = char.stats[self.dmg_stat].bonus
