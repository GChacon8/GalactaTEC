from abc import ABC, abstractmethod
from typing import Sequence
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
    super().kill()
    self.active = False
    self.isAlive = False

class Collidable(Entity,ABC):

    def __init__(self):
        super().__init__()
    
    def check_collision(self, other: "Collidable"):
        return self.rect.colliderect(other.rect)
    
    @abstractmethod
    def on_collision(self, other: "Collidable"):
        raise NotImplementedError("This method should be overridden by subclasses")
    

class CollisionRules:
    def __init__(self):
        self.rules = {
            "Ship": ["Bonus", "Enemy", "Bullet"],
            "Enemy": ["Ship", "Bullet"],
            "Bullet": ["Enemy", "Ship"],
            "Bonus": ["Ship"]
        }

    def can_collide(self, obj1: Collidable, obj2: Collidable):
        # Obtén el nombre de la clase de cada objeto
        class1 = obj1.__class__.__name__
        class2 = obj2.__class__.__name__
        # Comprueba si la colisión está permitida verificando una dirección
        return (
                class2 in self.rules.get(class1, []) or 
                class1 in self.rules.get(class2, [])
               )


class CollisionObserver:
    def __init__(self):
        self.collidables: list[Collidable] = []
        self.rules = CollisionRules()

    def register(self, collidable: Sequence[Collidable]):
        self.collidables.extend(collidable)

    def update(self):
        # Evita comprobar el mismo par dos veces
        for i in range(len(self.collidables)):
            for j in range(i + 1, len(self.collidables)):
                collidable1 = self.collidables[i]
                collidable2 = self.collidables[j]
                if (
                    collidable1.check_collision(collidable2) and 
                    self.rules.can_collide(collidable1, collidable2)
                   ):
                        collidable1.on_collision(collidable2)
                        collidable2.on_collision(collidable1)
                        if collidable1.get_isAlive() == False:
                            self.collidables.remove(collidable1)
                            # print(collidable1.__class__.__name__)

                        if collidable2.get_isAlive() == False:
                            self.collidables.remove(collidable2)
                            # print(collidable2.__class__.__name__)
