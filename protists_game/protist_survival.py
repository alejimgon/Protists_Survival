import sys
import pygame
import random

from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from protists import *
from energy import Energy
from danger import Danger
from group_polygons import GROUP_POLYGONS

class ProtistSurvival:
    """Overall class to manage game assets and behavior."""


    def __init__(self):
        """Initialize the game, and create game resources."""
        self.state = "INTRO" # Possible states: INTRO, SELECTION, GAMEPLAY, GAME_OVER
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # The screen is where all the game elements will be displayed.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        # Set the title of the game window.
        pygame.display.set_caption("Protists Survival")

        # Create an instance of the Protist class.
        self.protist = Gintestinalis(self) # This line creates an instance of the selected protist class.

        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self, self.protist)
        self.sb = Scoreboard(self, self.protist)
        
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

        self.game_active = True  # Flag to control the game loop
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            if self.state == "INTRO":
                self.run_intro()
                self.state = "SELECTION"
            elif self.state == "SELECTION":
                self.run_selection()
                self.state = "GAMEPLAY"
            elif self.state == "GAMEPLAY":
                self.run_gameplay()
            elif self.state == "GAME_OVER":
                self.run_game_over()

            self.clock.tick(60)
            
             
    def run_intro(self):
        """Display the introduction screen."""
        # Load the intro image
        intro_image = pygame.image.load('images/screen_images/intro_screen.png')
        intro_rect = self.screen.get_rect()

        # Scale the image to fit the screen, preserving aspect ratio
        intro_image = self._scale_image(intro_image, intro_rect)
        intro_rect = intro_image.get_rect(center=intro_rect.center)

        self.screen.fill(self.settings.intro_bg_color)
        self.screen.blit(intro_image, intro_rect)
        pygame.display.flip()

        # Wait for user input to proceed to protist selection
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()

    def run_selection(self):
        """Display the protist selection screen."""
        selection_image = pygame.image.load('images/screen_images/selection_screen.png')
        selection_rect = self.screen.get_rect()
        selection_image = self._scale_image(selection_image, selection_rect)
        selection_rect = selection_image.get_rect(center=selection_rect.center)

        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            highlighted_group = None
            for group_name, polygon in GROUP_POLYGONS.items():
                if self.point_in_polygon(mouse_pos, polygon):
                    highlighted_group = group_name
                    break

            self.screen.fill(self.settings.intro_bg_color)
            self.screen.blit(selection_image, selection_rect)
            if highlighted_group:
                pygame.draw.polygon(
                    self.screen,
                    (255, 255, 0),  # Yellow
                    GROUP_POLYGONS[highlighted_group],
                    5
                )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for group_name, polygon in GROUP_POLYGONS.items():
                        if self.point_in_polygon(mouse_pos, polygon):
                            self.selected_group = group_name
                            print(f"Selected group: {group_name}")
                            waiting = False
                            break


    def run_gameplay(self):
        """Start the main loop for the game."""
        if self.game_active: 
            self._check_events() # This function checks for any events that have occurred, such as key presses or mouse movements. It is called at the beginning of each iteration of the game loop to ensure that the game responds to user input.
            self.protist.update() # This line calls the update method of the selected protist instance.
                
            # Spawn food and energy
            self._spawn_entity('food_spawn_timer', self.settings.energy_spawn_rate, self.settings.energy_chance, Energy, self.foods)
            self._spawn_entity('danger_spawn_timer', self.settings.danger_spawn_rate, self.settings.danger_chance, Danger, self.danger)
            
            # Update all food and danger positions
            self.foods.update()
            self.danger.update()

            for food in pygame.sprite.spritecollide(self.protist, self.foods, dokill=True, collided=pygame.sprite.collide_mask):
                # Handle food collection (increase score)
                self.stats.score += self.settings.energy_points
                self.sb.prep_score()
                self.sb.check_high_score()

                # Level up every 10,000 points
                if self.stats.score // 2000 + 1 > self.stats.level:
                    self.stats.level = self.stats.score // 2000 + 1
                    self.settings.increase_speed()
                    self.sb.prep_level()

            for danger in pygame.sprite.spritecollide(self.protist, self.danger, dokill=True, collided=pygame.sprite.collide_mask):
                # Handle danger collision (decrease danger defence)
                self.stats.danger_defence -= self.settings.protist_danger_depletion_rate
                if self.stats.danger_defence <= 0:
                    self.stats.lives_left -= 1
                    if self.stats.lives_left > 0:
                        # Show default image and update display
                        self.protist.set_image(self.protist.images['default'])
                        self.protist.last_direction = 'default'
                        self.sb.prep_score()
                        self._update_screen()
                        pygame.display.flip()
                        sleep(1)
                        # Now reset protist and game state
                        self.stats.danger_defence = self.protist.danger_defence_max
                        self.foods.empty()
                        self.danger.empty()
                        self.protist.rect.midleft = self.screen.get_rect().midleft
                        self.protist.x = float(self.protist.rect.x)
                        self.protist.y = float(self.protist.rect.y)
                    else:
                        # Game over logic
                        self.stats.save_high_score()
                        self.state = "GAME_OVER"

            # Remove food and danger that has moved off the left edge
            self._remove_offscreen_entities(self.foods)
            self._remove_offscreen_entities(self.danger)
            self._update_screen()


    def run_game_over(self):
        """Display the game over screen."""
        # Load and display the game over image
        game_over_image = pygame.image.load('images/screen_images/game_over_screen.png')
        game_over_rect = game_over_image.get_rect(center=self.screen.get_rect().center)
        
        self.screen.fill(self.bg_color)
        self.screen.blit(game_over_image, game_over_rect)
        pygame.display.flip()

        # Wait for user input to restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        waiting = False
                        self.state = "SELECTION"

    
    def point_in_polygon(self, point, polygon):
        x, y = point
        inside = False
        n = len(polygon)
        p1x, p1y = polygon[0]
        for i in range(n+1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    
    def _scale_image(self, image, target_rect):
        """Scale an image to fit within target_rect, preserving aspect ratio."""
        img_rect = image.get_rect()
        scale_w = target_rect.width / img_rect.width
        scale_h = target_rect.height / img_rect.height
        scale = min(scale_w, scale_h)
        new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
        return pygame.transform.smoothscale(image, new_size)
    

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
        elif event.key == pygame.K_SPACE:
            # Danger defence replenish logic
            replenish_cost = 100
            replenish_amount = self.settings.protist_danger_replenish_rate
            max_defence = self.protist.danger_defence_max
            if self.stats.score >= replenish_cost and self.stats.danger_defence < max_defence:
                self.stats.score -= replenish_cost
                self.stats.danger_defence = min(self.stats.danger_defence + replenish_amount, max_defence)
                self.sb.prep_score()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self.stats.save_high_score()
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
       
        # Draw HUD background and border
        hud_rect = pygame.Rect(0, 0, self.settings.screen_width, self.settings.hud_height)
        pygame.draw.rect(self.screen, self.settings.hud_bg_color, hud_rect)
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (0, self.settings.hud_height - 1),
            (self.settings.screen_width, self.settings.hud_height - 1),
            3
        )
        # Draw the protist, scoreboard, foods, and dangers.
        self.protist.blitme() 
        self.sb.show_score()
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