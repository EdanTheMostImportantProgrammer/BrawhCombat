import pygame
import random
import math
import sys

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()
started = False
winner = None

SCREEN_SIZE = (800, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)
ground = pygame.image.load("ground.png").convert_alpha()
ground = pygame.transform.scale(ground, (80, 20))
grass1 = pygame.image.load("grass1.png").convert_alpha()
grass1 = pygame.transform.scale(grass1, (80, 20))
grass2 = pygame.image.load("grass2.png").convert_alpha()
grass2 = pygame.transform.scale(grass2, (80, 20))
temp = [grass1, grass2]
grasses = []
cloud = pygame.image.load("cloud.png").convert_alpha()
cloud = pygame.transform.scale(cloud, (200, 200))
clouds = []
for i in range(4):
    cloud_rect = cloud.get_rect(center=(150 + i * 250, 150))
    clouds.append(cloud_rect)



G = 1


class Character:
    def __init__(self, x, y, speed_x, speed_y, jumps, color, health_bar_x, health_bar_y, id):
        self.x = x
        self.y = y
        self.id = id
        if id == 1:
            self.images_left = [pygame.image.load("Player1/left.png").convert_alpha(),
                                pygame.image.load("Player1/left_1.png").convert_alpha(), pygame.image.load(
                    "Player1/left_2.png").convert_alpha(), pygame.image.load("Player1/left_3.png").convert_alpha(),
                                pygame.image.load("Player1/left_4.png").convert_alpha()]
            self.images_right = [pygame.image.load("Player1/right.png").convert_alpha(),
                                 pygame.image.load("Player1/right_1.png").convert_alpha(), pygame.image.load(
                    "Player1/right_2.png").convert_alpha(), pygame.image.load("Player1/right_3.png").convert_alpha(),
                                 pygame.image.load("Player1/right_4.png").convert_alpha()]
            for i in range(len(self.images_left)):
                self.images_left[i] = pygame.transform.scale(self.images_left[i], (100, 100))
                self.images_right[i] = pygame.transform.scale(self.images_right[i], (100, 100))
            self.current_img = self.images_left[0]
        else:
            self.images_left = [pygame.image.load("Player2/left.png").convert_alpha(), pygame.image.load("Player2/left_1.png").convert_alpha(), pygame.image.load(
                "Player2/left_2.png").convert_alpha(), pygame.image.load("Player2/left_3.png").convert_alpha(), pygame.image.load("Player2/left_4.png").convert_alpha()]
            self.images_right = [pygame.image.load("Player2/right.png").convert_alpha(),
                                pygame.image.load("Player2/right_1.png").convert_alpha(), pygame.image.load(
                    "Player2/right_2.png").convert_alpha(), pygame.image.load("Player2/right_3.png").convert_alpha(),
                                pygame.image.load("Player2/right_4.png").convert_alpha()]
            for i in range(len(self.images_left)):
                self.images_left[i] = pygame.transform.scale(self.images_left[i], (100, 100))
                self.images_right[i] = pygame.transform.scale(self.images_right[i], (100, 100))
            self.current_img = self.images_left[0]
        self.img_rect = self.current_img.get_rect(topright=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.current_img)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.jump_limit = 1
        self.jumps = jumps
        self.color = color
        self.touching_ground = False
        self.health = 100
        self.health_bar_x = health_bar_x
        self.health_bar_y = health_bar_y
        self.health_bar = pygame.rect.Rect(self.health_bar_x, self.health_bar_y, self.health, 20)
        self.health_bar_outline = pygame.rect.Rect(self.health_bar.left, self.health_bar.top, 100, 20)
        self.index = 0

    def gravity(self):
        self.speed_y += G

    def move_right(self):
        if not self.touching_ground:
            self.current_img = self.images_right[0]
        else:
            if self.index > 4:
                self.index = 0
            self.current_img = self.images_right[self.index]
            self.index += 1
            pygame.time.delay(1)
        self.mask = pygame.mask.from_surface(self.current_img)
        self.speed_x += 1
        if self.speed_x > 8:
            self.speed_x = 8

    def move_left(self):
        if not self.touching_ground:
            self.current_img = self.images_left[0]
        else:
            if self.index > 4:
                self.index = 0
            self.current_img = self.images_left[self.index]
            self.index += 1
            pygame.time.delay(1)
        self.mask = pygame.mask.from_surface(self.current_img)
        self.speed_x -= 1
        if self.speed_x < -8:
            self.speed_x = -8

    def jump(self):
        self.speed_y = -12
        self.jumps += 1



    def bump(self, target):
        damage = (abs(self.speed_x) + abs(self.speed_y)) - (abs(target.speed_x) + abs(target.speed_y))
        if damage > 0:
            target.health -= damage
            target.health_bar = pygame.rect.Rect(target.health_bar_x, target.health_bar_y, target.health, 20)
        elif damage < 0:
            self.health += damage
            self.health_bar = pygame.rect.Rect(self.health_bar_x, self.health_bar_y, self.health, 20)
        else:
            pass
        if self.x > target.x:
            self.x += 1
            target.x -= 1
        if target.x > self.x:
            target.x += 1
            self.x -= 1
        if target.y - self.y >= 32:
            self.speed_y = 0
            self.jump()
        if self.y - target.y >= 32:
            target.speed_y = 0
            target.jump()
        else:
            swapselfx = self.speed_x
            self.speed_x = target.speed_x
            target.speed_x = swapselfx


    def move(self):
        if self.x >= 831:
            self.speed_x *= -0.9
            self.x -= 1
        if self.x <= 84:
            self.speed_x *= -0.9
            self.x += 1
        if not self.touching_ground:
            self.gravity()
        else:
            self.jumps = 0
        self.x += self.speed_x
        self.y += self.speed_y


player1 = Character(200, 500, 0, 0, 0, (255, 0, 0), 10, 10, 1)
player2 = Character(700, 500, 0, 0, 0, (0, 0, 255), 690, 10, 2)
players = [player1, player2]


def main():
    global started, winner
    while not started:
        started = main_menu()

    winner = game()
    game_over(winner)


def restart():
    global started
    global winner
    global player1
    global player2
    global players

    started = False
    winner = None

    player1 = Character(200, 500, 0, 0, 0, (255, 0, 0), 10, 10, 1)
    player2 = Character(700, 500, 0, 0, 0, (0, 0, 255), 690, 10, 2)
    players = [player1, player2]

    main()


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

        player1.move()
        player2.move()

        for player in players:
            if player.y + 100 >= 600:
                player.touching_ground = True
                player.y = 500
                player.speed_y = 0
            else:
                player.touching_ground = False
            player.img_rect = player.current_img.get_rect(topright=(player.x, player.y))
            player.mask = pygame.mask.from_surface(player.current_img)
            screen.blit(player.current_img, player.img_rect)



        pygame.draw.rect(screen, (0, 255, 0), player1.health_bar)
        pygame.draw.rect(screen, (0, 255, 0), player2.health_bar)
        pygame.draw.rect(screen, (255, 255, 255), player1.health_bar_outline, 2)
        pygame.draw.rect(screen, (255, 255, 255), player2.health_bar_outline, 2)

        if player1.mask.overlap(player2.mask, (player1.x - player2.x, player1.y - player2.y)):
            player1.bump(player2)

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
                    restart()
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


if __name__ == "__main__":
    main()