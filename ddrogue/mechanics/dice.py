from random import randint
from itertools import repeat


def split_die(notation):
    times, sides = notation.split('d')
    if '+' in sides:
        sides, bonus = sides.split('+')
    else:
        bonus = 0
    return int(times), int(sides), int(bonus)


def die_to_val(notation):
    """ Converts die notation to highest possible value """
    t, s = split_die(notation)
    return t * s


def roll(notation, split_results=False):
    """
    Expects traditional die formula; ex. 1d20. Rolls the die and returns the
    total results as default.
    """
    times, sides, bonux = split_die(notation)
    roll = [randint(1, sides) for _ in repeat(None, times)]

    if split_results:
        return roll
    return sum(roll)


def perform_action(bonus, difficulty):
    """
    As per pathfinder OGC rules, to do anything you must roll a d20 to
    accomplish the feat
    """
    return (roll('1d20') + bonus) > difficulty
