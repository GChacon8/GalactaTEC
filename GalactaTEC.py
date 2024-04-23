import pygame
import tkinter as tk
import itertools
import os
import random
import sys
from typing import Sequence


from Bonus import Bonus, BonusType
from Enemy import Enemy
from Entity import Entity
from Factory import EnemyFactory
from Enemy_movement import EnemyMovement
from Observer import Collidable, CollisionObserver


class galacta:
  def __init__(self):
    #inst_init_menu = init_menu()
    inst_game = game()
    inst_game.run()


class init_menu:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("GalactaTEC")
    self.window.configure(bg="#120043")
    self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Courier", 16, "italic"))
    self.etiqueta.pack(padx=20, pady=30)
    self.btnSinglePlayer = tk.Button(self.window, text="Single Player", font=("Courier", 12, "italic"))
    self.btnSinglePlayer.pack(pady=10)
    self.btnMultiPlayer = tk.Button(self.window, text="Multiplayer", font=("Courier", 12, "italic"))
    self.btnMultiPlayer.pack(pady=10)
    self.btnNewProfile = tk.Button(self.window, text="Profiles", font=("Courier", 12, "italic"), command= self.clear_win)
    self.btnNewProfile.pack(pady=10)
    self.window.mainloop()
  
  def clear_win(self):
    for widget in self.window.winfo_children():
        widget.destroy()
    
  def gotoProfiles(self):
    self.clear_win()

class Bullet (Collidable):
  def __init__(self, ship):
    super().__init__()
    self.image = pygame.image.load("Images/bullet.png")
    self.image = pygame.transform.smoothscale(self.image, (10, 10))
    self.rect = self.image.get_rect()
    self.rect.center = ship.rect.center

  def draw(self, screen: pygame.Surface):
    if self.active:
      screen.blit(self.image, self.rect)

  def on_collision(self, other: Collidable):
    print("Bullet collided with:", other)

  def desactive(self):
    self.active = False

class Ship (Collidable):
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("Images/spaceship.png")
    self.image = pygame.transform.smoothscale(self.image, (80, 80))
    self.rect = self.image.get_rect()
    self.rect.center = (200, 500)
    self.speed = 7

    self.active = True

  def update(self, keys):
    if keys[pygame.K_LEFT]:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT]:
      self.rect.x += self.speed
    if keys[pygame.K_UP]:
      self.rect.y -= self.speed
    if keys[pygame.K_DOWN]:
      self.rect.y += self.speed
    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  def draw(self, screen: pygame.Surface):
    if self.active:
      screen.blit(self.image, self.rect)

  def on_collision(self, other: Collidable):
    print("Spaceship collided with:", other)

  def desactive(self):
    self.active = False


class AnimatedBackground(pygame.sprite.Sprite):
    def __init__(self, position, images, delay):
        super(AnimatedBackground, self).__init__()

        self.images = itertools.cycle(images)
        self.image = next(self.images)
        self.rect = pygame.Rect(position,  self.image.get_rect().size)

        self.animation_time = delay
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image = next(self.images)


def load_images(path, target_size):
    images = []
    for file_name in sorted(os.listdir(path)):
        image = pygame.image.load(os.path.join(path, file_name)).convert()
        image = pygame.transform.scale(image, target_size)
        images.append(image)
    return images



class game:
  def __init__(self):
    pygame.init()
    self.width = 800
    self.height = 600
    self.screen = pygame.display.set_mode((self.width, self.height))

    self.images = [pygame.image.load('background_frames' + os.sep + file_name).convert() for file_name in sorted(os.listdir('background_frames'))]
    self.background = AnimatedBackground(position=(0, 0), images=self.images, delay = 0.03)
    self.all_sprites = pygame.sprite.Group()
    self.all_sprites.add(self.background)



    pygame.display.set_caption("GalactaTEC")
    #self.background = pygame.Surface(self.screen.get_size())
    #self.background.fill((255, 255, 255))  # Blanco

    self.inst_ship = Ship()
    enemies = EnemyFactory.create_enemies(6,6)  
    # Save the matrix of enemies
    self.inst_enemies: list[list[Enemy]] = enemies[0]
    self.inst_enemyMovement = EnemyMovement(self.inst_enemies)
    self.bullets: list[Bullet] = []
    self.inst_bonuses: list[Bonus] = []

    # Create List Entities
    self.inst_entities: Sequence[Entity] = [self.inst_ship] + enemies[1]

    # Create the Observer
    self.collision_observer = CollisionObserver()
    # Register the Ship and the enemies
    self.collision_observer.register(self.inst_entities)  

    self.create_bonus()


    self.setup_counter = 0
    self.t=0
    self.running = True
    self.movement = False
  

  def run(self):
    while self.running:

      dt=pygame.time.Clock().tick(60)
      


    # Manejo de eventos
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

    # Obtener estado del teclado
      keys = pygame.key.get_pressed()

    # Actualizar la nave según las teclas presionadas
      self.inst_ship.update(keys)
      self.all_sprites.update(dt)    

    # Dibujar todo
      self.screen.blit(self.background.image, self.background.rect)  # Dibujar fondo
      self.all_sprites.draw(self.screen)
       

      if self.t == 60:
        if self.movement:#elegir acá el patron de movimiento
          self.inst_enemyMovement.pattern_1()
        if self.setup_counter<6:
          for i in self.inst_enemies:
            for j in i:
              j.move_down()
        else:
          self.movement = True

        self.setup_counter+=1
        self.t=0
      else:
        self.t+=2 #cambiar a +=1

      # Draw all entities
      for entity in self.inst_entities:
        entity.draw(self.screen)

      # Check for collisions
      self.collision_observer.update()

    # Actualizar la pantalla
      pygame.display.flip()

  def create_bonus(self):
    self.inst_bonuses = [
                          Bonus(100, 100, BonusType.EXTRA_LIFE),
                          Bonus(200, 200, BonusType.SHIELD)
                        ]

    for bonus in self.inst_bonuses:
      bonus.set_active(True)
      self.collision_observer.register(bonus)
    self.inst_entities.extend(self.inst_bonuses)

if __name__ == "__main__":
  inst_galacta = galacta()

  