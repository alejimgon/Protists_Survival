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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # This function creates a window or screen for the game with the specified width and height.
        self.settings.screen_width = self.screen.get_rect().width # This line sets the screen width to the width of the screen rectangle, which is the area where the game will be displayed.
        self.settings.screen_height = self.screen.get_rect().height # This line sets the screen height to the height of the screen rectangle.
        # The object we assign to self.screen is a surface object. A surface in Pygame is a part of the screen where a game element can be displayed.
        pygame.display.set_caption("Protists Survival")

        self.gintestinalis = Gintestinalis(self) # This line creates an instance of the Gintestinalis class, which represents the Giardia intestinalis protist in the game.
        
        # Set the background color of the screen.
        self.bg_color = self.settings.bg_color # This line sets the background color of the screen to the value specified in the Settings class.
    
    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events() # This function checks for any events that have occurred, such as key presses or mouse movements. It is called at the beginning of each iteration of the game loop to ensure that the game responds to user input.
            self.gintestinalis.update() # This line calls the update method of the Gintestinalis instance, which updates the position and state of the protist based on user input or game logic. This is important for making the protist move or change in response to player actions
            self._update_screen() # This function updates the screen with the current state of the game. It is called at the end of each iteration of the game loop to ensure that the screen is redrawn with the latest game elements.
            self.clock.tick(60) # This function limits the frame rate of the game to 60 frames per second. This is important for ensuring that the game runs smoothly and consistently across different hardware configurations.

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        # Watch for keyboard and mouse events. An event is an action that the user performs while playing the game, such as pressing a key or moving the mouse.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event) 
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # This function checks if a key has been pressed down. If it has, it checks which key was pressed and sets the corresponding movement flag to True.
        if event.key == pygame.K_UP:
            self.gintestinalis.moving_up = True
            self.gintestinalis.image = self.gintestinalis.images['up']  # Change image to the one for moving up 
        elif event.key == pygame.K_DOWN:
            self.gintestinalis.moving_down = True 
            self.gintestinalis.image = self.gintestinalis.images['down']
        elif event.key == pygame.K_LEFT:
            self.gintestinalis.moving_left = True 
            self.gintestinalis.image = self.gintestinalis.images['left']
        elif event.key == pygame.K_RIGHT:
            self.gintestinalis.moving_right = True
            self.gintestinalis.image = self.gintestinalis.images['right']
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # Quit the game when 'q' or 'ESC' is pressed.
            sys.exit()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        # This function checks if a key has been released. If it has, it checks which key was released and sets the corresponding movement flag to False.
        if event.key == pygame.K_UP:
            self.gintestinalis.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.gintestinalis.moving_down = False
        elif event.key == pygame.K_LEFT:
            self.gintestinalis.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.gintestinalis.moving_right = False

        # Set image based on which keys are still pressed
        if self.gintestinalis.moving_up:
            self.gintestinalis.image = self.gintestinalis.images['up']
        elif self.gintestinalis.moving_down:
            self.gintestinalis.image = self.gintestinalis.images['down']
        elif self.gintestinalis.moving_left:
            self.gintestinalis.image = self.gintestinalis.images['left']
        elif self.gintestinalis.moving_right:
            self.gintestinalis.image = self.gintestinalis.images['right']
        else:
            self.gintestinalis.image = self.gintestinalis.images['default']
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color) # This function fills the entire screen with the specified color. This is done to clear the screen before drawing new elements on it.
        self.gintestinalis.blitme() # This line calls the blitme method of the Gintestinalis instance, which draws the protist on the screen at its current position.
        # Make the most recently drawn screen visible.
        pygame.display.flip()
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    protist = ProtistSurvival()
    protist.run_game()