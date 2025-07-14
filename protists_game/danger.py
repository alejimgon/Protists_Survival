import pygame
import random

from moving_entity import MovingEntity

# Remember to modify the GROUP_ALLOWED_ENERGY and GROUP_ALLOWED_DANGER in group_polygons.py when adding new danger types.

DANGER_TYPES = {
    'hydroxyl_radical': {
        'images': [
            'images/danger/hydroxyl_radical.png',
            # add more hydroxyl radical images if you have them
        ],
        'category': 'ROS',
        'damage': 10,
    },
    'oxygen': {
        'images': [
            'images/danger/oxygen.png',
        ],
        'category': 'ROS',
        'damage': 5,
    },
    'peroxide': {
        'images': [
            'images/danger/peroxide.png',
        ],
        'category': 'ROS',
        'damage': 10,
    },
    'superoxide': {
        'images': [
            'images/danger/superoxide.png',
        ],
        'category': 'ROS',
        'damage': 15,
    },
    # Add more danger types as needed
}

class Danger(MovingEntity):
    """A class to represent danger sources in the game."""

    def __init__(self, screen_rect, settings, danger_type=None):
        if danger_type is None:
            danger_type = random.choice(list(DANGER_TYPES.keys()))
        self.danger_type = danger_type
        image_path = random.choice(DANGER_TYPES[self.danger_type]['images'])
        self.image = pygame.image.load(image_path).convert_alpha()
        super().__init__(screen_rect, settings, 'danger_speed')
        self.rect = self.image.get_rect()
        self.rect.right = screen_rect.right
        min_y = settings.hud_height
        max_y = screen_rect.height - self.rect.height
        self.rect.y = random.randint(min_y, max_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.category = DANGER_TYPES[self.danger_type]['category']
        self.damage = DANGER_TYPES[self.danger_type]['damage']