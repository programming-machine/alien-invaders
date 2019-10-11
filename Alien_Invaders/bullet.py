import pygame
from pygame.sprite import Sprite
import random


class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):

        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor


    def draw_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)


    def update(self):

        self.y -= self.speed_factor

        self.rect.y = self.y


class Laser(Sprite):


    def draw_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):

        self.y += self.speed_factor

        self.rect.y = self.y

    def __init__(self, ai_settings, screen, ship):

        super(Laser, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y)

        self.color = (255, 0, 0)

        self.speed_factor = ai_settings.laser_speed_factor


class Explosion(Sprite):
    def __init__(self, x_pos, y_pos, row_num, is_ufo):
        super(Explosion, self).__init__()

        self.font = (None, 20)

        self.time_start = pygame.time.get_ticks()
        self.is_ufo = is_ufo
        if is_ufo:
            self.score = random.randint(300, 500)
            self.font = pygame.font.Font(None, 100)
            self.image = self.font.render(str(self.score), True, (255, 255, 0))
            self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

        else:
            if row_num == 0:
                self.image = pygame.image.load("images/explosion_p.png")

            elif row_num < 3:
                self.image = pygame.image.load("images/explosion_b.png")

            elif row_num >= 3:
                self.image = pygame.image.load("images/explosion_g.png")

            self.rect = self.image.get_rect()
            self.rect.x = x_pos
            self.rect.y = y_pos
