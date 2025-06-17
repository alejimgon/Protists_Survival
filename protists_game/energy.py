from moving_entity import MovingEntity

class Energy(MovingEntity):
    """A class to represent energy sources in the game."""
    IMAGE_LIST = [
        'images/food/glucose.png',
        'images/food/fructose.png',
        'images/food/arginine.png'
    ]

    def __init__(self, screen_rect, settings):
        super().__init__(screen_rect, settings, 'energy_speed')