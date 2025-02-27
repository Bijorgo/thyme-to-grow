# player.py
import pygame

class Player:
    def __init__(self, x, y, character_img):
        self.x = x
        self.y = y
        self.character_img = character_img
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def handle_keys(self, event):
        """Handle key events to move the player."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.moving_right = True
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            if event.key == pygame.K_UP:
                self.moving_up = True
            if event.key == pygame.K_DOWN:
                self.moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.moving_right = False
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            if event.key == pygame.K_UP:
                self.moving_up = False
            if event.key == pygame.K_DOWN:
                self.moving_down = False

    def move(self, delta_time):
        """Update player position based on movement flags."""
        if self.moving_right:
            self.x += 50 * delta_time
        if self.moving_left:
            self.x -= 50 * delta_time
        if self.moving_down:
            self.y += 50 * delta_time
        if self.moving_up:
            self.y -= 50 * delta_time

    def draw(self, screen):
        """Draw the player character on the screen."""
        screen.blit(self.character_img, (self.x, self.y))
