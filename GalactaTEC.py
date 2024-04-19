import pygame
import tkinter as tk
import random
import sys

from Factory import EnemyFactory


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


class game:
  def __init__(self):
    pygame.init()
    self.width = 800
    self.height = 600
    self.screen = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("GalactaTEC")
    self.background = pygame.Surface(self.screen.get_size())
    self.background.fill((255, 255, 255))  # Blanco
    self.inst_ship = Ship()
    self.inst_enemies = EnemyFactory.create_enemies(6,6)
    self.setup_counter = 0
    self.t=0
    self.running = True
  

  def run(self):
    
    while self.running:
    # Manejo de eventos
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

    # Obtener estado del teclado
      keys = pygame.key.get_pressed()

    # Actualizar la nave según las teclas presionadas
      self.inst_ship.update(keys)

      
      
  

    # Dibujar todo
      self.screen.blit(self.background, (0, 0))  # Dibujar fondo
      self.inst_ship.draw(self.screen)  # Dibujar la nave en su nueva posición

      #"""
      if self.t==60 and self.setup_counter<6:
        for i in self.inst_enemies:#cambiar para que se dibujen para todos los enemigos
          for j in i:
            j.move_down()
          #i.move(self.test,100) 
          #self.test+=5
          #i.draw(self.screen)
        self.t=0
        self.setup_counter+=1
      self.t+=1
      #"""

      for i in self.inst_enemies:
        for j in i:
          j.draw(self.screen)
              
    # Actualizar la pantalla
      pygame.display.flip()

    # Pequeña pausa para controlar la velocidad de fotogramas
      pygame.time.Clock().tick(60)

if __name__ == "__main__":
  inst_galacta = galacta()

  