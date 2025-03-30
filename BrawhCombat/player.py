import time
from CPU import *

from variables import *


class Character:
    def __init__(self, x, y, speed_x, speed_y, jumps, color, health_bar_x, health_bar_y, energy_bar_x,
                 energy_bar_y, id):
        self.x = x
        self.y = y
        self.id = id
        folder = "Player1" if self.id == 1 else "Player2"
        self.images_left = [pygame.image.load(f"{folder}/left_{j}.png").convert_alpha() for j in range(6)]
        self.images_right = [pygame.image.load(f"{folder}/right_{j}.png").convert_alpha() for j in range(6)]
        for j in range(6):
            self.images_left[j] = pygame.transform.scale(self.images_left[j], (100, 100))
            self.images_right[j] = pygame.transform.scale(self.images_right[j], (100, 100))
        self.current_img = self.images_right[0] if self.id == 1 else self.images_left[0]
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
        self.energy = 0
        self.energy_bar_x = energy_bar_x
        self.energy_bar_y = energy_bar_y
        self.energy_bar = pygame.rect.Rect(self.energy_bar_x, self.energy_bar_y, self.energy, 20)
        self.energy_bar_outline = pygame.rect.Rect(self.energy_bar.left, self.energy_bar.top, 100, 20)
        self.index = 0
        self.ulted = False
        self.ulting = False
        self.ult_time = pygame.time.get_ticks()
        self.invisible = False
        self.direction = "right" if self.id == 1 else "left"
        mixer.music.load("Sound/jump.mp3")
        mixer.music.set_volume(0.4)
        self.sword = False
        self.sword_timer = 0

    def gravity(self):
        if not self.invisible:
            self.speed_y += G

    def move_right(self):
        if not self.invisible:
            self.direction = "right"
            if not self.touching_ground:
                self.current_img = self.images_right[0]
            else:
                if self.index > 4:
                    self.index = 0
                self.current_img = self.images_right[self.index]
                self.index += 1
                pygame.time.delay(10)
            self.mask = pygame.mask.from_surface(self.current_img)
            self.speed_x += 1
            if self.speed_x > 8:
                self.speed_x = 8

    def move_left(self):
        if not self.invisible:
            self.direction = "left"
            if not self.touching_ground:
                self.current_img = self.images_left[0]
            else:
                if self.index > 4:
                    self.index = 0
                self.current_img = self.images_left[self.index]
                self.index += 1
                pygame.time.delay(10)
            self.mask = pygame.mask.from_surface(self.current_img)
            self.speed_x -= 1
            if self.speed_x < -8:
                self.speed_x = -8

    def jump(self):
        mixer.music.play()
        if not self.invisible:
            self.speed_y = -12
            self.jumps += 1

    def switch_speeds(self, target):
        swapselfx = self.speed_x
        self.speed_x = target.speed_x
        target.speed_x = swapselfx

    def bump(self, target):
        damage = (abs(self.speed_x) + abs(self.speed_y)) - (abs(target.speed_x) + abs(target.speed_y))
        if damage > 0:
            if self.sword:
                damage *= 4
            target.health -= damage
            target.health_bar = pygame.rect.Rect(target.health_bar_x, target.health_bar_y, target.health, 20)
            if self.energy < 100:
                self.energy += 5
                self.energy_bar = pygame.rect.Rect(self.energy_bar_x, self.energy_bar_y, self.energy, 20)
        elif damage < 0:
            if target.sword:
                damage *= 4
            self.health += damage
            self.health_bar = pygame.rect.Rect(self.health_bar_x, self.health_bar_y, self.health, 20)
            if target.energy < 100:
                target.energy += 5
                target.energy_bar = pygame.rect.Rect(target.energy_bar_x, target.energy_bar_y, target.energy, 20)


        if self.x > target.x:
            self.x += 1
            target.x -= 1
        if target.x > self.x:
            target.x += 1
            self.x -= 1
        if target.y > self.y:
            if target.touching_ground:
                self.y = target.y - 100

            self.jump()
        if self.y > target.y:
            if self.touching_ground:
                target.y = self.y - 100

            target.jump()
        elif target.img_rect.top > self.img_rect.bottom and not target.touching_ground:
            self.jump()
        elif self.img_rect.top > target.img_rect.bottom and not self.touching_ground:
            target.jump()

        self.switch_speeds(target)

    def update(self):
        if not self.invisible:
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
            self.check_collision(player2)
            if self.sword:
                if self.sword_timer + 0.5 <= time.time():
                    self.sword = False
                    self.current_img = self.images_right[0] if self.id == 1 else self.images_left[0]

    def check_collision(self, target):
        if self.mask.overlap(target.mask, (self.x - target.x, self.y - target.y)):
            if self.x > target.x:
                self.img_rect.left = target.img_rect.right
            elif target.x > self.x:
                target.img_rect.left = self.img_rect.right
            if self.y < target.y:
                self.img_rect.top = target.img_rect.bottom
            elif target.y < self.y:
                target.img_rect.top = self.img_rect.bottom

    def sword_attack(self):
        self.energy -= 5
        self.energy_bar = pygame.rect.Rect(self.energy_bar_x, self.energy_bar_y, self.energy, 20)
        self.sword = True
        self.sword_timer = time.time()
        print("sword_on")

    def dash_attack(self):
        self.energy -= 5
        self.energy_bar = pygame.rect.Rect(self.energy_bar_x, self.energy_bar_y, self.energy, 20)
        mx, my = pygame.mouse.get_pos()
        target = pygame.math.Vector2(mx, my)
        start = pygame.math.Vector2(self.x, self.y)
        self.direction = (target - start).normalize() * 10
        self.speed_x += self.direction.x
        self.speed_y = self.direction.y


player1 = Character(200, 500, 0, 0, 0, (255, 0, 0), 10, 10, 10, 40, 1)
player2 = Character(700, 500, 0, 0, 0, (0, 0, 255), 690, 10, 690, 40, 2)
players = [player1, player2]
cpu = CPU(100, player2, player1)
