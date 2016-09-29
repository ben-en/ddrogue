from .bab import HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves


class Fighter(object):
    def __init__(self):
        self.class_skills = 'climb craft handle animal intimidate '.split() + \
                            'knowledge profession ride survival swim'.split()
        self.knowledges = 'dungeoneering engineering'.split()

        self.hd = '1d10'
        self.bab = HIGH_BAB
        self.saves = compile_saves(GOOD_SAVE, BAD_SAVE, BAD_SAVE)
        self.skill_progression = 2  # implies "int+2"
        self.base_gold = '5d6'  # implies roll(5d6) * 10gp

    def init_specials(self):
        """ Should add special abilities, eg fighter's bonus feat every level
        """
        pass
