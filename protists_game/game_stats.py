class GameStats:
    """Class to manage game statistics for Protists Game."""

    def __init__(self, ps_game, protist):
        """Initialize statistics."""
        self.settings = ps_game.settings
        self.protist = protist
        self.danger_defence = protist.danger_defence_max
        self.high_score = 0
        self.load_high_score()
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.protist_lives
        self.score = 0
        self.level = 1
        self.danger_defence = self.protist.danger_defence_max

    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open("protists_game/high_score.txt", "r") as f:
                self.high_score = int(f.read())
        except (FileNotFoundError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        with open("protists_game/high_score.txt", "w") as f:
            f.write(str(self.high_score))