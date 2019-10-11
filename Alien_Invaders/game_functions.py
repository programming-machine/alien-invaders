import sys

import pygame
from bullet import Bullet
from bullet import Explosion
from bullet import Laser
from alien import Alien
import random




def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

def check_events(ai_settings, screen, stats, sb, play_button, score_button, ship, aliens, bullets):
    # Listen for keyboard & mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_score_button(stats, score_button, mouse_x, mouse_y)



def check_score_button(stats, score_button, mouse_x, mouse_y):
    button_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        stats.show_high_score = not stats.show_high_score


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if stats.game_active:
            fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_explosions(explosions):
    for explosion in explosions:
        if explosion.is_ufo:
            if (pygame.time.get_ticks() - explosion.time_start) >= 360:
                explosions.remove(explosion)
        else:
            if (pygame.time.get_ticks() - explosion.time_start) >= 45:
                explosions.remove(explosion)

def update_ufo(ufo, ai_settings):
    if ufo.is_dead and pygame.time.get_ticks() - ufo.timer > random.randint(8000, 12000):
        ufo.is_dead = False
        ufo.timer = pygame.time.get_ticks()
    else:
        if ufo.check_edges():
            ai_settings.ufo_direction *= -1
        ufo.update()


def check_bunker_collisions(aliens, bullets, lasers, bunkers):

    for x in range(0, 4):
        collisions = pygame.sprite.spritecollide(bunkers[x], lasers, False, False)
        if collisions:
                for sprite in collisions:
                    if not bunkers[x].is_destroyed():
                        sprite.kill()
                        bunkers[x].damage()
        collisions = pygame.sprite.spritecollide(bunkers[x], bullets, False, False)
        if collisions:
            for sprite in collisions:
                if not bunkers[x].is_destroyed():
                    sprite.kill()
                    bunkers[x].damage()
        collisions = pygame.sprite.spritecollide(bunkers[x], aliens, False, False)
        if collisions:
            bunkers[x].damage()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets, ufo, explosions):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)

    if collisions:

        for values in collisions.values():
            for sprite in values:
                aliens.remove(sprite)

                explosion = Explosion(sprite.rect.x, sprite.rect.y, sprite.row, False)
                explosions.add(explosion)
                dead_alien = pygame.mixer.Sound('sounds/invaderkilled.wav')
                dead_alien.play()
                stats.score += sprite.score
                sb.prep_score()

    check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens)

        stats.level += 1
        sb.prep_level()
    if not ufo.is_dead:
        ufo_shot = pygame.sprite.spritecollide(ufo, bullets, True)
        if ufo_shot:
            ufo.timer = pygame.time.get_ticks()
            explosion = Explosion(ufo.rect.x, ufo.rect.y, 0, True)
            stats.score += explosion.score
            explosions.add(explosion)
            dead_alien = pygame.mixer.Sound('sounds/invaderkilled.wav')
            dead_alien.play()
            sb.prep_score()
            ufo.is_dead = True



def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, lasers, ufo, explosions, bunkers):
    bullets.update()
    lasers.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for laser in lasers.copy():
        if laser.rect.bottom >= ai_settings.screen_height:
            lasers.remove(laser)

    deaths = pygame.sprite.spritecollide(ship, lasers, True, False)
    if deaths:
        ship_hit(stats, sb, ship, ufo, lasers, bullets)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, aliens, bullets, ufo, explosions)
    check_bunker_collisions(aliens, bullets, lasers, bunkers)




