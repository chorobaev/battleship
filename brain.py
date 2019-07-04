import random
import datetime

import objects


def get_random_player():
    """
    Creates a Player object with a random map
    :return: Player
    """
    player = objects.Player()
    ships = objects.get_list_of_ships()

    j = 0
    for ship in ships:
        i = 0
        j += 1
        while not __is_added(player, ship):
            i += 1

    return player


def __is_added(player, ship):
    """
    :param player: Player - an object Player
    :param ship: Ship - a ship that has to be tried to put on the map of Player
    :return: True if the given ship has been put successfully
    """
    random.seed(datetime.datetime.now().microsecond)

    orientation = random.randint(1, 2)
    if orientation == objects.HORIZONTAL:
        x = random.randint(1, 11 - ship)
        y = random.randint(1, 10)
    else:
        x = random.randint(1, 10)
        y = random.randint(1, 11 - ship)

    return player.add_ship(objects.Ship(ship, orientation, x, y))
