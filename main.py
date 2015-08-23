import pygame, sys, text_to_screen
from tileC import Tile
from object_classes import *
from interaction import interaction
from A_Star import A_Star

pygame.init()
pygame.font.init()

pygame.mixer.init()

pygame.mixer.music.load('audio/tristram.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.25)

screen = pygame.display.set_mode((1280, 960)) # 40, 30

Tile.pre_init(screen)

clock = pygame.time.Clock()
FPS = 20
total_frames = 0
 
dungeon = pygame.image.load('images/map1.png')
survivor = Survivor(128, 512)

while True:

    screen.blit(dungeon, (0,0) )
    Zombie.spawn(total_frames, FPS)

    survivor.movement()
    Bullet.super_massive_jumbo_loop(screen)
    A_Star(screen, survivor, total_frames, FPS)
    interaction(screen, survivor)
    survivor.draw(screen)
    Zombie.update(screen)

    pygame.display.flip()
    clock.tick(FPS)
    total_frames += 1
