from tkinter import *
from tkinter import messagebox as msg
from res import Strings as String
from res import Colors as Color
from res import BOT_SHOOT_TIME
import objects
import brain


class MapBuilder(object):

    def __init__(self, context, master, width_and_height):
        """
        init the map
        :param context: Main - context
        :param: tkinter master - container
        :param width_and_height: int - width of a single grid (default(1))
        """
        self.__context = context
        self.__frame_map = Frame(master)
        self.__buttons = self.__create_frame(self.__frame_map, width_and_height)
        self.__player = None

    def __str__(self):
        return str(self.__buttons)

    def __on_mouse_entered(self, event, x, y):
        """
        Calls when the mouse has entered to the buttons
        :param event: tkinter event
        :return: None
        """
        try:
            self.__context.on_mouse_entered(event, x, y)
        except AttributeError:
            pass

    def __on_mouse_leaved(self, event, x, y):
        """
        Calls when the mouse has leaved to the buttons
        :param event: tkinter event
        :return: None
        """
        try:
            self.__context.on_mouse_leaved(event, x, y)
        except AttributeError:
            pass

    def __on_mouse_right_clicked(self, event, x, y):
        """
        Calls when right button of the mouse is clicked
        :param event: tkinter event
        :return: None
        """
        try:
            self.__context.on_mouse_right_clicked(event, x, y)
        except AttributeError:
            print()

    def __create_frame(self, root, width_and_height):  # Creating MapFrame getting
        """
        Creates a map (10x10), private
        :param root: tkinter object (master, Frame) - container
        :param width_and_height: int - width end height of a single grid
        :return: list of tkinter Buttons
        """
        print("MapBuilder: map created")
        buttons = [None]
        letter_coordinates = "ABCDEFGHIJ"

        for y in range(1, 11):

            Label(root,
                  text=str(y)).grid(row=y, column=0)
            Label(root,
                  text=letter_coordinates[y-1]).grid(row=0, column=y)

            row_buttons = [None]
            for x in range(1, 11):
                bt = Button(root,
                            text="",
                            width=width_and_height,
                            height=width_and_height,
                            bg=Color.MAP_COLOR,
                            activebackground=Color.MAP_COLOR,
                            command=lambda coord_x=x, coord_y=y: self.__on_button_clicked(coord_x, coord_y))

                bt.grid(row=y, column=x)
                bt.bind("<Enter>", lambda e, coord_x=x, coord_y=y: self.__on_mouse_entered(e, coord_x, coord_y))
                bt.bind("<Leave>", lambda e, coord_x=x, coord_y=y: self.__on_mouse_leaved(e, coord_x, coord_y))
                bt.bind("<Button-3>", lambda e, coord_x=x, coord_y=y:
                        self.__on_mouse_right_clicked(e, coord_x, coord_y))

                row_buttons.append(bt)
            buttons.append(row_buttons)

        return buttons

    def __on_button_clicked(self, x, y):
        """
        Map click listener, private
        :param x: int - X coordinate of the clicked grid
        :param y: int - Y coordinate of the clicked grid
        :return: None
        """
        #  print(x, y)
        self.__context.on_point_clicked(x, y)

    def set_player(self, player: objects.Player):
        """
        Sets player object ot this map
        :param player: Player - the player
        :return: None
        """
        self.__player = player

    def connect_maps(self):
        """
        Shows player's map on this map
        :return: None
        """
        for i in range(1, 11):
            ship = self.__player.get_ship(i)
            if ship is not None:
                for j in range(ship.get_type()):
                    self.get_button(ship.get_x_at(j), ship.get_y_at(j)).config(bg=Color.SHIP_COLOR)

    def get_button(self, x, y):
        """
        Gets the button at the fixed coordinate
        :param x: int - X coordinate
        :param y: int - Y coordinate
        :return: tkinter object Button
        """
        return self.__buttons[y][x]

    def refresh(self):
        """
        Makes a map as normal
        :return: None
        """
        for y in range(1, 11):
            for x in range(1, 11):
                self.__buttons[y][x].config(bg=Color.MAP_COLOR)

    def clickable(self, state: bool):
        """
        Makes the map impossible to click
        :return: None
        """
        if state is True:
            bt_state = NORMAL
        else:
            bt_state = DISABLED
        for y in range(1, 11):
            for x in range(1, 11):
                self.__buttons[y][x].config(state=bt_state)

    def get_frame(self):
        """
        :return: tkinter object Frame - the created MapFrame
        """
        return self.__frame_map


