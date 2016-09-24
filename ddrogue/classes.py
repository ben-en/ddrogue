from .mechanics import HIGH_BAB, GOOD_SAVE, BAD_SAVE, compile_saves


class Fighter:
    def __init__(self):
        self.skill_progression = 2  # implies "int+2"
        self.hd = '1d10'
        self.bab = HIGH_BAB
        self.saves = compile_saves(GOOD_SAVE, BAD_SAVE, BAD_SAVE)
        self.init_specials()

    def init_specials(self):
        """ Should add special abilities, eg fighter's bonus feat every level
        """
        pass
