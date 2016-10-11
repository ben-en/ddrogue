import pygame

from .colors import WHITE


def fullscreen_menu(screen, options):
    """
    Creates a menu centered on screen with the options provided.

    Options is expected to be an ordered dict, eg:
        options = OrderedDict()
        options["New Game"] = new_game
        options["Settings"] = settings
        options["Exit"] = quit
    """
    # Create a blank surface to draw the menu on
    menu = pygame.surface.Surface((screen.get_width(), screen.get_height()))
    # Assume the font is initialized, and create a new font object
    menu_font = pygame.font.Font(None, 24)
    # Create images for each option provided
    images = [menu_font.render(x, False, (255, 255, 255)) for x in options]
    # TODO Find the optimal location to start writing the menu
    cursor_start = (menu.get_width()/2 - 50, menu.get_height()/3)

    image_positions = []  # Empty list to hold rects of the images
    x, y = cursor_start
    # Get image positions and blit options onto menu
    for i in images:
        image_positions.append(pygame.rect.Rect([x - 4, y - 4], [100, 20]))
        menu.blit(i, (x, y))
        y += 20

    selected = 0
    # Enter main loop
    while 1:
        # Draw the menu on the screen
        screen.blit(menu, [0, 0])
        # Draw the selection box on the screen
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
                    func = options.values()[image_positions.index(i)]
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
                func = options.values()[selected]
                func(screen)
            elif event.key == 27:  # esc
                break
        else:
            pass
            # print(event)
