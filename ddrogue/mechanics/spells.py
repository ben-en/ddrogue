def bonus_spells(bonus, level):
    """
    Returns the number of bonus spells for a given attribute bonus and level

    simple test:
        for y in range(1, 10):
            for x in range(1, 15):
                print('mod', x)
                print('level', y)
                print(bonus_spells(x, y))
                a = raw_input()  # wait for enter
    """
    if level == 0 or bonus == 0 or (bonus - level) < 0:
        return 0
    i = bonus - (level - 1)
    return (i / 4) + (1 if i % 4 else 0)
