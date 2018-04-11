import pygame
from algorithms import *


class Ship:
    def __init__(self, ai_settings, screen):
        self.screen = screen

        # Load ship image and its rectangle
        self.image = pygame.image.load('image/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Load sounds
        self.hit_sound = pygame.mixer.Sound('music/ship_hit.ogg')
        self.death_sound = pygame.mixer.Sound('music/ship_death.ogg')

        # Put every new ship at the middle bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.speedx = 0
        self.speedy = 0
        self.speed_factor = ai_settings.ship_speed_factor

        self.acceleration_x = 0
        self.acceleration_y = 0
        self.acceleration_factor = ai_settings.ship_acceleration_factor
        self.friction_factor = ai_settings.ship_friction_factor

        self.HP_max = self.HP = ai_settings.ship_HP

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.weapons = []

    def blitme(self):
        # Draw the ship in a particular place
        self.screen.blit(self.image, self.rect)

        # Draw the HP bar
        display_HP_bar(self)

    def move(self):
        self.speedx += self.acceleration_x * self.acceleration_factor
        self.speedy += self.acceleration_y * self.acceleration_factor
        self.speedx = max(-1, min(self.speedx, 1))
        self.speedy = max(-1, min(self.speedy, 1))

        if self.speedx > 0 and self.rect.right < self.screen_rect.right\
                or self.speedx < 0 and self.rect.left > self.screen_rect.left:
            self.centerx += self.speedx * self.speed_factor
        else:
            self.speedx = 0
        if self.speedy > 0 and self.rect.bottom < self.screen_rect.bottom\
                or self.speedy < 0 and self.rect.top > self.screen_rect.top:
            self.centery += self.speedy * self.speed_factor
        else:
            self.speedy = 0

        self.speedx *= self.friction_factor
        self.speedy *= self.friction_factor

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def next_level(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.speedx = 0
        self.speedy = 0
        self.weapons[self.current_weapon].set_active(True)

    def refresh(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.speedx = 0
        self.speedy = 0
        self.HP = self.HP_max

    def fire(self):
        for each in self.weapons:
            if each.active:
                each.fire()

    def set_weapon_active(self, num):
        num -= 1
        self.current_weapon = num
        for each in self.weapons:
            each.set_active(False)
        self.weapons[num].set_active(True)

    def gain_damage(self, damage):
        self.HP -= damage
        if self.HP > 0:
            self.hit_sound.play()
        else:
            self.death_sound.play()