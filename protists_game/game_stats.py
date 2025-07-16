import json
import os

class GameStats:
    """Class to manage game statistics for Protists Game."""

    def __init__(self, ps_game, protist):
        """Initialize statistics."""
        self.settings = ps_game.settings
        self.protist = protist
        self.danger_defence = protist.danger_defence_max
        self.high_scores = self.load_high_scores()
        self.high_score = self.high_scores.get(self.protist.name, 0)
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.protist_lives
        self.score = 0
        self.level = 1
        self.danger_defence = self.protist.danger_defence_max

    def load_high_scores(self):
        """Load the high scores from a file."""
        try:
            with open("protists_game/high_score.txt", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_high_score(self):
        """Save the high score for the current protist."""
        # Update the high score for this protist
        self.high_scores[self.protist.name] = max(self.score, self.high_scores.get(self.protist.name, 0))
        with open("protists_game/high_score.txt", "w") as f:
            json.dump(self.high_scores, f, indent=4)

    def check_high_score(self):
        """Check and update high score if needed."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()