class StatusBuilder(object):

    def __init__(self, context, master, title: str, player: objects.Player):

        self.__context = context
        self.__player = player

        # Attributes
        self.__label_battleship = None
        self.__label_cruiser = None
        self.__label_destroyer = None
        self.__label_submarine = None

        # Frame status
        self.__frame = Frame(master)
        self.__create_frame(self.__frame, title)

    def __create_frame(self, root, title: str):
        """
        Creates the status frame
        :param root: tkinter master - container
        :return: None
        """
        root.config(padx=35,
                    pady=10,
                    highlightthickness=1,
                    highlightbackgroun=Color.MenuFrame.BACKGROUND_BUTTONS)
        Label(root,
              text=title,
              padx=14,
              pady=7,
              font="time 14 bold").pack(anchor=W)

        # Battleship
        self.__label_battleship = Label(root,
                                        text=String.StatusFrame.SHIPS[0][1]+": ",
                                        padx=7,
                                        pady=3,
                                        font="time 10 italic")
        self.__label_battleship.pack(anchor=W)

        # Cruiser
        self.__label_cruiser = Label(root,
                                     text=String.StatusFrame.SHIPS[1][1] + ": ",
                                     padx=7,
                                     pady=3,
                                     font="time 10 italic")
        self.__label_cruiser.pack(anchor=W)

        # Destroyer
        self.__label_destroyer = Label(root,
                                       text=String.StatusFrame.SHIPS[2][1] + ": ",
                                       padx=7,
                                       pady=3,
                                       font="time 10 italic")
        self.__label_destroyer.pack(anchor=W)

        # Submarine
        self.__label_submarine = Label(root,
                                       text=String.StatusFrame.SHIPS[3][1] + ": ",
                                       padx=7,
                                       pady=3,
                                       font="time 10 italic")
        self.__label_submarine.pack(anchor=W)

    def refresh(self):
        """
        Refreshes the table of ships
        :return: None
        """
        self.__label_battleship.config(text=String.StatusFrame.SHIPS[0][1]+": "
                                       + str(1 - self.__player.get_non_placed_amount(4)))
        self.__label_cruiser.config(text=String.StatusFrame.SHIPS[1][1] + ": "
                                    + str(2 - self.__player.get_non_placed_amount(3)))
        self.__label_destroyer.config(text=String.StatusFrame.SHIPS[2][1] + ": "
                                      + str(3 - self.__player.get_non_placed_amount(2)))
        self.__label_submarine.config(text=String.StatusFrame.SHIPS[3][1] + ": "
                                      + str(4 - self.__player.get_non_placed_amount(1)))

    def get_frame(self):
        """
        :return: Frame - created Status Frame
        """
        return self.__frame


class MenuFrame(object):

    def __init__(self, context):
        """
        :param context: Main object
        """
        self.__context = context
        self.__frame = self.__create_frame(self.__context.get_root())

    def __on_start_button_pressed(self):  # Button to start new game
        """
        Handles Start button's click events
        :return: None
        """
        print("The game has started...")
        self.__context.on_start_arrange_button_pressed()

    def __on_help_button_pressed(self):  # Button to show help section
        """
        Handles Help button's click events
        :return: None
        """
        print("MenuFrame: Help button pressed")
        self.__context.on_help_button_pressed()

    def __on_exit_button_pressed(self):  # Button to show exit dialog
        """
        Handles Exit button's click events
        :return:
        """
        print("MenuFrame: Exit button clicked...")
        self.__context.on_exit_button_pressed()

    def __create_frame(self, root):
        """
        Creates MenuFrame
        :param root: tkinter master - container that the frame must be in
        :return: tkinter Frame - created Frame
        """

        frame = Frame(root,
                      padx=10,
                      pady=10,
                      highlightthickness=1,
                      highlightbackgroun=Color.MenuFrame.BACKGROUND_BUTTONS)

        Label(frame,
              text=String.MenuFrame.TITLE,
              pady=5,
              font="time 14 bold").pack()

        # Start game button
        bt_start_game = Button(frame,
                               text=String.MenuFrame.BUTTON_START,
                               width=20,
                               padx=4,
                               takefocus="tab",
                               command=self.__on_start_button_pressed)
        # Help button
        bt_help = Button(frame,
                         text=String.MenuFrame.BUTTON_HELP,
                         width=20,
                         padx=4,
                         command=self.__on_help_button_pressed)
        # Exit button
        bt_exit = Button(frame,
                         text=String.MenuFrame.BUTTON_EXIT,
                         width=20,
                         padx=4,
                         command=self.__on_exit_button_pressed)

        # Packing buttons
        bt_start_game.pack()
        bt_help.pack()
        bt_exit.pack()

        return frame

    def place_frame(self):
        """
        Places the frame on the root (attaches)
        :return: None
        """
        self.__frame.place(relx=0.17,
                           rely=0.3,
                           anchor=CENTER)

    def displace_frame(self):
        """
        Displace the Frame (removes)
        :return: None
        """
        self.__frame.place_forget()

    def get_frame(self):
        """
        :return: Frame - created Frame
        """
        return self.__frame


