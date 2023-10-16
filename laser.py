import pygame
from pygame.sprite import Sprite, Group
from pacman import Pacman
from mazes import maze
from random import randint
# from timer import Timer
# For some reason line 6 doesn't import properly

# Claire Swiatek : Portal Laser Class
# Attempting to refactor/repurpose the laser code from Alien Invasion. 

class Shots():
    def __init__(self, settings, type):
        self.shots = Group()
        self.settings = settings
        self.type = type

    def reset(self):
        self.shots.empty()
    
    def shoot(self, game, x, y):
        self.shots.add(Shot(settings=game.settings, screen = game.screen, x=x, y=y))
    
    def update(self):
        self.shots.update()
        for shot in self.shots.copy():
            if shot.rect.bottom or shot.rect.top or shot.rect.left or shot.rect.right <= 0:
                self.shots.remove(shot)
    
    def draw(self):
        for shot in self.shots.sprites(): shot.draw()

# Shot class below

class Shot(Sprite):
    """Meant to manage the portal shots for PacMan"""
    blue_shot_l_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Blue/Left/Blue_Shot_L{n}.png'), 0, 1) for n in range(4)]
    blue_shot_r_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Blue/Left/Blue_Shot_R{n}.png'), 0, 1) for n in range(4)]
    blue_shot_up_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Blue/Left/Blue_Shot_Up{n}.png'), 0, 1) for n in range(4)]
    blue_shot_down_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Blue/Left/Blue_Shot_Down{n}.png'), 0, 1) for n in range(4)]

    orange_shot_l_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Orange/Left/Orange_Shot_L{n}.png'), 0, 1) for n in range(4)]
    orange_shot_r_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Orange/Left/Orange_Shot_R{n}.png'), 0, 1) for n in range(4)]
    orange_shot_up_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Orange/Left/Orange_Shot_Up{n}.png'), 0, 1) for n in range(4)]
    orange_shot_down_images = [pygame.transform.rotozoom(pygame.image.load(f'Sprites/Portal_Effects/Shots/Orange/Left/Orange_Shot_Down{n}.png'), 0, 1) for n in range(4)]

    def __init__(self, settings, screen, x, y):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.type = type
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed = settings.laser_speed

        imageListBl = Shot.blue_shot_l_images[type]
        imageListBr = Shot.blue_shot_r_images[type]
        imageListBUp = Shot.blue_shot_up_images[type]
        imageListBDown = Shot.blue_shot_down_images[type]

        imageListOl = Shot.orange_shot_l_images[type]
        imageListOr = Shot.orange_shot_r_images[type]
        imageListOUp = Shot.orange_shot_up_images[type]
        imageListODown = Shot.orange_shot_down_images[type]
        # self.timer = Timer(image_list=imagelist, delay=200)
        # trying to figure out how to hook this to PacMan
    
    def update(self):
        self.y += self.speed if self.type == type else -self.speed
        self.rect.y = self.y
        self.rect.x = self.x
        self.draw()
    # WIP/TODO

    def draw(self):
        image = self.timer.image()
        # rect for PacMan?
        rect = image.get_rect()
        self.screen.blit(image, rect)
    #WIP/TODO
    