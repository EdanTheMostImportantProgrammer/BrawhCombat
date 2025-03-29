import random
import sys

import pygame.time

from bullet import *


def restart():
    global started, winner, player1, player2, players
    started = False
    winner = None

    player1 = Character(200, 500, 0, 0, 0, (255, 0, 0), 10, 10, 10, 40, 1)
    player2 = Character(700, 500, 0, 0, 0, (0, 0, 255), 690, 10, 690, 40, 2)
    players = [player1, player2]

    return started, winner, player1, player2, players


def main_menu():
    text1_surface = my_font.render("Welcome To Our Game!", True, (255, 255, 255))
    text2_surface = my_font.render("Press Any Key To Start", True, (255, 255, 255))
    text1_x = 239
    base1_y = 200
    text2_x = 239
    base2_y = 300
    amplitude = 50
    frequency = 0.05

    t = 0
    while True:
        clock.tick(30)
        screen.fill((0, 216, 255))
        for i in range(4):
            screen.blit(cloud, clouds[i])
            clouds[i].x -= 1
            if clouds[i].x <= -200:
                clouds[i].x = 800

        text1_y = base1_y + amplitude * math.sin(t)
        text2_y = base2_y + amplitude * math.sin(t)

        screen.blit(text1_surface, (text1_x, int(text1_y)))
        screen.blit(text2_surface, (text2_x, int(text2_y)))

        t += frequency

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                started = True
                return started

        for i in range(10):
            for j in range(10):
                if i == 0:
                    grass = random.randint(0, 1)
                    grasses.append(temp[grass])
                    screen.blit(grasses[j], (j * 80, 600 + (i * 20)))
                else:
                    screen.blit(ground, (j * 80, 600 + (i * 20)))

        pygame.display.update()


def game():
    bullet1 = Bullet(0, 0, player1)
    bullet2 = Bullet(0, 0, player2)
    while True:
        clock.tick(30)
        screen.fill((0, 216, 255))
        for i in range(4):
            screen.blit(cloud, clouds[i])
            clouds[i].x -= 1
            if clouds[i].x <= -200:
                clouds[i].x = 800

        if player1.health <= 0:
            winner = "Player 2"
            return winner
        elif player2.health <= 0:
            winner = "Player 1"
            return winner

        player1.update()
        player2.update()

        if player1.mask.overlap(player2.mask, (player1.x - player2.x, player1.y - player2.y)):
            player1.bump(player2)

        for player in players:
            if player.sword:
                player.current_img = player.images_right[5] if player.id == 1 else player.images_left[5]
            if player.y + 100 >= 600:
                player.touching_ground = True
                player.y = 500
                player.speed_y = 0
            else:
                player.touching_ground = False

            if player.ulted:
                if player.speed_y >= 0:
                    player.invisible = True
                    player.ult_time = pygame.time.get_ticks()
                    if player.id == 1:
                        if player1.x < 768:
                            bullet1 = Bullet(player.x, player.y, player2)
                        else:
                            bullet1 = Bullet(768, player.y, player2)
                    else:
                        if player2.x < 768:
                            bullet2 = Bullet(player.x, player.y, player1)
                        else:
                            bullet2 = Bullet(768, player.y, player1)
                    player.ulting = True
                    player.ulted = False

            if player.ulting:
                if player.id == 1:
                    bullet1.update()
                else:
                    bullet2.update()
                if pygame.time.get_ticks() - player.ult_time > 7500:
                    player.ulting = False
                    player.invisible = False

            if not player.invisible:
                player.img_rect = player.current_img.get_rect(topright=(player.x, player.y))
                player.mask = pygame.mask.from_surface(player.current_img)
                screen.blit(player.current_img, player.img_rect)

            pygame.draw.rect(screen, (0, 255, 0), player.health_bar)
            pygame.draw.rect(screen, (255, 255, 255), player.health_bar_outline, 2)
            pygame.draw.rect(screen, (0, 0, 255), player.energy_bar)
            pygame.draw.rect(screen, (255, 255, 255), player.energy_bar_outline, 2)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player1.jumps < player1.jump_limit:
                    player1.jump()
                if event.key == pygame.K_UP and player2.jumps < player2.jump_limit:
                    player2.jump()
                if event.key == pygame.K_e and not player1.ulted and player1.energy == 100:
                    player1.ulted = True
                    player1.speed_y = -20
                    player1.energy = 0
                    player1.energy_bar = pygame.rect.Rect(player1.energy_bar_x,
                                                          player1.energy_bar_y, player1.energy, 20)
                if event.key == pygame.K_DOWN and not player2.ulted and player2.energy == 100:
                    player2.ulted = True
                    player2.speed_y = -20
                    player2.energy = 0
                    player2.energy_bar = pygame.rect.Rect(player2.energy_bar_x, player2.energy_bar_y,
                                                          player2.energy, 20)

                if event.key == pygame.K_r and player1.energy >= 5 and not player1.sword:
                    player1.sword_attack()

                if event.key == pygame.K_q and player1.energy >= 5:
                    player1.dash_attack()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_d]:
            player1.move_right()

        if pressed_keys[pygame.K_a]:
            player1.move_left()

        if pressed_keys[pygame.K_RIGHT]:
            player2.move_right()

        if pressed_keys[pygame.K_LEFT]:
            player2.move_left()

        for i in range(10):
            for j in range(10):
                if i == 0:
                    grass = random.randint(0, 1)
                    grasses.append(temp[grass])
                    screen.blit(grasses[j], (j * 80, 600 + (i * 20)))
                else:
                    screen.blit(ground, (j * 80, 600 + (i * 20)))

        pygame.display.update()


def game_over(winner):
    current_time = pygame.time.get_ticks()
    text1_surface = my_font.render(f"{winner} Has Won!", True, (255, 255, 255))
    text2_surface = my_font.render("Press R To Restart Or Any Other Key To Quit", True, (255, 255, 255))
    text1_x = 400 - text1_surface.get_width() // 2
    base1_y = 200
    text2_x = 400 - text2_surface.get_width() // 2
    base2_y = 300
    amplitude = 50
    frequency = 0.05

    t = 0
    while True:
        clock.tick(30)
        screen.fill((0, 216, 255))

        for i in range(4):
            screen.blit(cloud, clouds[i])
            clouds[i].x -= 1
            if clouds[i].x <= -200:
                clouds[i].x = 800

        text1_y = base1_y + amplitude * math.sin(t)
        text2_y = base2_y + amplitude * math.sin(t)

        screen.blit(text1_surface, (text1_x, int(text1_y)))
        screen.blit(text2_surface, (text2_x, int(text2_y)))

        t += frequency

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and pygame.time.get_ticks() - current_time >= 500:
                if event.key == pygame.K_r:
                    return True
                else:
                    pygame.quit()
                    sys.exit()

        for i in range(10):
            for j in range(10):
                if i == 0:
                    grass = random.randint(0, 1)
                    grasses.append(temp[grass])
                    screen.blit(grasses[j], (j * 80, 600 + (i * 20)))
                else:
                    screen.blit(ground, (j * 80, 600 + (i * 20)))

        pygame.display.update()