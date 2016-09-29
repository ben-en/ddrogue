from .stats import iterate_stat_list


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


#######################
# Base Attack Bonuses #
#######################
HIGH_BAB = [expand_bab(i) for i in xrange(1, 21)]
MED_BAB = iterate_stat_list(16, lambda x: [bool(x % 4 == 0)], start=0,
                            expand_func=expand_bab)
LOW_BAB = iterate_stat_list(11, lambda x: [bool((x > 0) and (x < 10))],
                            start=0, expand_func=expand_bab)

# >>> print(HIGH_BAB)
# ['+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20']
# >>> print(MED_BAB)
# ['+0', '+0', '+1', '+2', '+3', '+4', '+4', '+5', '+6', '+7', '+8', '+8', '+9', '+10', '+11', '+12', '+12', '+13', '+14', '+15']
# >>> print(LOW_BAB)
# ['+0', '+1', '+1', '+2', '+2', '+3', '+3', '+4', '+4', '+5', '+5', '+6', '+6', '+7', '+7', '+8', '+8', '+9', '+9', '+10']
