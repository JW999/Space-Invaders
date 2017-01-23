class Settings():
    """A class to store all settigs for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings'"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (141, 144, 146)

        # Ship settings
        self.ship_height = 50
        self.ship_width = 50
        self.ship_speed_factor = 1.5

        # Alien settings
        self.alien_height = 50
        self.alien_width = 50
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Bullet settings
        self.bullet_speed_factor = 1.5
        self.bullet_height = 15
        self.bullet_width = 800
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
