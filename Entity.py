
from abc import ABC, abstractmethod
import pygame


class Entity(ABC,pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image: pygame.Surface = pygame.Surface((0, 0))
    self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    self.active: bool = False
    self.isAlive: bool = True

  @abstractmethod
  def draw(self, screen: pygame.Surface):
      pass  

  def desactive(self):
    self.active = False

  def get_active(self) -> bool:
    return self.active
  
  def set_active(self, active: bool):
    self.active = active
  
  def get_isAlive(self) -> bool:
    return self.isAlive
  
  def set_isAlive(self, isAlive: bool):
    self.isAlive = isAlive

  def kill(self):
    self.active = False
    self.isAlive = False