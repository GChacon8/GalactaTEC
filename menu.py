import tkinter as tk
from PIL import Image, ImageTk

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
