import pygame

class Protist:
    """Base class for all protists."""

    def __init__(self, ps_game, image_path): # ps_game is an instance of the ProtistSurvival class.
        """Initialize the protist and set its starting position."""
        self.screen = ps_game.screen
        self.screen_rect = ps_game.screen.get_rect()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

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
