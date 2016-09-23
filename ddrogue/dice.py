from random import randint
from itertools import repeat


def roll(die_formula):
    """
    Expects traditional die formula; ex. 1d20. Rolls the die and returns the
    total results.
    """
    roll = 0
    times, sides = die_formula.split('d')
    for _ in repeat(None, times):  # TODO Find out why i copypasta'd None
        roll += randint(1, sides)
    return roll


def perform_action(bonus, difficulty):
    """
    As per pathfinder OGC rules, to do anything you must roll a d20 to
    accomplish the feat
    """
    return (roll('1d20') + bonus) > difficulty
