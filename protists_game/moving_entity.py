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
        self.rect = self.image.get_rect()
        self.rect.right = screen_rect.right
        self.rect.y = random.randint(0, screen_rect.height - self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = getattr(settings, speed_attr)

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)