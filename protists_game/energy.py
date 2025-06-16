import pygame
from pygame.sprite import Sprite
import random

class Energy(Sprite):
    """A class to represent energy sources in the game."""


    FOOD_IMAGES = [
        'images/food/glucose.png',
        'images/food/fructose.png',
        'images/food/arginine.png'
    ]

    def __init__(self, screen_rect, speed=2):
        super().__init__()
        # Choose a random food image
        image_path = random.choice(self.FOOD_IMAGES)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        # Start at a random vertical position on the right edge
        self.rect.right = screen_rect.right
        self.rect.y = random.randint(0, screen_rect.height - self.rect.height)

        # For pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed

    def update(self):
        """Move the food left across the screen."""
        self.rect.x -= self.speed

    def draw(self, screen):
        """Draw the food on the screen."""
        screen.blit(self.image, self.rect)