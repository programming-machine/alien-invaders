
import pygame

from pygame.sprite import Group
from settings import Settings
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bunker import Bunker
from ship import Ship
from alien import UFO


def run_game():
    # Initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Inveders")
    clock = pygame.time.Clock()
    # make a ship
    ship = Ship(ai_settings, screen)
    ufo = UFO(ai_settings, screen)

    play_button = Button(screen, "Play", 200)
    score_button = Button(screen, "High Scores", 300)
    screen_rect = screen.get_rect()
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    bullets = Group()
    lasers = Group()
    aliens = Group()
    explosions = Group()
    bunkers = [Bunker(screen_rect.width/4, screen_rect.bottom - 150, screen, 1),
               Bunker(screen_rect.width/2, screen_rect.bottom - 150, screen, 2),
               Bunker(3 * screen_rect.width / 4, screen_rect.bottom - 150, screen, 3),
               Bunker(screen_rect.width, screen_rect.bottom - 150, screen, 4)]

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, score_button, ship, aliens, bullets)

        if stats.game_active:

            pygame.mixer.music.load('sounds/bgm.wav')
            pygame.mixer.music.set_volume(400)
            pygame.mixer.music.play(-1)
            ship.update()

            gf.update_ufo(ufo, ai_settings)
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufo, explosions, bunkers)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, ufo,  aliens, bullets, lasers)
            gf.update_explosions(explosions)

        gf.update_screen(ai_settings, stats, screen, sb, ship, ufo, aliens, bullets, lasers,
                         play_button, score_button, explosions, bunkers)
        clock.tick(60)


run_game()
