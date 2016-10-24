from collections import namedtuple


FEATS = {}

Feat = namedtuple('Feat', 's desc requirements tags func'.split())


def feat(func):
    FEATS[func.__name__] = func
    return func


@feat
def acrobatic():
    """ +2 to acrobatics and fly """
    pass


@feat
def agile_maneuvers():
    """
    use dex bonux instead of str for cmb

    +fighter feat
    """
    pass


@feat
def alertness():
    """ +2 to perception and sense motive """
    pass


@feat
def animal_affinity():
    """ +2 to handle animal and ride"""
    pass


@feat
def arcane_armor_training():
    """ arcane spell failure from armor -10% """
    pass


@feat
def arcane_armor_mastery():
    """ arcane spell failure from armor -10%
    stacks with training, requires arcane armor training"""
    pass


@feat
def athletic():
    """ +2 to climb and swim"""
    pass


@feat
def blind_fight():
    """ reroll miss chance for concealment """
    pass


@feat
def fleet():
    """ +5ft move speed """
    pass


@feat
def brew_potion():
    """
    craft potions

    requires cl 3
    craft feat
    """
    pass


@feat
def enlarge_spell():
    """
    double spell range

    metamagic
    """
    pass


@feat
def silent_spell():
    """
    cast spell silently

    metamagic
    """
    pass


FEAT_LIST = [
    Feat('Acrobatic', '+2 to acrobatics and fly', {}, [], acrobatic),
    Feat('Agile Maneuvers', 'use dex instead of str for cmb', {}, ['fighter'],
         agile_maneuvers),
    Feat('Brew Potion', 'allows crafting potions', {'CL': 3}, ['craft'],
         brew_potion)
]
