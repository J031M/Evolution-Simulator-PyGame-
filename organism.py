from keras import Sequential
import numpy as np
import random
from keras import layers
from math import cos,sin,radians
import pygame

class organism:
    normprob = lambda self,x: x*2-1
    divdist = lambda self,x,settings: x/(settings['x_max']**2+settings['y_max']**2)**.5

    def __init__(self,settings,name=None):
        self.brain = Sequential([
            layers.Input(shape=(1,1)),
            layers.Dense(5,activation='tanh',name='l1'),
            layers.Dense(5,activation='tanh',name='l2'),
            layers.Dense(2,activation='tanh',name='l3')
            ])

        self.x = random.uniform(settings['x_min'],settings['x_max'])
        self.y = random.uniform(settings['y_min'],settings['y_max'])

        self.r = random.uniform(0,360)
        self.v = random.uniform(0,settings['v_max']//2)  
        self.dv = random.uniform(-settings['dv_max'], settings['dv_max'])

        self.health = 700
        self.d_food = 100   
        self.r_food = 0    
        self.fitness = 0  

        self.name = name

    def move(self,settings):
        input_data = np.array([[[self.normprob(self.divdist(self.d_food,settings))]]])
        nndr,nndv = [x.numpy() for x in self.brain(input_data)[0][0]]

        self.r += nndr * settings['dr_max'] * settings['dt']
        self.r %= 360

        self.v += nndv * settings['dv_max'] * settings['dt']
        if self.v < 0: self.v = 0
        if self.v > settings['v_max']: self.v = settings['v_max']

        dx = self.v * cos(radians(self.r)) * settings['dt']
        dy = self.v * sin(radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy

    def layEgg(self,mutation_rate):
        egg = Egg(self,mutation_rate)
        return egg

    def draw(self, screen, width, height):
        rotated_rect = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_rect, (255,255,255), (0, 0, width, height))
        rotated_rect = pygame.transform.rotate(rotated_rect, -self.r)
        new_rect = rotated_rect.get_rect(center=(self.x, self.y))
        screen.blit(rotated_rect, new_rect.topleft)

class Egg:
    def __init__(self,parent,mutation_rate):
        self.laid = pygame.time.get_ticks()
        self.brain = parent.brain
        self.x = parent.x
        self.y = parent.y
        self.mutation_rate = mutation_rate

    def hatch(self,settings):
        egg_organism = organism(settings)
        egg_organism.brain = self.brain
        egg_organism.x = self.x
        egg_organism.y = self.y

        for layer in egg_organism.brain.layers:
            weights = layer.get_weights()
            x,y = weights[0].shape
            for m in range(x):
                for n in range(y):
                    if random.random() <= self.mutation_rate:
                        weights[0][m][n] += random.gauss(0,.04)
            layer.set_weights(weights)

        # ADD capability for neural network architecture to change

        return egg_organism

    def draw(self,screen):
        pygame.draw.circle(screen, (100, 100, 0), (self.x, self.y), 7)
        

def main():

    settings = {
        'x_min': 0,
        'x_max': 1000,
        'y_min': 0,
        'y_max': 1000,
        'v_max': 5,
        'dv_max': 1,
        'dr_max': 5,
        'dt': 0.1
    }

    my_organism = organism(settings)
    my_egg = my_organism.layEgg(.1)
    for layer in my_egg.brain.layers:
        weights = layer.get_weights()
        x,y = weights[0].shape
        for m in range(x):
            for n in range(y):
                weights[0][m][n] += random.gauss(0,.1)
        layer.set_weights(weights)

    print('done')

if __name__ == "__main__":
    main()
