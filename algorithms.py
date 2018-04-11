from math import *
import pygame
import math
from settings import Settings


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def display_HP_bar(self):
    ai_settings = Settings()
    HP_proportion = self.HP / self.HP_max
    HP_length = math.ceil(HP_proportion * self.rect.width)
    HP_posy = self.rect.top - 2 * ai_settings.HP_height
    HP_rect = pygame.Rect(self.rect.left, HP_posy,
                          HP_length, ai_settings.HP_height)
    self.screen.fill(get_HP_color(HP_proportion, ai_settings), HP_rect)


def get_HP_color(proportion, ai_settings):
    if proportion > 0.5:
        return ai_settings.HP_color_full
    elif proportion > 0.2:
        return ai_settings.HP_color_half
    else:
        return ai_settings.HP_color_empty