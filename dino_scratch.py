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
NUM_LIVES = 6
PLAYER_START = 0
SUPER_JUMP_DURATION = 15

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 12
PLAYER_JUMP_SPEED = 18
SUPER_JUMP_SPEED = 19


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
        self.super_jump_time = 0

        self.wall_list = arcade.SpriteList() #TODO: Create a class for this
        self.obstacle_list = arcade.SpriteList() #TODO: Create a class for this
        self.power_up_list = arcade.SpriteList()
        self.cloud_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.title = "Parkour Dino"
        self.update_rate = UPDATE_RATE
        self._background_color = (arcade.csscolor.CORNFLOWER_BLUE)

        
        self.background_sound = arcade.load_sound("Sounds/funkyrobot.mp3")
        self.obstacle_sound = arcade.load_sound("Sounds/hurt2.wav")
        self.extra_jump_sound = arcade.load_sound("Sounds/power_up_01.ogg")

        arcade.play_sound(self.background_sound, 0.3)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1026, 25):
            wall = Ground()
            wall.set_position(x, 32)
            self.wall_list.append(wall)
        
        x = 0
        for i in range(5):
            x += random.randint(250, 400)
            #create_obstacle = random.randint()
            if i < 4:
                obstacle = Obstacle()
                obstacle.set_position(x, 32 + random.randint(38, 150))
                self.obstacle_list.append(obstacle)

            cloud = Cloud()
            cloud.set_position(x + random.randint(20, 100), 32 + random.randint(200, 450))
            self.cloud_list.append(cloud)
            cloud = Cloud("StormCloud1.png") # Included to speed up loading time

        self.player_list = arcade.SpriteList() #TODO: Create a class for this
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.obstacle_list.draw()
        self.wall_list.draw()
        self.power_up_list.draw()
        self.player_list.draw()
        self.cloud_list.draw()


        if self.player_sprite.get_lives() == 0:
            arcade.draw_text("Game Over!", SCREEN_WIDTH / 2 + self.view_left, SCREEN_HEIGHT / 2 + self.view_bottom, arcade.csscolor.RED, 75, width=500, align="center")
        
        else:
            self.score = self.player_sprite.get_score()

        score_text = f"Score: {self.score}"

        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.BLACK, 18)

        if self.super_jump_time > 0:

            super_jump_text = f"Super Jump Time: {self.super_jump_time - int(time.time())}"

            arcade.draw_text(super_jump_text, 10 + self.view_left, 40 + self.view_bottom, arcade.csscolor.BLACK, 18)

        for x in range(self.player_sprite.get_lives()):
            arcade.draw_polygon_filled([[20*x + self.view_left+10,self.view_bottom+450],[20*x + self.view_left+1,self.view_bottom+459],[20*x + self.view_left+2,self.view_bottom+462],
            [20*x + self.view_left+5,self.view_bottom+464],[20*x + self.view_left+8,self.view_bottom+464],[20*x + self.view_left+10,self.view_bottom+461],
            [20*x + self.view_left+12,self.view_bottom+464],[20*x + self.view_left+15,self.view_bottom+464],[20*x + self.view_left+18,self.view_bottom+462],
            [20*x + self.view_left+19,self.view_bottom+459]], (255,0,0))

        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump(20):
                if self.physics_engine.jumps_since_ground > 0:
                    self.player_sprite.jump(SUPER_JUMP_SPEED, True)
                else:
                    self.player_sprite.jump(PLAYER_JUMP_SPEED)
                self.physics_engine.increment_jump_counter()


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
            if self.player_sprite.get_lives() > 0:
                arcade.play_sound(self.obstacle_sound)

        if len(obstacle_hits) > 0 and self.player_sprite.get_lives() > 0:
            self.player_sprite.subtract_life()

        if self.super_jump_time == int(time.time()):
            self.physics_engine.disable_multi_jump()
            self.super_jump_time = 0

        if self.player_sprite.get_lives() == 0:
            self._background_color = (arcade.csscolor.DARK_GRAY)

        
        power_ups_collected = arcade.check_for_collision_with_list(self.player_sprite, self.power_up_list)

        if self.player_sprite.get_lives() > 0:
            for power_up in power_ups_collected:
                # Remove the power up item
                power_up.remove_from_sprite_lists()
                if power_up.get_id() == 2:
                    self.player_sprite.add_life(random.randint(1, 3))
                elif power_up.get_id() == 3:
                    self.player_sprite.add_bonus(1000)
                elif power_up.get_id() == 4:
                    # Enable double jump for some time
                    self.physics_engine.enable_multi_jump(2)
                    if self.super_jump_time > 0:
                        self.super_jump_time += int(0.8 * SUPER_JUMP_DURATION)
                    else:
                        self.super_jump_time = int(time.time()) + SUPER_JUMP_DURATION
                    arcade.play_sound(self.extra_jump_sound)

        #print(f"Num obstacles remaining: {len(obstacle_list)}")

        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Remove clouds as the leave the screen, then add more
        for s in range(len(self.cloud_list)):
            self.cloud_list[s].change_x = PLAYER_MOVEMENT_SPEED
            if self.cloud_list[s].get_x_position() < self.view_left - 75:
                self.cloud_list.pop(s)
                if self.player_sprite.get_lives() == 0:
                    new_cloud = Cloud("StormCloud1.png", 0.1)
                else:
                    new_cloud = Cloud()
                new_x_position = self.cloud_list[-1].get_x_position() + random.randint(90, 700)
                new_y_position = self.wall_list[-1].get_y_position() + random.randint(200, 450)
                new_cloud.set_position(new_x_position, new_y_position)
                self.cloud_list.append(new_cloud)

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
            if self.obstacle_list[i].get_x_position() < self.view_left - 15:
                self.obstacle_list.pop(i)
                new_obstacle = Obstacle()
                new_x_position = self.obstacle_list[-1].get_x_position() + random.randint(300, 400)
                new_y_position = self.wall_list[-1].get_y_position() + random.randint(45, 150)
                new_obstacle.set_position(new_x_position, new_y_position)
                self.obstacle_list.append(new_obstacle)
                #print("I am adding obstacles")

        # Remove power ups that have left the screen
        for i in range(len(self.power_up_list)):
            if self.power_up_list[i].get_x_position() < self.view_left - 15:
                self.power_up_list.pop(i)

        # Adds ground and deletes them as they leave the screen.
        for i in range(len(self.wall_list)):
            if self.wall_list[i].get_x_position() < self.view_left - 15:
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

        

        # Generate random power-ups
        ping2 = int(time.time())

        if ping2 - self.reference_time2 == (2 * LUCK):
            power_up_id = random.randint(2, 4)
            image_names = ["Life.png", "Coin.png", "SuperJump.png"]
            power_up = Power_Up(power_up_id, image_names[power_up_id - 2])
            altitude = self.wall_list[-1].get_y_position() + random.randint(35, 70)
            power_up.set_position(self.wall_list[-1].get_x_position(), altitude)
            self.power_up_list.append(power_up)
            self.reference_time2 = ping2



