def move_down(coordinate_object, unit):
    """ Move the given object down by adding one from the given y value.
    """
    coordinate_object.y += unit


def move_up(coordinate_object, unit):
    """ Move the given object up by subracting one from the given y value.
    """
    coordinate_object.y -= unit


def move_left(coordinate_object, unit):
    """ Move the given object left by subracting one from the given x value.
    """
    coordinate_object.x -= unit


def move_right(coordinate_object, unit):
    """ Move the given object right by adding one from the given x value.
    """
    coordinate_object.x += unit
