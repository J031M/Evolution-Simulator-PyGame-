import pygame
from random import uniform

class food:
    '''
    a pretty simple class, the food just appears and waits to get eaten
    '''
    def __init__(self,settings):
        self.x = uniform(settings['x_min'],settings['x_max'])
        self.y = uniform(settings['y_min'],settings['y_max'])
        # nutrition is directly added to the health of an organism
        self.nutrition = 200

    def spawn(self,screen,radius):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), radius)
