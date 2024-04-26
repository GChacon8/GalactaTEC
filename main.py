import login
import tkinter as tk
import AnimatedGIF


class main:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry("800x600")

        #Configuracion del fondo 
        gif_path = "Images/space_background.gif"
        self.animated_gif = AnimatedGIF.AnimatedGIF(self.window, gif_path)
        self.animated_gif.place(x=0, y=0, relwidth=1, relheight=1)

        win = login.login(self.window, self.animated_gif)
        win.showLogin()
        
>>>>>>> Stashed changes
main()