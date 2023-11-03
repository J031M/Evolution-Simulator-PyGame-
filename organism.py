from keras import Sequential
import numpy as np
import random
from keras import layers
from math import cos,sin,radians
import pygame

class organism:
    '''
    Defines an organism that moves around, eats food and lays eggs
    '''
    # converts a sample space from [0,1] to [-1,1]
    normprob = lambda self,x: x*2-1
    # divides distance with the diagonal length of the screen
    divdist = lambda self,x,settings: x/(settings['x_max']**2+settings['y_max']**2)**.5

    def __init__(self,settings,name=None):
        # The neural network of the organism takes in 1 input: distance to nearest food
        self.brain = Sequential([
            layers.Input(shape=(1,1)),
            layers.Dense(5,activation='tanh',name='l1'),
            layers.Dense(5,activation='tanh',name='l2'),
            layers.Dense(2,activation='tanh',name='l3')
            ])

        # Organism's coordinates
        self.x = random.uniform(settings['x_min'],settings['x_max'])
        self.y = random.uniform(settings['y_min'],settings['y_max'])

        # Organism's rotation, velocity and acceleration
        self.r = random.uniform(0,360)
        self.v = random.uniform(0,settings['v_max']//2)  
        self.dv = random.uniform(-settings['dv_max'], settings['dv_max'])

        # health, distance to nearest food, orientation of nearest food
        self.health = 700
        self.d_food = 100   
        self.r_food = 0    

        # its name
        self.name = name

    def move(self,settings):
        ''' 
        moves the organism 

        sends the organism distance to nearest food to the NN and updates the
        x,y coordinates based on the NN output
        '''
        # normalising distance to nearest food to [-1,1] (to avoid NN saturation)
        input_data = np.array([[[self.normprob(self.divdist(self.d_food,settings))]]])
        # the outputs of the NN are the change in rotation and velocity
        nndr,nndv = [x.numpy() for x in self.brain(input_data)[0][0]]

        # scaling neural network rotation output
        self.r += nndr * settings['dr_max'] * settings['dt']
        self.r %= 360

        # scaling neural network velocity output and and checking for max velocity
        self.v += nndv * settings['dv_max'] * settings['dt']
        if self.v < 0: self.v = 0
        if self.v > settings['v_max']: self.v = settings['v_max']

        # updating the organism's coordinates
        dx = self.v * cos(radians(self.r)) * settings['dt']
        dy = self.v * sin(radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy

    def layEgg(self,mutation_rate):
        '''
        the organism lays an egg!
        '''
        egg = Egg(self,mutation_rate)
        return egg

    def draw(self, screen, width, height):
        '''
        pygame stuff to make the organism visible on screen
        '''
        rotated_rect = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rotated_rect, (255,255,255), (0, 0, width, height))
        rotated_rect = pygame.transform.rotate(rotated_rect, -self.r)
        new_rect = rotated_rect.get_rect(center=(self.x, self.y))
        screen.blit(rotated_rect, new_rect.topleft)

class Egg:
    '''
    defines an egg that hatches into a mutated version of its parent
    '''
    def __init__(self,parent,mutation_rate):
        # the time it was laid
        self.laid = pygame.time.get_ticks()
        # copies the parent's NN
        self.brain = parent.brain
        # and x,y coordinates
        self.x = parent.x
        self.y = parent.y
        # probability of a mutation occuring
        self.mutation_rate = mutation_rate

    def hatch(self,settings):
        '''
        after incubation period, the egg hatches into an organism that's 
        slightly mutated from its parent
        '''
        # Copies the parent organism
        egg_organism = organism(settings)
        egg_organism.brain = self.brain
        egg_organism.x = self.x
        egg_organism.y = self.y

        # Applies mutations to the organism
        # This for loop slightly modifies the weights of the NN based on the
        # mutation rate
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
        '''
        pygame stuff to make the egg visible
        '''
        pygame.draw.circle(screen, (100, 100, 0), (self.x, self.y), 7)

# IGNORE THE STUFF BELOW, I was just testing things
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
