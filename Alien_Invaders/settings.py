import pygame


class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 18
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = 255, 255, 0
        self.bullets_allowed = 3
        self.lasers_allowed = 10
        self.laser_speed_factor = 6

        # Alien settings
        self.fleet_drop_speed = 10
        # fleet direction: 1 is right, -1 is left
        self.fleet_direction = 1

        self.speedup = 1.5
        self.score_scale = 1.5
        self.laser_timer = pygame.time.get_ticks()

        self.alien_speed_factor = 3
        self.fleet_direction = 1
        self.ufo_speed_factor = 3
        self.ufo_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup
        self.bullet_speed_factor *= self.speedup
        self.alien_speed_factor *= self.speedup
