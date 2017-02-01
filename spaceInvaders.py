import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from playbutton import Button
from scoreboard import Scoreboard
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
    alien_bullets = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make the play button.
    play_button = Button(screen)

    # Initialize pygame clock to control the FPS of the game
    clock = pygame.time.Clock()
    fps = 200

    # Start the main loop for the game.
    while True:
        clock.tick(fps)

        gf.check_event(ai_settings, aliens, sb, screen, stats, play_button,
                       ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, play_button,
                              aliens, bullets, alien_bullets, sb, stats)
            gf.update_aliens(ai_settings, play_button, sb, stats,
                             screen, ship, aliens, bullets, alien_bullets)

        gf.update_screen(ai_settings, screen, ship, alien_bullets,
                         aliens, bullets, stats, sb, play_button)


run_game()
