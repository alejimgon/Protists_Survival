import sys
import pygame
import random

from settings import Settings
from protists import *
from energy import Energy
from danger import Danger

class ProtistSurvival:
    """Overall class to manage game assets and behavior."""


    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # This function initializes the background settings that Pygame needs to work properly.
        self.clock = pygame.time.Clock() # This function creates a clock object that can be used to control the frame rate of the game.
        self.settings = Settings()

        # The screen is where all the game elements will be displayed.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        # Set the title of the game window.
        pygame.display.set_caption("Protists Survival")

        self.protist = Gintestinalis(self) # This line creates an instance of the selected protist class.

        self.foods = pygame.sprite.Group()
        self.danger = pygame.sprite.Group()
        self.food_spawn_timer = 0  # Timer for spawning food
        self.danger_spawn_timer = 0  # Timer for spawning dangers
        
        # Set the background color of the screen.
        self.bg_color = self.settings.bg_color

        # Map pygame keys to protist movement attributes
        self.key_to_flag = {
            pygame.K_LEFT: 'moving_left',
            pygame.K_RIGHT: 'moving_right',
            pygame.K_UP: 'moving_up',
            pygame.K_DOWN: 'moving_down'
        }

    
    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events() # This function checks for any events that have occurred, such as key presses or mouse movements. It is called at the beginning of each iteration of the game loop to ensure that the game responds to user input.
            self.protist.update() # This line calls the update method of the Gintestinalis instance, which updates the position and state of the protist based on user input or game logic. This is important for making the protist move or change in response to player actions
            
            # Spawn food and energy
            self._spawn_entity('food_spawn_timer', self.settings.energy_spawn_rate, self.settings.energy_chance, Energy, self.foods)
            self._spawn_entity('danger_spawn_timer', self.settings.danger_spawn_rate, self.settings.danger_chance, Danger, self.danger)
        
            # Update all food and danger positions
            self.foods.update()
            self.danger.update()

            for food in pygame.sprite.spritecollide(self.protist, self.foods, dokill=True, collided=pygame.sprite.collide_mask):
                # Handle food collection (increase score, energy, etc.)
                pass

            for danger in pygame.sprite.spritecollide(self.protist, self.danger, dokill=True, collided=pygame.sprite.collide_mask):
                # Handle danger collision (reduce health, game over, etc.)
                pass

            # Remove food and danger that has moved off the left edge
            self._remove_offscreen_entities(self.foods)
            self._remove_offscreen_entities(self.danger)

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
    

    def _set_movement_flag(self, event, value):
        """Set the appropriate movement flag on the protist."""
        if event.key in self.key_to_flag:
            setattr(self.protist, self.key_to_flag[event.key], value)
    

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        self._set_movement_flag(event, True)
        if event.key == pygame.K_LEFT:
            self.protist.anim_toggle = True
            self.protist.last_direction = 'left'
        elif event.key == pygame.K_RIGHT:
            self.protist.anim_toggle = True
            self.protist.last_direction = 'right'
        elif event.key == pygame.K_UP:
            self.protist.anim_toggle = True
            # If neither left nor right is pressed, default to right
            if not self.protist.moving_left and not self.protist.moving_right:
                self.protist.last_direction = 'right'
            self.protist.set_image(self.protist.images[self.protist.last_direction])
        elif event.key == pygame.K_DOWN:
            self.protist.anim_toggle = True
            # If neither left nor right is pressed, default to right
            if not self.protist.moving_left and not self.protist.moving_right:
                self.protist.last_direction = 'right'
            self.protist.set_image(self.protist.images[self.protist.last_direction])
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        self._set_movement_flag(event, False)
        # Only stop animation if no movement keys are pressed
        if not (self.protist.moving_left or self.protist.moving_right or
                self.protist.moving_up or self.protist.moving_down):
            self.protist.anim_toggle = False
        self._update_protist_image()


    def _update_protist_image(self):
        """Update the protist's image based on movement."""
        # Only set to default if NO movement keys are pressed
        if not (self.protist.moving_left or self.protist.moving_right or
                self.protist.moving_up or self.protist.moving_down):
            self.protist.set_image(self.protist.images['default'])
        else:
            # If still moving left or right, keep that image
            if self.protist.moving_left:
                self.protist.set_image(self.protist.images['left'])
                self.protist.last_direction = 'left'
            elif self.protist.moving_right:
                self.protist.set_image(self.protist.images['right'])
                self.protist.last_direction = 'right'
            else:
                # If moving up/down only, keep last horizontal direction image
                self.protist.set_image(self.protist.images[self.protist.last_direction])


    def _spawn_entity(self, timer_attr, spawn_rate, chance, entity_class, group):
        """Generic spawner for food and danger."""
        setattr(self, timer_attr, getattr(self, timer_attr) + 1)
        if getattr(self, timer_attr) > spawn_rate:
            if random.random() < chance:
                entity = entity_class(self.screen.get_rect(), self.settings)
                group.add(entity)
            setattr(self, timer_attr, 0)

    
    def _remove_offscreen_entities(self, group):
        for entity in list(group):
            if entity.rect.right < 0:
                group.remove(entity)
          
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.bg_color) # This function fills the entire screen with the specified color. This is done to clear the screen before drawing new elements on it.
        self.protist.blitme() # This line calls the blitme method of the selected protist instance, which draws the protist on the screen at its current position.
        
        self._draw_entities(self.foods)
        self._draw_entities(self.danger)
        
        # Make the most recently drawn screen visible.
        pygame.display.flip()


    def _draw_entities(self, group):
        for entity in group:
            entity.draw(self.screen)
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    protist = ProtistSurvival()
    protist.run_game()