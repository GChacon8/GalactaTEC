import pygame
import tkinter as tk
import itertools
import os
import random
import menu
import login

from Factory import EnemyFactory
from Enemy_movement import EnemyMovement


class galacta:
  def __init__(self):
    #inst_init_menu = init_menu()
    inst_game = game()
    inst_game.run()

class Bullet:
  def __init__(self, ship):
    self.image = pygame.image.load("Images/bullet.png")
    self.image = pygame.transform.smoothscale(self.image, (10, 10))
    self.rect = self.image.get_rect()
    self.rect.center = ship.rect.center

class Ship:
  def __init__(self):
    self.image = pygame.image.load("Images/spaceship.png")
    self.image = pygame.transform.smoothscale(self.image, (80, 80))
    self.rect = self.image.get_rect()
    self.rect.center = (200, 500)
    self.speed = 7

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

  def draw(self, screen):
    screen.blit(self.image, self.rect)


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
    self.all_sprites = pygame.sprite.Group(self.background)



    pygame.display.set_caption("GalactaTEC")
    #self.background = pygame.Surface(self.screen.get_size())
    #self.background.fill((255, 255, 255))  # Blanco

    self.inst_ship = Ship()
    self.inst_enemies = EnemyFactory.create_enemies(6,6)
    self.inst_enemyMovement = EnemyMovement(self.inst_enemies)

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
       



      self.inst_ship.draw(self.screen)  # Dibujar la nave en su nueva posición


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

      #Dibujar los enemigos
      for i in self.inst_enemies:
        for j in i:
          j.draw(self.screen)
              
    # Actualizar la pantalla
      pygame.display.flip()
      

if __name__ == "__main__":
  inst_galacta = galacta()

  