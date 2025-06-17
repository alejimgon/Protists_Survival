import pygame
from pygame.sprite import Sprite
import random

class Danger(Sprite):
    """A class to represent danger sources in the game."""

    DANGER_IMAGES = [
        'images/danger/hydroxyl_radical.png',
        'images/danger/oxygen.png',
        'images/danger/peroxide.png',
        'images/danger/superoxide.png'
    ]


    def __init__(self, screen_rect, settings):
        super().__init__()
        # Choose a random danger image
        image_path = random.choice(self.DANGER_IMAGES)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        # Start at a random vertical position on the right edge
        self.rect.right = screen_rect.right
        self.rect.y = random.randint(0, screen_rect.height - self.rect.height)

        # For pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = settings.danger_speed  # Speed at which dangers move across the screen

    def update(self):
        """Move the danger left across the screen."""
        self.rect.x -= self.speed

    def draw(self, screen):
        """Draw the danger on the screen."""
        screen.blit(self.image, self.rect)