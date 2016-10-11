from collections import namedtuple


Stat = namedtuple('Stat', ['val', 'bonus'])


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
        if expand_func:  # Used in bab calculations, replacing 9 with [9, 4]
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


def ensure_stat(stat):
    if type(stat) == int:
        return Stat(stat, stat_bonus(stat))
    try:
        if 'val' in stat._fields and 'bonus' in stat._fields:
            return stat
    except AttributeError:
        pass
    try:
        i = int(stat)
        return Stat(i, stat_bonus(i))
    except TypeError as e:
        # TODO use logging for this
        print('ERROR: unable to coerce value %s to Stat object' % stat)
        raise e


class StatBlock(dict):
    """ Mutable, accessible with both attributes and dict items """
    def __init__(self, l=None, str=0, dex=0, con=0, int=0, wis=0, cha=0):
        if l and len(l) == 6:
            self.str = ensure_stat(l[0])
            self.dex = ensure_stat(l[1])
            self.con = ensure_stat(l[2])
            self.int = ensure_stat(l[3])
            self.wis = ensure_stat(l[4])
            self.cha = ensure_stat(l[5])
        elif str and dex and con and int and wis and cha:
            self.str = ensure_stat(str)
            self.dex = ensure_stat(dex)
            self.con = ensure_stat(con)
            self.int = ensure_stat(int)
            self.wis = ensure_stat(wis)
            self.cha = ensure_stat(cha)

    def __setattr__(self, key, val):
        dict.__setattr__(self, key, val)
        dict.__setitem__(self, key, val)
