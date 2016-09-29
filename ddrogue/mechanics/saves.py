from .stats import iterate_stat_list


def compile_saves(fort, ref, wis):
    compiled = []
    for i in xrange(0, 20):
        compiled.append((fort[i], ref[i], wis[i]))
    return compiled


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
