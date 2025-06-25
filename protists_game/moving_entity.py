import pygame
import random

from pygame.sprite import Sprite

class MovingEntity(Sprite):
    """Base class for moving entities like food and danger."""

    IMAGE_LIST = []  # Should be overridden by subclasses

    def __init__(self, screen_rect, settings, speed_attr):
        super().__init__()
        image_path = random.choice(self.IMAGE_LIST)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.settings = settings
        self.screen_rect = screen_rect
        self.rect = self.image.get_rect()
        self.rect.right = screen_rect.right
        # Only spawn below the HUD area
        min_y = settings.hud_height
        max_y = screen_rect.height - self.rect.height
        self.rect.y = random.randint(min_y, max_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = getattr(settings, speed_attr)
        self.vertical_speed = random.choice([-1, 1]) * random.uniform(1, 2) # Random initial direction and speed


    def update(self):
        self.rect.x -= self.speed

        # Zig-zag vertical movement
        self.rect.y += self.vertical_speed

        # Prevent entity from moving into the HUD area or below the screen
        min_y = self.settings.hud_height
        max_y = self.screen_rect.height - self.rect.height

        if self.rect.y < min_y:
            self.rect.y = min_y
            self.vertical_speed *= -1  # Reverse direction
        elif self.rect.y > max_y:
            self.rect.y = max_y
            self.vertical_speed *= -1  # Reverse direction


    def draw(self, screen):
        screen.blit(self.image, self.rect)