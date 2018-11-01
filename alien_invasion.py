import pygame
import time

import game_functions as gf
from settings import *
from ship import Ship
from pygame.sprite import Group
from bullet import *
from alien import Alien
from game_stats import GameStats
from button import *
from weapon import *
from textbox import *


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien invasion')

    bullets = Group()
    aliens = Group()
    ticker = pygame.time.Clock()

    ship = Ship(ai_settings, screen)
    gf.weapons_init(ai_settings, screen, ship, bullets, aliens)

    buttons = Group()
    stats = GameStats(screen, ai_settings)

    gf.create_fleet(ai_settings, screen, ship, aliens, stats.alien_level)
    start_button = StartButton(ai_settings, screen, 'Start!', stats, ship)
    buttons.add(start_button)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets, buttons)

        if stats.game_active:
            ship.move()
            ship.restore()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens)
            gf.update_weapon(ship)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)
            stats.scoreboard -= 0.1

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, buttons)
        gf.clear_bullets(ai_settings, bullets)
        ticker.tick(ai_settings.default_fps)


run_game()