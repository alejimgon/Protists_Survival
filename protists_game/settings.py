class Settings:
    """A class to store all settings for Protist Survival."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200 # This is the width of the game screen in pixels.
        self.screen_height = 775 # This is the height of the game screen in pixels.
        self.bg_color = (230, 230, 230)  # This is a tuple that represents the RGB color of the background. The values range from 0 to 255, where 0 means no color and 255 means full color.

        # Protist settings
        self.protist_speed = 1.5 # This is the speed at which the protists move across the screen. The value is in pixels per frame, meaning that each time the game updates, the protists will move by this number of pixels.