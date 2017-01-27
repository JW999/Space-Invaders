class Settings():
    """A class to store all settigs for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings'"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (141, 144, 146)

        # Ship settings
        self.ship_height = 50
        self.ship_width = 50
        self.ship_limit = 3

        # Alien settings
        self.alien_height = 50
        self.alien_width = 50
        self.fleet_drop_speed = 100

        # Bullet settings
        self.bullet_speed_factor = 1.5
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
