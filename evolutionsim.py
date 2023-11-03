# todo:
# reduce how often eggs are laid, maybe take egg laying as an output of the NN?
# add mutation to the NN, architectural and random weight additions


import pygame
from organism import organism
import random
from food import food
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolution Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Simulation Settings
settings = {
    'x_min': 0,
    'x_max': WIDTH,
    'y_min': 0,
    'y_max': HEIGHT,
    'v_max': 30,
    'dv_max': 20,
    'dr_max': 90,
    'dt': .2,
    'incubation':15000,
    'FPS' : 30
}

# Initialize list of organisms
my_organisms = [organism(settings) for _ in range(15)]
# Initialize list of food
many_food = [food(settings) for _ in range(70)]
# Initialize list of eggs
eggs = []

# Main game loop
running = True

last_food_spawn = pygame.time.get_ticks()
clock = pygame.time.Clock()

while running:
    # Checking for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Spawns food randomly between 1 and 5 seconds
    food_spawn_interval = random.uniform(1000,5000)
    cur_tick = pygame.time.get_ticks()
    if cur_tick - last_food_spawn > food_spawn_interval:
        many_food.append(food(settings))
        last_food_spawn = cur_tick

    # This loop does a lot of calculations
    for my_organism in my_organisms:
        min_dist = WIDTH+HEIGHT
        for some_food in many_food:
           cur_dist = (my_organism.x - some_food.x)**2 + (my_organism.y - some_food.y)**2
           # Searching for closest food to each organism
           min_dist = min(min_dist,cur_dist)
           # Checks for collision with food
           if cur_dist <= 400:
               # Eats food, updates organism health, if organism is healthy it might lay an egg
               many_food.remove(some_food)
               my_organism.health += some_food.nutrition
               if my_organism.health >= 600 and random.random() < .8:
                   # Lays the egg
                   eggs.append(my_organism.layEgg(.1))
        my_organism.d_food = min_dist

    # This loop moves the organisms and reduces their health
    for my_organism in my_organisms:
        my_organism.move(settings)
        my_organism.draw(screen,20,20)
        my_organism.health-=1.5
        # Organism dies
        if my_organism.health <= 0:
            my_organisms.remove(my_organism)

    # Displays the food
    for some_food in many_food:
        some_food.spawn(screen,5)

    # Waits for incubation time to elapse and hatches the egg into an organism
    for egg in eggs:
        if cur_tick >= egg.laid + settings['incubation']:
            my_organisms.append(egg.hatch(settings))
            eggs.remove(egg)
        egg.draw(screen)


    # Update the display
    pygame.display.update()
    clock.tick(settings['FPS'])

# Quit Pygame
# Don't ask me why I use such a forceful way to close the program, the normal method just wasn't working.
os._exit(0)
