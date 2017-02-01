import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Creat a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        # Other miscellaneous settigns
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen"""
        # Update the decomal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw this bullet onto the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Alien_bullet(Bullet):
    """A class to manage bullets fired from Aliens"""

    def __init__(self, ai_settings, screen, ship, alien):
        super().__init__(ai_settings, screen, ship)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.speed_factor = ai_settings.alien_bullet_speed_factor

    def update(self):
        """Draw this bullet onto the screen"""
        # Update the decomal position of the bullet
        self.y += self.speed_factor
        # Update the rect position
        self.rect.y = self.y
