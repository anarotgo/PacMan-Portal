import pygame as pg
from pygame.sprite import Sprite, Group


class Portal(Sprite): 

  def __init__(self, game, type): 
    super().__init__()
    self.screen = game.screen
    self.image = pg.image.load('images/alien0.bmp')
    self.rect = self.image.get_rect()
    self.rect.y = self.rect.height
    self.x = float(self.rect.x)
    self.type = type
    
  def update(self): self.draw()

  def draw(self): 
    if self.type == 0:
      image = pg.image.load(f'assets/Portals/Portal_Blue0.png')
      rect = image.get_rect()
      rect.left, rect.top = self.rect.left, self.rect.top
      self.screen.blit(image, rect)

    if self.type == 1:
      image = pg.image.load(f'assets/Portals/Portal_Orange0.png')
      rect = image.get_rect()   
      rect.left, rect.top = self.rect.left, self.rect.top
      self.screen.blit(image, rect)
