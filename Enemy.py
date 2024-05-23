import pygame
import random
from Observer import Collidable

class Enemy(Collidable):
  def __init__(self,posx,posy):
    super().__init__()
    self.image = pygame.image.load("Images/enemy.png")
    self.image = pygame.transform.smoothscale(self.image, (40, 40))
    self.rect = self.image.get_rect()
    self.rect.x = posx
    self.rect.y = posy

    #self.startx = posx
    #self.starty = posy
    self.pos = posx

    self.active = True  #Para saber si está vivo o no
  
  #No la he usado aún, pero sirve para "teletransportarse"
  def move(self, x, y):
    self.rect.x = x
    self.rect.y = y

    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  def move_rigth(self,num):
     self.rect.x += num
  
  def move_left(self,num):
     self.rect.x -= num

  def move_down(self, num):
    self.rect.y += num
    #print(max(0, min(self.rect.x, 800 - self.rect.width)))

  def move_up(self,num):
     self.rect.y -= num

  def draw(self, screen: pygame.Surface):
    if self.active:
      screen.blit(self.image, self.rect)
    else:
      pass

  def get_x_coords(self):
    return self.rect.x

  def get_y_coords(self):
    return self.rect.y

  def on_collision(self, other: Collidable):
    # print("Enemy collided with:", other)
    pass
   
  def is_alive(self):
    return self.active

  def kill(self):
    self.active = False