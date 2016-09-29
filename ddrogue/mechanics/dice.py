from random import randint
from itertools import repeat


def roll(die_formula, split_results=False):
    """
    Expects traditional die formula; ex. 1d20. Rolls the die and returns the
    total results as default.
    """
    times, sides = die_formula.split('d')
    roll = [randint(1, int(sides)) for _ in repeat(None, int(times))]

    if split_results:
        return roll
    return sum(roll)  # TODO sum


def perform_action(bonus, difficulty):
    """
    As per pathfinder OGC rules, to do anything you must roll a d20 to
    accomplish the feat
    """
    return (roll('1d20') + bonus) > difficulty
