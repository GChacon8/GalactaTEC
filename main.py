import login
import tkinter as tk
import AnimatedGIF
from tkinter import messagebox
import ceremony

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

        #win = login.login(self.window, self.animated_gif)
        #win.showLogin()

        win = ceremony.ceremony(self.window, self.animated_gif, 2, 3)


def show_error_message(error):
    messagebox.showerror("Error", f"Ocurrió un error: {str(error)}")
if __name__ == "__main__":
    try:  
        win = main()
    except Exception as e:
        show_error_message(e)