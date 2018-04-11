import pygame
from textbox import *


class GameStats:
    def __init__(self, screen, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.screen = screen
        self.screen_rect = screen.get_rect()
        pygame.mixer.music.load('music/zuizhongguichumei.ogg')
        self.scoreboard = ScoreBoard(ai_settings, screen, self.screen_rect.x + 20, self.screen_rect.y + 20)

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.alien_level = 0

    def game_activate(self):
        self.game_active = True
        pygame.mixer.music.play(100)