import math

from player import *

class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.speed = 30
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(0, 0)
        self.aimed = False
        self.bullet_right = pygame.image.load("Bullet/bullet_right.png").convert_alpha()
        self.bullet_right = pygame.transform.scale(self.bullet_right, (80, 80))
        self.current_image = self.bullet_right
        self.img_rect = self.current_image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.current_image)
        self.target = target
        self.correction_angle = 0
        self.rotating = False
        self.rot_image = self.current_image
        self.rot_image_rect = self.current_image.get_rect()
        self.angle = 0

    def aim(self):
        if not self.aimed:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= 2000:
                self.rotating = False
                self.aimed = True
                mx, my = pygame.mouse.get_pos()
                target = pygame.math.Vector2(mx, my)
                start = pygame.math.Vector2(self.x, self.y)
                self.direction = (target - start).normalize() * self.speed
            else:
                mx, my = pygame.mouse.get_pos()
                dx, dy = mx - self.img_rect.centerx, my - self.img_rect.centery
                self.angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle
                self.rot_image = pygame.transform.rotate(self.current_image, self.angle)
                self.rotating = True

    def collision(self):
        if self.x >= 800 or self.x <= 0:
            self.direction.x *= -1
            self.angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) - self.correction_angle
            self.rot_image = pygame.transform.rotate(self.current_image, self.angle)

        if self.y >= 600 or self.y <= 0:
            self.angle = math.degrees(math.atan2(self.direction.y, self.direction.x)) - self.correction_angle
            self.direction.y *= -1
            self.rot_image = pygame.transform.rotate(self.current_image, self.angle)

        if not self.target.invisible:
            if self.target.mask.overlap(self.mask, (self.img_rect.x - self.target.img_rect.x,
                                                    self.img_rect.y - self.target.img_rect.y)):
                self.target.health = 0

    def update(self):
        self.aim()
        self.collision()
        self.x += self.direction.x
        self.y += self.direction.y
        self.img_rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.current_image)
        self.draw_rotate()

    def draw_rotate(self):
        screen.blit(self.rot_image, self.img_rect)
