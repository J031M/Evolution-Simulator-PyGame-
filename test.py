import os
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here

    # Drawing code
    screen.fill(white)  # Clear the screen with a white background

    # Draw game objects here

    pygame.display.update()  # Update the display

# Quit Pygame
os._exit(0)
pygame.quit()
print('done')

