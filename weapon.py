from bullet import *
from time import clock


class Weapon:
    def __init__(self, ai_settings, bullet, screen, ship, bullets):
        self.bullet = bullet
        self.timer = 0
        self.interval = 0.3 * ai_settings.default_fps
        self.ship = ship
        self.ai_settings = ai_settings
        self.screen = screen
        self.bullets = bullets
        self.damage_factor = 1

        self.bullet_scatter_angle = 0
        self.bullet_scatter_x = 0
        self.bullet_amount = 1
        self.total_scatter_angle = 0
        self.total_scatter_x = 0

        self.active = True

    def check_routine(self):
        self.timer += 1
        if self.timer >= self.interval:
            self.timer -= self.interval
            return True
        return False

    def fire(self):
        if self.check_routine():
            for i in range(self.bullet_amount):
                intervals = i - (self.bullet_amount - 1)/2
                new_bullet = self.bullet(self.screen, self.ship,
                                         self.bullet_scatter_x * intervals,
                                         - self.bullet_scatter_angle * intervals)
                self.bullets.add(new_bullet)

    def set_scatter_angle(self, angle):
        self.total_scatter_angle = angle
        self.bullet_scatter_angle = angle / (self.bullet_amount - 1 + 1e-10)

    def set_scatter_x(self, x):
        self.total_scatter_x = x
        self.bullet_scatter_x = x / (self.bullet_amount - 1 + 1e-10)

    def set_bullet_amount(self, num):
        self.bullet_amount = num
        self.set_scatter_angle(self.total_scatter_angle)
        self.set_scatter_x(self.total_scatter_x)

    def set_active(self, x):
        self.active = x


class GrapeShot(Weapon):
    def __init__(self, ai_settings, screen, ship, bullets):
        super().__init__(ai_settings, BulletAP, screen, ship, bullets)
        self.set_bullet_amount(12)
        self.set_scatter_x(10)
        self.set_scatter_angle(270)


class CloseQuarters(Weapon):
    def __init__(self, ai_settings, screen, ship, bullets):
        super().__init__(ai_settings, BulletNM, screen, ship, bullets)
        self.set_bullet_amount(6)
        self.set_scatter_x(40)
        self.set_scatter_angle(11)
        self.interval = 0.2 * ai_settings.default_fps


class LaserWeapon(Weapon):
    def __init__(self, ai_settings, screen, ship, bullets):
        super().__init__(ai_settings, Laser, screen, ship, bullets)
        self.set_bullet_amount(1)
        self.set_scatter_x(10)
        self.set_scatter_angle(30)
        self.interval = 1
        self.settled = False

    def fire(self):pass

    def set_active(self, x):
        self.active = x
        if not x:
            for each in self.bullets.copy():
                if isinstance(each, Laser):
                    self.bullets.remove(each)
        else:
            super().fire()


class MissleLauncher(Weapon):
    def __init__(self, ai_settings, screen, ship, bullets, aliens):
        super().__init__(ai_settings, Missle, screen, ship, bullets)
        self.set_bullet_amount(3)
        self.set_scatter_x(50)
        self.set_scatter_angle(20)
        self.aliens = aliens
        self.interval = 1 * ai_settings.default_fps

    def fire(self):
        if self.check_routine():
            for i in range(self.bullet_amount):
                intervals = i - (self.bullet_amount - 1)/2
                new_bullet = self.bullet(self.screen, self.ship,
                                         self.bullet_scatter_x * intervals,
                                         - self.bullet_scatter_angle * intervals, self.aliens)
                self.bullets.add(new_bullet)