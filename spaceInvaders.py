import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
import game_functions as gf


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    # Make a ship, a group bullets and a group of aliens.
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Make the play button.
    play_button = Button(screen, "Play")

    # Start the main loop for the game.
    while True:
        gf.check_event(ai_settings, screen, stats, play_button, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship,
                         aliens, bullets, stats, play_button)


run_game()
