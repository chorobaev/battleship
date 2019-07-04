# BattleShip-game-in-Python
A demo game in python using tkinter.

<img src="https://github.com/chorobaev/BattleShip-game-in-Python/blob/master/sreenshots/main.jpg"/>

More screenshots [here](https://github.com/chorobaev/BattleShip-game-in-Python/tree/master/sreenshots).

## Requirements: 
  1. Python 3.+.
  2. PNG viewing in the GUI: Python Imaging Library (**PIL**) *ImageTk*. 
    Can be installed using command `sudo apt-get install python-imaging-tk` for linux. 
    It is optional. If you don't want the cool image background as shown above, you can skip this.

## Setup instructions:
  1. Download or import the project.
  2. Open `main.py` file (if you don't have installed **PIL** you should open `main_without_image.py`).
  3. Run and enjoy the game.
  
## Creating a custom bot:
  If someone wants to create own bot and play agains it, it is possible to create and integrate custom bots.
  Sees the instruction how to do that, bellow.
      
### Bot class requirements:
  1. It must be a class
  2. It must have a function `say(value: str)` that returns *tuple* of Integers, 
  coordinates of the field where the bot wants to shoot `(x, y)`.
  There, `value` is a string which can be only one of these values:
      * "**shoot**" - means, the player missed, and bot's turn.
      * "**hit**" - means, bot's previous shoot was successful, but didn't destroy the player's ship complataly.
      * "**destroyed**" - means, bot's previous shoot was successful, and destroyed the player's ship complataly.
  As an example open `bots.py` file, and see the bot ***Fati***.
  
### Adding the custom bot:
  1. Open `bots.py` file.
  2. Paste implementation of a custom bot class bellow the bot ***Fati*** class.
  3. Open 'main.py` file.
  4. Go to `class Main` > `def __init__(self):`.
  5. Find the line `self.__bot = bots.Fati()`.
  6. Change it to `self.__bot = bots.CustomBot()` (here *"CustomBot"* is a created bot's name).
  5. Go to `class Main` > `def on_game_back_button_pressed(self):`, 
  6. Change the line `self.__bot = bots.Fati()` to `self.__bot = bots.CustomBot()` 
  (here *"CustomBot"* the same as within step **5**)
  
  
*If you have any questions, feel free to ask chorobaev.nurbol@gmail.com =)*
