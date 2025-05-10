import sys

import pygame

class ProtistSurvival:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # This function initializes the background settings that Pygame needs to work properly.
        self.clock = pygame.time.Clock() # This function creates a clock object that can be used to control the frame rate of the game.
        self.screen = pygame.display.set_mode((1200, 775)) # This function creates a window  of the specified size, on which we'll draw all the game's graphical elements.
        # The object we assign to self.screen is a surface object. A surface in Pygame is a part of the screen where a game element can be displayed.
        pygame.display.set_caption("Protists Survival")

        # Set the background color of the screen.
        self.bg_color = (230, 230, 230) # This is a tuple that represents the RGB color of the background. The values range from 0 to 255, where 0 means no color and 255 means full color.

    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            # Watch for keyboard and mouse events. An event is an action that the user performs while playing the game, such as pressing a key or moving the mouse.
            for event in pygame.event.get(): # This function returns a list of events that have taken place since the last time this function was called.
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color) # This function fills the entire screen with the specified color. This is done to clear the screen before drawing new elements on it.

            # Make the most recently drawn screen visible.
            pygame.display.flip()
            self.clock.tick(60) # This function limits the frame rate of the game to 60 frames per second. This is important for ensuring that the game runs smoothly and consistently across different hardware configurations.

if __name__ == '__main__':
    # Make a game instance, and run the game.
    protist = ProtistSurvival()
    protist.run_game()