class Actor:
    """A visible, moveable thing that participates in the game.
    
    The responsibility of Actor is to keep track of its appearance, position 
    and velocity in 2d space.

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
