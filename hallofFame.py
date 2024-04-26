import tkinter as tk
import json
from PIL import Image, ImageTk

class hallofFame:
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


        self.etiqueta = tk.Label(self.window, text="!Hall Of Fame!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.1, anchor="center")

        self.vertical_offset = 0.2

        # Leer datos del archivo JSON
        with open("data.json", "r") as file:
            self.data = json.load(file)

        # Ordenar los datos por puntaje de mayor a menor
        self.data.sort(key=lambda x: int(x['highscore']), reverse=True)

        # Mostrar la lista de usuarios en la ventana
        self.mostrar_lista()

    def mostrar_lista(self):
    # Mostrar los datos de los primeros usuarios en la ventana
        for i in range(5):
            if i < len(self.data):
                usuario = self.data[i]
                photo = usuario["photo"]
                print(photo)
                foto_texto = f"Foto {i+1}"
                username = usuario['username']
                puntaje = usuario['highscore']
            else:
                foto_texto = "Disponible" #cambiar a photo y que cargue la imagen de sin perfil
                photo = "Images/no-profile-picture.png"
                username = "Disponible"
                puntaje = "Disponible"
            
            if i < 3:
                vertical_offset = self.SCREEN_HEIGHT * 0.2
                relx = self.SCREEN_WIDTH * (0.2 + i * 0.2)  # Posición horizontal para la fila superior
            else:
                vertical_offset = self.SCREEN_HEIGHT * 0.5
                relx = self.SCREEN_WIDTH * (0.3 + (i % 3) * 0.2)  # Posición horizontal centrada para la fila inferior

            relx_centered = relx - self.SCREEN_WIDTH / 2

            
            usuario_label = tk.Label(self.window, text=username, bg="#120043", fg="white")
            usuario_label.place(relx=(self.SCREEN_WIDTH / 2 + relx_centered+75) / self.SCREEN_WIDTH, rely=vertical_offset / self.SCREEN_HEIGHT, anchor="center")          

            #Para colocar las imagenes
            pic = tk.Label(self.window, background="#2b5a81")
            pic.place(relx=((self.SCREEN_WIDTH / 2 + relx_centered+75) / self.SCREEN_WIDTH), rely=(vertical_offset + self.SCREEN_HEIGHT*0.1) / self.SCREEN_HEIGHT, anchor="center")
            ppImage = Image.open(photo).resize((70,70))
            ppPhoto = ImageTk.PhotoImage(ppImage)
            pic.config(image=ppPhoto)
            pic.image = ppPhoto

            puntaje_label = tk.Label(self.window, text=puntaje, bg="#120043", fg="white")
            puntaje_label.place(relx=(self.SCREEN_WIDTH / 2 + relx_centered+75) / self.SCREEN_WIDTH, rely=(vertical_offset + self.SCREEN_HEIGHT*0.2) / self.SCREEN_HEIGHT, anchor="center")

        btnBack = tk.Button(self.window, text=" Go Back ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.goBack)
        btnBack.place(relx=0.5, rely=0.9, anchor="center") 

    def goBack(self):
        import menu
        for widget in self.window.winfo_children():
            if widget != self.animated_gif:
                widget.destroy()
        menu.init_menu(self.window, self.animated_gif, self.key)


"""
window = tk.Tk()
hallofFame(window, None, None)
window.mainloop()
#"""