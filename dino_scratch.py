# Name: Daniel Uchytil, Spencer Warner, Alex Smith, Matthew Larson.
# About: This is a platforming game where the player is required to jump over
# obstacles as they approach the player. Hit any obstacle and you are dead.

import arcade

#Game constant variables. 
GAME_SPEED = -5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
UPDATE_RATE = 1 / 60


class Dino_Game(arcade.Window):
    #Acts as a controller. Determines how the game is played.
    #Sets up the screen
    def __init__(self):
        super().__init__()

        self.ground = Ground()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = "Hardcore Dino"
        self.update_rate = UPDATE_RATE
        self._background_color = (arcade.csscolor.CORNFLOWER_BLUE)


class Player():
    #Player class is responsible for creating the player.
    pass


class Ground(arcade.Sprite):
    #Creates the gound and its location.
    def __init__(self):
        super().__init__("blackbox.png")
        #self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10



class Obstacle():
    pass


if __name__ == "__main__":
    dino_game = Dino_Game()
    dino_game.game_play()
