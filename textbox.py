import pygame
from pygame import font


class TextBox:
    def __init__(self, ai_settings, screen, x, y, text = '', color = (0, 0, 0)):
        self.x = x
        self.y = y
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.message = text
        self.font = font.SysFont('Courier New', 48)
        self.text_color = color

    def blitme(self):
        self.message_image = self.font.render(self.message, True, self.text_color, self.ai_settings.bg_color)

        self.rect = self.message_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.screen.blit(self.message_image, self.rect)


class ScoreBoard(TextBox):
    def __init__(self, ai_settings, screen, x, y):
        super().__init__(ai_settings, screen, x, y)
        self.score = 1000

    def blitme(self):
        self.message = "%08d" % self.score
        super().blitme()

    def __add__(self, other):
        return self.score + other

    def __sub__(self, other):
        return self.score - other

    def __iadd__(self, other):
        self.score += other
        return self

    def __isub__(self, other):
        self.score -= other
        return self