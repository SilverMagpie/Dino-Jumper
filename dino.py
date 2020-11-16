# Name: Daniel Uchytil, Alex Smith, Spencer Warner, Matthew Larson
# Game: Dino jumper

import arcade


# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 1000 - 249
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class dino_game(arcade.Window):

    '''
    A 2D game where the player jumps to avoid obstacles moving toward them.

    The responsibility of this class is to use other classes to controll how
    this game is played. 

    Sterotype: Controller
    '''

    def __init__(self):
        #sets up the screen
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #Changes background color to Blue.
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        #Sets up character view.
        self.view_bottom = 0
        self.view_left = 0

        self._dino = Dino()
        self._obstacle = Obstacle()
        self._actor = Actor()
        
    def game_play(self):
        ''' This method is responsible for game play sequence. '''
        pass


    def update_score(self):
        ''' This method is responsible for updating Dino's Score. '''
        pass


<<<<<<< HEAD
=======
class Actor:
    """A visible, moveable thing that participates in the game.
    
    The responsibility of Actor is to keep track of its appearance,
    position and velocity in 2d space.

    Stereotype:
        Information Holder
    """
    def __init__(self):
        self._image_source = ""
        self._position = (0, 0) # Gives the x, y coordinates of the actor
        self._velocity = (0, 0)
        
    def get_position(self):
        return self._position
    
    def get_image_source(self):
        return self._image_source

    def get_velocity(self):
        return self._velocity
    
    def move_next(self):
        x = 1 + (self._position[0] + self._velocity[0] - 1) % (MAX_X - 2)
        y = 1 + (self._position[1] + self._velocity[1] - 1) % (MAX_Y - 2)
        self._position = (x, y)
    
    def set_position(self, position):
        self._position = position
    
    def set_image_source(self, text):
        self._image_source = text

    def set_velocity(self, velocity):
       self._velocity = velocity
>>>>>>> d9ba5a20d8f9497ea7cf08b7c9a6cc69bb5df4e4

class dino():
    pass


class obstacle():
    pass


<<<<<<< HEAD
class actor():
    pass


    


if __name__ == "__main__":
    pass
=======
if __name__ == "__main__":
        pass
>>>>>>> d9ba5a20d8f9497ea7cf08b7c9a6cc69bb5df4e4











