

class Size(object):
    def initialize_size(self):
        self.name = type(self).__name__.lower()
        self.ac_bonus = 0
        self.atk_bonus = 0
        self.cmb_bonus = 0
        self.cmd_bonus = 0
        self.skill_bonus = {}


class Medium(Size):
    def __init__(self):
        self.initialize_size()


class Small(Size):
    def __init__(self):
        self.initialize_size()
        self.ac_bonus = 1
        self.atk_bonus = 1
        self.cmb_bonus = -1
        self.cmd_bonus = -1
        self.skill_bonus['stealth'] = 4