class Player(arcade.Sprite):
    #Player class is responsible for creating the player and keeping track of its life and score.
    
    def __init__(self):
        super().__init__("T_Rex0.png", 0.07)

        self.change_x = 0
        self.change_y = 0
        self.center_x = PLAYER_START
        self.center_y = 100
        self._life_count = NUM_LIVES
        self._score_bonus = 0
        self.die_sound = arcade.load_sound("Sounds/lose5.wav")
        self.jump_sound = arcade.load_sound("Sounds/jump_2.ogg")
        self.super_jump_sound = arcade.load_sound("Sounds/laser1.mp3")
        self.power_up_sounds = [arcade.load_sound("Sounds/power_up_01.ogg"),
         arcade.load_sound("Sounds/power_up_02.ogg"), arcade.load_sound("Sounds/power_up_03.ogg")]
        self.coin_sound = arcade.load_sound("Sounds/retro_coin_01.ogg")

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def jump(self, jump_speed, second_jump = False):
        if second_jump:
            self.change_y = jump_speed
            arcade.play_sound(self.super_jump_sound, 1.5)
        else:
            self.change_y = jump_speed
            arcade.play_sound(self.jump_sound)

    def get_lives(self):
        return self._life_count

    def subtract_life(self):
        self._life_count -= 1
        if self._life_count == 0:
            arcade.play_sound(self.die_sound)

    def add_life(self, added_life = 1):
        self._life_count += added_life
        arcade.play_sound(self.power_up_sounds[2])

    def add_bonus(self, bonus = 0):
        self._score_bonus += bonus
        if self._life_count > 0:
            arcade.play_sound(self.coin_sound)

    def get_score(self):
        return int((self.center_x - PLAYER_START) / 10) + self._score_bonus



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
    def __init__(self, image_name_in = "boxCrate_single.png", scale = 0.45):
        super().__init__(image_name_in, scale)
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

class Cloud(arcade.Sprite):
    def __init__(self, image_name_in = "Cloud1.png", scale_in = 0.1):
        super().__init__(image_name_in, scale_in)
        #self.boundary_top = None
        self.change_x = int(PLAYER_MOVEMENT_SPEED)
        self.change_y = 0
        self.center_x = 10
        self.center_y = 10

    def set_position(self, location_x, location_y):
        self.center_x = location_x
        self.center_y = location_y

    def set_id(self, new_id = 1):
        self._id = new_id

    def get_x_position(self):
        return self.center_x

    def set_speed(self, speed_in = PLAYER_MOVEMENT_SPEED):
        self.change_x = speed_in


if __name__ == "__main__":
    dino_game = Dino_Game()
    arcade.run()