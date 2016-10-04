import sys
from textwrap import wrap

import pygame

from .colors import WHITE
from .game import new_game


def load_text(screen, text_file):
    text_font = pygame.font.Font(None, 18)
    characters = (screen.get_width() - 10) / 7

    text = ['loaded from: %s' % text_file, '']
    with open(text_file, 'r') as input:
        for l in input.readlines():
            text += wrap(l, characters)
            text += ['']

    image = pygame.surface.Surface((screen.get_width(), len(text) * 15))

    x, y = 0, 0
    for t in text:
        image.blit(text_font.render(t, False, (255, 255, 255)), (x, y))
        y += 15

    x, y = cursor = 5, 5
    bottom = image.get_height() - screen.get_height()
    while 1:
        screen.blit(image, (x, y))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYUP:
            if event.key in [27, 13]:
                break
            if event.key == 273:
                y += 30
                if y >= 0:
                    y = cursor[0]
            if event.key == 274:
                y -= 30
                if y <= - bottom:
                    y = - (bottom + 5)


def settings(screen):
    pass


def guide(screen):
    load_text(screen, './ogc/mechanics.txt')


def legal(screen):
    """ Loads legal text """
    load_text(screen, './ogc/license.txt')


def quit(_):
    sys.exit()


def main_menu(screen):
    options = ["New Game", "Settings", "Guide", "Legal", "Exit"]
    option_funcs = [new_game, settings, guide, legal, quit]

    menu_font = pygame.font.Font(None, 24)
    selected = 0
    images = [menu_font.render(x, False, (255, 255, 255)) for x in options]
    image_positions = []
    cursor_start = (screen.get_width()/2 - 50, screen.get_height()/3)
    menu = pygame.surface.Surface((screen.get_width(), screen.get_height()))

    # Get image positions
    x, y = cursor_start
    for i in images:
        image_positions.append(pygame.rect.Rect([x - 4, y - 4], [100, 20]))
        menu.blit(i, (x, y))
        y += 20

    # Enter main loop
    while 1:
        screen.blit(menu, [0, 0])
        pygame.draw.rect(screen, WHITE, image_positions[selected], 2)
        # Flip the staging area to the display
        pygame.display.flip()
        # Wait for the next state
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            # TODO DRY
            for i in image_positions:
                if i.collidepoint(event.pos):
                    func = option_funcs[image_positions.index(i)]
                    func(screen)
        elif event.type == pygame.MOUSEMOTION:
            for i in image_positions:
                if i.collidepoint(event.pos):
                    selected = image_positions.index(i)
        elif event.type == pygame.KEYUP:
            if event.key == 273:  # up
                selected -= 1
                if selected < 0:
                    selected = len(image_positions) - 1
            elif event.key == 274:  # down
                selected += 1
                if selected >= len(image_positions):
                    selected = 0
            elif event.key == 13:  # enter
                func = option_funcs[selected]
                func(screen)
            elif event.key == 27:  # esc
                break
        else:
            pass
            #print(event)
