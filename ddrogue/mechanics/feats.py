from collections import namedtuple


FEATS = {}

Feat = namedtuple('Feat', 'title desc requirements tags func'.split())


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
