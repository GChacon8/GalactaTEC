import pygame
import random



class Enemy:
  def __init__(self,posx,posy):
    self.image = pygame.image.load("Images/enemy.png")
    self.image = pygame.transform.smoothscale(self.image, (40, 40))
    self.rect = self.image.get_rect()
    self.rect.x = posx
    self.rect.y = posy
    self.pos = posx

    self.active = True
  
  #No la he usado aún, pero sirve para "teletransportarse"
  def move(self, x, y):
    self.rect.x = x
    self.rect.y = y

    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  def move_rigth(self):
     self.rect.x += 40
  
  def move_left(self):
     self.rect.x -= 40

  def move_down(self):
    self.rect.y += 40
    #print(max(0, min(self.rect.x, 800 - self.rect.width)))
  
  def move_up(self):
     self.rect.y -= 40



  def kill(self):
    self.active = False
  
  def draw(self, screen):
    if self.active:
      screen.blit(self.image, self.rect)
    else:
      pass

  def get_x_coords(self):
    return self.rect.x
  
  def get_y_coords(self):
    return self.rect.y
  
  def isDead(self):
    return self.active
  
 
