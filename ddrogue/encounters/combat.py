from time import sleep

import pygame
from pygame.rect import Rect

from ..colors import RED_T, LIGHT_BLUE
from ..pathfinding import astar


def grid_select(state, start_pos, steps, end_pos_func=None, COLOR=LIGHT_BLUE):
    x, y = start_pos
    speed = steps
    speed_offset = speed/2 + (1 if (speed % 2) else 0)
    pos_list = []
    rect_list = []
    for i in range(speed + 1):
        for n in range(speed + 1):
            p = ((x + i - speed_offset), (y + n - speed_offset))
            pos_list.append(p)
            pixel_p = tuple(axis * state.map.unit for axis in p)
            rect_list.append(Rect(pixel_p, state.map.unit_t))
    state.draw()
    end_pos_found = False
    for i in range(len(pos_list)):
        p = pos_list[i]
        r = rect_list[i]
        if end_pos_func:
            if end_pos_func(p):
                pygame.draw.rect(state.screen, COLOR, r, 1)
                end_pos_found = True
        else:
            pygame.draw.rect(state.screen, COLOR, r, 1)
    pygame.display.flip()
    if end_pos_func and not end_pos_found:
        state._print('End position not found, cannot perform action')
        return
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key == 27:  # esc
                return None
        if event.type == pygame.MOUSEBUTTONUP:
            r = Rect(event.pos, (1, 1))
            index = r.collidelist(rect_list)
            if not index == -1:
                return state.map.grid_pos(event.pos)


def move_to(state, char, pos, steps=None):
    """
    Using state's access to the map, move given `char` to `pos`, max `steps`
    """
    path = astar(state.map.floor.transpose(), tuple(char.pos), tuple(pos))
    # For some reason astar figures the path backwards. Dunno why,
    path.reverse()
    if steps:
        path = path[:steps]
    state._print(', '.join([str(p) for p in path]))
    for step in path:
        char.pos = step
        state._print(str(char.pos))
        state._print(str(state.char.pos))
        state.draw()
        sleep(0.1)


def attack_ui(state, steps):
    state._print('attack ui starting')
    enemy = None
    while not enemy:
        grid_pos = grid_select(state, state.char, steps,
                               end_pos_func=state.map.enemy_adjacent,
                               COLOR=RED_T)
        for npc in state.npcs:
            if npc.pos == grid_pos:
                enemy = npc
    attack(state, npc)


def attack(state, defender):
    state._print('%s attacking %s' % (state.char.s, defender.s))


# Combat actions
def withdraw(state):
    """
    a full round action that prevents attacks of opportunity by aby characters
    in reach when the movement is started. other enemies attack normally
    """
    state._print('Withdrawing')
    grid_select(state, state.char.speed * 2)
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
    grid_select(state.char, 1)
    state.actions[0] = 0


def move(state):
    """
    full round action to move at 4x speed
    """
    state._print('Select where you\'d to move to')
    while 1:
        move_pos = grid_select(state, state.char, state.char.speed)
        if not move_pos:
            state._print('aborted')
            return
        if not state.map.is_occupied(move_pos):
            break
        else:
            state._print('Can\'t move there')
    move_to(state, state.char, move_pos)
    state.actions[0] = 0
    state.actions[1] = 0


def run(state):
    """
    full round action to move at 4x speed
    """
    state._print('Run')
    grid_select(state.char, state.char.speed * 4)
    state.actions = [0, 0, 0, state.actions[3]]


def charge(state):
    """
    full round action that lets you move up to twice your speed in a straight
    line then attack
    """
    state._print('Charge')
    npc = None
    while not npc:
        move_pos = grid_select(state, state.char, (state.char.speed * 4),
                               end_pos_func=state.map.enemy_adjacent)
        if not move_pos:
            state._print('aborted')
            return
        npc = state.map.obj_at(move_pos)
        if npc and not npc.hostile:
            if not state.output.ask('Are you sure you want to attack a '
                                    'non-hostile npc?'):
                npc = None
    attack_ui(state.char, npc)
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
