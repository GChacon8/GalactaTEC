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
  
  def move(self, x, y):
    self.rect.x = x
    self.rect.y = y

    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  def move_down(self):
    self.rect.y += 40
    print(self.rect.y)

    # Limitar la nave dentro de los límites de la pantalla
    #self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    #self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  
  def draw(self, screen):
    screen.blit(self.image, self.rect)
