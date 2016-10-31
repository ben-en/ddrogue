from .ui import move_ui, attack_ui


def withdraw(state):
    """
    a full round action that prevents attacks of opportunity by aby characters
    in reach when the movement is started. other enemies attack normally
    """
    state._print('Withdrawing')
    move_ui(state, state.char.speed * 2)
    # No 5ft step after, full round action so no move or standard actions.
    # Swift action is the same.
    state.actions = [0, 0, 0, state.actions[3]]


def total_defense_debuff(state):
    """ reduce AC to normal """
    state.char.ac -= 4


def total_defense(state):
    """
    full round action that gives +4 dodge bonus to ac
    """
    state._print('Total defense')
    state.char.ac += 4
    # Next turn reduce AC to normal
    state.char.effects[0] = total_defense_debuff
    state.actions[2] = 0


def stand_up(state):
    """
    move action that provokes an attack of opportunity
    """
    print('not implemented')


def five_foot_step(state):
    """
    free action that may be taken when a character has made no other nove
    actions and is not specially prohobited from taking it
    """
    state._print('Five foot step')
    move_ui(state.char, 1)
    state.actions[0] = 0


def move(state):
    """
    full round action to move at 4x speed
    """
    state._print('Regular move')
    move_ui(state, state.char, state.char.speed)
    state.actions[0] = 0
    state.actions[1] = 0


def run(state):
    """
    full round action to move at 4x speed
    """
    state._print('Five foot step')
    move_ui(state.char, state.char.speed * 4)
    state.actions = [0, 0, 0, state.actions[3]]


def charge(state):
    """
    full round action that lets you move up to twice your speed in a straight
    line then attack
    """
    state._print('Five foot step')
    move_ui(state.char, state.char.speed * 4,
            end_pos_func=state.map.enemy_adjacent)
    attack_ui(state.char)
    state.actions = [0, 0, 0, state.actions[3]]


def aid_another(state):
    """
    +2 to an ally's attack or ac against an enemy
    """
    print('not implemented')


def bull_rush(state):
    """
    combat maneuver to push an enemy
    """
    print('not implemented')


def disarm(state):
    """
    combat maneuver to force an enemu to drop their equopped weapon
    """
    print('not implemented')


def grapple(state):
    """
    initiate a grapple with the chosen enemy
    """
    print('not implemented')


def overrun(state):
    """
    attempt to force through an enemy's square
    """
    print('not implemented')


def trip(state):
    """
    try to trip an enemy, knocking them prone
    """
    print('not implemented')


def feint(state):
    """
    trick your opponent and knock the off balance,leaving them flatfooted
    against your next attack
    """
    print('not implemented')


def throw(state):
    """
    throw something at the enemy
    """
    print('not implemented')


def ready(state):
    """
    prepare a spear, counterspell, bow, or similar
    """
    print('not implemented')
