import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):

        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ship image and get its rect
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.exploding = False
        self.frame = 0

        self.exp_frames = {0: 'images/ship_exp_1.png', 1: 'images/ship_exp_2.png', 2: 'images/ship_exp_3.png',
                           3: 'images/ship_exp_4.png', 4: 'images/ship_exp_5.png', 5: 'images/ship_exp_6.png',
                           6: 'images/ship_exp_7.png', 7: 'images/ship_exp_8.png'}

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):

        if self.exploding:
            if self.frame == 8:
                self.exploding = False
                self.frame = 1
            else:
                self.image = pygame.image.load(self.exp_frames[self.frame])
                self.frame += 1

        else:
            self.image = pygame.image.load("images/ship.png")
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            elif self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
