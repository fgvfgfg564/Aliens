import pygame
import math

from pygame.sprite import Sprite
from settings import *
from algorithms import *


class Bullet(Sprite):
    def __init__(self, settings, screen, ship, delta, angle, image):
        super().__init__()
        self.screen = screen
        self.ship = ship
        self.angle = angle / 360 * math.pi * 2
        self.angle_degree = angle

        # create an rectangle (the bullet) at (0, 0) and then put it at the right place
        self.image_origin = pygame.image.load(image)
        self.image = self.image_origin
        self.image = pygame.transform.rotate(self.image_origin, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx + delta
        self.rect.bottom = ship.rect.top

        # save the bullet's position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_factor = settings.speed_factor

        self.damage = settings.damage
        self.is_AP = settings.is_AP

    def update(self):
        """move the bullet forward"""
        # Rotate the bullet
        self.image = pygame.transform.rotate(self.image_origin, self.angle_degree)
        self.rect = self.image.get_rect()

        # Push it forward
        speed_x = self.speed_factor * math.sin(self.angle)
        speed_y = self.speed_factor * math.cos(self.angle)
        self.x += speed_x
        self.rect.x = self.x
        self.y += speed_y
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet on the screen"""
        self.screen.blit(self.image, self.rect)


class BulletAP(Bullet):
    def __init__(self, screen, ship, delta, angle):
        super().__init__(BulletSettingsAP(), screen, ship, delta, angle, 'particles/bullet_AP.png')


class BulletNM(Bullet):
    def __init__(self, screen, ship, delta, angle):
        super().__init__(BulletSettingsNM(), screen, ship, delta, angle, 'particles/bullet_NM.png')


class Laser(Bullet):
    def __init__(self, screen, ship, delta, angle):
        super().__init__(BulletSettingsLaser(), screen, ship, delta, angle, 'particles/bullet_Laser.png')

    def update(self):
        self.rect.center = self.ship.rect.center
        self.rect.bottom = self.ship.rect.top


class Missle(Bullet):
    def __init__(self, screen, ship, delta, angle, aliens):
        settings = BulletSettingsMissle()
        super().__init__(settings, screen, ship, delta, angle, 'particles/missle.png')
        self.aliens = aliens
        self.maximum_rotation_angle = settings.maximum_rotation_angle
        self.maximum_total_rotation = settings.maximum_total_rotation
        self.detect_range = settings.detect_range
        self.rotation_radius = self.speed_factor / self.maximum_rotation_angle
        self.find_target()

    def update(self):
        if self.maximum_total_rotation > 0:
            self.find_target()
        super().update()

    def find_target(self):
        target = []
        for each in self.aliens:
            if isinstance(target, list) or \
                    (dist(each.rect.center, self.rect.center)
                     < dist(target.rect.center, self.rect.center)):
                target = each

        if dist(target.rect.center, self.rect.center) <= self.detect_range:
            self.target = target
            angle_delta = math.atan2(self.rect.centerx - self.target.rect.centerx,
                                     self.rect.centery - self.target.rect.centery) - self.angle
            angle_delta = min(self.maximum_rotation_angle, max(-self.maximum_rotation_angle, angle_delta))
            self.angle += angle_delta
            self.maximum_total_rotation -= abs(angle_delta)
            self.angle_degree = self.angle / (2 * pi) * 360
