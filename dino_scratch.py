# Name: Daniel Uchytil, Spencer Warner, Alex Smith, Matthew Larson.
# About: This is a platforming game where the player is required to jump over
# obstacles as they approach the player. Hit any obstacle and you are dead.

import arcade
import random
import time

#Game constant variables. 
LUCK = 4
GAME_SPEED = 0
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
UPDATE_RATE = 1 / 60
GRAVITY = 1
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH - LEFT_VIEWPORT_MARGIN + 1
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100
NUM_LIVES = 20
PLAYER_START = 0

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 12
PLAYER_JUMP_SPEED = 18


class Dino_Game(arcade.Window):
    #Acts as a controller. Determines how the game is played.
    #Sets up the screen
    def __init__(self):
        super().__init__()

        self.view_bottom = 0
        self.view_left = 0
        self.count_collisions = 0
        self._direction = 1
        self.score = 0
        self.reference_time = int(time.time())
        self.reference_time2 = int(time.time())

        self.wall_list = arcade.SpriteList() #TODO: Create a class for this
        self.obstacle_list = arcade.SpriteList() #TODO: Create a class for this
        self.power_up_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = "Hardcore Dino"
        self.update_rate = UPDATE_RATE
        self._background_color = (arcade.csscolor.CORNFLOWER_BLUE)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1000, 25):
            wall = Ground()
            wall.set_position(x, 32)
            self.wall_list.append(wall)

        
        x = 0
        for i in range(6):
            x += random.randint(250, 400)
            #create_obstacle = random.randint()
            obstacle = Obstacle()
            obstacle.set_position(x, 32 + random.randint(38, 150))
            self.obstacle_list.append(obstacle)

        self.player_list = arcade.SpriteList() #TODO: Create a class for this
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.obstacle_list.draw()
        self.player_list.draw()
        self.power_up_list.draw()

        if self.player_sprite.get_lives() == 0:
            arcade.draw_text("YOU LOSE!", SCREEN_WIDTH / 2 + self.view_left, SCREEN_HEIGHT / 2 + self.view_bottom, arcade.csscolor.RED, 75, width=500, align="center")
        
        else:
            self.score = self.player_sprite.get_score()

        score_text = f"Score: {self.score}"
        life_text = f"Lives: {self.player_sprite.get_lives()}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        arcade.draw_text(life_text, 10 + self.view_left, 40 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.jump(PLAYER_JUMP_SPEED)
        

    # def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        '''if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0'''

    def on_update(self, delta_time):
        """ Movement and game logic """

        obstacle_hits = arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list)
        # print(obstacle_hits)
        # print(f"Length of list: {len(obstacle_hits)}")


        for obstacle in obstacle_hits:
            # Remove the coin
            obstacle.remove_from_sprite_lists()
            new_obstacle = Obstacle()
            new_x_position = self.obstacle_list[-1].get_x_position() + random.randint(300, 400)
            new_y_position = self.wall_list[-1].get_y_position() + random.randint(33, 175)
            new_obstacle.set_position(new_x_position, new_y_position)
            self.obstacle_list.append(new_obstacle)
            # Play a sound
            #arcade.play_sound(self.collect_coin_sound)

        if len(obstacle_hits) > 0 and self.player_sprite.get_lives() > 0:
            self.player_sprite.subtract_life()


        if self.player_sprite.get_lives() == 0:
            self._background_color = (arcade.csscolor.ORANGE)
            #arcade.pause(5)
            #print("You LOSE!")
            #arcade.close_window()

        
        power_ups_collected = arcade.check_for_collision_with_list(self.player_sprite, self.power_up_list)

        for power_up in power_ups_collected:
            # Remove the coin
            power_up.remove_from_sprite_lists()
            if power_up.get_id() == 2 and self.player_sprite.get_lives() > 0:
                self.player_sprite.add_life(random.randint(1, 3))
            elif power_up.get_id() == 3:
                self.player_sprite.add_bonus(1000)

            # Play a sound
            #arcade.play_sound(self.collect_coin_sound)

        #print(f"Num obstacles remaining: {len(obstacle_list)}")

        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Move the player with the physics engine
        self.physics_engine.update()

        # # --- Manage Scrolling ---

        # # Track if we need to change the viewport

        changed = True

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

        # Adds obstacles and deletes them as they leave the screen.
        for i in range(len(self.obstacle_list)):
            if self.obstacle_list[i].get_x_position() < self.view_left:
                self.obstacle_list.pop(i)
                new_obstacle = Obstacle()
                new_x_position = self.obstacle_list[-1].get_x_position() + random.randint(300, 400)
                new_y_position = self.wall_list[-1].get_y_position() + random.randint(45, 150)
                new_obstacle.set_position(new_x_position, new_y_position)
                self.obstacle_list.append(new_obstacle)
                #print("I am adding obstacles")

        

        # Adds ground and deletes them as they leave the screen.
        for i in range(len(self.wall_list)):
            if self.wall_list[i].get_x_position() < self.view_left:
                self.wall_list.pop(i)
                new_wall = Ground()

                ping1 = int(time.time())

                if ping1 - self.reference_time == 17:
                    self._direction = self._direction * -1
                    self.reference_time = ping1

                magnitude = random.randint(1, 2)
                
                offset = self._direction * int(random.randint(0, 10) % LUCK == 0) * magnitude

                x_pos = self.wall_list[-1].get_x_position() + 25
                y_pos = self.wall_list[-1].get_y_position() + offset

                new_wall.set_position(x_pos, y_pos)
                self.wall_list.append(new_wall)
                #print("I am adding ground")

        ping2 = int(time.time())

        if ping2 - self.reference_time2 == (2 * LUCK):
            power_up_id = random.randint(2, 3)
            image_names = ["Life.png", "Coin.png"]
            power_up = Power_Up(power_up_id, image_names[power_up_id - 2])
            altitude = self.wall_list[-1].get_y_position() + random.randint(35, 70)
            power_up.set_position(self.wall_list[-1].get_x_position(), altitude)
            self.power_up_list.append(power_up)
            self.reference_time2 = ping2



