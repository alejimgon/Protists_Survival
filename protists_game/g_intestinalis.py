import pygame

class Gintestinalis:
    """Class to represent the Giardia intestinalis protist in the game."""

    def __init__(self, ai_game):
        """Initialize the protist and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the image of Giardia intestinalis and get its rect.
        self.image = pygame.image.load('images/metamonada/giardia_intestinalis.png')
        self.rect = self.image.get_rect()

        # Start each new protist at the left center of the screen.
        self.rect.midleft = self.screen_rect.midleft

    def blitme(self):
        """Draw the protist at its current location."""
        self.screen.blit(self.image, self.rect)
    