def update_screen(ai_settings, stats, screen, sb, ship, ufo, aliens, bullets, lasers, play_button,
                  score_button, explosions, bunkers):
    # Redraw the screen during each pass through the loop
    screen_rect = screen.get_rect()
    screen.fill(ai_settings.bg_color)
    font = pygame.font.Font(None, 50)
    if stats.game_active:
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        for laser in lasers.sprites():
            laser.draw_bullet()

        ship.blitme()
        aliens.draw(screen)
        explosions.draw(screen)
        sb.show_score()
        for x in range(0, 4):
            bunkers[x].update()
        if not ufo.is_dead:
            ufo.blitme()
    elif stats.show_high_score:

        surface = font.render("HIGH SCORE", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx - 20, screen_rect.centery - 300))
        screen.blit(surface, text_rect)
        surface = font.render(str(stats.high_score), True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx - 20, screen_rect.centery - 100))
        screen.blit(surface, text_rect)
        play_button.draw_button()
        score_button.msg = "Back"
        score_button.draw_button()

    else:

        surface = font.render("Alien Invaders", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx - 20, screen_rect.centery - 300))
        screen.blit(surface, text_rect)
        surface = font.render("= 10 PTS", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx, screen_rect.centery - 200))
        screen.blit(surface, text_rect)
        surface = font.render("= 20 PTS", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx, screen_rect.centery - 100))
        screen.blit(surface, text_rect)
        surface = font.render("= 40 PTS", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx, screen_rect.centery))
        screen.blit(surface, text_rect)
        surface = font.render("= ????", True, (255, 255, 255))
        text_rect = surface.get_rect(center=(screen_rect.centerx, screen_rect.centery + 100))
        screen.blit(surface, text_rect)
        enemy_1 = pygame.image.load("images/alien1.1.png")
        enemy_2 = pygame.image.load("images/alien2.1.png")
        enemy_3 = pygame.image.load("images/alien3.1.png")
        rect_1 = enemy_1.get_rect()
        rect_1.centerx = screen_rect.centerx - 150
        rect_1.centery = screen_rect.centery - 200
        rect_2 = enemy_2.get_rect()
        rect_2.centerx = screen_rect.centerx - 150
        rect_2.centery = screen_rect.centery - 100
        rect_3 = enemy_2.get_rect()
        rect_3.centerx = screen_rect.centerx - 150
        rect_3.centery = screen_rect.centery
        screen.blit(enemy_1, rect_1)
        screen.blit(enemy_2, rect_2)
        screen.blit(enemy_3, rect_3)
        ufo = pygame.image.load("images/ufo.png")
        ufo_rect = ufo.get_rect()
        ufo_rect.centerx = screen_rect.centerx - 150
        ufo_rect.centery = screen_rect.centery + 100
        screen.blit(ufo, ufo_rect)
        score_button.msg = "High Score"
        score_button.draw_button()
        play_button.draw_button()
    # Make the most recently drawn screen visible
    pygame.display.flip()

def update_aliens(ai_settings, stats, screen, sb, ship, ufo, aliens, bullets, lasers):

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.time.get_ticks() - ai_settings.laser_timer >= 600:
        ai_settings.laser_timer = pygame.time.get_ticks()
        sprite_list = aliens.sprites()
        random.seed()
        fire_laser(ai_settings, screen, sprite_list[random.randint(0, len(sprite_list)-1)], lasers)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, sb, ship, ufo, lasers, bullets)

    check_aliens_bottom(stats, screen, sb, ship, ufo, lasers, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
        shoot_sound.play()



def get_number_rows(ai_settings, ship_height, alien_height):

    available_space_y = (ai_settings.screen_height - (2*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def get_number_aliens_x(ai_settings, alien_width):

    available_space_x = ai_settings.screen_width - 1.25 * alien_width
    number_aliens_x = int(available_space_x / (1.25 * alien_width))
    return number_aliens_x

def fire_laser(ai_settings, screen, alien, lasers):
    if len(lasers) < ai_settings.lasers_allowed:
        new_laser = Laser(ai_settings, screen, alien)
        lasers.add(new_laser)
        shoot_sound = pygame.mixer.Sound('sounds/shoot2.wav')
        shoot_sound.play()





def create_alien(ai_settings, screen, aliens, alien_number, row_number, frame):

    alien = Alien(ai_settings, screen, row_number, frame)
    alien_width = alien.rect.width

    alien.x = alien_width + 1.15 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 156 + 56 * row_number
    aliens.add(alien)




def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, sb, ship, ufo, lasers, bullets):
    ship_explosion = pygame.mixer.Sound('sounds/explosion.wav')
    ship_explosion.play()
    ship.exploding = True
    if stats.ships_left > 1:
        stats.ships_left -= 1

        sb.prep_ships()
        bullets.empty()
        lasers.empty()

        # time.sleep(0.5)
    else:
        stats.game_active = False
        stats.show_high_score = False
        stats.write()
        pygame.mouse.set_visible(True)
        ufo.is_dead = False

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_high_score(stats, sb):

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_aliens_bottom(stats, screen, sb, ship, ufo, lasers, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, sb, ship, ufo, lasers, bullets)
            break

def create_fleet(ai_settings, screen, aliens):
    frame = 1
    alien = Alien(ai_settings, screen, 1, frame)
    frame = 2
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = 5

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, frame)
            if frame == 1:
                frame = 2
            elif frame == 2:
                frame = 1

