# Name: Daniel Uchytil, Spencer Warner, Alex Smith, Matthew Larson.
# About: This is a platforming game where the player is required to jump over
# obstacles as they approach the player. Hit any obstacle and you are dead.

import arcade

#Game constant variables. 
GAME_SPEED = -5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
UPDATE_RATE = 1 / 60

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 0
GRAVITY = 1
PLAYER_JUMP_SPEED = 30


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

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    # def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        '''if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0'''
    
    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

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