class ArrangeFrame(object):

    def __init__(self, context):
        self.__context = context
        self.__chosen_ship = IntVar()
        self.__chosen_ship.set(4)

        # Ships choosing frame
        self.__frame_choose = Frame(self.__context.get_root())
        self.__create_choose_frame(self.__frame_choose)

        # Attributes of status frame
        self.__label_type = None
        self.__label_amount = None
        self.__orientation = True  # True if the ship is horizontal else Folse

        # Chosen ship status frame
        self.__frame_status = Frame(self.__context.get_root())
        self.__create_status_frame(self.__frame_status)

        # Sets up first status frame
        self.__frame_of_orientation = \
            self.__draw_ship(self.__frame_status, self.__chosen_ship.get(), self.__orientation)
        self.__frame_of_orientation.pack()

        # Map frame
        self.__frame_map = Frame(self.__context.get_root())
        self.__map = None
        self.__create_map_frame(self.__frame_map)

        # Attributes of message frame
        self.__label_warnings = None

        # Message frame
        self.__frame_message = Frame(self.__context.get_root())
        self.__create_message_frame(self.__frame_message)

        # Special frame
        self.__frame_special = Frame(self.__context.get_root())
        self.__create_special_frame(self.__frame_special)

        # Player object
        self.__player = objects.Player()
        self.__can_ship_be_put = True

    def on_point_clicked(self, x, y):
        """
        Map click listener
        :param x: int - X coordinate of the clicked grid
        :param y: int - Y coordinate of the clicked grid
        :return: None
        """
        if self.__player.get_non_placed_amount(self.__chosen_ship.get()) != 0:
            if self.__orientation:
                orientation = 1
            else:
                orientation = 2

            ship_is_added = False
            possible = self.__can_ship_be_put  # Checks weather the chosen ship can be put
            if possible:
                ship = objects.Ship(self.__chosen_ship.get(), orientation, x, y)
                ship_is_added = self.__player.add_ship(ship)
                if ship_is_added:

                    if self.__chosen_ship.get() > 1 and \
                            self.__player.get_non_placed_amount(self.__chosen_ship.get()) == 0:
                        self.__chosen_ship.set(self.__chosen_ship.get() - 1)

                    print("StatusFrame: this ship is added\n" + str(ship))

            if not possible or not ship_is_added:  # Warms if the ship cannot be placed
                self.__show_warning(String.StatusFrame.WARNING_CANNOT_PUT
                                    % (String.StatusFrame.SHIPS[4 - self.__chosen_ship.get()][1]), "red")

            # At the end, refreshing the status
            self.__on_ship_chosen()
            self.__orientation = not self.__orientation
            self.__on_change_button_pressed()

            if self.__player.is_completed():
                self.__show_warning(String.StatusFrame.WARNING_CAN_START, "green")
        else:
            print("StatusFrame: all", self.__chosen_ship.get(), "type ships are added")
            self.__show_warning(String.StatusFrame.WARNING_ALL_SHIPS_PUT
                                % (String.StatusFrame.SHIPS[4 - self.__chosen_ship.get()][1]), "red")

    def on_mouse_entered(self, event, x, y):
        """
        Calls when the mouse is entered any button
        :param event: tkinter event object
        :param x: int - x coordinate of the clicked button
        :param y: int - y coordinate of the clicked button
        :return: None
        """
        # Checks weather there is enough ship in chosen type to put
        if self.__player.get_non_placed_amount(self.__chosen_ship.get()) > 0:

            if self.__orientation:  # orientation is horizontal
                if x + self.__chosen_ship.get() > 11:
                    end_x = 11
                    self.__can_ship_be_put = False
                    color = Color.ERROR_COLOR
                else:
                    end_x = x + self.__chosen_ship.get()
                    self.__can_ship_be_put = True
                    color = Color.SHIP_COLOR

                # Setting up active background (the button that is the mouse on it)
                if self.__player.get_point_on_map(x, y) != 0:
                    event.widget.config(activebackground=Color.ERROR_COLOR)
                else:
                    event.widget.config(activebackground=color)

                for i in range(x, end_x):
                    point = self.__player.get_point_on_map(i, y)
                    if point != 0:  # is not possible to put on this point
                        self.__map.get_button(i, y).config(bg=Color.ERROR_COLOR)
                    else:
                        self.__map.get_button(i, y).config(bg=color)

            else:  # orientation is vertical

                if y + self.__chosen_ship.get() > 11:
                    end_y = 11
                    self.__can_ship_be_put = False
                    color = Color.ERROR_COLOR
                else:
                    end_y = y + self.__chosen_ship.get()
                    self.__can_ship_be_put = True
                    color = Color.SHIP_COLOR

                # Setting up active background (the button that is the mouse on it)
                if self.__player.get_point_on_map(x, y) != 0:
                    event.widget.config(activebackground=Color.ERROR_COLOR)
                else:
                    event.widget.config(activebackground=color)

                for i in range(y, end_y):
                    point = self.__player.get_point_on_map(x, i)
                    if point != 0:  # is not possible to put on this point
                        self.__map.get_button(x, i).config(bg=Color.ERROR_COLOR)
                    else:
                        self.__map.get_button(x, i).config(bg=color)
        else:
            if self.__player.get_point_on_map(x, y) not in ('.', 0):
                event.widget.config(activebackground=Color.SHIP_COLOR)

    def on_mouse_leaved(self, event, x, y):
        """
        Calls when the mouse is leaved any button
        :param event: tkinter event object
        :param x: int - x coordinate of the clicked button
        :param y: int - y coordinate of the clicked button
        :return: None
        """
        event.widget.config(activebackground=Color.MAP_COLOR)

        if self.__orientation:  # is horizontal
            if x + self.__chosen_ship.get() > 10:
                end_x = 11
                self.__can_ship_be_put = False
            else:
                end_x = x + self.__chosen_ship.get()
                self.__can_ship_be_put = True

            for i in range(x, end_x):
                point = self.__player.get_point_on_map(i, y)  # Checks weather point is not a ship
                if point == '.' or point == 0:  # is empty point
                    self.__map.get_button(i, y).config(bg=Color.MAP_COLOR)
                else:  # is a ship
                    if self.__map.get_button(i, y).cget("bg") == Color.ERROR_COLOR:  # Checks weather point is ship
                        self.__map.get_button(i, y).config(bg=Color.SHIP_COLOR)

        else:  # orientation is vertical

            if y + self.__chosen_ship.get() > 10:
                end_y = 11
                self.__can_ship_be_put = False
            else:
                end_y = y + self.__chosen_ship.get()
                self.__can_ship_be_put = True

            for i in range(y, end_y):
                point = self.__player.get_point_on_map(x, i)  # Checks weather point is not a ship
                if point == '.' or point == 0:  # is empty point
                    self.__map.get_button(x, i).config(bg=Color.MAP_COLOR)
                else:  # is a ship
                    if self.__map.get_button(x, i).cget("bg") == Color.ERROR_COLOR:  # Checks weather point is ship
                        self.__map.get_button(x, i).config(bg=Color.SHIP_COLOR)

    def on_mouse_right_clicked(self, event, x, y):
        """
        Calls when right button of the mouse is clicked
        :param event: tkinter event
        :param x: int - x coordinate of the clicked button
        :param y: int - y coordinate of the clicked button
        :return: None
        """
        self.on_mouse_leaved(event, x, y)
        self.__on_change_button_pressed()
        self.on_mouse_entered(event, x, y)

    def __on_change_button_pressed(self):
        """
        Calls when change orientation is clicked
        :return: None
        """
        if self.__frame_of_orientation is not None:
            self.__frame_of_orientation.pack_forget()
        self.__orientation = not self.__orientation
        self.__frame_of_orientation = \
            self.__draw_ship(self.__frame_status, self.__chosen_ship.get(), self.__orientation)
        self.__frame_of_orientation.pack()

    def __on_random_button_pressed(self):
        """
        Calls when random button is clicked
        :return: None
        """
        self.__player = brain.get_random_player()
        self.__map.refresh()
        for y in range(1, 11):
            for x in range(1, 11):
                point = self.__player.get_point_on_map(x, y)
                if point != 0 and point != '.':  # is ship
                    self.__map.get_button(x, y).config(bg=Color.SHIP_COLOR)

        # Refresh status frame
        self.__orientation = not self.__orientation
        self.__on_change_button_pressed()

    def __on_back_menu_button_pressed(self):
        """
        Calls when back to menu button is clicked
        :return: None
        """
        is_player_agree = msg.askyesno(String.APP_NAME, String.StatusFrame.DIALOG_BACK_MENU)
        if is_player_agree:
            self.__context.on_arrange_back_button_pressed()

    def __on_start_button_pressed(self):
        """
        Calls when the start button is clicked
        :return: None - starts the game if all ships put on the map
        """
        print("StatusFrame: start button pressed...")
        if self.__player.is_completed():
            self.__context.on_start_game_button_pressed(self.__player)
        else:
            self.__show_warning(String.StatusFrame.WARNING_PUT_ALL_SHIPS, "red")

    def __on_clear_button_pressed(self):
        """
        Calls when clear all button is clicked
        :return: None - Clears all built ships
        """
        if self.__player.is_some_ships_placed():

            is_player_agree = msg.askyesno(String.APP_NAME, String.StatusFrame.DIALOG_CLEAR_ALL)

            if is_player_agree:
                self.__player = None
                self.__player = objects.Player()
                self.__map.refresh()
                self.__show_warning(String.StatusFrame.WARNING_SHIPS_CLEARED, "green")

                # Refresh status frame
                self.__on_ship_chosen()
        else:
            self.__show_warning(String.StatusFrame.WARNING_EMPTY_MAP, "red")

    def __on_ship_chosen(self):
        """
        Calls when one of the ships is chosen
        :return: None
        """
        text = String.StatusFrame.HEADER_TYPE + " " + String.StatusFrame.SHIPS[4-self.__chosen_ship.get()][1]
        self.__label_type.config(text=text)

        text = String.StatusFrame.HEADER_AMOUNT + " " + str(
            self.__player.get_non_placed_amount(self.__chosen_ship.get()))

        self.__label_amount.config(text=text)

        # Refresh status frame
        self.__orientation = not self.__orientation
        self.__on_change_button_pressed()

    def __show_warning(self, warning: str, color: str):
        """
        :param warning: str - a warning that must be shown
        :return: None
        """
        self.__label_warnings.config(text=warning,
                                     fg=color)
        self.__label_warnings.after(4000, lambda: self.__label_warnings.config(text=""))

    @staticmethod
    def __draw_ship(root, tp: int, orientation: bool):
        """
        Draws the orientation displaying frame
        :param root: tkinter master - container that the frame must be in
        :param tp: int [1, 4] - type of a ship that will be drown
        :param orientation: bool - orientation of a ship that will be drown, True if Horizontal else False
        :return:
        """
        frame = Frame(root,
                      pady=25)

        for i in range(tp):
            bt = Button(frame,
                        width=1,
                        height=1,
                        bg=Color.SHIP_COLOR,
                        state=DISABLED)
            if orientation:
                bt.grid(row=0, column=i)
            else:
                bt.grid(row=i, column=0)

        return frame

    def __create_choose_frame(self, root):
        """
        Creates Ships choosing frame
        :param root: tkinter master - container that the frame must be in
        :return: tkinter Frame - created Frame
        """
        root.config(padx=10,
                    pady=10)

        # Choose frame
        Label(root,
              pady=3,
              padx=15,
              text=String.StatusFrame.MSG_CHOSE,
              font="time 14 bold").pack(anchor=W)

        for value, ship in String.StatusFrame.SHIPS:
            Radiobutton(root,
                        text=ship,
                        padx=10,
                        pady=4,
                        width=16,
                        anchor=W,
                        indicatoron=0,
                        variable=self.__chosen_ship,
                        value=value,
                        command=self.__on_ship_chosen).pack(anchor=W)

    def __create_status_frame(self, root):
        """
        Creates Ship status frame
        :param root: tkinter master - container that the frame must be in
        :return: tkinter Frame - created Frame
        """
        root.config(padx=11,
                    pady=10)

        # Title
        Label(root,
              pady=3,
              padx=15,
              text=String.StatusFrame.MSG_CHOSEN,
              font="time 14 bold").pack(anchor="w")

        # Type variables
        print("StatusFrame: __label_type created")
        self.__label_type = Label(root,
                                  text="Type: BATTLESHIP",
                                  padx=10,
                                  pady=3)
        self.__label_type.pack(anchor=W)

        # Amount variable
        self.__label_amount = Label(root,
                                    text="Amount: 1",
                                    padx=10,
                                    pady=2)
        self.__label_amount.pack(anchor=W)

        Label(root,
              text=String.StatusFrame.HEADER_ORIENTATION,
              padx=10,
              pady=2).pack(anchor=W)

        # Change orientation button
        #Button(root,
        #       text=String.StatusFrame.BUTTON_CHANGE,
        #       width=15,
        #       command=self.__on_change_button_pressed).pack(anchor=W)

    def __create_map_frame(self, root):
        """
        Creates Ships choosing frame
        :return: tkinter Frame - created Frame
        """
        self.__map = MapBuilder(self, root, 2)

        # Map
        self.__map.get_frame().pack()

    def __create_message_frame(self, root):
        """
        Creates Ship status frame
        :param root: tkinter master - container that the frame must be in
        :return: tkinter Frame - created Frame
        """
        # Warnings
        self.__label_warnings = Label(root,
                                      fg=Color.ERROR_COLOR,
                                      bg=Color.MAP_COLOR,
                                      width=43,
                                      height=1,
                                      font="time 12 italic")
        self.__label_warnings.pack(anchor=W)

    def __create_special_frame(self, root):
        """
        Creates Ship status frame
        :param root: tkinter master - container that the frame must be in
        :return: tkinter Frame - created Frame
        """
        # Clears all button
        Button(root,
               text=String.StatusFrame.BUTTON_CLEAR_ALL,
               width=18,
               anchor=W,
               bg=Color.ERROR_COLOR,
               fg="white",
               command=self.__on_clear_button_pressed).pack()

        # Random arrange button
        Button(root,
               text=String.StatusFrame.BUTTON_RANDOM,
               width=18,
               anchor=W,
               bg=Color.SHIP_COLOR,
               fg="white",
               command=self.__on_random_button_pressed).pack()

        # Back to menu button
        Button(root,
               text=String.StatusFrame.BUTTON_BACK_MENU,
               width=18,
               anchor=W,
               bg=Color.BACK_BUTTON,
               fg="white",
               command=self.__on_back_menu_button_pressed).pack()

        # Start button
        Button(root,
               text=String.StatusFrame.BUTTON_START,
               anchor=W,
               width=18,
               command=self.__on_start_button_pressed).pack()

    def place_frame(self):
        """
        Places the frame onto the master
        :return: None
        """
        self.__frame_choose.place(relx=0.03,
                                  rely=0.1,
                                  anchor=NW)

        self.__frame_status.place(relx=0.03,
                                  rely=0.45,
                                  anchor=NW)

        self.__frame_map.place(relx=0.5,
                               rely=0.08,
                               anchor=N)

        self.__frame_message.place(relx=0.5,
                                   rely=0.95,
                                   anchor=CENTER)

        self.__frame_special.place(relx=0.97,
                                   rely=0.9,
                                   anchor=SE)

    def displace_frame(self):
        """
        Displaces the frame from the master
        :return: None
        """
        self.__frame_choose.place_forget()
        self.__frame_status.place_forget()
        self.__frame_map.place_forget()
        self.__frame_message.place_forget()
        self.__frame_special.place_forget()

    def get_root(self):
        """
        :return: tkinter master
        """
        return self.__frame_map


