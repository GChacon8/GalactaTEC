import pygame
import tkinter as tk
import random
import sys
from PIL import Image, ImageTk

class galacta:
  def __init__(self):
    inst_init_menu = init_menu()
    inst_game = game()

#Clase para el movimiento del fondo de pantalla del menu, imagen tipo gif
class AnimatedGIF(tk.Label):
    def __init__(self, master, path):
        super().__init__(master)
        self._master = master
        self._gif_path = path
        self._gif_frames = []
        self._index = 0
        self._delay = 100
        self._load_frames()
        self._animate()

    def _load_frames(self):
        gif = Image.open(self._gif_path)
        try:
            while True:
                self._gif_frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(self._gif_frames)) # Move to the next frame
        except EOFError:
            pass

    def _animate(self):
        self.config(image=self._gif_frames[self._index])
        self._index = (self._index + 1) % len(self._gif_frames)
        self._master.after(self._delay, self._animate)

class init_menu:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("GalactaTEC")
    self.window.configure(bg="#120043")
    self.window.geometry("800x600")
    
    #Configuracion del fondo 
    gif_path = "Images/space_background.gif"
    animated_gif = AnimatedGIF(self.window, gif_path)
    animated_gif.place(x=0, y=0, relwidth=1, relheight=1) 
    
    #Etiquetas y botones del menu principal
    self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
    self.etiqueta.place(relx=0.5, rely=0.2, anchor="center")  # Centra la etiqueta horizontalmente y la coloca 30% desde la parte superior
    
    self.btnUserSettings = tk.Button(self.window, text="User Settings", font=("Fixedsys", 15))
    self.btnUserSettings.place(relx=0.5, rely=0.3, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 40% desde la parte superior
  
    self.btnGameSettings = tk.Button(self.window, text="Game Settings", font=("Fixedsys", 15))
    self.btnGameSettings.place(relx=0.5, rely=0.4, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 50% desde la parte superior

    self.btnHallofFame = tk.Button(self.window, text="Hall of Fame", font=("Fixedsys", 15), command=self.clear_win)
    self.btnHallofFame.place(relx=0.5, rely=0.5, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 60% desde la parte superior

    self.btnInitP2 = tk.Button(self.window, text="Start Player 2", font=("Fixedsys", 15), command=self.clear_win)
    self.btnInitP2.place(relx=0.5, rely=0.6, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 60% desde la parte superior

    self.btnStartGame = tk.Button(self.window, text="Start Game", font=("Fixedsys", 15), command=self.clear_win)
    self.btnStartGame.place(relx=0.5, rely=0.7, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 60% desde la parte superior

    self.btnExit = tk.Button(self.window, text="Exit", font=("Fixedsys", 15), command=self.clear_win)
    self.btnExit.place(relx=0.5, rely=0.8, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 60% desde la parte superior

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

class Enemy:
  def __init__(self):
    self.image = pygame.image.load("Images/enemy.png")
    self.image = pygame.transform.smoothscale(self.image, (70, 70))
    self.rect = self.image.get_rect()
    self.rect.center = (100, 100)
  
  def update(self):
    self.rect.x += random.randint(-20,20)
    self.rect.y += random.randint(-20,20)

    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
  
  def draw(self, screen):
    screen.blit(self.image, self.rect)

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
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("GalactaTEC")
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))  # Blanco
    inst_ship = Ship()
    inst_enemy = Enemy()
    running = True
    while running:
    # Manejo de eventos
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

    # Obtener estado del teclado
      keys = pygame.key.get_pressed()

    # Actualizar la nave según las teclas presionadas
      inst_ship.update(keys)
      inst_enemy.update()

    # Dibujar todo
      screen.blit(background, (0, 0))  # Dibujar fondo
      inst_ship.draw(screen)  # Dibujar la nave en su nueva posición
      inst_enemy.draw(screen)

    # Actualizar la pantalla
      pygame.display.flip()

    # Pequeña pausa para controlar la velocidad de fotogramas
      pygame.time.Clock().tick(60)

if __name__ == "__main__":
  inst_galacta = galacta()