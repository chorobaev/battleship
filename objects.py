from exceptions import ShipException
from res import MyExceptions as Errors
import res

BATTLESHIP = 4
CRUISER = 3
DESTROYER = 2
SUBMARINE = 1
HORIZONTAL = 1
VERTICAL = 2


def get_list_of_ships():
    """
    return: All names of ships that must be created
    """
    return res.LIST_OF_SHIPS


class Ship(object):

    def __init__(self, tp: int, orientation: int, init_x: int, init_y: int) -> None:
        """
        :param tp: int (1-4) - which type is a ship(BATTLESHIP, CRUISER, DESTROYER, SUBMARINE)
        :param orientation: int (1 or 2) - orientation of a ship (VERTICAL, HORIZONTAL)
        :param init_y: int (1-10): X upper right coordinate of a ship
        :param init_y: int (1-10): Y upper right coordinate of a ship
        """
        self.__type = tp
        self.__orientation = orientation
        self.__coordinate_x = []
        self.__coordinate_y = []
        self.__destroyed = []
        self.__health = tp

        # Check weather given ship is not out of the map
        if 1 <= init_x <= 10 and 1 <= init_y <= 10 and \
                (orientation == HORIZONTAL and init_x + tp <= 11 or orientation == VERTICAL and init_y + tp <= 11):

            for i in range(self.__type):                    # Init coordinates Id and Destroyed param

                if orientation == HORIZONTAL:               # Sets coordinates depending on orientation
                    self.__coordinate_x.append(init_x + i)
                    self.__coordinate_y.append(init_y)
                else:
                    self.__coordinate_x.append(init_x)
                    self.__coordinate_y.append(init_y + i)

                self.__destroyed.append(False)              # Setting coordinateIds and destroyed bool list
        else:
            # Raises an Error
            raise ShipException("Ship is out of map", Errors.MAP_ERROR)

    def __str__(self):
        """
        :return: type, orientation, coordinates, destroyed sells
        """
        coors = "Coordinates: "
        destroyed_sells = "Destroyed sells: "
        for i in range(self.__type):
            coors += "(" + str(self.__coordinate_x[i]) + ", " + str(self.__coordinate_y[i]) + ") "
            destroyed_sells += str(self.__destroyed[i]) + ", "

        string = "Type: " + str(self.__type) + "\nOrientation: " \
                 + str(self.__orientation) + "\n" + coors + "\n" + destroyed_sells

        return string

    def get_type(self):
        """
        :return: int [1, 4] - type of the ship
        """
        return self.__type

    def hit(self, x, y):
        """
        Hit the part of the ship on the given coors
        :param x: int (1-10) - X coordinate to check
        :param y: int (1-10) - Y coordinate to check
        :return: True if some part of the ship is destroyed, False otherwise
        """
        result = -1
        for i in range(self.__type):
            if x == self.__coordinate_x[i] and y == self.__coordinate_y[i]:
                result = i
                break

        if result != -1 and not self.__destroyed[result]:
            self.__destroyed[result] = True
            return True

        return False

    def mark_on_map(self, map_to_mark_on: list, ship_id: int):
        """
        Marks the ship to the given map
        :param map_to_mark_on: map 10x10 list
        :param ship_id: int - id of the ship
        :return: None
        """
        x = self.__coordinate_x
        y = self.__coordinate_y
        for i in range(self.__type):
            map_to_mark_on[x[i]][y[i]] = ship_id

            if map_to_mark_on[x[i] - 1][y[i]] == 0:
                map_to_mark_on[x[i] - 1][y[i]] = '.'
            if map_to_mark_on[x[i] + 1][y[i]] == 0:
                map_to_mark_on[x[i] + 1][y[i]] = '.'
            if map_to_mark_on[x[i]][y[i] - 1] == 0:
                map_to_mark_on[x[i]][y[i] - 1] = '.'
            if map_to_mark_on[x[i]][y[i] + 1] == 0:
                map_to_mark_on[x[i]][y[i] + 1] = '.'
            if map_to_mark_on[x[i] - 1][y[i] - 1] == 0:
                map_to_mark_on[x[i] - 1][y[i] - 1] = '.'
            if map_to_mark_on[x[i] + 1][y[i] + 1] == 0:
                map_to_mark_on[x[i] + 1][y[i] + 1] = '.'
            if map_to_mark_on[x[i] + 1][y[i] - 1] == 0:
                map_to_mark_on[x[i] + 1][y[i] - 1] = '.'
            if map_to_mark_on[x[i] - 1][y[i] + 1] == 0:
                map_to_mark_on[x[i] - 1][y[i] + 1] = '.'

    def is_possible_put_onto_map(self, map_to_mark_on: list):
        """
        :param map_to_mark_on: Player map 10x10 list
        :return: True if it is possible to put onto the given map, False otherwise
        """
        x = self.__coordinate_x
        y = self.__coordinate_y
        for i in range(self.__type):
            if map_to_mark_on[x[i]][y[i]] != 0:
                return False
        return True

    def get_status(self):
        """
        :return: True if this ship is not destroyed, else False
        """
        for i in range(self.__type):
            if not self.__destroyed[i]:
                return True
        return False

    def get_x_at(self, index: int):
        """
        :param index: int - the index
        :return: return coordinate X at the given index
        """
        return self.__coordinate_x[index]

    def get_y_at(self, index: int):
        """
        :param index: int - the index
        :return: return coordinate Y at the given index
        """
        return self.__coordinate_y[index]