class GameFrame(object):
    time = 0

    def __init__(self, context, player: objects.Player, enemy: objects.Player):
        self.__context = context
        self.__last_hit_field = "", ""

        # Creating players
        self.__player = player
        self.__enemy = enemy

        # Player map frame
        self.__frame_player = Frame(self.__context.get_root())
        self.__map_player = None
        self.__create_player_frame(self.__frame_player)
        self.__map_player.set_player(self.__player)  # Sets the player to the created map
        self.__map_player.connect_maps()  # Shoes the ships of the player on the map

        # Enemy map frame
        self.__frame_enemy = Frame(self.__context.get_root())
        self.__map_enemy = None
        self.__create_enemy_frame(self.__frame_enemy)
        self.__map_enemy.set_player(self.__enemy)  # Sets the enemy to the created map

        # Player status frame
        self.__frame_status_player = Frame(self.__context.get_root())
        self.__status_player = None
        self.__create_status_player_frame(self.__frame_status_player)

        # Enemy status frame
        self.__frame_status_enemy = Frame(self.__context.get_root())
        self.__status_enemy = None
        self.__create_status_enemy_frame(self.__frame_status_enemy)

        # Bar frame
        self.__frame_bar = Frame(self.__context.get_root())
        self.__label_turn = None
        self.__label_warning = None
        self.__create_bar_frame(self.__frame_bar)

        # Turn value
        self.__is_turn_of_player = True  # True if player's turn else False
        self.__set_turn(self.__is_turn_of_player)  # Setting turns label

    def on_point_clicked(self, x, y):
        """
        Map click listener
        :param x: int - X coordinate of the clicked grid
        :param y: int - Y coordinate of the clicked grid
        :return: None
        """
        if self.__is_turn_of_player:
            self.time += 1
            print("Player shoot #%d" % self.time, (x, y))
            self.__last_hit_field = x, y
            self.__hit_point(x, y, self.__enemy, self.__map_enemy)
        else:
            self.__set_warning(String.GameFrame.WARNING_TURN_OF_ENEMY, "red")

    def __on_back_menu_button_clicked(self):
        """
        Calls when back menu button is clicked
        :return: None
        """
        is_player_agree = msg.askyesno(String.APP_NAME, String.StatusFrame.DIALOG_BACK_MENU)
        if is_player_agree:
            self.__context.on_game_back_button_pressed()

    def __get_shoot_from_enemy(self, sms: str):
        """
        Calls when enemy shoots
        :param sms: str - the message that have to be sent to enemy
        :return: None
        """
        coord: tuple = self.__context.get_shoot(sms)
        '''
        if len(coord) != 2 or type(coord[0]) is not int or type(coord[1]) is not int \
                or self.__map_player.get_button(coord[0], coord[1]).cget("state") == DISABLED \
                or coord[0] not in range(1, 11) or coord[1] not in range(1, 11) or coord is None:
            self.__context.get_shoot(String.GameFrame.BOT_ERROR)
            raise ShipException("Bot shot incorrectly! Unexpected bot!", "")
        '''

        if not self.__is_turn_of_player:
            self.__last_hit_field = coord
            self.__hit_point(coord[0], coord[1], self.__player, self.__map_player)
        else:
            print("GameFrame: enemy tries to shoot while it is player's turn")

    def __create_player_frame(self, root):
        """
        Creates players map
        :param root: tkinter master - container that the frame must be in
        :return: None
        """
        print("GameFrame: player map created")
        self.__map_player = MapBuilder(self, root, 1)
        self.__map_player.clickable(False)
        self.__map_player.get_frame().pack()

    def __create_enemy_frame(self, root):
        """
        Creates enemies map
        :param root: tkinter master - container that the frame must be in
        :return: None
        """
        self.__map_enemy = MapBuilder(self, root, 2)
        self.__map_enemy.get_frame().pack()

    def __create_status_player_frame(self, root):
        """
        Creates status frame
        :param root: tkinter master - container
        :return: None
        """
        self.__status_player = StatusBuilder(self, root, String.GameFrame.PLAYER_SHIPS, self.__player)
        self.__status_player.get_frame().pack()
        self.__status_player.refresh()

    def __create_status_enemy_frame(self, root):
        """
        Creates status frame
        :param root: tkinter master - container
        :return: None
        """
        self.__status_enemy = StatusBuilder(self, root, String.GameFrame.ENEMY_SHIPS, self.__enemy)
        self.__status_enemy.get_frame().pack()
        self.__status_enemy.refresh()

    def __create_bar_frame(self, root):
        """
        Creates the bar frame
        :param root: tkinter master - container
        :return: None
        """
        root.config(padx=2,
                    pady=2)

        # Back to menu button
        Button(root,
               text=String.StatusFrame.BUTTON_BACK_MENU,
               bg=Color.SHIP_COLOR,
               command=self.__on_back_menu_button_clicked).pack(side="left")

        # Turn label
        self.__label_turn = Label(root,
                                  text="Your turn",
                                  width=30,
                                  padx=3,
                                  fg=Color.SHIP_COLOR)
        self.__label_turn.pack(side="left")

        # Warning label
        self.__label_warning = Label(root,
                                     width=46,
                                     padx=4,
                                     fg=Color.ERROR_COLOR,
                                     font="time 12 bold italic")
        self.__label_warning.pack(side="left")

    def __set_turn(self, turn: bool):
        """
        :param turn: bool - Player's turn if True else Enemy's turn
        :return: None - changes label_turn
        """
        if turn:
            string = (String.GameFrame.WARNING_LAST_SHOT % str(self.__last_hit_field)) + String.GameFrame.TURN_OF_PLAYER
        else:
            string = (String.GameFrame.WARNING_LAST_SHOT % str(self.__last_hit_field)) + String.GameFrame.TURN_OF_ENEMY
        self.__label_turn.config(text=string)

    def __set_warning(self, warning: str, color: str):
        """
        Shows warning on the warning label
        :param warning: str - the warning
        :param color: str - color of the warning
        :return: None
        """
        self.__label_warning.config(text=warning,
                                    fg=color)
        self.__label_warning.after(700, lambda: self.__label_warning.config(text=""))

    def __show_result_of_battle(self, loser: objects.Player):
        """
        Shows a dialog that contains results of the battle
        :param loser: Player - a player that lost the game
        :return:
        """
        if loser is not self.__player:
            msg.showinfo(String.GameFrame.TITLE_VICTORY, String.GameFrame.MSG_VICTORY)
        else:
            msg.showinfo(String.GameFrame.TITLE_DEFEAT, String.GameFrame.MSG_DEFEAT)

        self.__context.on_game_back_button_pressed()  # Goes to the menu

    def __hit_point(self, x: int, y: int, defence: objects.Player, mp: MapBuilder):
        """
        Calls when some one hit the map
        :param x: int - X coordinate
        :param y: int - Y coordinate
        :param defence: Player - a player whose map is hit
        :param mp: MapBuilder - Player's map
        :return: None
        """
        point = defence.get_point_on_map(x, y)

        if point != 0 and point != '.':  # Checks whether the player hit a ship
            ship = defence.get_ship(point)  # Getting the ship at the chosen point

            destroyed = ship.hit(x, y)  # Hits the ship
            if destroyed:
                if ship.get_status():
                    print(ship, "\n")
                    mp.get_button(x, y).config(bg=Color.DESTROYED_PART,
                                               state=DISABLED)
                    self.__set_warning(String.GameFrame.WARNING_HIT, "blue")

                    if defence is self.__player:  # Letting to enemy know that he hit
                        mp.get_button(1, 1).after(BOT_SHOOT_TIME["hit"], lambda: self.__get_shoot_from_enemy(String.GameFrame.BOT_HIT))

                else:
                    mp.get_button(x, y).config(state=DISABLED)
                    self.__ship_destroyed(ship, mp)
                    self.__set_warning(String.GameFrame.WARNING_SHIP_DESTROYED, "green")

                    defence.remove_ship(point)  # Removes the destroyed ship from the player's list

                    if defence is self.__player:  # Letting to enemy know that he destroyed
                        self.__status_player.refresh()
                        mp.get_button(1, 1).after(BOT_SHOOT_TIME["destroyed"], lambda: self.__get_shoot_from_enemy(String.GameFrame.BOT_DESTROYED))  # Refreshes status
                    else:
                        self.__status_enemy.refresh()  # Refreshes status

                    if not defence.is_some_ships_placed():
                        self.__show_result_of_battle(defence)  # Shows the results of the battle

        else:
            self.__is_turn_of_player = not self.__is_turn_of_player  # Changes the turn
            self.__set_turn(self.__is_turn_of_player)

            self.__set_warning(String.GameFrame.WARNING_MISS, "red")
            mp.get_button(x, y).config(text="*",
                                       bg=Color.BROKEN_POINT,
                                       state=DISABLED)

            if defence is self.__enemy:  # Letting to enemy to shoot
                mp.get_button(1, 1).after(BOT_SHOOT_TIME["shoot"], lambda: self.__get_shoot_from_enemy(String.GameFrame.BOT_SHOOT))

    @staticmethod
    def __ship_destroyed(ship: objects.Ship, mp: MapBuilder):
        """
        :param ship: Ship - a ship that has destroyed
        :param mp: MapBuilder - a map that the ship is placed
        :return: None
        """
        for i in range(ship.get_type()):
            x = ship.get_x_at(i)
            y = ship.get_y_at(i)

            mp.get_button(x, y).config(text="X",
                                       bg=Color.DESTROYED_SHIP)

            # Automatically hitting adjacent points
            if x < 10 and mp.get_button(x + 1, y).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x + 1, y).config(bg=Color.BROKEN_POINT,
                                               text="*",
                                               state=DISABLED)
            if x > 1 and mp.get_button(x - 1, y).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x - 1, y).config(bg=Color.BROKEN_POINT,
                                               text="*",
                                               state=DISABLED)
            if y < 10 and mp.get_button(x, y + 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x, y + 1).config(bg=Color.BROKEN_POINT,
                                               text="*",
                                               state=DISABLED)
            if y > 1 and mp.get_button(x, y - 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x, y - 1).config(bg=Color.BROKEN_POINT,
                                               text="*",
                                               state=DISABLED)
            if x < 10 and y < 10 and mp.get_button(x + 1, y + 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x + 1, y + 1).config(bg=Color.BROKEN_POINT,
                                                   text="*",
                                                   state=DISABLED)
            if x > 1 and y > 1 and mp.get_button(x - 1, y - 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x - 1, y - 1).config(bg=Color.BROKEN_POINT,
                                                   text="*",
                                                   state=DISABLED)
            if x > 1 and y < 10 and mp.get_button(x - 1, y + 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x - 1, y + 1).config(bg=Color.BROKEN_POINT,
                                                   text="*",
                                                   state=DISABLED)
            if x < 10 and y > 1 and mp.get_button(x + 1, y - 1).cget("bg") == Color.MAP_COLOR:
                mp.get_button(x + 1, y - 1).config(bg=Color.BROKEN_POINT,
                                                   text="*",
                                                   state=DISABLED)

    def place_frame(self):
        """
        Places frame onto the root frame
        :return: None
        """
        self.__frame_player.place(relx=0.05,
                                  rely=0.95,
                                  anchor=SW)
        self.__frame_enemy.place(relx=0.95,
                                 rely=0.95,
                                 anchor=SE)
        self.__frame_status_player.place(relx=0.05,
                                         rely=0.116,
                                         anchor=NW)
        self.__frame_status_enemy.place(relx=0.247,
                                        rely=0.116,
                                        anchor=NW)
        self.__frame_bar.place(relx=0.05,
                               rely=0.03,
                               anchor=NW)

    def displace_frame(self):
        """
        Displace the frame from the map
        :return: None
        """
        self.__frame_player.place_forget()
        self.__frame_enemy.place_forget()
        self.__frame_status_player.place_forget()
        self.__frame_status_enemy.place_forget()
        self.__frame_bar.place_forget()

    def destroy_frame(self):
        """
        Destroys this Game frame
        :return:
        """
        self.__frame_player.destroy()
        self.__frame_enemy.destroy()
        self.__frame_status_player.destroy()
        self.__frame_status_enemy.destroy()
        self.__frame_bar.destroy()


