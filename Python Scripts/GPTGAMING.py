# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:03:54 2023

@author: hv872f
"""
import sys
import pygame
from pygame.time import Clock

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [screen_width // 2, screen_height // 2]
        self.speed = 5

    def update(self, keys):
        # Handle player movement
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed
        self.rect.move_ip(dx, dy)

# Define the AI class
class AI(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, player_pos):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = [screen_width // 2, 0]
        self.speed = 3
        self.player_pos = player_pos
        self.spear_timer = 0

    def update(self, delta_time):
        # Calculate the direction vector towards the player
        direction = [self.player_pos[0] - self.rect.centerx, self.player_pos[1] - self.rect.centery]

        # Normalize the direction vector
        magnitude = (direction[0]**2 + direction[1]**2)**0.5
        if magnitude > 0:
            normalized_direction = [direction[0] / magnitude, direction[1] / magnitude]
        else:
            normalized_direction = [0, 0]

        # Update the AI's position
        self.rect.move_ip(normalized_direction[0] * self.speed, normalized_direction[1] * self.speed)

        # Update the spear timer
        self.spear_timer += delta_time

        # Check if the AI is in range to thrust the spear
        if self.spear_timer > 1000 and magnitude <= 60:  # Adjust the range if needed
            self.spear_timer = 0
            # Code for AI spear thrusting

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('My 2D Overhead Game')

# Create the player and AI sprites
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
ai = AI(SCREEN_WIDTH, SCREEN_HEIGHT, player.rect.center)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player, ai)

# Main game loop
clock = Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Update the AI
    ai.update(clock.tick(60))

    # Draw the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Update the display
    pygame.display.update()

    # Set the maximum frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()



