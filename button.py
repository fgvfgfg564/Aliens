import pygame
from pygame.sprite import Sprite


class Button(Sprite):
    def __init__(self, ai_settings, screen, msg, stats, ship):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.stats = stats
        self.ship = ship

        self.width, self.height = 200, 50
        self.button_color = ai_settings.button_color
        self.text_color = ai_settings.button_words_color
        self.font = pygame.font.SysFont(ai_settings.button_font, 42)

        # Create the rectangle of the button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check(self, event):
        if self.rect.collidepoint(event[0], event[1]):
            return self.action()

    def action(self):
        pass


class StartButton(Button):
    def action(self):
        self.stats.game_activate()
        return True