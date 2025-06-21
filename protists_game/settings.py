class Settings:
    """A class to store all settings for Protist Survival."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200 
        self.screen_height = 775
        self.bg_color = (230, 230, 230)
        self.hud_height = 100
        self.hud_bg_color = (200, 220, 255)

        # Protist settings
        self.protist_lives = 3
        self.protist_danger_depletion_rate = 10
        self.protist_danger_replenish_rate = 5

        # Energy settings
        self.energy_spawn_rate = 60
        self.energy_chance = 0.5 

        # Danger settings 
        self.danger_spawn_rate = 60 
        self.danger_chance = 0.3

        # How quickly the game and the protist speed up
        self.speedup_scale = 1.1
        self.protist_speedup_scale = 1.05

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.protist_speed = 2.0
        self.energy_speed = 1.5
        self.danger_speed = 1.5

         # Scoring settings
        self.energy_points = 50


    def increase_speed(self):
        """Increase speed settings."""
        self.protist_speed *= self.protist_speedup_scale
        self.energy_speed *= self.speedup_scale
        self.danger_speed *= self.speedup_scale

       