import sys
import pygame

from bullet import Bullet
from bullet import Alien_bullet
from alien import Alien
from time import sleep
from random import randint


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # Move the ship to the right or left.
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    # Stop the ship from moving
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, sb, stats, screen, ship, aliens, bullets,
                      play_button, mouse_x, mouse_y):
    """Start a new game when the player click play."""
    collide = play_button.rect.collidepoint(mouse_x, mouse_y)
    if collide and not stats.game_active:
        if play_button.play:
            play_button.play = False
            stats.game_active = True
            pygame.mouse.set_visible(False)
        else:
            reset_game(ai_settings, sb, stats, screen, ship, aliens, bullets)


def check_event(ai_settings, aliens, sb, screen, stats,
                play_button, ship, bullets):
    """ Watch for keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, sb, stats, screen, ship, aliens,
                              bullets, play_button, mouse_x, mouse_y)


def update_screen(ai_settings, screen, ship, alien_bullets, alien, bullets, stats, sb,
                  play_button):
    """Redraw the screen durin each pass through the loop"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()
    alien.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive:
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, play_button, aliens, bullets, alien_bullets, sb, stats):
    """Update position of bullets and get rid of old ones."""
    # Update bullet position.
    bullets.update()
    alien_bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in alien_bullets.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            alien_bullets.remove(bullet)

    check_bullet_alien_collision(
        ai_settings, screen, ship, aliens, bullets, stats, sb)

    check_ship_bullet_collision(ai_settings, play_button, sb, stats, screen,
                                ship, aliens, bullets, alien_bullets)


def fire_bullets(ai_settings, screen, ship, bullets):
    # Create a new bullet adn add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit the screen horizontally."""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of alien rows that will fit the screen"""
    available_space_y = ((ai_settings.screen_height * 3 / 4) -
                         (3 * alien_height + ship_height))
    number_rows = available_space_y / (2 * alien_height)
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an aliena nad find the number of aliens in a row
    # Spacing between each aliens is equal to one alien's width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = int(get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height))

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def aliens_fire(ai_settings, aliens, alien_bullets, ship, screen):
    """Aliens can fire bullets now"""
    # There's a one in 3 in 10 chance that an alien will be able to shoot.
    # The number of aliens that will shoot is capped, to avoid unplayable
    # situations where the ship can't escape from the bullets falling down.
    for alien in aliens:
        if len(alien_bullets) <= ai_settings.alien_bullets_allowed:
            if randint(1, 10) < 4:
                # Create a bullet object(pew?)
                new_bullet = Alien_bullet(ai_settings, screen, ship, alien)
                alien_bullets.add(new_bullet)
        else:
            break


def update_aliens(ai_settings, play_button, sb, stats, screen, ship, aliens, bullets, alien_bullets):
    """
    Check if aliens erach the edges of the screen, and then update the fleet.
    Initiate the aliens-shooting process.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, play_button, sb, stats,
                 screen, ship, aliens, bullets, alien_bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, play_button, sb, stats,
                        screen, ship, aliens, bullets)

    aliens_fire(ai_settings, aliens, alien_bullets, ship, screen)


def check_fleet_edges(ai_settings, aliens):
    """Responds appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """"Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets,
                                 stats, sb):
    """Respond to bullet-alien collisions"""
    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_ship_bullet_collision(ai_settings, play_button, sb, stats, screen, ship, aliens, bullets, alien_bullets):
    """Respond to ship-alien_bullets collisions"""
    if pygame.sprite.spritecollideany(ship, alien_bullets):
        ship_hit(ai_settings, play_button, sb, stats, screen, ship,
                 aliens, bullets, alien_bullets)


def ship_hit(ai_settings, play_button, sb, stats, screen, ship, aliens, bullets, alien_bullets):
    """Respond to ship being hit by alien"""
    # Decrement ships left(lives).
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sb.prep_ships()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        stats.game_ended = True
        play_button.play = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, play_button, sb, stats, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, play_button, sb, stats,
                     screen, ship, aliens, bullets)
            break


def reset_game(ai_settings, sb, stats, screen, ship, aliens, bullets):
    # Reset game various game elements
    stats.reset_stats()
    ai_settings.initialize_dynamic_settings()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Reset the score
    stats.level = 0
    sb.prep_score()
    sb.prep_level()
    sb.prep_high_score()
    sb.prep_ships()

    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Start the game
    stats.game_active = True
    pygame.mouse.set_visible(False)
