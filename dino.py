# Name: Daniel Uchytil, Alex Smith, Spencer Warner, Matthew Larson
# Game: Dino jumper

import arcade
import math
import time


class dino_game():

    '''
    A 2D game where the player jumps to avoid obstacles moving toward them.

    The responsibility of this class is to use other classes to controll how
    this game is played. 

    Sterotype: Controller
    '''

    def __init__(self):
        self._obstacle = Obstacle()
        self._dino = Dino()
        self._score = Score()
        self._map = Map()


    def game_play(self):
        ''' This method is responsible for game play sequence. '''
        pass


    def update_score(self):
        ''' This method is responsible for updating Dino's Score. '''
        pass


    





    if __name__ == "__main__":
        pass











