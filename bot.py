import random as rd


class Vivi(object):
    """
    Hello gays!  My name is Vivi! ... I'm a special bot for
    playing "Battle Ship". My level is not so high but I can
    play very hard. Sorry if ou loose...

    Good Luck my friend! ....

    ########################################################

                        BOT DOCUMENTATION

    ########################################################

    VERSION  . . . .  1.0

    CODE NAME  . . .  Vivi

    GAME . . . . . .  Battle Ship

    AUTHOR . . . . .  Tilek Sydykov

    YEAR . . . . . .  2018

    LICENCE  . . . .  Ala-Too University Licence 2.0

    #########################################################

    Main methods of a Class Vivi

    ##  say        ##

    ##  shoot      ##

    ##  hit        ##

    ##  destroyed  ##


    """
    i_map = {}
    random_array = []
    last_point_id = ""
    last_ship = []
    enemy_ships = []
    on_ship = False
    on_ship_array = []

    def __init__(self):
        for i in range(10):
            for j in range(10):
                new_key = str(i)+str(j)
                self.i_map[new_key] = i, j
                self.random_array.append(new_key)

    def say(self, sms: str):
        """"
        Method  SAY  gets a message from game and
        depending on a message return a
        bot's methods

        :returns: one a bot's methods
        """
        if sms == "shoot":
            return self.shoot()
        elif sms == "hit":
            return self.hit()
        elif sms == "destroyed":
            return self.destroyed()

    def shoot(self):
        """
        This method is generate a random numbers
        for shooting on enemy's field depending
        on a factors which should be sited in
        Battle ship

        :returns: a tuple of two numbers
                  where
                  firs is X coordinate
                  second is Y coordinate
        """

        if self.on_ship:
            on = self.on_ship_array
            if len(on) > 1:
                print("bot ### len of on_ship_array > 1")
                if not self.is_hor(on):
                    for i in on:
                        if i[0] != self.last_point_id[0]:
                            self.on_ship_array.remove(i)
                elif self.is_hor(on):
                    for i in on:
                        if i[1] != self.last_point_id[1]:
                            self.on_ship_array.remove(i)

            print("## bots arrays ", self.on_ship_array, on)
            on = self.on_ship_array
            point_id = on[rd.randint(0, len(on)-1)]
            self.on_ship_array.remove(point_id)
        else:
            local_array = self.random_array
            point_id = local_array[rd.randint(0, len(local_array)-1)]
        if point_id not in self.random_array:
            return self.shoot()
        self.random_array.remove(point_id)
        self.last_point_id = point_id

        x = self.i_map[point_id][0]+1
        y = self.i_map[point_id][1]+1
        return x, y

    def hit(self):
        """
        This method activates when the player says
        that his ship was injured but not destroyed

        In this method BOT creates an array of possible
        fields where can be located other part of ship

        In this case bot can shoot one more time.

        :returns: the shoot() method
        """
        hit_point = self.last_point_id
        ship = self.last_ship
        self.last_ship.append(hit_point)
        self.enemy_ships.append(hit_point)
        self.on_ship = True
        if len(self.last_ship) == 1:
            x = int(ship[0][0])
            y = int(ship[0][1])
            left = str(x + 1) + str(y)
            right = str(x) + str(y + 1)
            top = str(x - 1) + str(y)
            bottom = str(x) + str(y - 1)
            print("Directions:", left, right, top, bottom)
            if left in self.random_array and x < 9:
                self.on_ship_array.append(left)
                print("Left added...")
            if right in self.random_array and y < 9:
                self.on_ship_array.append(right)
                print("Right added...")
            if top in self.random_array and x > 0:
                self.on_ship_array.append(top)
                print("Top added...")
            if bottom in self.random_array and y > 0:
                self.on_ship_array.append(bottom)
                print("Bottom added...")
        else:
            x = int(ship[len(ship) - 1][0])
            y = int(ship[len(ship) - 1][1])
            if self.is_hor(ship):
                if str(x + 1) + str(y) in self.random_array and x < 9:
                    self.on_ship_array.append(str(x + 1) + str(y))
                if str(x - 1) + str(y) in self.random_array and x > 0:
                    self.on_ship_array.append(str(x - 1) + str(y))
                left_id = str(x) + str(y + 1)
                right_id = str(x) + str(y - 1)
                if left_id not in self.on_ship_array and left_id in self.random_array and y < 9:
                    self.on_ship_array.append(left_id)
                if right_id not in self.on_ship_array and right_id in self.random_array and y > 0:
                    self.on_ship_array.append(right_id)
            else:
                if str(x) + str(y + 1) in self.random_array:
                    self.on_ship_array.append(str(x) + str(y + 1))
                if str(x) + str(y - 1) in self.random_array:
                    self.on_ship_array.append(str(x) + str(y - 1))
                left_id = str(x + 1) + str(y)
                right_id = str(x - 1) + str(y)
                if left_id not in self.on_ship_array and left_id in self.random_array:
                    self.on_ship_array.append(left_id)
                if right_id not in self.on_ship_array and right_id in self.random_array:
                    self.on_ship_array.append(right_id)
        print("Last Ship location Array # ", self.last_ship)
        print("Last shooted point # ", self.last_point_id)
        return self.shoot()

    def destroyed(self):
        """
        This method is activates when player says "destroyed"
        Method destriyed() is deletes all fields from random_array
        where the user cant placed his ships.

        also cleaned his

        :return: Nothing
        """
        print("## Bot: Destroyed ship ", self.last_ship)
        if self.last_ship == []:
            self.last_ship.append(self.last_point_id)
        if self.is_hor(self.last_ship):

            x = []
            y = int(self.last_ship[0][1])
            for k in self.last_ship:
                x.append(int(k[0]))
            x.append(min(x) - 1)
            x.append(max(x) + 1)

            print("Destroyed ship X coordinates # ", x)

            x.sort()

            for i in x:
                if str(i) + str(y) in self.random_array:
                    self.random_array.remove(str(i) + str(y))

                if y - 1 >= 0 and str(i) + str(y - 1) in self.random_array:

                    self.random_array.remove(str(i) + str(y - 1))
                else:
                    print("removing out of range")
                if y + 1 <= 9 and str(i) + str(y + 1) in self.random_array:
                    self.random_array.remove(str(i) + str(y + 1))
                else:
                    print("removing out of range")
        else:
            y = []
            x = int(self.last_ship[0][0])
            for k in self.last_ship:
                y.append(int(k[0]))
            y.append(min(y) - 1)
            y.append(max(y) + 1)

            print("Destroyed ship X coordinates # ", x)

            y.sort()

            for i in y:
                if str(x) + str(i) in self.random_array:
                    self.random_array.remove(str(x) + str(i))
                if x - 1 >= 0 and str(x - 1) + str(i) in self.random_array:
                    self.random_array.remove(str(x - 1) + str(i))
                else:
                    print("removing out of range")
                if x + 1 <= 9 and str(x + 1) + str(i) in self.random_array:
                    self.random_array.remove(str(x + 1) + str(i))
                else:
                    print("removing out of range")
        self.last_ship = []
        self.on_ship = False
        self.on_ship_array = []
        return self.shoot()

    def is_hor(self, a):
        if self.on_ship_array == a:
            print("Damn it!!! ")
        if len(a) == 1:
            return None
        elif a[1][1] == a[0][1]:
            return True
        else:
            return False
