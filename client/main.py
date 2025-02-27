# client/main.py
# Import Modules
import os
import pygame
import requests

# entry point for game
# from documentation- line by line chimp :
#main_dir = os.path.split(os.path.abspath(__file__))[0] #returns absolute path of current script(main.py), split into tuple (directory path, file name), [0] accesses first element of tuple
    # in short: sets main_dir to where main.py is located
#data_dir = os.path.join(main_dir, "data") # creates path to sub directory "data"

pygame.init()

# Create window, dimensions f window as a tuple
screen = pygame.display.set_mode((640,640))
    # top left = (0,0)
    # middle = (320, 320) => x/2, y/2

# load imgs
character_img = pygame.image.load('charactersprite.png').convert_alpha()
# Change img size by scale
character_img = pygame.transform.scale( character_img,
                                       (character_img.get_width() * 2,
                                        character_img.get_height() *2
                                        ))


# Game loop
running = True
# Starting coodinates
x = 0
y = 320
clock = pygame.time.Clock()
# Assists in frame rate for smooth 
delta_time = 0.1

# Gate movement for key events
moving_right = False
moving_left = False
moving_up = False
moving_down = False
while running:

    # Fill background in green:(0, 255, 0)
    screen.fill((0, 255, 0))

    screen.blit(character_img, (x, y))

    if moving_right:
        x += 50 * delta_time
    if moving_left:
        x -= 50 * delta_time
    if moving_down:
        y += 50 * delta_time
    if moving_up:
        y -= 50 * delta_time

    # Allow game window to close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement
        if event.type == pygame.KEYDOWN: # on keypress:
            if event.key == pygame.K_RIGHT: # check docs for available keys
                moving_right = True
            if event.key == pygame.K_LEFT:
                    moving_left = True
            if event.key == pygame.K_UP:
                    moving_up = True
            if event.key == pygame.K_DOWN:
                    moving_down = True

        if event.type == pygame.KEYUP: # on let go of key:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                    moving_left = False
            if event.key == pygame.K_UP:
                    moving_up = False
            if event.key == pygame.K_DOWN:
                    moving_down = False

    # Takes what we've put on the screen surface and displays on window
    pygame.display.flip() 

    # desired frame rate
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()