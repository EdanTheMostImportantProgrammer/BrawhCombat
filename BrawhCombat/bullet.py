from player import *

class Bullet:
    def __init__(self, x, y, p_direction, target):
        self.x = x
        self.y = y
        self.p_direction = p_direction
        self.speed = 25
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.math.Vector2(0, 0)
        self.aimed = False
        self.bullet_left = pygame.image.load("Bullet/bullet_left.png").convert_alpha()
        self.bullet_right = pygame.image.load("Bullet/bullet_right.png").convert_alpha()
        self.bullet_up = pygame.image.load("Bullet/bullet_up.png").convert_alpha()
        self.bullet_down = pygame.image.load("Bullet/bullet_down.png").convert_alpha()
        self.current_image = self.bullet_left if self.p_direction == "left" else self.bullet_right
        self.img_rect = self.current_image.get_rect(topright=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.current_image)
        self.target = target

    def aim(self):
        if not self.aimed:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= 2000:
                self.aimed = True
                mx, my = pygame.mouse.get_pos()
                target = pygame.math.Vector2(mx, my)
                start = pygame.math.Vector2(self.x, self.y)
                self.direction = (target - start).normalize() * self.speed

    def collision(self):
        if self.x >= 800 or self.x <= 0:
            if self.x >= 800:
                self.current_image = self.bullet_left
            else:
                self.current_image = self.bullet_right
            self.direction.x *= -1

        if self.y >= 600 or self.y <= 0:
            if self.y >= 600:
                self.current_image = self.bullet_up
            else:
                self.current_image = self.bullet_down
            self.direction.y *= -1


        if self.target.mask.overlap(self.mask, (self.img_rect.x - self.target.img_rect.x, self.img_rect.y - self.target.img_rect.y)):
            self.target.health = 0

    def update(self):
        self.aim()
        self.collision()
        self.x += self.direction.x
        self.y += self.direction.y
        self.img_rect.center = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.current_image)
        self.draw()

    def draw(self):
        screen.blit(self.current_image, self.img_rect)
