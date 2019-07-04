from tkinter import *
from tkinter import messagebox as msb

import frames
import res
import objects
import brain
import bots


class Main(object):
    time = 0

    def __init__(self):

        self.__root = Tk()
        self.__root.title(res.Strings.APP_NAME)
        self.__root.minsize(res.Dimensions.APP_MIN_WIDTH,
                            res.Dimensions.APP_MIN_HEIGHT)
        self.__root.maxsize(res.Dimensions.APP_MAX_WIDTH,
                            res.Dimensions.APP_MAX_HEIGHT)
        self.__root.protocol("WM_DELETE_WINDOW", self.on_exit_button_pressed)

        # Setting MainFrame
        self.__menu_frame = frames.MenuFrame(self)
        self.__arrange_frame = None
        self.__game_frame = None
        self.__menu_frame.place_frame()
        self.__bot = bots.Fati()

        # Setting HelpFrame
        self.__help_frame = frames.HelpFrame(self)

    def start(self):
        """
        Starts the mainloop
        :return: None
        """
        self.__root.mainloop()

    def get_root(self):
        """
        :return: BaseWidget tkinter root (master)
        """
        return self.__root

    # Menu frame
    def on_start_arrange_button_pressed(self):
        """
        Calls when the start button of the MainFram is clicked
        :return: None
        """
        print("Main: OnStartButtonPressed")
        self.__menu_frame.displace_frame()
        self.__arrange_frame = frames.ArrangeFrame(self)
        self.__arrange_frame.place_frame()

    def on_help_button_pressed(self):
        """
        Callback: MenuFrame
        :return:
        """
        self.__menu_frame.displace_frame()
        self.__help_frame.place_frame()

    def on_exit_button_pressed(self):
        """
        Callback: MenuFrame
        :return:
        """
        print("Main: onExitButtonPressed")
        dialog = msb.askokcancel(res.Strings.APP_NAME, res.Strings.MenuFrame.EXIT_DIALOG_MSG)

        if dialog:
            self.__root.destroy()

    # Arrange frame
    def on_start_game_button_pressed(self, player: objects.Player):
        """
        Calls when the start button of the ArrangeFrame is clicked
        :param player: Player - a player that was created
        :return: None
        """
        print("Main: Game started!")
        self.__arrange_frame.displace_frame()
        self.__game_frame = frames.GameFrame(self, player, brain.get_random_player())
        self.__game_frame.place_frame()

    def on_arrange_back_button_pressed(self):
        """
        Calls when the start button of the ArrangeFrame is clicked
        :return:
        """
        self.__arrange_frame.displace_frame()
        self.__menu_frame.place_frame()

    # Help frame
    def on_help_back_button_pressed(self):
        """
        Calls when the start button of the ArrangeFrame is clicked
        :return:
        """
        self.__help_frame.displace_frame()
        self.__menu_frame.place_frame()

    # Game frame
    def on_game_back_button_pressed(self):
        """
        Calls when the start button of the ArrangeFrame is clicked
        :return:
        """
        self.__game_frame.displace_frame()
        self.__menu_frame.place_frame()
        self.__bot = None
        self.__bot = bots.Fati()

    def get_shoot(self, sms: str):
        """
        Callback to get shot coordinates from the opponent
        :param sms: str - command to the opponent
        :return: tuple of two ints - (0: X coordinate, 1: Y coordinate)
        """
        return self.__bot.say(sms)


master = Main()

master.start()
