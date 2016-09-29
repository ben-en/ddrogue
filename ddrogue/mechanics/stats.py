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


def iterate_stat_list(highest_value, dup_test, start=1, expand_func=None):
    """
    Expects a value to stop at, a function to test the number of times the
    value should be added to the list in addition to the base one, and
    optionally a value to start at.
    """
    stat_list = []
    for i in xrange(start, highest_value):
        if expand_func:
            stat_val = expand_func(i)
        else:
            stat_val = i
        for _ in dup_test(i):
            # For each item in the response, if the value is true, add the
            # stat_val to the list again
            if _:
                stat_list.append(stat_val)
        stat_list.append(stat_val)
    return stat_list


# I wonder if i should add the type of stat it is? eg dex, str, con
Stat = namedtuple('Stat', ['val', 'bonus'])
StatBlock = namedtuple('StatBlock', 'str dex con int wis cha'.split())


class StatBlock(dict):
    """ Mutable, accessible with both attributes and dict items """
    def __init__(self, str, dex, con, int, wis, cha):
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha

    def __setattr__(self, key, val):
        print(key, val)
        dict.__setattr__(self, key, val)
        dict.__setitem__(self, key, val)
