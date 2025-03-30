
import pygame
from pygame import mixer

pygame.init()
mixer.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

SCREEN_SIZE = (800, 800)
clock = pygame.time.Clock()
started = False
winner = None
G = 1
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_icon(pygame.image.load("Background/Logo.png").convert_alpha())  # Add Icon
pygame.display.set_caption("BrawhCombat")
ground = pygame.image.load("Background/ground.png").convert_alpha()
ground = pygame.transform.scale(ground, (80, 20))
grass1 = pygame.image.load("Background/grass1.png").convert_alpha()
grass1 = pygame.transform.scale(grass1, (80, 20))
grass2 = pygame.image.load("Background/grass2.png").convert_alpha()
grass2 = pygame.transform.scale(grass2, (80, 20))
temp = [grass1, grass2]
grasses = []
cloud = pygame.image.load("Background/cloud.png").convert_alpha()
cloud = pygame.transform.scale(cloud, (200, 200))
clouds = []
for i in range(4):
    cloud_rect = cloud.get_rect(center=(150 + i * 250, 150))
    clouds.append(cloud_rect)
