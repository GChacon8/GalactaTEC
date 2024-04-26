import tkinter as tk
from tkinter import PhotoImage

class howtoplay:
    def __init__(self, window, animated_gif, key):
        self.key = key
        self.key1 = 0 #llaves de las cuentas que iniciaron sesion (para el goBack)
        self.key2 = 0
        self.window = window
        self.animated_gif = animated_gif
        self.filename = None
        self.music_file = None

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")


        self.etiqueta = tk.Label(self.window, text="!How To Play!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.1, anchor="center")
        self.show()

    def show(self):
        #start_x = 0.5 - (3 * 165 / 2) / self.SCREEN_WIDTH

        #Movement
        labelmove = tk.Label(self.window, text="Movement", font=("Fixedsys", 18), bg="#120043", fg="white")
        labelmove.place(relx=0.5, rely=0.2, anchor="center")
        # Arrows
        image_path = "Images/keyboardArrowsNB.png"
        image = PhotoImage(file=image_path)
        resized_image = image.subsample(4) 
        label_image = tk.Label(self.window, image=resized_image, bg="#120043")
        label_image.image = resized_image
        label_image.place(relx=0.5, rely=0.35, anchor="center")

        #Shoot
        labelshoot = tk.Label(self.window, text="Shooting", font=("Fixedsys", 18), bg="#120043", fg="white")
        labelshoot.place(relx=0.5, rely=0.5, anchor="center")
        # Spacebar Image
        image_path = "Images/spacebarNB.png"
        image = PhotoImage(file=image_path)
        resized_image = image.subsample(5) 
        label_image2 = tk.Label(self.window, image=resized_image, bg="#120043")
        label_image2.image = resized_image
        label_image2.place(relx=0.5, rely=0.6, anchor="center")

        #Select Powerup
        labelshoot = tk.Label(self.window, text="Select PowerUp", font=("Fixedsys", 18), bg="#120043", fg="white")
        labelshoot.place(relx=0.3, rely=0.7, anchor="center")
        #M Image
        image_path = "Images/MLetterNB.png"
        image = PhotoImage(file=image_path)
        resized_image = image.subsample(4) 
        label_image3 = tk.Label(self.window, image=resized_image, bg="#120043")
        label_image3.image = resized_image
        label_image3.place(relx=0.3, rely=0.8, anchor="center")


         #Select Powerup
        labelshoot = tk.Label(self.window, text="Activate PowerUp", font=("Fixedsys", 18), bg="#120043", fg="white")
        labelshoot.place(relx=0.7, rely=0.7, anchor="center")
        #P Image
        image_path = "Images/PLetterNB.png"
        image = PhotoImage(file=image_path)
        resized_image = image.subsample(4) 
        label_image4 = tk.Label(self.window, image=resized_image, bg="#120043")
        label_image4.image = resized_image
        label_image4.place(relx=0.7, rely=0.8, anchor="center")

        btnBack = tk.Button(self.window, text=" Go Back ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.goBack)
        btnBack.place(relx=0.5, rely=0.9, anchor="center") 


    def clear_win(self):
        for widget in self.window.winfo_children():
            if widget != self.animated_gif:
                widget.destroy()


    def goBack(self):
        self.clear_win()
        import menu
        if(self.key2 == 0): #juego individual
            win = menu.init_menu(self.window, self.animated_gif, self.key)
            win.showMenu()
        else: #multijugador
            win = menu.init_menu(self.window, self.animated_gif, self.key1)
            win.multiplayer(self.key1, self.key2)
            win.showMenu()






"""
window = tk.Tk()
howtoplay(window, None, None)
window.mainloop()
#"""