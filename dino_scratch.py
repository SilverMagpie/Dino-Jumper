# Name: Daniel Uchytil, Spencer Warner, Alex Smith, Matthew Larson.
# About: This is a platforming game where the player is required to jump over
# obstacles as they approach the player. Hit any obstacle and you are dead.

import arcade

#Game constant variables. 
GAME_SPEED = -5
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
UPDATE_RATE = 1 / 60
GRAVITY = 1
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 1000 - 249
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 0
PLAYER_JUMP_SPEED = 30


class Dino_Game(arcade.Window):
    #Acts as a controller. Determines how the game is played.
    #Sets up the screen
    def __init__(self):
        super().__init__()

        self.view_bottom = 0
        self.view_left = 0

        self.wall_list = arcade.SpriteList() #TODO: Create a class for this
        self.ground = Ground()
        self.player_sprite = Player()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = "Hardcore Dino"
        self.update_rate = UPDATE_RATE
        self._background_color = (arcade.csscolor.CORNFLOWER_BLUE)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1500, 25):
            wall = Ground()
            wall.set_position(x, 32)
            self.wall_list.append(wall)

        self.player_list = arcade.SpriteList() #TODO: Create a class for this
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        #self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.jump(PLAYER_JUMP_SPEED)
        
        #self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

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

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

class Physics(arcade.PhysicsEnginePlatformer):

    def __init__(self):
        super().__init__(self.player_sprite, self.wall_list, GRAVITY)

class Player(arcade.Sprite):
    #Player class is responsible for creating the player.
    
    def __init__(self):
        super().__init__("blackbox.png")

        self.change_x = 0
        self.change_y = 0
        self.center_x = 75
        self.center_y = 100

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def jump(self, jump_speed):
        self.change_y = jump_speed



class Ground(arcade.Sprite):
    #Creates the gound and its location.
    def __init__(self):
        super().__init__("blackbox.png")
        #self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y



class Obstacle():
    pass


if __name__ == "__main__":
    dino_game = Dino_Game()
    arcade.run()
