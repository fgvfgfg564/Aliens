import sys
import pygame
from pygame.locals import *
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame.sprite import Group
from algorithms import *
from weapon import *


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == K_RIGHT:
        ship.acceleration_x += 1
    elif event.key == K_LEFT:
        ship.acceleration_x -= 1
    elif event.key == K_UP:
        ship.acceleration_y -= 1
    elif event.key == K_DOWN:
        ship.acceleration_y += 1
    elif event.key == K_q:
        sys.exit()
    elif event.key >= K_0 and event.key <= K_9:
        ship.set_weapon_active(event.key - K_0)


def check_keyup_events(event, ship):
    if event.key == K_RIGHT:
        ship.acceleration_x -= 1
    elif event.key == K_LEFT:
        ship.acceleration_x += 1
    elif event.key == K_UP:
        ship.acceleration_y += 1
    elif event.key == K_DOWN:
        ship.acceleration_y -= 1


def check_mousebuttondown_events(event, buttons):
    for each in buttons.copy():
        if each.check(event.pos):
            buttons.remove(each)


def check_events(ai_settings, screen, ship, bullets, buttons):
    """answer to game events"""
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == KEYUP:
            check_keyup_events(event, ship)
        elif event.type == MOUSEBUTTONDOWN:
            check_mousebuttondown_events(event, buttons)


def update_screen(ai_settings, screen, ship, aliens, bullets, stats, buttons = []):
    """update the images on the screen"""
    # update screen
    screen.fill(ai_settings.bg_color)

    # Draw game stats
    stats.scoreboard.blitme()

    # Draw all the bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    for alien in aliens:
        alien.blitme()

    # Draw the buttons
    for each in buttons:
        each.blitme()

    # illustrate the screen
    pygame.display.flip()


def clear_bullets(ai_settings, bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0 or bullet.rect.left < 0 or \
                bullet.rect.right > ai_settings.screen_width or bullet.rect.top > ai_settings.screen_height:
            bullets.remove(bullet)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(space_y / (2*alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, level):
    # Create a single alien
    alien = Alien(ai_settings, screen, level)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + 2*alien.rect.height*row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, level):
    alien = Alien(ai_settings, screen, 1)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row in range(number_rows):
        for number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, number, row, level)


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    # Update the positions of bullets
    bullets.update()


def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets):
    """Check the collisions between aliens and bullets"""
    for each_alien in aliens.copy():
        for each_bullet in bullets.copy():
            if pygame.sprite.collide_rect(each_alien, each_bullet):
                each_alien.HP -= each_bullet.damage
                if not each_bullet.is_AP:
                    bullets.remove(each_bullet)
                if each_alien.HP <= 0:
                    each_alien.death_sound.play()
                    aliens.remove(each_alien)
                    stats.scoreboard += ai_settings.alien_score
                    break

    if len(aliens) == 0:
        bullets.empty()
        stats.alien_level += 1
        stats.scoreboard += ai_settings.level_score
        create_fleet(ai_settings, screen, ship, aliens, stats.alien_level)
        ship.next_level()


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    # Move aliens randomly
    aliens.update()

    # Check the collision between aliens and ship
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    collisions = pygame.sprite.spritecollide(ship, aliens, True)
    for each in collisions:
        each.hit(ship)
        if ship.HP <= 0:
            ship_crash(ai_settings, stats, screen, ship, aliens, bullets)
            break


def ship_crash(ai_settings, stats, screen, ship, aliens, bullets):
    """If a ship was hit by aliens"""
    if stats.ship_left > 0:
        ship.death_sound.play()
        stats.ship_left -= 1

        # Clear up the aliens and bullets
        aliens.empty()
        bullets.empty()

        # Creat a new fleet of aliens
        create_fleet(ai_settings, screen, ship, aliens, stats.alien_level)
        ship.refresh()

        # Refresh the screen
        update_screen(ai_settings, screen, ship, aliens, bullets, stats)

        # Pause
        sleep(2)
    else:
        stats.game_active = False


def update_weapon(ship):
    ship.fire()


def weapons_init(ai_settings, screen, ship, bullets, aliens):
    weapon1 = GrapeShot(ai_settings, screen, ship, bullets)
    weapon2 = CloseQuarters(ai_settings, screen, ship, bullets)
    weapon3 = MissleLauncher(ai_settings, screen, ship, bullets, aliens)
    weapon4 = LaserWeapon(ai_settings, screen, ship, bullets)

    weapon1.set_scatter_angle(270)
    ship.weapons.append(weapon1)
    ship.weapons.append(weapon2)
    ship.weapons.append(weapon3)
    ship.weapons.append(weapon4)
    ship.set_weapon_active(1)