class Player(arcade.Sprite):
    #Player class is responsible for creating the player.
    
    def __init__(self):
        super().__init__("redbox.png")

        self.change_x = 0
        self.change_y = 0
        self.center_x = PLAYER_START
        self.center_y = 100
        self._life_count = NUM_LIVES
        self._score_bonus = 0

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def jump(self, jump_speed):
        self.change_y = jump_speed

    def get_lives(self):
        return self._life_count

    def subtract_life(self):
        self._life_count -= 1

    def add_life(self, added_life = 1):
        self._life_count += added_life

    def add_bonus(self, bonus = 0):
        self._score_bonus += bonus

    def get_score(self):
        return int((self.center_x - PLAYER_START) / 4) + self._score_bonus



class Ground(arcade.Sprite):
    #Creates the gound and its location.
    def __init__(self):
        super().__init__("Ground.png")
        #self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10
        self._id = 0

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def get_id(self):
        return self._id

    def get_x_position(self):
        return self.center_x

    def get_y_position(self):
        return self.center_y


class Obstacle(arcade.Sprite):
    def __init__(self):
        super().__init__("obstacle.png")
        #self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10
        self._id = 1

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def get_id(self):
        return self._id

    def get_x_position(self):
        return self.center_x


class Power_Up(arcade.Sprite):
    def __init__(self, item_id = 2, image_name_in = "obstacle.png"):
        super().__init__(image_name_in)
        #self.boundary_top = None
        self.change_x = GAME_SPEED
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10
        self._id = item_id

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def get_id(self):
        return self._id

    def set_id(self, new_id = 1):
        self._id = new_id

    def get_x_position(self):
        return self.center_x


if __name__ == "__main__":
    dino_game = Dino_Game()
    arcade.run()