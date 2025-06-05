import pygame

class Protist:
    """Base class for all protists."""

    def __init__(self, ps_game, image_path): # ps_game is an instance of the ProtistSurvival class.
        """Initialize the protist and set its starting position."""
        self.screen = ps_game.screen
        self.screen_rect = ps_game.screen.get_rect()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft # Position the protist at the left middle of the screen.
        # Movement flag; start with a protist that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Update the protist's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= 1
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= 1
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 1

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Gintestinalis(Protist):
    """Class representing the Giardia intestinalis protist."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/g_intestinalis.png')

class Gmuris(Protist):
    """Class representing the Giardia muris protist."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/g_muris.png')

class Spironucleus(Protist):
    """Class representing the Spironucleus salmonicida protist."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/s_salmonicida.png')

class Trepomonas(Protist):
    """Class representing the Trepomonas sp. protist."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/trepomonas.png')

class Hinflata(Protist):
    """Class representing the Hexamita inflata protist."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/h_inflata.png')
