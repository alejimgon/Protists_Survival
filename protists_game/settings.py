class Settings:
    """A class to store all settings for Protist Survival."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200 # This is the width of the game screen in pixels.
        self.screen_height = 775 # This is the height of the game screen in pixels.
        self.bg_color = (230, 230, 230)  # This is a tuple that represents the RGB color of the background.

        # Protist settings
        self.protist_speed = 2 # This is the speed at which the protists move across the screen. The value is in pixels per frame, meaning that each time the game updates, the protists will move by this number of pixels.

        # Energy settings
        self.energy_speed = 2  # Speed at which energy sources move across the screen.
        self.energy_spawn_rate = 60

        # Danger settings
        self.danger_speed = 2  # Speed at which dangers move across the screen.
        self.danger_spawn_rate = 60