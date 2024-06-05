import enum
import pygame
import tkinter as tk
from tkinter import messagebox
import itertools
import os
import sys
import random
import menu
import login
import json
import AnimatedGIF
import ceremony

from Enemy_movement import EnemyMovement
from Observer import Collidable, CollisionObserver

class Ship (Collidable):

  WIDTH = 80
  INVISIBLE_TIME = 4 # 4 segundos
  DOUBLE_POINTS_TIME = 16 # 16 segundos

  def __init__(self, player, numPlayer):
    super().__init__()
    with open('data.json', 'r') as file:
    # Cargar el JSON desde el archivo
      data = json.load(file)

    user_data = None
    for user in data:
      if user["key"] == player:
         user_data = user
    

    self.image = pygame.image.load(user_data["ship"])
    self.image = pygame.transform.smoothscale(self.image, (Ship.WIDTH, Ship.WIDTH))
    self.rect = self.image.get_rect()
    self.rect.center = (int(game.SCREEN_WIDTH / 2)-int(0.5*Ship.WIDTH), 
                        game.SCREEN_HEIGHT-int(1.0625*Ship.WIDTH)) 
    self.speed = 8

    self.active = True

    self.bonus_colleted = []

    self.bonus_sound = pygame.mixer.Sound("sounds/bonus.wav")
    self.bonus_sound.set_volume(0.5)
    self.hit_sound = pygame.mixer.Sound("sounds/hit.wav") 
    self.hit_sound.set_volume(0.5)
    self.moving_sound = pygame.mixer.Sound("sounds/move.mp3")
    self.moving_sound.set_volume(0.05)
    self.sound_bullet = pygame.mixer.Sound("sounds/bullet.wav")
    self.sound_bullet.set_volume(0.05)

    self.life = 3
    self.points = 0
    self.points_multiplier = 1

    self.invulnerable_time = 0
    self.double_points_time = 0


    # Aviable Bullet Type 
    self.bullet_types = [BulletShipType.SIMPLE]  # Por defecto, solo tiene balas simples

    self.shield: Shield | None = None


  def update(self, keys, h_axis, v_axis):
    if self.invulnerable_time > 0:
      self.invulnerable_time -= 1
    if keys[pygame.K_LEFT] or h_axis<-0.5:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] or h_axis>0.5:
      self.rect.x += self.speed
    if keys[pygame.K_UP] or v_axis<-0.5:
      self.rect.y -= self.speed
    if keys[pygame.K_DOWN] or v_axis>0.5:
      self.rect.y += self.speed
    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, game.SCREEN_WIDTH - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, game.SCREEN_HEIGHT - self.rect.height-50))
  def draw(self, screen: pygame.Surface):
      if self.active:
          if self.invulnerable_time > 0:
              # Hacer la nave semi-transparente durante la invulnerabilidad
              alpha = 32 if self.invulnerable_time % 20 < 10 else 255
              ship_image = self.image.copy()
              ship_image.set_alpha(alpha)
              screen.blit(ship_image, self.rect)
          else:
              screen.blit(self.image, self.rect)
  def on_collision(self, other: Collidable):
    if isinstance(other, Bonus):
        self.bonus_colleted.append(other)
        self.bonus_sound.play()
    elif isinstance(other, Enemy):
        if self.invulnerable_time == 0:  # Solo resta vida si no está invulnerable
            self.hit_sound.play()
            hit = 1
            if self.shield is not None:
               self.shield.hits -= hit
               if self.shield.hits <= 0:
                   self.shield.kill()
                   self.shield = None
            else:
              self.life -= hit
              game.CHANGE_PLAYER = True
            self.invulnerable_time = Ship.INVISIBLE_TIME * game.FRAME_RATE  # 4 segundos de invulnerabilidad
            game.VIBRATION = True
            game.POINTS_TO_ADD += 200
    elif isinstance(other, BulletEnemy):
      if self.invulnerable_time == 0:  # Solo resta vida si no está invulnerable
        self.hit_sound.play()
        hit = 1 if other.type == BulletEnemyType.SIMPLE else 2
        if self.shield is not None:
            self.shield.hits -= hit
            if self.shield.hits <= 0:
                self.shield.kill()
                self.shield = None
        else:
          self.life -= hit
          game.CHANGE_PLAYER = True
        self.invulnerable_time = Ship.INVISIBLE_TIME * game.FRAME_RATE  # 4 segundos de invulnerabilidad
        game.VIBRATION = True

            
  def get_life(self):
    return self.life
  def add_life(self, life=1):
    self.life += life
  def get_points(self):
    return self.points
  def add_points(self, points=200):
    self.points += points * self.points_multiplier
    if self.points_multiplier != 1:
      self.points_multiplier = 1
  def bonus_colleted(self):
    return self.bonus_colleted
  def desactive(self):
    self.active = False 
  def shoot(self):
    bullet_type = self.bullet_types[0]  # Obtiene el primer tipo de bala de la lista
    bullet = BulletShip(self, bullet_type)
    self.sound_bullet.play()
    return bullet
  
  def set_shield(self, shield):
    self.shield = shield

  def get_shield(self):
    return self.shield

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

