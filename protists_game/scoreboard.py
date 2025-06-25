import pygame.font

class Scoreboard:
    """A class to report scoring information."""
    
    def __init__(self, ps_game, protist):
        """Initialize scorekeeping attributes."""
        self.screen = ps_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ps_game.settings
        self.stats = ps_game.stats
        self.protist = protist
        self.protist_image = ps_game.protist.images['default']  # Get the protist default image

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"Score: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.hud_bg_color)

        # Display the score at the top right corner of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.hud_bg_color)

        # Display the high score at the top center of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats.save_high_score()
            self.prep_high_score()

    def show_score(self):
        """Draw the score, level and lives to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        
        # Draw the protist lives and danger defence bar.
        self.show_lives()
        self.show_danger_defence()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.hud_bg_color)

        # Display the level bellow the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10  # Add some space below

    def show_lives(self):
        """Draw protist icons for remaining lives in the HUD."""
        max_height = 75
        orig_width = self.protist_image.get_width()
        orig_height = self.protist_image.get_height()
        # Calculate new width to keep aspect ratio
        scale_factor = min(1, max_height / orig_height)
        icon_width = int(orig_width * scale_factor)
        icon_height = int(orig_height * scale_factor)
        scaled_icon = pygame.transform.smoothscale(self.protist_image, (icon_width, icon_height))
        spacing = 10
        for i in range(self.stats.lives_left):
            x = 20 + i * (icon_width + spacing)
            y = 20  # Align with the top margin of the HUD
            self.screen.blit(scaled_icon, (x, y))

    def show_danger_defence(self):
        """Draw the protist's danger defence as a horizontal red bar in the HUD, after the lives icons and vertically centered."""
        # Lives icon settings (should match show_lives)
        max_icon_height = 75
        orig_width = self.protist_image.get_width()
        orig_height = self.protist_image.get_height()
        scale_factor = min(1, max_icon_height / orig_height)
        icon_width = int(orig_width * scale_factor)
        icon_height = int(orig_height * scale_factor)
        spacing = 10
        lives_count = self.settings.protist_lives  # Always use the max number of lives

        # Calculate bar position after the last icon, with some extra spacing
        bar_x = 20 + lives_count * (icon_width + spacing) + 20  # 20px extra space after last icon

        # Bar settings
        bar_width = self.protist.danger_defence_max
        bar_height = 25

        # Vertically center the bar with respect to the icons
        icons_top = 20
        bar_y = icons_top + (icon_height - bar_height) // 2

        # Calculate fill based on current defence
        max_defence = max_defence = self.protist.danger_defence_max
        current_defence = self.stats.danger_defence if hasattr(self.stats, "danger_defence") else self.protist.danger_defence_max

        fill_width = int(bar_width * current_defence / max_defence)
        # Draw background (gray)
        pygame.draw.rect(self.screen, (180, 180, 180), (bar_x, bar_y, bar_width, bar_height))
        # Draw filled part (red)
        pygame.draw.rect(self.screen, (220, 50, 50), (bar_x, bar_y, fill_width, bar_height))
        # Optional: Draw border
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)