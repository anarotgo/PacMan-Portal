import pygame
from pygame.sprite import Sprite, Group
from timer import Timer
from random import randint
from enum import Enum

class ShotType(Enum):
    BLUELEFT = 1
    BLUERIGHT = 2
    BLUEUP = 3
    BLUEDOWN = 4
    ORANGELEFT = 5
    ORANGERIGHT = 6
    ORANGEUP = 7
    ORANGEDOWN = 8


class Shots():
    def __init__(self, type):
        self.shots = Group()
        self.type = type

    def reset(self):
        self.shots.empty()
    
    def shoot(self, screen, x, y, type):
        self.shots.add(Shot(screen = screen, x=x, y=y, type=type))
    
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
    blue_shot_l_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Blue/Left/Blue_Shot_L{n}.png'), 0, 1) for n in range(4)]
    blue_shot_r_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Blue/Right/Blue_Shot_R{n}.png'), 0, 1) for n in range(4)]
    blue_shot_up_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Blue/Up/Blue_Shot_Up{n}.png'), 0, 1) for n in range(4)]
    blue_shot_down_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Blue/Down/Blue_Shot_Down{n}.png'), 0, 1) for n in range(4)]

    orange_shot_l_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Orange/Left/Orange_Shot_L{n}.png'), 0, 1) for n in range(4)]
    orange_shot_r_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Orange/Right/OrangeShot_R{n}.png'), 0, 1) for n in range(4)]
    orange_shot_up_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Orange/Up/OrangeShot_Up{n}.png'), 0, 1) for n in range(4)]
    orange_shot_down_images = [pygame.transform.rotozoom(pygame.image.load(f'assets/Portal_Effects/Shots/Orange/Down/OrangeShot_Down{n}.png'), 0, 1) for n in range(4)]
    shot_images = {ShotType.BLUELEFT: blue_shot_l_images, ShotType.BLUERIGHT: blue_shot_r_images, ShotType.BLUEUP: blue_shot_up_images, ShotType.BLUEDOWN: blue_shot_down_images,
                    ShotType.ORANGELEFT: orange_shot_l_images, ShotType.ORANGERIGHT: orange_shot_r_images,ShotType.ORANGEUP: orange_shot_up_images, ShotType.ORANGEDOWN: orange_shot_down_images,}


    def __init__(self, screen, x, y, type):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 10, 30)
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.type = type
        self.speed = 1
        imagelist = self.shot_images[type]
        self.timer = Timer(image_list=imagelist, delay=200)
       


    def update(self):
        if self.type == ShotType.BLUEDOWN or ShotType.BLUEUP or ShotType.ORANGEDOWN or ShotType.ORANGEUP:
            self.y += self.speed if self.type == ShotType.BLUEDOWN or ShotType.ORANGEDOWN else -self.speed
        else:
            self.x += self.speed if self.type == ShotType.BLUELEFT or ShotType.ORANGELEFT else -self.speed
        self.rect.y = self.y
        self.draw()
        
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # pg.draw.rect(self.screen, self.color, self.rect)
    
