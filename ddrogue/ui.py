from collections import OrderedDict
from textwrap import wrap

import pygame
from pygame.rect import Rect

from .colors import BLACK, GREY, WHITE, BLUE, LIGHT_BLUE


def create_tile(color, xy):
    """ Takes a color and a height/width pair and returns a surface object """
    new_img = pygame.Surface(xy)
    new_img.fill(GREY)
    new_img.fill(color, rect=[1, 1, xy[0] - 2, xy[1] - 2])
    return new_img


def str_bonus(val, just=3):
    """ Returns a justified stringed bonus. eg '3' returns ' +3' by default """
    if val >= 0:
        bonus = '+%s' % val
    else:
        bonus = str(val)
    return bonus.rjust(just)


def confirm(screen):
    """ user dialog, ask yes/no """
    options = OrderedDict()
    options['Yes'] = True
    options['No'] = False
    res = fullscreen_menu(screen, options)
    return options.get(res, False)


def multi_panel_ui(screen, panels):
    """
    For each panel presented, expect a panel that functions similarly to pick
    or the player HUD.

    Attributes:
        pos
        img
    Methods:
        event_handler
        resolve


    Specifically, they should have size/location rects, a list of clickable
    areas coupled with the function to execute if the area is clicked, and
    probably their own selections.

    Primary use case is in character generation, where skills need to be
    +/-'able, abilities should be rerollable, classess and races need to be
    selectable, and most fields need a hover feature to display help info

    In theory if implemented properly, could also handle the main game screen.
    Or something that copies a lot of the main functionality could handle the
    main game screen.

    """
    panel_areas = [Rect(p.pos, p.img.get_size()) for p in panels]
    area = 0
    # Enter main loop
    while 1:
        screen.fill(BLACK)
        # Draw the panels on the screen
        for p in panels:
            screen.blit(p.img, p.pos)
        pygame.draw.rect(screen, LIGHT_BLUE, panel_areas[area], 2)
        pygame.display.flip()

        # Wait for the next state
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            print('keycode: ', event.key)
            print('key: ', chr(event.key))
            if event.key == 27:  # esc
                if confirm(screen):
                    break
            elif event.key == ord('\t'):
                area += 1
                if area >= len(panels):
                    area = 0
                elif area < 0:
                    area = len(panels) - 1
                continue
        elif event.type == pygame.QUIT:
            break
        elif event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            for index in range(len(panel_areas)):
                if panel_areas[index].collidepoint(event.pos):
                    area = index
                    panels[index].event_handler(event)
                    continue
        panels[area].event_handler(event)
    # When finished in the while loop, return selected values
    return [p.resolve() for p in panels]


def select_loop(screen, selectable):
    selected = 0
    # Enter main loop
    while 1:
        screen.fill(BLACK)
        # Draw the img on the screen
        screen.blit(selectable.img, selectable.top_left)
        # Draw the selection box on the screen
        pygame.draw.rect(screen, selectable.select_color,
                         selectable.positions[selected], 2)
        # Flip the staging area to the display
        pygame.display.flip()

        # TODO make action loop separate from the menu so controls can be
        # customized
        # Wait for the next state
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            # TODO DRY
            for i in selectable.positions:
                if i.collidepoint(event.pos):
                    return selectable.positions.index(i)
        elif event.type == pygame.MOUSEMOTION:
            for i in selectable.positions:
                if i.collidepoint(event.pos):
                    selected = selectable.positions.index(i)
        elif event.type == pygame.KEYUP:
            print('keycode', event.key)
            if event.key == 273:  # up
                selected -= 1
                if selected < 0:
                    selected = len(selectable.positions) - 1
            elif event.key == 274:  # down
                selected += 1
                if selected >= len(selectable.positions):
                    selected = 0
            elif event.key == 13:  # enter
                return selected
            elif event.key == 27:  # esc
                return None
        else:
            pass
            # print(event)


class Selectable(object):
    """
    Object that has an img, a list of selectable areas mapped to functions,
    """
    def __init__(self, img, positions, top_left=(0, 0), text_color=WHITE,
                 select_color=BLUE):
        self.img = img
        self.positions = positions
        self.top_left = top_left
        self.text_color = text_color
        self.select_color = select_color


def fullscreen_menu(screen, options, **kwargs):
    # blank the screen
    screen.fill(BLACK)
    return menu(screen, options, **kwargs)


def menu(screen, options, xy=(1000, 1000), top_left=(0, 0), text_color=WHITE,
         font=None, select_color=BLUE,
         loop_func=select_loop):
    """
    Generic selection menu

    TODO make more generic

    TODO make selected separate from highlighted, allowing user to hover over
    other elements and view descriptions for them and preserve their selection.

    TODO use txt_to_img to create the img instead of duplicating
    """
    # Font
    font = font or pygame.font.Font(None, 24)
    # Create a blank surface to draw the menu on
    menu_img = pygame.surface.Surface(xy)
    # Create imgs for each option provided
    option_keys = options.keys()
    imgs = [font.render(x, False, text_color) for x in options]
    # TODO Find the optimal location to start writing the menu
    cursor_start = (10, 10)
    img_positions = []  # Empty list to hold rects of the imgs
    x, y = cursor_start
    # Get img positions and blit options onto menu
    for i in imgs:
        select_box = Rect(x - 4 + top_left[0], y - 4 + top_left[1], 100, 20)
        img_positions.append(select_box)
        menu_img.blit(i, (x, y))
        y += 20

    selectable = Selectable(menu_img, img_positions, top_left, text_color,
                            select_color)

    res = select_loop(screen, selectable)
    if res is None:
        # If player hit escape, return None
        return None
    return option_keys[res]


def render_text(screen, text_file):
    """ Render the text file on the screen in a readable format """
    # Add a header that shows the path of the text file so the user can look it
    # up for manual inspection at their discretion
    text = ['loaded from: %s' % text_file, '']
    with open(text_file, 'r') as input:
        for l in input.readlines():
            text.append(l)
    img = text_to_img(screen.get_width(), text)
    navigable_loop(screen, img, start_pos=-1)


def text_to_img(width, lines):
    """ Put lines on an img that would fit within the screen """
    # Initialize the font
    text_font = pygame.font.Font(None, 18)
    # Calculate the number of characters that can be shown on one row
    characters = (width - 10) / 7
    text = ['']
    for l in lines:
        text += wrap(l, characters)
        # Add an extra space to clearly show a new line in the file
        text += ['']

    # Create an img the size of the text
    img = pygame.surface.Surface((width, len(text) * 15))

    # Write the text onto the img
    x, y = 0, 0
    for t in text:
        img.blit(text_font.render(t, False, WHITE), (x, y))
        y += 15

    return img


def navigable_loop(screen, img, start_pos=0):
    # Disply the img
    bottom = - (img.get_height() - screen.get_height())
    if start_pos == -1:
        start_pos = bottom
    x, y = 5, start_pos
    while 1:
        screen.blit(img, (x, y))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            # Esc key or ??
            # TODO figure out keycode 13
            if event.key in [27, 13]:
                break
            # Arrow keys
            if event.key == 273:
                y += 30
                if y >= 0:
                    # If you're trying to scroll too high, reset to 0
                    y = 0
            if event.key == 274:
                y -= 30
                if y <= bottom:
                    # If you're trying to scroll to low, reset to bottom
                    y = bottom
            # TODO page up/down
