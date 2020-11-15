# Name: Daniel Uchytil, Spencer Warner, Alex Smith, Matthew Larson.
# About: This is a platforming game where the player is required to jump over
# obstacles as they approach the player. Hit any obstacle and you are dead.

import arcade

#Game constant variables. 
GAME_SPEED = -5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
UPDATE_RATE = 1 / 60

class dino_game():
    #Acts as a controller. Determines how the game is played. 
    def __init__(self):

        self.display = Display()

    def game_play():
        pass




class display(arcade.Window):
    #Sets up the screen
    def __init__(self):
        super().__init__()

        self.ground = Ground()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = "Hardcore Dino"
        self.update_rate = UPDATE_RATE
        self._background_color = (arcade.csscolor.CORNFLOWER_BLUE)


class player():
    #Player class is responsible for creating the player.
    pass


class ground(arcade.Sprite):
    #Creates the gound and its location.
    def __init__(self):
        super().__init__("blackbox.png")
        self._image = None
        self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = None
        self.center_y = None



class obstacle():
    pass


if __name__ == "__main__":
    pass
