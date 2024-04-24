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
        self.background = AnimatedBackground(position=(0, 0), images=self.images, delay=0.03)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.background)

        pygame.display.set_caption("GalactaTEC")

        self.inst_ship = Ship()
        enemies = EnemyFactory.create_enemies(6, 6)
        self.inst_enemies = enemies[0]
        self.inst_enemyMovement = EnemyMovement(self.inst_enemies)
        self.bullets = []
        self.inst_bonuses = []
        self.available_bonus_types = list(BonusType)  # Lista de tipos de bonos disponibles
        self.active_bonuses = []  # Bonos actualmente en pantalla
        self.bonus_timer = 0
        self.bonus_interval = 3000  # 30 segundos

        self.inst_entities = [self.inst_ship] + enemies[1]
        self.collision_observer = CollisionObserver()
        self.collision_observer.register(self.inst_entities)

        self.setup_counter = 0
        self.t = 0
        self.running = True
        self.movement = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60)
            self.bonus_timer += dt

            # Generar bonos de forma aleatoria
            if self.bonus_timer >= self.bonus_interval:
                self.bonus_timer = 0
                self.generate_bonus()

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.change_bonus()
                    elif event.key == pygame.K_p:
                        self.use_bonus()

            keys = pygame.key.get_pressed()
            self.inst_ship.update(keys)
            self.all_sprites.update(dt)

            # Dibujar fondo
            self.screen.blit(self.background.image, self.background.rect)
            self.all_sprites.draw(self.screen)


            # Movimiento de enemigos
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


            # Dibujar todos los elementos y nave
            for entity in self.inst_entities + self.active_bonuses:
                entity.draw(self.screen)

            self.collision_observer.update()

            pygame.display.flip()

    def generate_bonus(self):
        if self.available_bonus_types and random.random() < 0.5:  # 50% chance
            bonus_type = random.choice(self.available_bonus_types)
            self.available_bonus_types.remove(bonus_type)  # Remove to avoid repetition
            x_position = random.randint(0, self.width - Bonus.WIDTH)  # Assume bonus width is 40
            new_bonus = Bonus(x_position, 0, bonus_type)
            self.active_bonuses.append(new_bonus)
            self.inst_entities.append(new_bonus)
            self.collision_observer.register([new_bonus])

    def change_bonus(self):
        if self.active_bonuses:
            self.active_bonuses.append(self.active_bonuses.pop(0))

    def use_bonus(self):
        if self.active_bonuses:
            selected_bonus = self.active_bonuses.pop(0)
            print(f"Using bonus: {selected_bonus.type.value}")
            # Implementar efectos del bonus aquí
if __name__ == "__main__":
  inst_galacta = galacta()

  