class Player(object):

    def __init__(self):
        # Amount of ships for each type: NONE, 1: SUBMARINE, 2: DESTROYER, 3: CRUISER, 4: BATTLESHIP
        self.__shipsAmount = [None, 0, 0, 0, 0]
        # List of ships: [0]: BATTLESHIP, [1, 2]: CRUISER, [3, 5]: DESTROYER, [6, 9]: SUBMARINE
        self.__ships = [None, None, None, None, None,
                        None, None, None, None, None, None]
        # Map of the player
        self.__map = []

        # Creates empty map, 0: empty space, 1: ship, indexes = [1, 10]
        for i in range(12):
            row = []
            for j in range(12):
                row.append(0)
            self.__map.append(row)

    def __str__(self):

        string = ""
        for i in range(10):
            string += "\nShip #" + str(i+1) + " >>>>>>>>>>>>>>>>>>>>>>>\n" + str(self.__ships[i+1])

        return string

    def get_point_on_map(self, x: int, y: int):
        """
        :param x: int - X coordinate of the map
        :param y: int - y coordinate of the map
        :return:
        """
        return self.__map[x][y]

    def get_non_placed_amount(self, tp: int):
        """
        :param tp: int - type of the ship
        :return: int - amount of the given type
        """
        return 5 - tp - self.__shipsAmount[tp]

    def is_some_ships_placed(self):
        """
        :return: True if at list one ship is placed else False
        """
        for i in range(1, 11):
            if self.__ships[i] is not None:
                return True
        return False

    def is_completed(self):
        """
        :return: True if player's all ships put on the map, False otherwise
        """
        for i in range(1, 11):
            if self.__ships[i] is None:
                return False
        return True

    def show_map(self):
        """
        Prints the player's map X = [1, 10], Y = [1, 10]
        :return: None
        """
        for i in range(1, 11):
            for j in range(1, 11):
                print(self.__map[i][j], end=" ")
            print()

    def remove_ship(self, index: int):
        """
        Removes the ship at the given point
        :param index: int - index of the ship
        :return: None
        """
        self.__ships[index] = None
        if index == 1:
            tp = 4
        elif index in (2, 3):
            tp = 3
        elif index in (4, 5, 6):
            tp = 2
        else:
            tp = 1
        self.__shipsAmount[tp] -= 1

    def add_ship(self, ship: Ship):
        """
        :param ship: Ship - a ship which have to be added
        :return: True if the given ship placed successfully, False otherwise
        """
        tp = ship.get_type()
        amount = self.__shipsAmount[tp]

        if amount >= 5 - tp:
            raise ShipException("All " + str(tp) + "type ships have already placed", res.MyExceptions.MAP_ERROR)

        # Check adding possibilities
        if amount < 5 - tp and ship.is_possible_put_onto_map(self.__map):
            ship_id = amount + sum([i for i in range(5 - tp)]) + 1
            self.__ships[ship_id] = ship
            self.__shipsAmount[tp] += 1
            ship.mark_on_map(self.__map, ship_id)
            return True

        return False

    def get_ship(self, index: int):
        """
        :return: list of Ships - ships of this player
        """
        return self.__ships[index]
