import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_settings, screen, row_num, frame):

        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.row = row_num
        self.frame = frame
        if self.row == 0:
            self.image = pygame.image.load("images/alien1.1.png")
            self.score = 10
            self.rect = self.image.get_rect()
        elif self.row < 3:
            self.image = pygame.image.load("images/alien2.1.png")
            self.score = 20
            self.rect = self.image.get_rect()
        elif self.row >= 3:
            self.image = pygame.image.load("images/alien3.1.png")
            self.score = 40
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.image.load("images/alien1.1.png")
            self.rect = self.image.get_rect()
        self.timer = pygame.time.get_ticks()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        if pygame.time.get_ticks() - self.timer >= 360:
            if self.frame == 1:
                if self.row == 0:
                    self.image = pygame.image.load("images/alien1.2.png")

                elif self.row < 3:
                    self.image = pygame.image.load("images/alien2.2.png")

                elif self.row >= 3:
                    self.image = pygame.image.load("images/alien3.2.png")

                self.frame = 2
            else:
                if self.row == 0:
                    self.image = pygame.image.load("images/alien1.1.png")

                elif self.row < 3:
                    self.image = pygame.image.load("images/alien2.1.png")

                elif self.row >= 3:
                    self.image = pygame.image.load("images/alien3.1.png")

                self.frame = 1
            self.timer = pygame.time.get_ticks()
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.image = pygame.image.load("images/ufo.png")
        self.rect = self.image.get_rect()
        self.is_dead = True
        self.ufo_sound = pygame.mixer.Sound("sounds/ufo_lowpitch.wav")
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = 80
        self.direction = 1
        self.x = float(self.rect.x)
        self.timer = pygame.time.get_ticks()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        self.ufo_sound.play()

    def check_edges(self):
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.ufo_speed_factor *
                   self.ai_settings.ufo_direction)
        self.rect.x = self.x
