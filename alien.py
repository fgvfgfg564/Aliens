import pygame
import random
import math
from pygame.sprite import Sprite
from algorithms import *


class Alien(Sprite):
    """resembles a single alien"""

    def __init__(self, ai_settings, screen, level):
        super().__init__()
        self.image = pygame.image.load('image/huaji.png')
        self.death_sound = pygame.mixer.Sound('music/alien_death.ogg')
        self.screen = screen
        self.ai_settings = ai_settings

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.attack = ai_settings.alien_attack + ai_settings.alien_attack_per_level * level
        self.HP_max = self.HP = ai_settings.alien_HP + ai_settings.alien_HP_per_level * level
        self.speed = ai_settings.alien_speed_factor + ai_settings.alien_speed_per_level * level

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_angle = 0

        self.level = level

    def blitme(self):
        """Draw the alien at the particular place"""
        self.screen.blit(self.image, self.rect)

        # Draw the HP bar
        display_HP_bar(self)

    def update(self):
        # Make aliens move randomly
        theta = random.randint(-10, 10) / 360 * math.pi * 2
        self.speed_angle += theta
        speed_x = self.speed * math.sin(self.speed_angle)
        speed_y = self.speed * math.cos(self.speed_angle)
        self.x += speed_x
        self.y += speed_y

        if self.x < 0 or self.x > self.ai_settings.screen_width - self.rect.width:
            self.speed_angle = -self.speed_angle
            self.x = max(self.x, 0)
            self.x = min(self.x, self.ai_settings.screen_width - self.rect.width)

        if self.y < 0 or self.y > self.ai_settings.screen_height - self.rect.height:
            self.speed_angle = math.pi - self.speed_angle
            self.y = max(self.y, 0)
            self.y = min(self.y, self.ai_settings.screen_height - self.rect.height)

        self.rect.x = self.x
        self.rect.y = self.y

    def hit(self, ship):
        ship.gain_damage(self.attack)