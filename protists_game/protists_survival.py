import sys
import pygame

from settings import Settings
from protists import *

class ProtistSurvival:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # This function initializes the background settings that Pygame needs to work properly.
        self.clock = pygame.time.Clock() # This function creates a clock object that can be used to control the frame rate of the game.
        self.settings = Settings() # This line creates an instance of the Settings class, which contains all the settings for the game, such as screen size and background color.
        
        # The screen is where all the game elements will be displayed.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) # This function creates a window or screen for the game with the specified width and height.
        # The object we assign to self.screen is a surface object. A surface in Pygame is a part of the screen where a game element can be displayed.
        pygame.display.set_caption("Protists Survival")

        self.gintestinalis = Gintestinalis(self) # This line creates an instance of the Gintestinalis class, which represents the Giardia intestinalis protist in the game.
        self.gmuris = Gmuris(self) # This line creates an instance of the Gmuris class, which represents the Giardia muris protist in the game.
        self.spironucleus = Spironucleus(self) # This line creates an instance of the Spironucleus class, which represents the Spironucleus salmonicida protist in the game.
        self.trepomonas = Trepomonas(self) # This line creates an instance of the Trepomonas class, which represents the Trepomonas sp. protist in the game.
        self.hinflata = Hinflata(self) # This line creates an instance of the Hinflata class, which represents the Hexamita inflata protist in the game.

        # Set the background color of the screen.
        self.bg_color = self.settings.bg_color # This line sets the background color of the screen to the value specified in the Settings class.
    
    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            # Watch for keyboard and mouse events. An event is an action that the user performs while playing the game, such as pressing a key or moving the mouse.
            for event in pygame.event.get(): # This function returns a list of events that have taken place since the last time this function was called.
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color) # This function fills the entire screen with the specified color. This is done to clear the screen before drawing new elements on it.
            self.gintestinalis.blitme() # This line calls the blitme method of the Gintestinalis instance, which draws the protist on the screen at its current position.
            
            # Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60) # This function limits the frame rate of the game to 60 frames per second. This is important for ensuring that the game runs smoothly and consistently across different hardware configurations.

if __name__ == '__main__':
    # Make a game instance, and run the game.
    protist = ProtistSurvival()
    protist.run_game()