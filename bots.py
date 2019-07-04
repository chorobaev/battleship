from res import Strings as String
import random as rd
import datetime as dt


class Fati(object):

    def __init__(self):

        self.__x = 0
        self.__y = 0
        self.__last_ship = []
        self.__time = 0

        # Setting up an empty array
        self.__mp = []  # True if the field is hit else False
        for y in range(12):
            row = []
            for x in range (12):
                row.append(False)
            self.__mp.append(row)

    def say(self, sms: str):
        """
        :param sms: str - the command, what should do the bot
        :return: tuple of two int - (x, y) coordinates
        """
        result = None
        if sms == String.GameFrame.BOT_SHOOT:
            result = self.__shoot()

        elif sms == String.GameFrame.BOT_HIT:
            if self.__time != 0:
                self.__last_ship.append((self.__x, self.__y))
            result = self.__hit()

        elif sms == String.GameFrame.BOT_DESTROYED:
            self.__last_ship.append((self.__x, self.__y))
            result = self.__destroyed()

        self.__time += 1
        print(">>> Bot1: shoot #%d - (%d, %d)" % (self.__time, result[0], result[1]))
        return result

    def __shoot(self):
        """
        Calls when the bot receives "shoot" command
        :return: tuple of two ints - x and y, coordinate of the bot's chose
        """
        if not self.__last_ship:
            x = self.__random(1, 10)
            y = self.__random(1, 10)

            if not self.__mp[y][x]:
                self.__x = x
                self.__y = y

                self.__mp[y][x] = True
                self.__print_map()
                return x, y

            return self.__shoot()
        else:
            return self.__hit()

    def __hit(self):
        """
        Calls when the bot receives "hit" command
        :return: tuple of two ints - x and y, coordinate of the bot's chose
        """
        print("Bot's hit last ship: ", self.__last_ship)
        result = ()

        if len(self.__last_ship) == 1:
            result = self.__get_one_of_four()

        elif len(self.__last_ship) > 1:
            if self.__last_ship[0][0] != self.__last_ship[1][0]:  # is horizontal
                result = self.__get_right_or_left()
            else:
                result = self.__get_top_or_bottom()

        self.__x = result[0]
        self.__y = result[1]

        self.__mp[result[1]][result[0]] = True
        return result

    def __get_one_of_four(self):
        """
        :return: tuple of two ints - top, bottom, left or right of the hit point
        """
        where = self.__random(1, 4)  # 1 - top, 2 - bottom, 3 - left, 4 - right

        result = None
        if where == 1 and self.__last_ship[0][1] > 1:
            result = self.__last_ship[0][0], self.__last_ship[0][1] - 1

        elif where == 2 and self.__last_ship[0][1] < 10:
            result = self.__last_ship[0][0], self.__last_ship[0][1] + 1

        elif where == 3 and self.__last_ship[0][0] > 1:
            result = self.__last_ship[0][0] - 1, self.__last_ship[0][1]

        elif where == 4 and self.__last_ship[0][0] < 10:
            result = self.__last_ship[0][0] + 1, self.__last_ship[0][1]

        if result is not None and not self.__mp[result[1]][result[0]]:
            self.__print_map()
            return result

        return self.__get_one_of_four()

    def __get_right_or_left(self):
        """
        :return: tuple of two ints - left or right of the hit point
        """
        which = self.__random(1, 2)  # 1 - left, 2 - right
        result = None

        xes = list([ship[0] for ship in self.__last_ship])
        print("Bot1: xes: ", xes)
        right = max(xes)
        left = min(xes)

        if which == 1 and left > 1:
            result = left - 1, self.__last_ship[0][1]

        if which == 2 and right < 10:
            result = right + 1, self.__last_ship[0][1]

        if result is not None and not self.__mp[result[1]][result[0]]:
            return result

        return self.__get_right_or_left()

    def __get_top_or_bottom(self):
        """
        :return: tuple of two ints - top or bottom of the hit point
        """
        which = self.__random(3, 4)  # 3 - top, 4 - bottom
        result = None

        yes = list([ship[1] for ship in self.__last_ship])
        print("Bot1: yes: ", yes)
        bottom = max(yes)
        top = min(yes)

        if which == 3 and top > 1:
            result = self.__last_ship[0][0], top - 1

        if which == 4 and bottom < 10:
            result = self.__last_ship[0][0], bottom + 1

        if result is not None and not self.__mp[result[1]][result[0]]:
            return result

        return self.__get_top_or_bottom()

    def __destroyed(self):
        """
        Calls when the bot receives "destroyed" command
        :return:
        """
        for x, y in self.__last_ship:
            print("Bot1: destroyed coors -", x, y)
            self.__mp[y + 1][x] = True
            self.__mp[y - 1][x] = True
            self.__mp[y][x + 1] = True
            self.__mp[y][x - 1] = True

            self.__mp[y + 1][x + 1] = True
            self.__mp[y - 1][x - 1] = True
            self.__mp[y - 1][x + 1] = True
            self.__mp[y + 1][x - 1] = True

        self.__last_ship = []

        return self.__shoot()

    @staticmethod
    def __random(start: int, end: int):
        """
        :param start: int - start point
        :param end: int - end point
        :return: int - random number
        """
        rd.seed(dt.datetime.now().microsecond)
        return rd.randint(start, end)

    def __print_map(self):
        print("\n Time:", self.__time)
        for i in range(1, 11):
            for j in range(1, 11):
                print(self.__mp[i][j], end=" ")
            print()
