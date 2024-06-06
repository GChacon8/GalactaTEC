import tkinter as tk
import threading
import AnimatedGIF
import GalactaTEC
from GalactaTEC import game
import pygame

class init_menu:
  PATRONES = [1,2,3]

  def __init__(self, window, animated_gif, key):
    self.key = key 
    self.key1 = key
    self.key2 = 0
    self.window = window
    self.animated_gif = animated_gif

    pygame.mixer.init()
    self.song = "Songs/Planet Caravan 8bit.mp3"

    self.window.title("GalactaTEC")
    self.window.configure(bg="#120043")
    self.window.geometry("800x600")
    
    #Etiquetas y botones del menu principal
    self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
    self.etiqueta.place(relx=0.5, rely=0.1, anchor="center") 

    self.play_music()

  def showMenu(self):
    self.btnUserSettings = tk.Button(self.window, text="User Settings", font=("Fixedsys", 15), command=self.userSettings)
    self.btnUserSettings.place(relx=0.5, rely=0.3, anchor="center", width=230)  
  
    self.btnGameSettings = tk.Button(self.window, text="Game Settings", font=("Fixedsys", 15), command=self.gameSettings)
    self.btnGameSettings.place(relx=0.5, rely=0.4, anchor="center", width=230) 

    self.btnHallofFame = tk.Button(self.window, text="Hall of Fame", font=("Fixedsys", 15), command=self.hallofFame)
    self.btnHallofFame.place(relx=0.5, rely=0.5, anchor="center", width=230)  

    self.btnStartGame = tk.Button(self.window, text="Start Game", font=("Fixedsys", 15), command=lambda: self.initGame(self.key1, self.key2))
    self.btnStartGame.place(relx=0.5, rely=0.6, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 60% desde la parte superior

    self.btnHelp = tk.Button(self.window, text="How To Play", font=("Fixedsys", 15), command=self.howToPlay)

    self.btnExit = tk.Button(self.window, text="Exit", font=("Fixedsys", 15), command=self.clear_win) 

    if self.key2 == 0:
      self.btnInitP2 = tk.Button(self.window, text="Start Player 2", font=("Fixedsys", 15), command=self.initPlayer2)
      self.btnInitP2.place(relx=0.5, rely=0.6, anchor="center", width=230)  
      self.btnStartGame.place(relx=0.5, rely=0.7, anchor="center", width=230) 
      self.btnHelp.place(relx=0.5, rely=0.8, anchor="center", width=230) 
      self.btnExit.place(relx=0.5, rely=0.9, anchor="center", width=230) 

    else:
      self.btnStartGame.place(relx=0.5, rely=0.6, anchor="center", width=230)
      self.btnHelp.place(relx=0.5, rely=0.7, anchor="center", width=230) 
      self.btnExit.place(relx=0.5, rely=0.8, anchor="center", width=230) 

      self.window.mainloop()
      pygame.mixer.quit()

  def initPlayer2(self):
      self.clear_win()
      import login
      login2 = login.login(self.window, self.animated_gif) #llamar a login para el jugador 2
      login2.key = self.key #mantener la llave del jugador principal
      login2.player = "player2"
      login2.showLogin()

  def multiplayer(self, key1, key2):
    self.key2 = key2
    self.key1 = key1
    self.selected_player = tk.StringVar()
    self.player1_radio = tk.Radiobutton(self.window, text="Player 1", variable=self.selected_player, value="player1", font=("Fixedsys", 12), bg="#120043", fg="white")
    self.player1_radio.place(relx=0.4, rely=0.2, anchor="center")

    self.player2_radio = tk.Radiobutton(self.window, text="Player 2", variable=self.selected_player, value="player2", font=("Fixedsys", 12), bg="#120043", fg="white")
    self.player2_radio.place(relx=0.6, rely=0.2, anchor="center")

    def on_select():
        if self.selected_player.get() == "player1":
            print("selected menu for player 1")
            self.key = key1
        elif self.selected_player.get() == "player2":
            print("selected menu for player 2")
            self.key = key2

    # Configura una función que se llamará cuando cambie la selección del jugador
    self.selected_player.trace("w", lambda *args: on_select())

  def userSettings(self):
    import newUser
    self.clear_win()
    config = newUser.newUser(self.window, self.animated_gif, self.key)
    config.key1 = self.key1
    config.key2 = self.key2
    config.showConfig()
     
   
  def hallofFame(self):
    import hallofFame
    self.clear_win()
    hall = hallofFame.hallofFame(self.window, self.animated_gif, self.key)
    hall.key1 = self.key1
    hall.key2 = self.key2
    hall.showHall()


  def gameSettings(self):
      import gameConfiguration
      self.clear_win()
      gameConfiguration.gameConfiguration(self.window, self.animated_gif, self.key)
   
  def howToPlay(self):
      import howToPlay
      self.clear_win()
      howToPlay.howtoplay(self.window, self.animated_gif, self.key)
   
  def clear_win(self):
         for widget in self.window.winfo_children():
            if widget != self.animated_gif:
               widget.destroy()
      
  def gotoProfiles(self):
      self.clear_win()
    
  def initGame(self, key1, key2):
    self.window.destroy()
    if key2 == 0:
      inst_game = game(key1, None, init_menu.PATRONES )
      inst_game.run()
    else:
      inst_game = game(key1, key2, init_menu.PATRONES )
      inst_game.run()

      # Función para reproducir música
  def play_music(self):
    if self.song:
        pygame.mixer.music.load(self.song)  
        pygame.mixer.music.play(-1)  # Reproducir en bucle
    
