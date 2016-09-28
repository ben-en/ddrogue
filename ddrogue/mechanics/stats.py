from collections import namedtuple


def stat_bonus(stat):
    """ Returns the bonus for a given stat (int) """
    # Values for use in creating tests
    # (6, -2)
    # (7, -2)
    # (8, -1)
    # (9, -1)
    # (10, 0)
    # (11, 0)
    # (12, 1)
    # (13, 1)
    # (14, 2)
    # (15, 2)
    # (16, 3)
    # (17, 3)
    # (18, 4)
    # (19, 4)
    # (20, 5)
    # (21, 5)
    # (22, 6)
    # (23, 6)
    return (stat - 10) / 2


def expand_bab(high_bab):
    """
    Takes an integer and returns a string depending on the BAB, for example:
        fun(11):
            returns [11, 6, 1]
        fun(20):
            returns [20, 15, 10, 5]
    """
    bab_list = []
    modifier = 0
    current_bab = high_bab
    if not high_bab % 5 == 0:
        modifier = current_bab % 5
        current_bab = high_bab - modifier
    if modifier:
        bab_list.append(modifier)
    mult = current_bab / 5
    for i in xrange(0, mult):
        bab_list.append((i + 1) * 5 + modifier)
    return bab_list


def iterate_stat_list(highest_value, dup_test, start=1, is_bab=False):
    """
    Expects a value to stop at, a function to test the number of times the
    value should be added to the list in addition to the base one, and
    optionally a value to start at.
    """
    stat_list = []
    for i in xrange(start, highest_value):
        if is_bab:
            stat_val = expand_bab(i)
        else:
            stat_val = i
        for _ in dup_test(i):
            # For each item in the response, if the value is true, add the
            # stat_val to the list again
            if _:
                stat_list.append(stat_val)
        stat_list.append(stat_val)
    return stat_list


def compile_saves(fort, ref, wis):
    compiled = []
    for i in xrange(0, 20):
        compiled.append((fort[i], ref[i], wis[i]))
    return compiled


# I wonder if i should add the type of stat it is? eg dex, str, con
Stat = namedtuple('Stat', ['base', 'bonus'])
StatBlock = namedtuple('StatBlock', 'str dex con int wis cha'.split())

#########
# Saves #
#########
GOOD_SAVE = iterate_stat_list(13, lambda x: [bool((x > 2) and (x < 12))],
                              start=2)
BAD_SAVE = iterate_stat_list(7, lambda x: [True, bool(x > 0)], start=0)
# >>> print(GOOD_SAVE)
# ['+2', '+3', '+3', '+4', '+4', '+5', '+5', '+6', '+6', '+7', '+7', '+8', '+8', '+9', '+9', '+10', '+10', '+11', '+11', '+12']
# >>> print(BAD_SAVE)
# ['+0', '+0', '+1', '+1', '+1', '+2', '+2', '+2', '+3', '+3', '+3', '+4', '+4', '+4', '+5', '+5', '+5', '+6', '+6', '+6']


#######################
# Base Attack Bonuses #
#######################
HIGH_BAB = [expand_bab(i) for i in xrange(1, 21)]
MED_BAB = iterate_stat_list(16, lambda x: [bool(x % 4 == 0)], start=0,
                            is_bab=True)
LOW_BAB = iterate_stat_list(11, lambda x: [bool((x > 0) and (x < 10))],
                            start=0, is_bab=True)

# >>> print(HIGH_BAB)
# ['+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20']
# >>> print(MED_BAB)
# ['+0', '+0', '+1', '+2', '+3', '+4', '+4', '+5', '+6', '+7', '+8', '+8', '+9', '+10', '+11', '+12', '+12', '+13', '+14', '+15']
# >>> print(LOW_BAB)
# ['+0', '+1', '+1', '+2', '+2', '+3', '+3', '+4', '+4', '+5', '+5', '+6', '+6', '+7', '+7', '+8', '+8', '+9', '+9', '+10']
