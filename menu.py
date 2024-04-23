import tkinter as tk
import AnimatedGIF

class init_menu:
  def __init__(self, window, key):
    self.key = key
    self.window = window
    self.window.title("GalactaTEC")
    self.window.configure(bg="#120043")
    self.window.geometry("800x600")
    
    #Configuracion del fondo 
    gif_path = "Images/space_background.gif"
    animated_gif = AnimatedGIF.AnimatedGIF(self.window, gif_path)
    animated_gif.place(x=0, y=0, relwidth=1, relheight=1) 
    
    #Etiquetas y botones del menu principal
    self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
    self.etiqueta.place(relx=0.5, rely=0.2, anchor="center")  # Centra la etiqueta horizontalmente y la coloca 30% desde la parte superior
    
    self.btnUserSettings = tk.Button(self.window, text="User Settings", font=("Fixedsys", 15), command=self.userSettings)
    self.btnUserSettings.place(relx=0.5, rely=0.3, anchor="center", width=230)  # Centra el botón horizontalmente y lo coloca 40% desde la parte superior
  
    self.btnGameSettings = tk.Button(self.window, text="Game Settings", font=("Fixedsys", 15), command=self.clear_win)
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
  

  def userSettings(self):
     import newUser
     self.clear_win()
     newUser.newUser(self.window, self.key)
  
  def clear_win(self):
    for widget in self.window.winfo_children():
        widget.destroy()
    
  def gotoProfiles(self):
    self.clear_win()
