import sys
import pygame
import random

from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from protists import get_protist_class
from energy import ENERGY_TYPES, Energy
from danger import DANGER_TYPES, Danger
from group_polygons import *
from sounds import load_sounds, get_intro_music_path, get_bg_music_path, get_gameover_music_path

class ProtistSurvival:
    """Overall class to manage game assets and behavior."""


    def __init__(self):
        """Initialize the game, and create game resources."""
        self.state = "INTRO"
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # The screen is where all the game elements will be displayed.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        # Set the title of the game window.
        pygame.display.set_caption("Protists Survival")
        
        self.foods = pygame.sprite.Group()
        self.danger = pygame.sprite.Group()
        self.food_spawn_timer = 0  # Timer for spawning food
        self.danger_spawn_timer = 0  # Timer for spawning dangers
        
        # Set the background color of the screen.
        self.bg_color = self.settings.bg_color
        self.bg_image = None

        # Offset for background scrolling
        self.bg_offset_x = 0

        # Level up message
        self.levelup_message = None
        self.levelup_message_time = 0

        # Load sounds
        self.sounds = load_sounds()
        self.bg_music_path = get_bg_music_path()
        self.music_playing = False

        # Map pygame keys to protist movement attributes
        self.key_to_flag = {
            pygame.K_LEFT: 'moving_left',
            pygame.K_RIGHT: 'moving_right',
            pygame.K_UP: 'moving_up',
            pygame.K_DOWN: 'moving_down'
        }

    
    def run_game(self):
        while True:
            if self.state == "INTRO":
                pygame.mouse.set_visible(False)
                self.run_intro()
            elif self.state == "SELECTION":
                pygame.mouse.set_visible(True)
                self.run_selection()
            elif self.state == "PROTIST_SELECTION":
                self.run_protist_selection()
            elif self.state == "GAMEPLAY":
                pygame.mouse.set_visible(False)
                self.run_gameplay()
            elif self.state == "GAME_OVER":
                self.run_game_over()
            self.clock.tick(60)
            
             
    def run_intro(self):
        """Display the introduction screen."""
        # Load and play intro music
        pygame.mixer.music.stop()
        intro_music_path = get_intro_music_path()
        pygame.mixer.music.load(intro_music_path)
        pygame.mixer.music.play(-1)

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
                        self.state = "SELECTION"
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
            # Find the group under the mouse, if any
            highlighted_group = next(
                (g for g, poly in EUK_GROUP_SELECTION_POLYGONS.items() if self.point_in_polygon(mouse_pos, poly)),
                None
            )

            self.screen.fill(self.settings.intro_bg_color)
            self.screen.blit(selection_image, selection_rect)
            if highlighted_group:
                pygame.draw.polygon(
                    self.screen,
                    (1, 1, 1),  
                    EUK_GROUP_SELECTION_POLYGONS[highlighted_group],
                    5
                )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and highlighted_group:
                    if highlighted_group != "Metamonada":
                        self._show_message(
                            "Sorry! This Eukaryotic supergroup is still not included in the game.",
                            "Please select another supergroup (Metamonada).",
                            "Press any key to go back to the selection screen."
                        )
                    else:
                        self.selected_group = highlighted_group
                        self.sounds["select"].play()
                        self.state = "PROTIST_SELECTION"
                        waiting = False



    def run_protist_selection(self):
        """Display the protist selection screen for the chosen group, with info image on hover."""
        group = self.selected_group
        base_image_path = EUK_GROUP_SELECTION_IMAGES[group]
        base_image = pygame.image.load(base_image_path)
        base_image = self._scale_image(base_image, self.screen.get_rect())
        base_rect = base_image.get_rect(center=self.screen.get_rect().center)

        protist_polygons = PROTIST_SELECTION_POLYGONS.get(group, {})
        button_polygons = BOTTONS_POLYGONS.get(f"{group}_screen", {})

        waiting = True
        while waiting:
            mouse_pos = pygame.mouse.get_pos()
            highlighted_protist = None
            for name, polygon in protist_polygons.items():
                if polygon and self.point_in_polygon(mouse_pos, polygon):
                    highlighted_protist = name
                    break

            # Decide which image to show
            if highlighted_protist and highlighted_protist in PROTIST_INFO_IMAGES.get(group, {}):
                image_path = PROTIST_INFO_IMAGES[group][highlighted_protist]
                display_image = pygame.image.load(image_path)
                display_image = self._scale_image(display_image, self.screen.get_rect())
                display_rect = display_image.get_rect(center=self.screen.get_rect().center)
            else:
                display_image = base_image
                display_rect = base_rect

            self.screen.fill(self.settings.intro_bg_color)
            self.screen.blit(display_image, display_rect)
            if highlighted_protist:
                pygame.draw.polygon(
                    self.screen,
                    (255, 0, 0),
                    protist_polygons[highlighted_protist],
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
                    # Check BACK button
                    if "back" in button_polygons and self.point_in_polygon(mouse_pos, button_polygons["back"]):
                        self.state = "SELECTION"
                        waiting = False
                        break
                    # Check protist selection
                    for name, polygon in protist_polygons.items():
                        if polygon and self.point_in_polygon(mouse_pos, polygon):
                            self.selected_protist = name
                            protist_class = get_protist_class(name)
                            if protist_class:
                                self.sounds["protist_select"].play()
                                self.protist = protist_class(self)
                                self.stats = GameStats(self, self.protist)
                                self.sb = Scoreboard(self, self.protist)
                                bg_path = PROTIST_BACKGROUND_IMAGES.get(name)
                                if bg_path:
                                    bg_img = pygame.image.load(bg_path)
                                    self.bg_image = self._scale_image(bg_img, self.screen.get_rect())
                                else:
                                    self.bg_image = None
                                self.foods.empty()
                                self.danger.empty()
                                self.bg_offset_x = 0
                                self.settings.initialize_dynamic_settings()
                                pygame.mixer.music.stop()
                                self.state = "GAMEPLAY"
                                waiting = False
                            break
                    

    def run_gameplay(self):
        """Start the main loop for the game."""
        # Pick and play a random background music
        # Only start music if not already playing
        if not self.music_playing:
            pygame.mixer.music.stop()
            self.bg_music_path = get_bg_music_path()
            pygame.mixer.music.load(self.bg_music_path)
            pygame.mixer.music.play(-1)
            self.music_playing = True

        self._check_events() 
        self.protist.update()

        # Adjust scroll speed as desired
        scroll_speed = 4

        # Move background offset based on protist movement
        if self.protist.moving_right:
            self.bg_offset_x += scroll_speed
        elif self.protist.moving_left:
            self.bg_offset_x -= scroll_speed
                
        # Spawn food and energy
        self._spawn_entity('food_spawn_timer', self.settings.energy_spawn_rate, self.settings.energy_chance, Energy, self.foods)
        self._spawn_entity('danger_spawn_timer', self.settings.danger_spawn_rate, self.settings.danger_chance, Danger, self.danger)
            
        # Update all food and danger positions
        self.foods.update()
        self.danger.update()

        for food in pygame.sprite.spritecollide(self.protist, self.foods, dokill=False, collided=pygame.sprite.collide_mask):
            # Only eat if protist can eat this type
            if hasattr(food, 'energy_type') and food.energy_type in self.protist.can_eat:
                self.foods.remove(food)
                self.stats.score += food.points 
                self.sb.prep_score()
                self.sb.check_high_score()
                self.sounds["collect"].play()

            # Level up every 2,000 points
            if self.stats.score // 2000 + 1 > self.stats.level:
                self.stats.level = self.stats.score // 2000 + 1
                self.settings.increase_speed()
                self.sb.prep_level()
                self.levelup_message = f"Level {self.stats.level}"
                self.levelup_message_time = pygame.time.get_ticks()
                self.sounds["levelup"].play()

        for danger in pygame.sprite.spritecollide(self.protist, self.danger, dokill=False, collided=pygame.sprite.collide_mask):
            # Only affected if not resistant to this danger type
            if not hasattr(danger, 'danger_type') or danger.danger_type not in getattr(self.protist, 'danger_resist', []):
                self.danger.remove(danger)
                self.stats.danger_defence -= danger.damage  # Use the damage from the danger object
                self.sounds["damage"].play()
                
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
                        self.frozen_bg = self.screen.copy()
                        self.sounds["gameover"].play()
                        self.music_playing = False
                        self.state = "GAME_OVER"

        # Remove food and danger that has moved off the left edge
        self._remove_offscreen_entities(self.foods)
        self._remove_offscreen_entities(self.danger)
        self._update_screen()


    def run_game_over(self):
        """Display the game over screen, with flashing effect if new high score."""
        import time

        # Load and play intro music
        pygame.mixer.music.stop()
        gameover_music_path = get_gameover_music_path()
        pygame.mixer.music.load(gameover_music_path)
        pygame.mixer.music.play(-1)

        # Paths to your images
        game_over_path = 'images/screen_images/game_over/game_over.png'
        new_record_path = 'images/screen_images/game_over/game_over_record.png'

        # Load images
        game_over_image = pygame.image.load(game_over_path).convert_alpha()
        new_record_image = pygame.image.load(new_record_path).convert_alpha()

        # Define the gameplay area (below HUD)
        game_area_rect = pygame.Rect(
            0,
            self.settings.hud_height,
            self.settings.screen_width,
            self.settings.screen_height - self.settings.hud_height
        )

        # Optionally scale images to fit the gameplay area (if needed)
        game_over_image = self._scale_image(game_over_image, game_area_rect)
        new_record_image = self._scale_image(new_record_image, game_area_rect)

        # Center images in the gameplay area
        game_over_rect = game_over_image.get_rect(center=game_area_rect.center)
        new_record_rect = new_record_image.get_rect(center=game_area_rect.center)

        # Determine if new high score
        is_new_high = self.stats.score >= self.stats.high_score

        waiting = True
        flash = True
        last_switch = time.time()
        flash_interval = 0.6  # seconds

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        self.state = "SELECTION"
                    elif event.key == pygame.K_ESCAPE:
                        self.stats.save_high_score()
                        sys.exit()
            
            # Draw the frozen gameplay screen
            if hasattr(self, 'frozen_bg') and self.frozen_bg:
                self.screen.blit(self.frozen_bg, (0, 0))
            else:
                # fallback if for some reason frozen_bg is missing
                self.screen.fill(self.settings.bg_color)

            # Draw the game over images in the gameplay area (below HUD)
            if is_new_high:
                now = time.time()
                if now - last_switch > flash_interval:
                    flash = not flash
                    last_switch = now
                if flash:
                    self.screen.blit(game_over_image, game_over_rect)
                else:
                    self.screen.blit(new_record_image, new_record_rect)
            else:
                self.screen.blit(game_over_image, game_over_rect)

            pygame.display.flip()
            self.clock.tick(60)

    
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
    
    
    def _show_message(self, *lines, valid_keys=None):
        """Display a message and wait for a valid key (if given). Returns the key pressed."""
        self.screen.fill(self.settings.intro_bg_color)
        font = pygame.font.SysFont(None, 48)
        for i, msg in enumerate(lines):
            text = font.render(msg, True, (46, 49, 146))
            rect = text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 + i*60))
            self.screen.blit(text, rect)
        pygame.display.flip()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if valid_keys is None or e.key in valid_keys:
                        return e.key
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if valid_keys is None:
                        return None
    

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
        elif event.key == pygame.K_DOWN:
            self.protist.anim_toggle = True
            # If neither left nor right is pressed, default to right
            if not self.protist.moving_left and not self.protist.moving_right:
                self.protist.last_direction = 'right'
        elif event.key == pygame.K_SPACE:
            # Danger defence replenish logic
            replenish_cost = 100
            replenish_amount = self.settings.protist_danger_replenish_rate
            max_defence = self.protist.danger_defence_max
            if self.stats.score >= replenish_cost and self.stats.danger_defence < max_defence:
                self.stats.score -= replenish_cost
                self.sounds["defence"].play()
                self.stats.danger_defence = min(self.stats.danger_defence + replenish_amount, max_defence)
                self.sb.prep_score()
        elif event.key == pygame.K_ESCAPE:
            if self.state == "GAMEPLAY":
                key = self._show_message(
                    "Do you want to exit the game and go back to the selection screen?",
                    "Press Y or N.",
                    valid_keys={pygame.K_y, pygame.K_n}
                )
                if key == pygame.K_y:
                    self.stats.save_high_score()
                    self.music_playing = False
                    pygame.mixer.music.stop()
                    intro_music_path = get_intro_music_path()
                    pygame.mixer.music.load(intro_music_path)
                    pygame.mixer.music.play(-1)
                    self.state = "SELECTION"
                # If K_n, do nothing (resume game)
            else:
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
        # If no movement keys are pressed, show the last used image (left/right) or default
        if not (self.protist.moving_left or self.protist.moving_right or
                self.protist.moving_up or self.protist.moving_down):
            # Try to show the last used image, fallback to default
            img = self.protist.images.get(self.protist.last_direction)
            if img is None and self.protist.last_direction == 'right':
                img = self.protist.images.get('right_1', self.protist.images['default'])
            elif img is None and self.protist.last_direction == 'left':
                img = self.protist.images.get('left_1', self.protist.images['default'])
            elif img is None:
                img = self.protist.images['default']
            self.protist.set_image(img)
        # Otherwise, do nothing: let the protist's own animation logic handle the image
        

    def _expand_allowed_types(self, allowed_list, all_types_dict):
        """Expand allowed types/categories to a flat list of types."""
        expanded = []
        for entry in allowed_list:
            # If entry matches a category, add all types with that category
            found = False
            for tkey, tdata in all_types_dict.items():
                if tdata['category'] == entry:
                    expanded.append(tkey)
                    found = True
            if not found and entry in all_types_dict:
                expanded.append(entry)
        return expanded
    

    def _spawn_entity(self, timer_attr, spawn_rate, chance, entity_class, group):
        """Spawn entities like food or dangers based on a timer and chance, supporting categories."""
        setattr(self, timer_attr, getattr(self, timer_attr) + 1)
        if getattr(self, timer_attr) > spawn_rate:
            if random.random() < chance:
                if entity_class.__name__ == "Energy":
                    allowed = GROUP_ALLOWED_ENERGY.get(self.selected_group, list(ENERGY_TYPES.keys()))
                    allowed_types = self._expand_allowed_types(allowed, ENERGY_TYPES)
                    energy_type = random.choice(allowed_types)
                    entity = entity_class(self.screen.get_rect(), self.settings, energy_type=energy_type)
                elif entity_class.__name__ == "Danger":
                    allowed = GROUP_ALLOWED_DANGER.get(self.selected_group, list(DANGER_TYPES.keys()))
                    allowed_types = self._expand_allowed_types(allowed, DANGER_TYPES)
                    danger_type = random.choice(allowed_types)
                    entity = entity_class(self.screen.get_rect(), self.settings, danger_type=danger_type)
                else:
                    entity = entity_class(self.screen.get_rect(), self.settings)
                group.add(entity)
            setattr(self, timer_attr, 0)

    
    def _remove_offscreen_entities(self, group):
        """Remove entities that have moved off the left edge of the screen."""
        for entity in list(group):
            if entity.rect.right < 0:
                group.remove(entity)
          
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # Draw protist-specific background if set, only in the game area (below HUD)
        if self.bg_image:
            game_rect = pygame.Rect(
                0,
                self.settings.hud_height,
                self.settings.screen_width,
                self.settings.screen_height - self.settings.hud_height
            )
            # Scale the background to fit the game area
            bg_scaled = pygame.transform.smoothscale(self.bg_image, (game_rect.width, game_rect.height))
            bg_width = bg_scaled.get_width()
            offset_x = self.bg_offset_x % bg_width  # Loop the offset

            # Tile the background horizontally
            x = -offset_x
            while x < self.settings.screen_width:
                self.screen.blit(bg_scaled, (x, self.settings.hud_height))
                x += bg_width
        else:
            self.screen.fill(self.bg_color)

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

        # Draw level up message if active
        if self.levelup_message and pygame.time.get_ticks() - self.levelup_message_time < 1000:
            font = pygame.font.SysFont(None, 96)
            text = font.render(self.levelup_message, True, (220, 0, 0))
            rect = text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2))
            self.screen.blit(text, rect)
        else:
            self.levelup_message = None

        pygame.display.flip()  


    def _draw_entities(self, group):
        for entity in group:
            entity.draw(self.screen)
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    protist = ProtistSurvival()
    protist.run_game()