from moving_entity import MovingEntity

class Danger(MovingEntity):
    """A class to represent danger sources in the game."""
    IMAGE_LIST = [
        'images/danger/hydroxyl_radical.png',
        'images/danger/oxygen.png',
        'images/danger/peroxide.png',
        'images/danger/superoxide.png'
    ]

    def __init__(self, screen_rect, settings):
        super().__init__(screen_rect, settings, 'danger_speed')