class game:
  
  pygame.init()
  pygame.mixer.init()
  SCREEN_WIDTH = pygame.display.Info().current_w
  SCREEN_HEIGHT = pygame.display.Info().current_h
  FRAME_RATE = 60
  BONUS_TIME = 3000
  BONUS_PROBABILITY = 0.5
  PADDING_MENU = 50
  POINTS_TO_ADD = 0
  SHOT_ENEMY_COOLDOWN =  2000  # ms entre disparos
  VIBRATION = False
  CONTROLLER = False
  CHANGE_PLAYER = False

  def __init__(self, key1, key2 = None):
      self.level = 0
      self.patrones = [3,2,1]



      self.width = game.SCREEN_WIDTH
      self.height = game.SCREEN_HEIGHT
      self.screen = pygame.display.set_mode((self.width, self.height))
      self.images = [
            pygame.transform.scale(
                pygame.image.load('background_frames' + os.sep + file_name).convert(), 
                (self.width, self.height)
            ) 
            for file_name in sorted(os.listdir('background_frames'))
        ]
      self.background = AnimatedBackground(position=(0, 0), images=self.images, delay=0.03)
      self.background_sprites = pygame.sprite.Group()
      self.background_sprites.add(self.background)
      self.button_rect = pygame.Rect(self.width-75,self.height-75,25,25) #Posición del boton de ayuda COLOCAR EN LA BARRA DE JUEGO
      pygame.display.set_caption("GalactaTEC")

      self.key1 = key1
      self.key2 = key2
      self.inst_ship = None                             #---------------------
      self.turno = 0  
      self.startingPlayer()         
            
      self.factory = EnemyFactory(self.SCREEN_WIDTH)         #---------------------
      self.enemies = self.factory.create_enemies(6, 6, self.level)            #---------------------
      self.inst_enemies = self.enemies[0]                    #---------------------
      self.inst_enemyMovement = EnemyMovement(self.inst_enemies,self.SCREEN_WIDTH, self.SCREEN_HEIGHT,self.patrones[self.level])#se elige el patron de vuelo
      #---------------------
      
      self.bullets = []
      self.available_bonus_types = list(BonusType)  # Lista de tipos de bonos disponibles
      self.bonus_timer = 0
      self.bonus_interval = game.BONUS_TIME  # 30 segundos

      self.inst_entities = []                           
      self.inst_entities.append(self.inst_ship)         
      self.inst_entities.extend(self.enemies[1])             

      # Observer
      self.collision_observer = CollisionObserver()     
      self.collision_observer.register(self.inst_entities)  

      self.setup_counter = 0  
      self.t = 0              
      self.running = True    
      self.movement = False   
      self.paused = True   
      self.time_text = 0      #-------------------
      

      # Sounds
      volume = 0.10
      self.chose_song(self.level)

      self.sound_bonus_extra_life = pygame.mixer.Sound("sounds/extra_life.wav")
      self.sound_bonus_extra_life.set_volume(volume)

      self.sound_bonus_double_points = pygame.mixer.Sound("sounds/double_points.wav")
      self.sound_bonus_double_points.set_volume(volume)

      self.sound_bonus_shield = pygame.mixer.Sound("sounds/shield.wav")
      self.sound_bonus_shield.set_volume(volume)

      #argumentos para el control
      self.joystick = None
      self.v_axis = 0
      self.h_axis = 0

      #Variables para multijugador
      self.player_1_Status = []
      
      self.player_2_Status = []
           
      


      ## time for shooting enemy's bullets
      self.time_since_last_shot = 0  # ms desde el último disparo
      self.message = ""
      self.endgame = False
      self.setup_player2()



  def run(self):
      puntaje1 = 0
      puntaje2 = 0
      self.joystick_init()
      clock = pygame.time.Clock()
      self.time_text = 0
      while self.running:
          dt = clock.tick(game.FRAME_RATE)
          self.bonus_timer += dt
          self.time_since_last_shot += dt

          if self.paused:  #Juego en Pausa
            self.paused_events()                #Manejar evento de poner o quitar pausa
            self.show_Message()
            pygame.display.flip()  
          elif self.endgame: #FINALIZAR EL JUEGO
             self.paused_events()
             self.show_Message()
             if self.key2 is not None:
                puntaje1  = self.player_1_Status[0].points
                puntaje2 = self.player_2_Status[0].points
             else:
                puntaje1 = self.inst_ship.points
             pygame.quit()
             break
          else: #Jugando Ando
            self.generate_bonus()               #Generar bonos de forma aleatoria
            self.game_events()    
            # Disparos de enemigos
            self.manage_enemy_shooting()              #Manejo de eventos del juego, incluir
            self.background_sprites.update(dt)         #Update del fondo 
            self.screen.blit(self.background.image, self.background.rect)     #Dibujar fondo
            self.background_sprites.draw(self.screen)                                
            self.mover_enemigos()               #Movimiento de enemigos
            keys = pygame.key.get_pressed()
            self.controlconection()             #Conexión con el control
            self.draw_and_update_all_entities(keys, self.h_axis, self.v_axis)
            self.collision_observer.update()    #Actualizar colisiones
            self.vibration_ps4()


            if game.POINTS_TO_ADD > 0:
              self.inst_ship.add_points(game.POINTS_TO_ADD)
              game.POINTS_TO_ADD = 0
            pygame.display.flip()
            self.check_killed()

            self.change_level()
            # MESSAGE DE FINILIZACION DE JUEGO SI LAS VIDAS =0 O SI ES TERMINO EL ULTIMO NIVEL
            self.is_time_to_change()
            # IF TERMINO:
            #   PREMIACION = INITACION DE PREMACION()
      if self.key2 is not None:
        print("PUNTUACION 1: ",puntaje1," PUNTUACION 2: ",puntaje2)
        winnner = "GANO: "
        if puntaje1 > puntaje2:
           winnner = "El JUEGADOR 1"
        elif puntaje1 == puntaje2:
           winnner = "NADIE POR EMPATE"
        else:
           winnner = "El JUEGADOR 2"
        messagebox.showinfo("QUIEN GANO?", f"{winnner}. Felicidades!!")

      else:
        messagebox.showinfo("FIN DEL JUEGO", f"El jugador 1 ha terminado el juego")
      self.updateJson(puntaje1, puntaje2)
     
     
      window = tk.Tk()
      window.title("GalactaTEC")
      window.configure(bg="#120043")
      window.geometry("800x600")

      #Configuracion del fondo 
      gif_path = "Images/space_background.gif"
      self.animated_gif = AnimatedGIF.AnimatedGIF(window, gif_path)
      self.animated_gif.place(x=0, y=0, relwidth=1, relheight=1)
      win = ceremony.ceremony(window, self.animated_gif, self.key1, self.key2)

      # LLAMAR CORACION
  # Actualizacion de los puntos en la base de datos
  def updateJson(self, puntaje1, puntaje2):
    with open("data.json") as json_file:
            data = json.load(json_file)
            
    for usuario in data:
      if usuario["key"] == self.key1:
         totalScore = str(int(usuario["highscore"]) + puntaje1)
         user1 = {'lastScore': puntaje1,
                  'highscore': totalScore}
         usuario.update(user1)
      elif usuario["key"] == self.key2:
         totalScore = str(int(usuario["highscore"]) + puntaje2)
         user2 = {'lastScore': puntaje2,
                  'highscore': totalScore}
         usuario.update(user2)
     
    with open("data.json", "w") as json_file:
      json.dump(data, json_file, indent=4)
  
  def setup_player2(self):
      #No solo cambiar qué nave se utiliza, sino también la música y todas esas cosas
      try:
          if self.turno == 2:
            temp_level = 0
            # Creación de una instancia de Ship y EnemyFactory
            temp_inst_ship = Ship(self.key1, 1)             #INDICE 0
            temp_factory = EnemyFactory(self.SCREEN_WIDTH)  #INDICE 1
            temp_enemies = temp_factory.create_enemies(6, 6, temp_level)  #INDICE 2
            temp_inst_enemies = temp_enemies[0]             #INDICE 3
            temp_inst_enemyMovement = EnemyMovement(temp_inst_enemies, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.patrones[temp_level])  # INDICE 4
            temp_inst_entities = []                         #INDICE 5
            temp_inst_entities.append(temp_inst_ship)
            temp_inst_entities.extend(temp_enemies[1])
            temp_collision_observer = CollisionObserver()             #INDICE 6
            temp_collision_observer.register(temp_inst_entities)       #INDICE 7
            temp_setup_counter = 0                          #INDICE 8
            temp_t = 0                                      #INDICE 9
            temp_movement = False                           #INDICE 10

            # Lista de status del jugador
            self.player_1_Status = [
                temp_inst_ship,         # INDICE 0
                temp_factory,           # INDICE 1
                temp_enemies,           # INDICE 2
                temp_inst_enemies,      # INDICE 3
                temp_inst_enemyMovement,# INDICE 4
                temp_inst_entities,     # INDICE 5
                temp_collision_observer,# INDICE 6
                temp_setup_counter,     # INDICE 7
                temp_t,                 # INDICE 8
                temp_movement,           # INDICE 9
                temp_level              # INDICE 10
            ]

            print("setup del jugador1 porque el jugador 2 empieza")
          elif self.turno == 1:
            temp_level = 0
            temp_inst_ship = Ship(self.key2, 2)             #INDICE 0
            temp_factory = EnemyFactory(self.SCREEN_WIDTH)  #INDICE 1
            temp_enemies = temp_factory.create_enemies(6, 6, temp_level)  #INDICE 2
            temp_inst_enemies = temp_enemies[0]             #INDICE 3
            temp_inst_enemyMovement = EnemyMovement(temp_inst_enemies, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.patrones[temp_level])  # INDICE 4
            temp_inst_entities = []                         #INDICE 5
            temp_inst_entities.append(temp_inst_ship)
            temp_inst_entities.extend(temp_enemies[1])
            temp_collision_observer = CollisionObserver()             #INDICE 6
            temp_collision_observer.register(temp_inst_entities)       #INDICE 7
            temp_setup_counter = 0                          #INDICE 8
            temp_t = 0                                      #INDICE 9
            temp_movement = False                           #INDICE 10


            # Lista de status del jugador
            self.player_2_Status = [
                temp_inst_ship,         # INDICE 0
                temp_factory,           # INDICE 1
                temp_enemies,           # INDICE 2
                temp_inst_enemies,      # INDICE 3
                temp_inst_enemyMovement,# INDICE 4
                temp_inst_entities,     # INDICE 5
                temp_collision_observer,# INDICE 6
                temp_setup_counter,     # INDICE 7
                temp_t,                 # INDICE 8
                temp_movement,           # INDICE 9
                temp_level              # INDICE 10
            ]
            print("setup del jugador2 porque el jugador 1 empieza")
          print("SETUP LISTO-------------------------->")
          self.message = "Inicia el jugador " +str(self.turno) + " Presione la pantalla para continuar"
      except Exception as e:
          print(e)
          exit()
  
  #Manejo del cambio de jugador        HAY ERROR EN CAMBIAR AL PATRÓN DE MOVIMIENTO Y COLISIONES, probar reiniciar los objetos y hacer el append y eso
  def change_player(self):
      if self.turno == 1:
        # Actualizar la información del juego actual para el jugador 1
        self.player_1_Status = [
            self.inst_ship,           # INDICE 0
            self.factory,             # INDICE 1
            self.enemies,             # INDICE 2
            self.inst_enemies,        # INDICE 3
            self.inst_enemyMovement,  # INDICE 4
            self.inst_entities,       # INDICE 5
            self.collision_observer,  # INDICE 6
            self.setup_counter,       # INDICE 7
            self.t,                   # INDICE 8
            self.movement,             # INDICE 9
            self.level                # INDICE 10
        ]
        
        # Cambiar de turno
        if self.player_2_Status[0].life >0 and self.player_2_Status[10] < 3: 
          self.turno = 2
          # Actualizar instancias con la información del jugador 2
          self.inst_ship = self.player_2_Status[0]
          self.factory = self.player_2_Status[1]
          self.enemies = self.player_2_Status[2]
          self.inst_enemies = self.player_2_Status[3]
          self.inst_enemyMovement = self.player_2_Status[4]
          self.inst_entities = self.player_2_Status[5]
          self.collision_observer = self.player_2_Status[6]
          self.setup_counter = self.player_2_Status[7]
          self.t = self.player_2_Status[8]
          self.movement = self.player_2_Status[9]
          self.level = self.player_2_Status[10]


          # Acutaliza la musica
          self.chose_song(self.level)

      elif self.turno == 2:
        # Actualizar la información del juego actual para el jugador 2
        self.player_2_Status = [
            self.inst_ship,           # INDICE 0
            self.factory,             # INDICE 1
            self.enemies,             # INDICE 2
            self.inst_enemies,        # INDICE 3
            self.inst_enemyMovement,  # INDICE 4
            self.inst_entities,       # INDICE 5
            self.collision_observer,  # INDICE 6
            self.setup_counter,       # INDICE 7
            self.t,                   # INDICE 8
            self.movement,             # INDICE 9
            self.level
        ]
        
        if self.player_1_Status[0].life >0 and self.player_1_Status[10] < 3:
        # Cambiar de turno
          self.turno = 1
          # Actualizar instancias con la información del jugador 1
          self.inst_ship = self.player_1_Status[0]
          self.factory = self.player_1_Status[1]
          self.enemies = self.player_1_Status[2]
          self.inst_enemies = self.player_1_Status[3]
          self.inst_enemyMovement = self.player_1_Status[4]
          self.inst_entities = self.player_1_Status[5]
          self.collision_observer = self.player_1_Status[6]
          self.setup_counter = self.player_1_Status[7]
          self.t = self.player_1_Status[8]
          self.movement = self.player_1_Status[9]
          self.level = self.player_1_Status[10]


          # Acutaliza la musica
          self.chose_song(self.level)
    
      elif self.turno == 0:
        return 0  # Caso cuando hay un solo jugador, y prevenir cambios
      

      if self.player_1_Status[0].life <= 0 or self.player_2_Status[0].life <= 0:
        dato = 2 if self.turno == 1 else 1
        self.message = (
                        "El jugador " + str (dato) + 
                        " ha perdido.  Turno del jugador " + 
                        str(self.turno) + 
                        "Presione la pantalla para continuar"
                        )
      else:
        self.message = "Es el turno del jugador " +str(self.turno) + " Presione la pantalla para continuar"

      # listo
      if self.player_1_Status[0].life <= 0 and self.player_2_Status[0].life <= 0:
         self.message = "FIN DEL JUEGO NADIE TIENE VIDAS"
         self.endgame = True
      # listo
      elif self.player_1_Status[10] >= 3 and self.player_2_Status[10] >= 3:
         self.message = "FIN DEL JUEGO  LOS 2 JUGADORES SE ACABARON LOS NIVELES"
         self.endgame = True
      # listo
      elif self.player_1_Status[0].life <= 0 and self.player_2_Status[10] >= 3:
         self.message = "FIN DEL JUEGO EL JUGADOR 1 NO TIENE VIDAS y JUGADOR 2 ACABO LOS NIVELES"
         self.endgame = True
      # listo
      elif self.player_2_Status[0].life <= 0 and self.player_1_Status[10] >= 3:
         self.message = "FIN DEL JUEGO EL JUGADOR 2 NO TIENE VIDAS y JUGADOR 1 ACABO LOS NIVELES"
         self.endgame = True
      
      
  #Setup de los joysticks
  def joystick_init(self):
     # Inicializa los joysticks
    pygame.joystick.init()
    # Verifica cuántos joysticks están conectados
    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
      game.CONTROLLER = True
      self.joystick = pygame.joystick.Joystick(0)
      self.joystick.init()
      #print(f"Joystick name: {self.joystick.get_name()}")
  #Permitir quitar por medio del botón
  def paused_events(self):
    
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        self.paused = False
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):        #Revisión de presionar el boton rojo
          self.paused = False
      elif event.type == pygame.JOYBUTTONDOWN:
        if event.button == 6:
          self.paused = False
  #Revisar los eventos del juego
  def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.change_bonus()
                elif event.key == pygame.K_p:
                    self.use_bonus()
                elif event.key == pygame.K_SPACE:
                    bullet = self.inst_ship.shoot()
                    if bullet:
                        self.inst_entities.append(bullet)
                        self.collision_observer.register([bullet])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.button_rect.collidepoint(mouse_pos):
                    #self.paused = True
                    self.change_player()
                    
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 3:
                    self.change_bonus()
                elif event.button == 1:
                    self.use_bonus()
                elif event.button == 6:
                  self.paused = True
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 5 and event.value == 1.0:
                    bullet = self.inst_ship.shoot()
                    if bullet:
                        self.inst_entities.append(bullet)
                        self.collision_observer.register([bullet])
  #seleccionar que jugador comienza el juego
  def startingPlayer(self):
    if self.key2 == None:                           #Un jugador
      self.inst_ship = Ship(self.key1, 1)
    else:                                           #Dos Jugadores
      ran = random.randint(1,2)
      if ran ==1:
        self.inst_ship = Ship(self.key1, 1)
        self.turno = 1
        self.player_1_Status = [self.inst_ship]
      else:
        self.inst_ship = Ship(self.key2, 2)
        self.turno = 2
        self.player_2_Status = [self.inst_ship]
    print("Turno INICIAL ES: ", self.turno)
  #Intentar la conexion con el control
  def controlconection(self):
    try:
      self.v_axis = self.joystick.get_axis(1)
      self.h_axis = self.joystick.get_axis(0)
    except:
      self.v_axis = 0
      self.h_axis = 0
  #Mover a los enemigos
  def mover_enemigos(self): 
    if self.t >= 60:
      #Para bajar las naves hacia la pantalla de inicio  
      if self.setup_counter<6:
        for i in self.inst_enemies:
          for j in i:
            j.move_down(40)
      else:
        self.movement = True
      self.setup_counter+=1
      self.t=0
    else:
      self.t+=1 #para colocar las naves inicialmente poner en +=1            ------------------------------------------------------
    if self.movement:      
      self.inst_enemyMovement.do_movement()
  #Creación del bonus aleatorio
  def generate_bonus(self):
    if self.bonus_timer >= self.bonus_interval:
      self.bonus_timer = 0
      self.generate_bonus_aux()
  def generate_bonus_aux(self):
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
  #Cambiar el bonus por seleccionar
  def change_bonus(self):
      active_bonuses = self.inst_ship.bonus_colleted
      if active_bonuses:
          active_bonuses.append(active_bonuses.pop(0))
  #Usar bonus seleccionado
  def use_bonus(self):
      active_bonuses = self.inst_ship.bonus_colleted
      if active_bonuses:
          selected_bonus = active_bonuses[0]
          if selected_bonus.type == BonusType.EXTRA_LIFE:
              self.inst_ship.add_life()
              self.sound_bonus_extra_life.play()
              active_bonuses.pop(0)
          elif selected_bonus.type == BonusType.SHIELD:
              self.inst_ship.set_shield(
                 Shield(self.inst_ship.rect.centerx, self.inst_ship.rect.centery)
              )
              self.inst_entities.append(self.inst_ship.shield)  # Add shield to entities
              self.sound_bonus_shield.play()
              active_bonuses.pop(0)
          elif selected_bonus.type == BonusType.DOUBLE_POINTS:
             self.inst_ship.points_multiplier = 2
             self.inst_ship.bonus_colleted.pop(0)
          else:
              active_bonuses.pop(0)
  #Dibujar los bonuses
  def draw_colleted_bonuses(self,font,text_color = (0, 255, 255) ):
    active_bonuses = self.inst_ship.bonus_colleted
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
  #Dibujar las vidas
  def draw_lives(self, font, text_color):
    lives_text = f"{self.inst_ship.life}x"
    text_surface = font.render(lives_text, True, text_color)
    text_x = 10
    text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

    new_size = int (Ship.WIDTH * 0.5)
    ship_image = pygame.transform.scale(self.inst_ship.image, (new_size, new_size))
    ship_x = text_x + text_surface.get_width() + 1
    ship_y = text_y - 10

    self.screen.blit(text_surface, (text_x, text_y))
    self.screen.blit(ship_image, (ship_x, ship_y))
  #Dibujar el nivel actual
  def draw_level(self, font, text_color):
    level_text = f"Level: {self.level}"
    text_surface = font.render(level_text, True, text_color)
    text_x =text_x = game.SCREEN_WIDTH - int(game.SCREEN_WIDTH * (1-0.105)) 
    text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2

    self.screen.blit(text_surface, (text_x, text_y))
  #Dibujar el tiempo
  def draw_time(self, font, text_color):
    self.time_text = f"Time: {pygame.time.get_ticks() // 1000}"
    text_surface = font.render(self.time_text, True, text_color)
    text_x = game.SCREEN_WIDTH - int(game.SCREEN_WIDTH * (1-0.25))
    text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2
    self.screen.blit(text_surface, (text_x, text_y))
  #Dibujar los puntos
  def draw_points(self, font, text_color):
    if self.inst_ship.points_multiplier != 1:
      points_text = f"Points: {self.inst_ship.points}\nNext are x({self.inst_ship.points_multiplier})"
      lines = points_text.split('\n')
      text_surfaces = [font.render(line, True, text_color) for line in lines]

      total_height = sum(surface.get_height() for surface in text_surfaces)
      max_width = max(surface.get_width() for surface in text_surfaces)

      text_x = game.SCREEN_WIDTH // 2 - max_width // 2 - Bonus.WIDTH
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - total_height // 2

      for surface in text_surfaces:
        self.screen.blit(surface, (text_x, text_y))
        text_y += surface.get_height()
    else:
      points_text = f"Points: {self.inst_ship.points}"
      text_surface = font.render(points_text, True, text_color)
      text_x = game.SCREEN_WIDTH // 2 - text_surface.get_width() // 2 - Bonus.WIDTH
      text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - text_surface.get_height() // 2
      self.screen.blit(text_surface, (text_x, text_y))
  #Dibujar las balas
  def draw_next_bullet(self, font, text_color):
    next_bullet = self.inst_ship.bullet_types[0].value
    next_bullet_text = f"Next\nbullet:\n{next_bullet}"
    
    lines = next_bullet_text.split('\n')
    text_surfaces = [font.render(line, True, text_color) for line in lines]
    
    total_height = sum(surface.get_height() for surface in text_surfaces)
    max_width = max(surface.get_width() for surface in text_surfaces)
    
    text_x = game.SCREEN_WIDTH // 2 - max_width // 2
    text_x += 3 * Bonus.WIDTH
    text_y = game.SCREEN_HEIGHT - game.PADDING_MENU // 2 - total_height // 2
    
    for surface in text_surfaces:
      self.screen.blit(surface, (text_x, text_y))
      text_y += surface.get_height()
  #Dibujar el menu de juego
  def draw_menu_game(self):
    font_path = "fonts/GenericTechno.otf"
    font_size = 11
    font = pygame.font.Font(font_path, font_size)
    text_color = (255, 255, 255)  # Blanco
    pygame.draw.rect(self.screen, (255, 0, 0), self.button_rect) #Botón de ayuda
    pygame.draw.rect(self.screen, 
                    (128, 128, 128),
                    (0,
                      game.SCREEN_HEIGHT - game.PADDING_MENU, 
                      self.SCREEN_WIDTH, 
                      game.PADDING_MENU
                    )
                    )
    self.draw_colleted_bonuses(font)
    self.draw_lives(font, text_color)
    self.draw_level(font, text_color)
    self.draw_time(font, text_color)
    self.draw_points(font, text_color)
    self.draw_next_bullet(font, text_color)
  #Dibujar y actualizar todas las entidades actuales
  def draw_and_update_all_entities(self, keys, h_axis, v_axis):
    for entity in self.inst_entities:
      if isinstance(entity, Ship):
        entity.update(keys, h_axis, v_axis)
      elif isinstance(entity, Bonus):
        entity.update()
      elif isinstance(entity, Shield):
        entity.update(self.inst_ship.rect.centerx, self.inst_ship.rect.centery)
      elif isinstance(entity, BulletShip):
        entity.update()
      elif isinstance(entity, BulletEnemy):
         entity.update()
      entity.draw(self.screen)
    self.draw_menu_game()
  #Revisar colisiones
  def check_killed(self):
      # Copia para evitar modificar la lista mientras iteras
      entities_to_check = self.inst_entities.copy()
      for entity in entities_to_check:
          if not entity.get_isAlive():
              self.inst_entities.remove(entity)
              if isinstance(entity, Enemy):
                  # Elimina el enemigo de cada lista dentro de la matriz
                  for sublist in self.inst_enemies:
                      if entity in sublist:
                          sublist.remove(entity)
  #Dibujar texto multilinea
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
  #Salir
  def quit(self):
      self.running = False
      print("Thanks for playing!")
  #Manejo de los disparos de los enemigos
  def manage_enemy_shooting(self):
    if self.time_since_last_shot >= game.SHOT_ENEMY_COOLDOWN:
        available_enemies = [(i, j) for i, row in enumerate(self.inst_enemies) 
                             for j, enemy in enumerate(row) 
                             if not enemy.has_shot and enemy.get_isAlive()]
    
        if len(available_enemies) == 0:
          for row in self.inst_enemies:
                    for enemy in row:
                        enemy.has_shot = False
          # print("Reset disparos")
        # print(f"Enemigos disponibles: {len(available_enemies)}")
        if available_enemies:
            i, j = random.choice(available_enemies)
            enemy = self.inst_enemies[i][j]
            self.fire_enemy(enemy)
            # print("Disparando enemigo")
        self.time_since_last_shot = 0
  #Disparo del enemigo
  def fire_enemy(self, enemy):
      bullet_type = BulletEnemyType.CHARGED if (not enemy.charged_shot_used 
                          and random.random() < 0.1) else BulletEnemyType.SIMPLE
      bullet = BulletEnemy(enemy.rect.center, bullet_type, self.level)
      self.inst_entities.append(bullet)
      self.collision_observer.register([bullet])
      enemy.has_shot = True
      if bullet_type == BulletEnemyType.CHARGED:
          enemy.charged_shot_used = True
  #Vibración del control
  def vibration_ps4(self):
    if game.VIBRATION and game.CONTROLLER:
      self.joystick.rumble(1,1,1000)
      game.VIBRATION = False
  #Detectar cuando hay que realizar el cambio de jugador
  def is_time_to_change(self):
    if game.CHANGE_PLAYER and self.key2 is not None:
      game.CHANGE_PLAYER = False
      self.change_player()
      self.paused = True
    else:
      if self.key2 is None:
        if self.inst_ship.life <= 0:
          self.message = "FIN DEL JUEGO EL JUGADOR NO TIENE VIDAS"
          self.endgame = True
        elif self.level >= 3:
           self.message = "FIN DEL JUEGO SE ACABARON LOS NIVELES"
           self.endgame = True
      elif self.key2 is not None and self.level >= 3:
         game.CHANGE_PLAYER = True
         
  #Mensaje "Presione para continuar" y que cambie el jugador
  def show_Message(self):
    self.background_sprites.draw(self.screen)     
    self.inst_ship.draw(self.screen)
    self.draw_menu_game()
    font = pygame.font.Font("fonts/GenericTechno.otf", 12)
    text_surface = font.render(self.message, True, (255, 255, 255))
    text_x = (game.SCREEN_WIDTH - text_surface.get_rect().width) / 2
    text_y = (game.SCREEN_HEIGHT - text_surface.get_rect().height) / 2
    self.screen.blit(text_surface, (text_x, text_y))

    #print("JUGADOR 1: ",self.player_1_Status[0].life)
    #print("JUGADOR 2: ",self.player_2_Status[0].life)



  def chose_song(self, level):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    pygame.mixer.music.load(
        "Songs/music_" + str(level) + ".mp3"
    )
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

  def change_level(self):
    exist_enemies = False
    for i in self.inst_entities:
      if isinstance(i, Enemy):
        exist_enemies = True
        break
    if exist_enemies:
      return
    temp_level = self.level
    temp_level += 1
    
    self.level = temp_level if temp_level < 3 else 3
    if self.level < 3:
      self.chose_song(self.level)
      self.factory = EnemyFactory(self.SCREEN_WIDTH)         #---------------------
      self.enemies = self.factory.create_enemies(6, 6, self.level)            #---------------------
      self.inst_enemies = self.enemies[0]                    #---------------------
      self.inst_enemyMovement = EnemyMovement(self.inst_enemies,self.SCREEN_WIDTH, self.SCREEN_HEIGHT,self.patrones[self.level])#se elige el patron de vuelo
      #---------------------
      
      self.bullets = []
      self.available_bonus_types = list(BonusType)  # Lista de tipos de bonos disponibles
      self.bonus_timer = 0
      self.bonus_interval = game.BONUS_TIME  # 30 segundos

      self.inst_ship.shield = None          
      self.inst_ship.bonus_colleted = []   
      self.inst_entities = []                           
      self.inst_entities.append(self.inst_ship)         
      self.inst_entities.extend(self.enemies[1])

      # Observer
      self.collision_observer = CollisionObserver()     
      self.collision_observer.register(self.inst_entities)  

      self.setup_counter = 0 
      self.t = 0
      self.movement = False 





