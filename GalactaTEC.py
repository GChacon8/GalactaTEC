import enum
import pygame
import tkinter as tk
import itertools
import os
import random
import menu
import login

from Enemy import Enemy
from Factory import EnemyFactory
from Enemy_movement import EnemyMovement
from Observer import Collidable, CollisionObserver


class galacta:
  def __init__(self):
    #inst_init_menu = init_menu()
    inst_game = game()
    inst_game.run()

class Bullet (Collidable):
  WIDTH = 10

  def __init__(self, ship):
    super().__init__()
    self.image = pygame.image.load("Images/bullet.png")
    self.image = pygame.transform.smoothscale(self.image, (Bullet.WIDTH, Bullet.WIDTH))
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

  WIDTH = 80

  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("Images/spaceship.png")
    self.image = pygame.transform.smoothscale(self.image, (Ship.WIDTH, Ship.WIDTH))
    self.rect = self.image.get_rect()
    self.rect.center = (int(game.SCREEN_WIDTH / 2)-int(0.5*Ship.WIDTH), 
                        game.SCREEN_HEIGHT-int(1.0625*Ship.WIDTH)) 
    self.speed = 7

    self.active = True

    self.bonus_colleted = []

    self.bonus_sound = pygame.mixer.Sound("sounds/bonus.wav")
    self.hit_sound = pygame.mixer.Sound("sounds/hit.wav") 
    self.hit_sound.set_volume(0.5)

    self.life = 5
    self.points = 0

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
    self.rect.x = max(0, min(self.rect.x, game.SCREEN_WIDTH - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, game.SCREEN_HEIGHT - self.rect.height-50)) 

  def draw(self, screen: pygame.Surface):
    if self.active:
      screen.blit(self.image, self.rect)

  def on_collision(self, other: Collidable):
    # print("Spaceship collided with:", other)
    if isinstance(other, Bonus):
      self.bonus_colleted.append(other)
      self.bonus_sound.play()
    elif isinstance(other, Enemy):
      self.life -= 1
      self.hit_sound.play()


  def bonus_colleted(self):
    return self.bonus_colleted

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
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FRAME_RATE = 60
    BONUS_TIME = 3000
    BONUS_PROBABILITY = 0.5
    PADDING_MENU = 50

    def __init__(self):
        pygame.init()
        self.width = game.SCREEN_WIDTH
        self.height = game.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.images = [pygame.image.load('background_frames' + os.sep + file_name).convert() for file_name in sorted(os.listdir('background_frames'))]
        self.background = AnimatedBackground(position=(0, 0), images=self.images, delay=0.03)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.background)

        pygame.display.set_caption("GalactaTEC")

        self.inst_ship = Ship()
        enemies = EnemyFactory.create_enemies(6, 6)
        self.inst_enemies = enemies[0]
        self.inst_enemyMovement = EnemyMovement(self.inst_enemies,self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.bullets = []
        self.available_bonus_types = list(BonusType)  # Lista de tipos de bonos disponibles
        self.bonus_timer = 0
        self.bonus_interval = game.BONUS_TIME  # 30 segundos

        self.inst_entities = []
        self.inst_entities.append(self.inst_ship)
        self.inst_entities.extend(enemies[1])

        self.collision_observer = CollisionObserver()
        self.collision_observer.register(self.inst_entities)

        self.setup_counter = 0
        self.t = 0
        self.running = True
        self.movement = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(game.FRAME_RATE)
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
            keys = pygame.key.get_pressed()
            self.draw_and_update_all_entities(keys)

            # Actualizar colisiones
            self.collision_observer.update()

            pygame.display.flip()

            self.check_killed()

    def generate_bonus(self):
        if random.random() < game.BONUS_PROBABILITY:  # 50% chance
            if len(self.available_bonus_types) == 0:
               bonuses = self.inst_ship.bonus_colleted
               for t in list(BonusType):
                   if all(bonus.type!=t for bonus in bonuses):
                       self.available_bonus_types.append(t)
            if len(self.available_bonus_types) == 0:
                return
            bonus_type = random.choice(self.available_bonus_types)
            self.available_bonus_types.remove(bonus_type)  # Remove to avoid repetition
            x_position = random.randint(0, self.width - Bonus.WIDTH)  # Assume bonus width is 40
            new_bonus = Bonus(x_position, 0, bonus_type)
            self.inst_entities.append(new_bonus)
            self.collision_observer.register([new_bonus])

    def change_bonus(self):
        active_bonuses = self.inst_ship.bonus_colleted
        if active_bonuses:
            active_bonuses.append(active_bonuses.pop(0))
            print(f"Changed bonus to: {active_bonuses[-1].type.value}"
                  f" ({active_bonuses[0].type})")
        else:
            print("Empty bonuses list")

    def use_bonus(self):
        active_bonuses = self.inst_ship.bonus_colleted
        if active_bonuses:
            selected_bonus = active_bonuses.pop(0)
            print(f"Using bonus: {selected_bonus.type.value}")
            # Implementar efectos del bonus aquí
        else:
            print("No bonuses available")


    def draw_colleted_bonuses(self):
      active_bonuses = self.inst_ship.bonus_colleted
      font_path = "fonts/GenericTechno.otf"
      font_size = 12
      font = pygame.font.Font(font_path, font_size)
      text_color = (0, 255, 255)  # Azul cian
      
      if active_bonuses:
          for i, bonus in enumerate(active_bonuses):
              original_image = bonus.image
              original_width = original_image.get_width()
              original_height = original_image.get_height()
              s = 0.5
              new_width = int(original_width * s)
              new_height = int(original_height * s)
              
              # Calcular la posición del bonus en el menú
              bonus_x = game.SCREEN_WIDTH - (len(active_bonuses) - i) * (new_width + 10)
              bonus_y = game.SCREEN_HEIGHT - new_height
              
              # Escalar la imagen al 50%
              image = pygame.transform.scale(original_image, (new_width, new_height))
              
              # Resaltar el primer bonus de la lista
              if i == 0:
                  # Dibujar un rectángulo blanco alrededor del primer bonus
                  pygame.draw.rect(self.screen, (255, 255, 255), 
                                    (bonus_x - 2, bonus_y - 2,
                                      new_width + 4, new_height + 4), 2)
              
              # Dibujar el bonus en el menú
              self.screen.blit(image, (bonus_x, bonus_y))
              
              # Obtener el texto del bonus
              bonus_text = str(bonus.type.value)
              
              # Dibujar el texto del bonus debajo de la imagen
              text_surface = font.render(bonus_text, True, text_color)
              text_x = bonus_x + (new_width - text_surface.get_width()) // 2
              text_y = bonus_y + new_height + 5
              self.screen.blit(text_surface, (text_x, text_y))
      else:
          bonus_text = "Empty"
          game.draw_text_multiline(self.screen, bonus_text,
                                    game.SCREEN_WIDTH - 2*Bonus.WIDTH, 
                                    game.SCREEN_HEIGHT - Bonus.WIDTH,
                                    game.SCREEN_WIDTH, font, text_color)

    def draw_lives(self):
      font_path = "fonts/GenericTechno.otf"
      font_size = 16
      font = pygame.font.Font(font_path, font_size)
      text_color = (255, 255, 255)  # Blanco

      lives_text = f"{self.inst_ship.life} x "
      text_surface = font.render(lives_text, True, text_color)
      text_x = 10
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

      ship_image = pygame.transform.scale(self.inst_ship.image, (20, 20))
      ship_x = text_x + text_surface.get_width() + 5
      ship_y = text_y

      self.screen.blit(text_surface, (text_x, text_y))
      self.screen.blit(ship_image, (ship_x, ship_y))

    def draw_time(self):
      font_path = "fonts/GenericTechno.otf"
      font_size = 16
      font = pygame.font.Font(font_path, font_size)
      text_color = (255, 255, 255)  # Blanco

      time_text = f"Time: {pygame.time.get_ticks() // 1000}"
      text_surface = font.render(time_text, True, text_color)
      text_x = 150
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

      self.screen.blit(text_surface, (text_x, text_y))

    def draw_level(self):
      font_path = "fonts/GenericTechno.otf"
      font_size = 16
      font = pygame.font.Font(font_path, font_size)
      text_color = (255, 255, 255)  # Blanco

      level_text = f"Level: {0}"
      text_surface = font.render(level_text, True, text_color)
      text_x = game.SCREEN_WIDTH // 2 - text_surface.get_width() // 2
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

      self.screen.blit(text_surface, (text_x, text_y))

    def draw_points(self):
      font_path = "fonts/GenericTechno.otf"
      font_size = 16
      font = pygame.font.Font(font_path, font_size)
      text_color = (255, 255, 255)  # Blanco

      points_text = f"Points: {self.inst_ship.points}"
      text_surface = font.render(points_text, True, text_color)
      text_x = game.SCREEN_WIDTH - text_surface.get_width() - 10
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

      self.screen.blit(text_surface, (text_x, text_y))
           
    def draw_menu_game(self):
      pygame.draw.rect(self.screen, 
                      (128, 128, 128),
                      (0,
                        game.SCREEN_HEIGHT - game.PADDING_MENU, 
                        self.SCREEN_WIDTH, 
                        game.PADDING_MENU
                      )
                      )
      self.draw_colleted_bonuses()
      self.draw_lives()
      self.draw_time()
      self.draw_level()
      self.draw_points()

    def draw_and_update_all_entities(self, keys):
      for entity in self.inst_entities:
        if isinstance(entity, Ship):
          entity.update(keys)
        elif isinstance(entity, Bonus):
          entity.update()
        entity.draw(self.screen)
      self.draw_menu_game()

    def check_killed(self):
       for entity in self.inst_entities:
          if not entity.get_isAlive():
            self.inst_entities.remove(entity)
            if isinstance(entity, Enemy):
              self.inst_enemies.remove(entity)
            elif isinstance(entity, Ship):
              self.quit()


    def draw_text_multiline(surface, text, x_0, y_0, max_x, font, color):
      words = text.split()
      lines = []
      current_line = ""

      for word in words:
          test_line = current_line + " " + word if current_line else word
          test_text = font.render(test_line, True, color)
          test_width = test_text.get_width()

          if test_width <= max_x - x_0:
              current_line = test_line
          else:
              if current_line:
                  lines.append(current_line)
              current_line = word

      if current_line:
          lines.append(current_line)

      y = y_0
      for line in lines:
          text_surface = font.render(line, True, color)
          surface.blit(text_surface, (x_0, y))
          y += font.get_height()

      def quit(self):
          self.running = False
          print("Thanks for playing!")


### BONUS

class BonusType(enum.Enum):
    CHASING_BULLET = "Chasing Bullet"
    EXPANDING_BULLET = "Expanding Bullet"
    DOUBLE_POINTS = "Double Points"
    SHIELD = "Shield"
    EXTRA_LIFE = "Extra Life"


class Bonus(Collidable):

    WIDTH = 40

    def __init__(self, posx: int, posy: int, bonus_type: BonusType):
        super().__init__()
        self.image = pygame.image.load( "Images/" + 
                                        bonus_type.value
                                            .lower()
                                            .replace(" ", "_") +
                                        ".png"
                                      )
        self.image = pygame.transform.smoothscale(self.image, (Bonus.WIDTH, Bonus.WIDTH))
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.type = bonus_type
        self.active = True

    def update(self):
        # Mover el bonus hacia abajo en la pantalla
        self.rect.y += 5
        if self.rect.y > game.SCREEN_HEIGHT-game.PADDING_MENU:  # Suponiendo que el límite inferior es 600
            self.kill()


    def on_collision(self, other: Collidable):
        if isinstance(other, Ship):
            self.kill()
    
    def draw(self, screen: pygame.Surface):
        if self.active:
            screen.blit(self.image, self.rect)

    def desactive(self):
        self.active = False

if __name__ == "__main__":
  inst_galacta = galacta()

  