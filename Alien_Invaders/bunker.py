
import pygame
from pygame.sprite import Sprite
from PIL import Image
import random


class Bunker(Sprite):

    def __init__(self, x, y, screen, num):
        super(Bunker, self).__init__()
        self.edit_im = Image.open("images/bunker.png")
        self.image = pygame.image.load("images/bunker.png")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.rect.x = x - self.rect.width - 100
        self.rect.y = y
        self.num = num
        self.damaged = False


    def update(self):
        if self.damaged:
            self.image = pygame.image.load("images/bunker_edit_"+str(self.num)+".png")
            self.screen.blit(self.image, self.rect)
        else:
            self.image = pygame.image.load("images/bunker.png")
            self.screen.blit(self.image, self.rect)

    def damage(self):
        self.edit_im.convert("RGBA").save("images/bunker_edit_"+str(self.num)+".png")
        px = self.edit_im.load()
        self.damaged = True
        for x in range(0, 600):
            num_1 = (random.randint(0, 95))
            num_2 = (random.randint(0, 71))
            px[num_1, num_2] = (0, 0, 0, 0)
        self.edit_im.save("images/bunker_edit_"+str(self.num)+".png")

    def is_destroyed(self):
        self.edit_im.convert("RGBA").save("images/bunker_edit_" + str(self.num) + ".png")

        px = self.edit_im.load()

        for x in range(0, 95):
            for y in range(0, 71):
                if px[x, y] != (0, 0, 0, 0):
                    return False
        return True