class HelpFrame(object):

    def __init__(self, context):
        self.__context = context
        self.__frame = Frame(context.get_root())
        self.__button_back = None
        self.__create_frame(self.__frame)

    def __on_back_button_pressed(self):
        """
        Calls when the exit button is clicked
        :return: None - goes to the menu frame
        """
        self.__context.on_help_back_button_pressed()

    def __create_frame(self, root):
        """
        Creates the frame
        :param root: tkinter master - the root that this frame must to be placed on
        :return: None
        """
        root.config(padx=20,
                    width=20)
        self.__button_back = Button(self.__context.get_root(),
                                    text=String.StatusFrame.BUTTON_BACK_MENU,
                                    command=self.__on_back_button_pressed)

        Message(root,
                text=String.HelpFrame.MSG_HELP,
                justify=LEFT,
                fg=Color.HELP_MSG,
                font="Verdana 20 bold").pack()

    def place_frame(self):
        """
        Places the frame to the window
        :return: None
        """
        self.__button_back.place(relx=0.01,
                                 rely=0.05,
                                 anchor=NW)
        self.__frame.place(relx=0.17,
                           rely=0.05,
                           anchor=NW)

    def displace_frame(self):
        """
        Displaces the frame form the window
        :return: None
        """
        self.__button_back.place_forget()
        self.__frame.place_forget()
