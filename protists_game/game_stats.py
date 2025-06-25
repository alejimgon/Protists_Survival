class GameStats:
    """Class to manage game statistics for Protists Game."""

    def __init__(self, ps_game, protist):
        """Initialize statistics."""
        self.settings = ps_game.settings
        self.protist = protist
        self.danger_defence = protist.danger_defence_max
        self.high_score = 0
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.protist_lives
        self.score = 0
        self.danger_defence = self.protist.danger_defence_max