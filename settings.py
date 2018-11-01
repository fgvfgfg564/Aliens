import bullet
import math


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (220, 220, 220)
        self.default_fps = 60

        self.level_score = 2000

        self.bullet_intervals = 0.4

        self.ship_speed_factor = 300 / self.default_fps
        self.ship_limit = 3
        self.ship_acceleration_factor = 0.2
        self.ship_friction_factor = 0.90
        self.ship_HP = 300
        self.ship_HP_restore = 0.3

        self.alien_speed_factor = 30 / self.default_fps
        self.alien_HP = 1500
        self.alien_attack = 50
        self.alien_speed_per_level = 20 / self.default_fps
        self.alien_HP_per_level = 200
        self.alien_attack_per_level = 5
        self.alien_score = 200

        self.button_color = (0, 128, 0)
        self.button_words_color = (255, 255, 255)
        self.button_font = 'Comic sans ms'

        self.HP_height = 5
        self.HP_color_full = (0, 0, 255)
        self.HP_color_half = (200, 200, 12)
        self.HP_color_empty = (255, 0, 0)


class BulletSettings:
    def __init__(self):
        self.speed_factor = -6
        self.allowed = 1500
        self.is_AP = False
        self.damage = 100


class BulletSettingsAP(BulletSettings):
    def __init__(self):
        super().__init__()
        self.is_AP = True
        self.damage = 10
        self.bullet = bullet.BulletAP


class BulletSettingsNM(BulletSettings):
    def __init__(self):
        super().__init__()
        self.is_AP = False
        self.damage = 200
        self.bullet = bullet.BulletNM


class BulletSettingsLaser(BulletSettings):
    def __init__(self):
        super().__init__()
        self.is_AP = True
        self.damage = 50
        self.bullet = bullet.Laser
        self.speed_factor = -1200


class BulletSettingsMissle(BulletSettings):
    def __init__(self):
        super().__init__()
        self.damage = 1500
        self.bullet = bullet.Missle
        self.speed_factor = -8
        self.maximum_rotation_angle = 0.08
        self.maximum_total_rotation = math.pi
        self.detect_range = 600