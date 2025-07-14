import pygame

class Protist:
    """Base class for all protists."""

    def __init__(self, ps_game, image_path):
        self.screen = ps_game.screen
        self.settings = ps_game.settings
        self.screen_rect = ps_game.screen.get_rect()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.anim_toggle = False
        self.anim_frame = 0
        self.mask = pygame.mask.from_surface(self.image)

    def set_image(self, new_image):
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.mask = pygame.mask.from_surface(self.image)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.protist_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.protist_speed
        if self.moving_up:
            self.y = max(self.y - self.settings.protist_speed, self.settings.hud_height + 10)
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.protist_speed

        self.rect.x = self.x
        self.rect.y = self.y
        self._animation_logic()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def _animation_logic(self):
        if self.anim_toggle:
            self.anim_frame += 1
            if self.anim_frame % 20 < 10:
                if self.moving_left or ((self.moving_up or self.moving_down) and self.last_direction == 'left'):
                    self.set_image(self.images['left'])
                elif self.moving_right or ((self.moving_up or self.moving_down) and self.last_direction == 'right'):
                    self.set_image(self.images['right'])
            else:
                if self.moving_left or ((self.moving_up or self.moving_down) and self.last_direction == 'left'):
                    self.set_image(self.images['left_up'])
                elif self.moving_right or ((self.moving_up or self.moving_down) and self.last_direction == 'right'):
                    self.set_image(self.images['right_up'])
        else:
            self.set_image(self.images[self.last_direction])

# --- Subclasses for each playable protist ---

class Gintestinalis(Protist):
    """Giardia intestinalis"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/g_intestinalis/g_intestinalis.png')
        self.images = {
            'left': pygame.image.load('images/metamonada/g_intestinalis/g_intestinalis_left.png'),
            'left_up': pygame.image.load('images/metamonada/g_intestinalis/g_intestinalis_left2.png'),
            'right': pygame.image.load('images/metamonada/g_intestinalis/g_intestinalis_right.png'),
            'right_up': pygame.image.load('images/metamonada/g_intestinalis/g_intestinalis_right2.png'),
            'default': self.image
        }
        self.last_direction = 'default'
        self.danger_defence_max = 75
        self.can_eat = ['glucose', 'arginine']
        self.danger_resist = []


class Gmuris(Protist):
    """Giardia muris"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/g_muris/g_muris.png')
        self.images = {
            'left': pygame.image.load('images/metamonada/g_muris/g_muris_left.png'),
            'left_up': pygame.image.load('images/metamonada/g_muris/g_muris_left2.png'),
            'right': pygame.image.load('images/metamonada/g_muris/g_muris_right.png'),
            'right_up': pygame.image.load('images/metamonada/g_muris/g_muris_right2.png'),
            'default': self.image
        }
        self.last_direction = 'default'
        self.danger_defence_max = 60
        self.can_eat = ['glucose', 'fructose', 'arginine']
        self.danger_resist = []

class Spironucleus(Protist):
    """Spironucleus salmonicida"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/s_salmonicida/s_salmonicida.png')
        self.images = {
            'left': pygame.image.load('images/metamonada/s_salmonicida/s_salmonicida_left.png'),
            'left_up': pygame.image.load('images/metamonada/s_salmonicida/s_salmonicida_left2.png'),
            'right': pygame.image.load('images/metamonada/s_salmonicida/s_salmonicida_right.png'),
            'right_up': pygame.image.load('images/metamonada/s_salmonicida/s_salmonicida_right2.png'),
            'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 80
        self.can_eat = ['glucose', 'fructose', 'arginine', 'bacteria']
        self.danger_resist = []

class Trepomonas(Protist):
    """Trepomonas sp."""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/trepomonas.png')
        self.images = {'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 85
        self.can_eat = ['glucose', 'fructose', 'arginine', 'bacteria']
        self.danger_resist = []

class Hinflata(Protist):
    """Hexamita inflata"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/h_inflata/h_inflata.png')
        self.images = {'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 90
        self.can_eat = ['glucose', 'fructose', 'maltose', 'arginine', 'bacteria']
        self.danger_resist = []

class Kbialata(Protist):
    """Kipferlia bialata"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/k_bialata/k_bialata.png')
        self.images = {'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 75
        self.can_eat = ['glucose', 'arginine', 'bacteria']
        self.danger_resist = []


class Mexilis(Protist):
    """Monocercomonoides exilis"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/m_exilis/m_exilis.png')
        self.images = {'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 50
        self.can_eat = ['glucose', 'arginine', 'bacteria']
        self.danger_resist = []

class Tvaginalis(Protist):
    """Trichomonas vaginalis"""
    def __init__(self, ps_game):
        super().__init__(ps_game, 'images/metamonada/t_vaginalis/t_vaginalis.png')
        self.images = {'default': self.image}
        self.last_direction = 'default'
        self.danger_defence_max = 75
        self.can_eat = ['glucose', 'arginine', 'bacteria']
        self.danger_resist = []

# --- Factory function ---

def get_protist_class(name):
    """Return the protist class for a given protist name."""
    mapping = {
        "Giardia intestinalis": Gintestinalis,
        "Giardia muris": Gmuris,
        "Spironucleus salmonicida": Spironucleus,
        "Trepomonas sp.": Trepomonas,
        "Hexamita inflata": Hinflata,
        "Kipferlia bialata": Kbialata,
        "Monocercomonoides exilis": Mexilis,
        "Trichomonas vaginalis": Tvaginalis,
        # Add more mappings as you add more protists
    }
    return mapping.get(name)