from time import sleep

import pygame
from pygame.rect import Rect

from ..colors import RED_T, LIGHT_BLUE
from ..constants import SCREEN
from ..pathfinding import astar


COMBAT_ACTIONS = {}


def grid_select(state, start_pos, steps, area_func=None, end_pos_func=None,
                color=LIGHT_BLUE):
    """
    A function that displays a grid on the screen and only returns if the
    clicked point is within the grid list.

    Can be given an area_func to determine what area is allowed to be clicked
    on. Defaults to state.map.movable_area
    """
    x, y = start_pos
    rect_list = []
    if not area_func:
        area_func = state.map.movable_area
    pos_list = area_func(start_pos, steps)
    for p in pos_list:
        pixel_p = state.map.pixel_pos((x - p[0], y - p[1]))
        offset_p = ((state.map.ui_size[0] / 2) - pixel_p[0],
                    (state.map.ui_size[1] / 2) - pixel_p[1])
        rect_list.append(Rect(offset_p, state.map.unit_t))
    state.draw()
    end_pos_found = False
    for i in range(len(pos_list)):
        p = pos_list[i]
        r = rect_list[i]
        if end_pos_func:
            if end_pos_func(p):
                pygame.draw.rect(SCREEN, color, r, 2)
                end_pos_found = True
        else:
            pygame.draw.rect(SCREEN, color, r, 2)
    if end_pos_func and not end_pos_found:
        state._print('End position not found, cannot perform action')
        pygame.display.flip()
        return
    pygame.display.flip()
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == 27:  # esc
                return None
        if event.type == pygame.MOUSEBUTTONUP:
            r = Rect(event.pos, (1, 1))
            index = r.collidelist(rect_list)
            if not index == -1:
                return pos_list[index]


def move_to(state, char, pos, steps=None):
    """
    Using state's access to the map, move given `char` to `pos`, max `steps`
    """
    path = astar(state.map.floor.transpose(), tuple(char.pos), tuple(pos))
    # For some reason astar figures the path backwards. Dunno why,
    path.reverse()
    if steps:
        path = path[:steps]
    for step in path:
        char.pos = step
        state.draw()
        sleep(0.1)


def resolve_attack(state, defender):
    state._print('%s attacking %s' % (state.char.s, defender.s))


# Combat actions
def combat_action(func):
    COMBAT_ACTIONS[func.__name__] = func
    return func


@combat_action
def attack(state):
    if not state.char.standard_action:
        state._print('No standard action available')
        return
    state._print('Attack who?')
    enemy = None
    weapon = state.char.equipment[state.char.equipped['r_hand']]
    if 'reach' in weapon.tags:
        range = 2
    else:
        range = 1
    while not enemy:
        grid_pos = grid_select(state, state.char.pos, range,
                               end_pos_func=state.map.enemy_adjacent,
                               COLOR=RED_T)
        if not grid_pos:
            state._print('Aborting')
            break
        for npc in state.npcs:
            if npc.pos == grid_pos:
                enemy = npc
    state._print('selected %s' % enemy.s)
    resolve_attack(state, npc)


@combat_action
def withdraw(state):
    """
    a full round action that prevents attacks of opportunity by aby characters
    in reach when the movement is started. other enemies attack normally
    """
    if not (state.char.standard_action and state.char.move_action):
        state._print('Withdrawing is a full round action, you do not have'
                     'enough actions to perform a full round action.')
        return
    state._print('Withdrawing')
    move_pos = grid_select(state, state.char.pos, state.char.speed * 2)
    # No 5ft step after, full round action so no move or standard actions.
    # Swift action is the same.
    move_to(state, state.char, move_pos)
    state.char.moved = 1
    state.char.standard_action = 0
    state.char.move_action = 0


def total_defense_debuff(state):
    """ reduce AC to normal """
    state.char.ac -= 4


@combat_action
def total_defense(state):
    """
    full round action that gives +4 dodge bonus to ac
    """
    if not (state.char.standard_action and state.char.move_action):
        state._print('Total defense is a full round action, you do not have'
                     'enough actions to perform a full round action.')
        return
    state._print('Total defense')
    state.char.ac += 4
    # Next turn reduce AC to normal
    state.char.effects[0] = total_defense_debuff
    state.char.standard_action = 0


@combat_action
def five_foot_step(state):
    """
    free action that may be taken when a character has made no other nove
    actions and is not specially prohobited from taking it
    """
    if state.char.moved:
        state._print('You have already moved this turn.')
        return
    state._print('Five foot step')
    grid_select(state, state.char.pos, 1)
    state.char.moved = 1


@combat_action
def move(state):
    """
    full round action to move at 4x speed
    """
    if not state.char.move_action:
        state._print('No move action available.')
        return
    state._print('Select where you\'d to move to')
    while 1:
        move_pos = grid_select(state, state.char.pos, state.char.speed)
        if not move_pos:
            state._print('aborted')
            return
        if not state.map.is_occupied(move_pos):
            break
        else:
            state._print('Can\'t move there')
    move_to(state, state.char, move_pos)
    state.char.moved = 1
    state.char.move_action = 0


@combat_action
def run(state):
    """
    full round action to move at 4x speed
    """
    if not (state.char.standard_action and state.char.move_action):
        state._print('Run is a full round action, you do not have'
                     'enough actions to perform a full round action.')
        return
    state._print('Run')
    grid_select(state, state.char.pos, state.char.speed * 4)
    state.char.moved = 1
    state.char.standard_action = 0
    state.char.move_action = 0


@combat_action
def charge(state):
    """
    full round action that lets you move up to twice your speed in a straight
    line then attack
    """
    if not (state.char.standard_action and state.char.move_action):
        state._print('Charge is a full round action, you do not have'
                     'enough actions to perform a full round action.')
        return
    state._print('Charge')
    npc = None
    while not npc:
        move_pos = grid_select(state, state.char.pos, (state.char.speed * 4),
                               end_pos_func=state.map.enemy_adjacent)
        if not move_pos:
            state._print('aborted')
            return
        npc = state.map.obj_at(move_pos)
        if npc and not npc.hostile:
            if not state.output.ask('Are you sure you want to attack a '
                                    'non-hostile npc?'):
                npc = None
    resolve_attack(state, npc)
    state.char.moved = 1
    state.char.standard_action = 0
    state.char.move_action = 0


@combat_action
def stand_up(state):
    """
    move action that provokes an attack of opportunity
    """
    print('not implemented')


@combat_action
def aid_another(state):
    """
    +2 to an ally's attack or ac against an enemy
    """
    print('not implemented')


@combat_action
def bull_rush(state):
    """
    combat maneuver to push an enemy
    """
    print('not implemented')


@combat_action
def disarm(state):
    """
    combat maneuver to force an enemu to drop their equopped weapon
    """
    print('not implemented')


@combat_action
def overrun(state):
    """
    attempt to force through an enemy's square
    """
    print('not implemented')


@combat_action
def trip(state):
    """
    try to trip an enemy, knocking them prone
    """
    print('not implemented')


@combat_action
def feint(state):
    """
    trick your opponent and knock the off balance,leaving them flatfooted
    against your next attack
    """
    print('not implemented')


@combat_action
def grapple(state):
    """
    initiate a grapple with the chosen enemy
    """
    print('not implemented')


@combat_action
def throw(state):
    """
    throw something at the enemy
    """
    print('not implemented')


@combat_action
def ready(state):
    """
    prepare a spear, counterspell, bow, or similar
    """
    print('not implemented')


@combat_action
def delay(state):
    """
    delay your action until later in the initiative order
    """
    print('not implemented')
