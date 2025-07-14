import pygame
import random

from moving_entity import MovingEntity

# Remember to modify the GROUP_ALLOWED_ENERGY and GROUP_ALLOWED_DANGER in group_polygons.py when adding new energy types.

ENERGY_TYPES = {
    'glucose': {
        'images': [
            'images/food/glucose.png',
        ],
        'category': 'carbohydrate',
        'points': 50,
    },
    'fructose': {
        'images': [
            'images/food/fructose.png',
        ],
        'category': 'carbohydrate',
        'points': 50,
    },
    'maltose': {
        'images': [
            'images/food/maltose.png',
        ],
        'category': 'carbohydrate',
        'points': 50,
    },
    'arginine': {
        'images': [
            'images/food/arginine.png',
        ],
        'category': 'amino_acid',
        'points': 50,
    },
        'bacteria': {
            'images': [
                'images/food/bacteria1.png',
                'images/food/bacteria2.png',
                'images/food/bacteria3.png',
                'images/food/bacteria4.png',
                'images/food/bacteria5.png',
                # add more bacteria images
            ],
            'category': 'bacteria',
            'points': 100,
        },
    # Add more types as needed
}


class Energy(MovingEntity):
    """A class to represent energy sources in the game."""

    def __init__(self, screen_rect, settings, energy_type=None):
        if energy_type is None:
            energy_type = random.choice(list(ENERGY_TYPES.keys()))
        self.energy_type = energy_type
        image_path = random.choice(ENERGY_TYPES[self.energy_type]['images'])
        self.image = pygame.image.load(image_path).convert_alpha()
        super().__init__(screen_rect, settings, 'energy_speed')
        self.rect = self.image.get_rect()
        self.rect.right = screen_rect.right
        min_y = settings.hud_height
        max_y = screen_rect.height - self.rect.height
        self.rect.y = random.randint(min_y, max_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.category = ENERGY_TYPES[self.energy_type]['category']
        self.points = ENERGY_TYPES[self.energy_type]['points']