### BONUS
class BonusType(enum.Enum):
  # CHASING_BULLET = "Chasing Bullet"
  # EXPANDING_BULLET = "Expanding Bullet"
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


### SHIELD
class Shield(Collidable):
    PIXELS_FRONT_OF_SHIP = 40
    def __init__(self, x, y, hits=3):
        super().__init__()
        self.image = pygame.image.load("Images/shield_3.png")  # Asegúrate de tener la imagen del escudo en la carpeta Images
        self.image = pygame.transform.scale(self.image, 
                                            (Ship.WIDTH, int(Ship.WIDTH)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y - Shield.PIXELS_FRONT_OF_SHIP)  # Ajusta la posición vertical del escudo según sea necesario
        self.hits = hits
        self.font = pygame.font.Font("fonts/GenericTechno.otf", 14) 
        self.active = True

    def update(self, x, y):
        self.rect.center = (x, y - Shield.PIXELS_FRONT_OF_SHIP)  # Actualiza la posición del escudo según la posición de la nave

    def draw(self, screen):
      if self.active and self.hits > 0:
        self.image = pygame.image.load("Images/shield_" + str(self.hits) + ".png") 
        self.image = pygame.transform.scale(self.image, 
                                            (Ship.WIDTH, int( 0.25 * (self.hits) * Ship.WIDTH)))
        screen.blit(self.image, self.rect)
        level_text = str(self.hits)
        text_surface = self.font.render(level_text, True, (255,0,255))  # Color del texto en blanco
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def on_collision(self, other):
        print("Colisionando con:", other)


## BulletShip

class BulletShipType(enum.Enum):
    SIMPLE = "Simple"

class BulletShip(Collidable):
  WIDTH = 20

  def __init__(self, ship, bullet_type=BulletShipType.SIMPLE):
    super().__init__()

    self.image = pygame.image.load("Images/simple_bullet.png")
    self.image = pygame.transform.scale(self.image, (BulletShip.WIDTH, BulletShip.WIDTH))  # Ajusta el tamaño de la bala
    self.rect = self.image.get_rect()
    self.rect.center = ship.rect.center
    self.rect.y -= BulletShip.WIDTH*4
    self.bullet_type = bullet_type
    self.active = True

  def update(self):
    self.rect.y -= 5

    if self.rect.y < 0 or self.rect.x > game.SCREEN_WIDTH or self.rect.x < 0:
      self.kill()



  def draw(self, screen):
    if self.active:
      screen.blit(self.image, self.rect)

  def on_collision(self, other):
    if isinstance(other, Enemy):
        self.kill()
        game.POINTS_TO_ADD += 200

















############ Clase Enemy ##############

class Enemy(Collidable):

  sound_enemy = pygame.mixer.Sound("sounds/enemy_death.wav")
  sound_enemy.set_volume(0.5)

  def __init__(self,posx,posy, level):
    super().__init__()
    self.image = pygame.image.load("Images/enemy_" + str(level) + ".png")
    self.image = pygame.transform.smoothscale(self.image, (40, 40))
    self.rect = self.image.get_rect()
    self.rect.x = posx
    self.rect.y = posy

    #self.startx = posx
    #self.starty = posy
    self.pos = posx

    self.active = True  #Para saber si está vivo o no
    self.has_shot = False
    self.charged_shot_used = False

  
  #No la he usado aún, pero sirve para "teletransportarse"
  def move(self, x, y):
    self.rect.x = x
    self.rect.y = y

    # Limitar la nave dentro de los límites de la pantalla
    self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

  def move_rigth(self,num):
     self.rect.x += num
  
  def move_left(self,num):
     self.rect.x -= num

  def move_down(self, num):
    self.rect.y += num
    #print(max(0, min(self.rect.x, 800 - self.rect.width)))

  def move_up(self,num):
     self.rect.y -= num

  def draw(self, screen: pygame.Surface):
    if self.active:
      screen.blit(self.image, self.rect)
    else:
      pass

  def get_x_coords(self):
    return self.rect.x

  def get_y_coords(self):
    return self.rect.y

  def on_collision(self, other: Collidable):
    # print("Enemy collided with:", other)
    if isinstance(other, BulletShip):
      self.kill()
      Enemy.sound_enemy.play()
    elif isinstance(other, Ship):
       self.kill()

  
  def is_alive(self):
    return self.active




############ Clase Factory ############
class EnemyFactory:
    def __init__(self, screenWidth):
        self.screenWidth = screenWidth
        self.startx = screenWidth
        self.starty = -240

    def create_enemies(self,row:int,col:int, level) -> tuple[list[list[Enemy]],list[Enemy]]:
        enemies=[]
        enemies_aux=[]
        enemies_list:list[Enemy]=[]

        for i in range(row):
            self.startx = (self.screenWidth - (col * 90 - 45)) // 2
            for j in range(col):
                enemies_aux.append(Enemy(self.startx, self.starty, level))
                self.startx+=90

            enemies.append(enemies_aux)
            enemies_list.extend(enemies_aux)
            enemies_aux=[]
            col-=1
            self.startx=0
            self.starty+=40
        return (enemies,enemies_list)



############ Clase BulletEnemy ############

class BulletEnemyType(enum.Enum):
   SIMPLE = "Simple Enemy Bullet"
   CHARGED = "Charged Enemy Bullet"

class BulletEnemy(Collidable):

  WIDTH = 20
   
  def __init__(self, center, type, level):
    super().__init__()

    self.type = type
    self.image = pygame.image.load( "Images/" + 
                                      type.value
                                          .lower()
                                          .replace(" ", "_") +
                                      "_" + str(level) +
                                      ".png"
                                    )
    self.image = pygame.transform.scale(self.image, (BulletEnemy.WIDTH, BulletEnemy.WIDTH))  # Ajusta el tamaño de la bala
    self.rect = self.image.get_rect()

    sound = pygame.mixer.Sound("sounds/" +
                                      type.value
                                          .lower()
                                          .replace(" ", "_") +
                                      "_" + str(level) +
                               ".wav")

    sound.set_volume(0.5)
    sound.play()



    self.rect.center = center
    self.rect.y += BulletEnemy.WIDTH
    self.active = True

  def update(self):
    self.rect.y += 4

    if (self.rect.y > game.SCREEN_HEIGHT-game.PADDING_MENU or 
        self.rect.x > game.SCREEN_WIDTH or self.rect.x < 0):
      self.kill()



  def draw(self, screen):
    if self.active:
      screen.blit(self.image, self.rect)

  def on_collision(self, other: Collidable):
    if isinstance(other, Ship):
        if other.invulnerable_time <= 0:
          self.kill()    











