from random import randint
from itertools import repeat


def roll(sides):
    """ Roll a die and return the results """
    return randint(1, sides)


def perform_action(bonus, difficulty):
    """
    As per pathfinder rules, to do anything you must roll a d20 to accomplish
    the feat
    """
    return (roll(20) + bonus) > difficulty


def attack_damage(die_size, damage_bonus, no_of_die=1):
    """
    Requires the size of the attack die, the damage bonus, the defender armor
    class, and optionally the number of attack dice, default 1.
    """
    dmg = damage_bonus
    for _ in repeat(None, no_of_die):
        dmg += roll(die_size)
    return dmg
