import tkinter as tk
from tkinter import ttk


class gameConfiguration:
    def __init__(self, window, animated_gif, key):
        self.key = key
        self.window = window
        self.animated_gif = animated_gif
        self.filename = None
        self.music_file = None

        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")


        self.etiqueta = tk.Label(self.window, text="!Game Configuration!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.1, anchor="center")

        self.savedConfig=[]
        self.combobox_patrones = []

        self.show()

    
    def show(self):
        # Botón para retroceder
        btnBack = tk.Button(self.window, text="Save And Close", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.goBack)
        btnBack.place(relx=0.5, rely=0.9, anchor="center")


        #Style of the combobox
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TCombobox', background='#52112f', fieldbackground='#FFFFCC', foreground="black", selectbackground="#FFFFCC", selectforeground="black")
        start_x = 0.5 - (3 * 165 / 2) / self.SCREEN_WIDTH  # Iniciar x desde el centro
        self.combobox_patrones = []
        for i in range(3):
            label = tk.Label(self.window, text="Nivel "+str(i+1), font=("Fixedsys", 18), bg="#120043", fg="white")
            label.place(relx=start_x + i * 250 / self.SCREEN_WIDTH, rely=0.4, anchor="center")

            niveles = ["Pattern 1", "Pattern 2", "Pattern 3", "Pattern 4", "Pattern 5"]
            self.nivel_seleccionado = tk.StringVar(self.window)
            combobox_nivel = ttk.Combobox(self.window, textvariable=self.nivel_seleccionado, values=niveles, font=("Fixedsys", 13), state="readonly",width=9)
            combobox_nivel.place(relx=start_x + i * 250 / self.SCREEN_WIDTH, rely=0.5, anchor="center")
            self.combobox_patrones.append(combobox_nivel)


    def obtener_informacion(self):
        self.savedConfig=[]
        for i in range(3):
            nivel = "Nivel " + str(i+1)
            patron = self.combobox_patrones[i].get()
            self.savedConfig.append([nivel, patron])

    
    def goBack(self):
        import menu
        self.obtener_informacion()
        print("info guardada: -> ",self.savedConfig)
        for widget in self.window.winfo_children():
            if widget != self.animated_gif:
                widget.destroy()
        menu.init_menu(self.window, self.animated_gif, self.key)





"""
window = tk.Tk()
gameConfiguration(window, None, None)
window.mainloop()
#"""