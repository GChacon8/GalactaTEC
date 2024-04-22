import tkinter as tk
from tkinter import filedialog, messagebox
import menu
from PIL import Image, ImageTk
import json

class User:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry("800x600")

        #Configuracion del fondo 
        gif_path = "Images/space_background.gif"
        animated_gif = menu.AnimatedGIF(self.window, gif_path)
        animated_gif.place(x=0, y=0, relwidth=1, relheight=1)

        self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.1, anchor="center")

        # Etiqueta y campo de entrada para el nombre de usuario
        self.username = tk.Label(self.window, text="Username:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.username.place(relx=0.4, rely=0.2, anchor="center")

        self.entry_username = tk.Entry(self.window)
        self.entry_username.place(relx=0.6, rely=0.2, anchor="center", width=200)

        # Etiqueta y campo de entrada para el nombre completo
        self.name = tk.Label(self.window, text="Full name:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.name.place(relx=0.4, rely=0.25, anchor="center")

        self.entry_name = tk.Entry(self.window)
        self.entry_name.place(relx=0.6, rely=0.25, anchor="center", width=200)

        # Etiqueta y campo de entrada para el correo electronico
        self.email = tk.Label(self.window, text="E-mail:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.email.place(relx=0.4, rely=0.3, anchor="center")

        self.entry_email = tk.Entry(self.window)
        self.entry_email.place(relx=0.6, rely=0.3, anchor="center", width=200)
        
        # Etiqueta y campo de entrada para la contraseña
        self.password = tk.Label(self.window, text="Password:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.password.place(relx=0.4, rely=0.35, anchor="center")

        self.entry_password = tk.Entry(self.window)
        self.entry_password.place(relx=0.6, rely=0.35, anchor="center", width=200)

        # Etiqueta y boton de entrada para la foto
        self.photo = tk.Label(self.window, text="Profile Picture:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.photo.place(relx=0.4, rely=0.45, anchor="center")

        self.btn_select_photo = tk.Button(self.window, text="Select Photo", font=("Fixedsys", 10), bg="#120043", fg="white", command=self.select_photo)
        self.btn_select_photo.place(relx=0.6, rely=0.45, anchor="center")

        # Etiqueta y boton de entrada para la nave

        self.ship = tk.Label(self.window, text="Spaceship:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.ship.place(relx=0.35, rely=0.55, anchor="center")
        self.shipsCarousel()

        # Etiqueta y boton de entrada para la musica
        self.music = tk.Label(self.window, text="Music:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.music.place(relx=0.4, rely=0.7, anchor="center")

        self.btn_select_music = tk.Button(self.window, text="Select Music", font=("Fixedsys", 10), bg="#120043", fg="white", command=self.select_music)
        self.btn_select_music.place(relx=0.55, rely=0.7, anchor="center")

        #Crear
        self.btnCreate = tk.Button(self.window, text=" ★ Create User ★ ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.createUser)
        self.btnCreate.place(relx=0.5, rely=0.8, anchor="center") 


        self.window.mainloop()

    def shipsCarousel(self):
        self.ship_images = [
            "Images/ships/ship1.png",
            "Images/ships/ship3.png",
            "Images/ships/ship4.png"
        ]

        self.current_index = 0

        # Botones de selección de nave
        self.ship_button = tk.Button(self.window, text=">", font=("Fixedsys", 15, "bold") ,command=self.next_ship, background="#52112f", fg="white")
        self.ship_button.grid(row=0, column=1, padx=10, pady=10)
        self.ship_button.place(relx=0.7, rely=0.55, anchor="center")

        self.ship_button = tk.Button(self.window, text="<", font=("Fixedsys", 15, "bold"),command=self.prev_ship, background="#52112f", fg="white")
        self.ship_button.grid(row=0, column=1, padx=10, pady=10)
        self.ship_button.place(relx=0.5, rely=0.55, anchor="center")

        # Etiqueta para mostrar la imagen
        self.ship_image_label = tk.Label(self.window)
        self.ship_image_label.grid(row=0, column=0, padx=10, pady=10)
        self.ship_image_label.place(relx=0.6, rely=0.55, anchor="center")

        # Mostrar la primera imagen
        self.show_current_ship()

    def show_current_ship(self):
        # Cargar la imagen actual
        current_ship_image_path = self.ship_images[self.current_index]
        current_ship_image = Image.open(current_ship_image_path)
        current_ship_photo = ImageTk.PhotoImage(current_ship_image)

        # Mostrar la imagen en la etiqueta
        self.ship_image_label.config(image=current_ship_photo)
        self.ship_image_label.image = current_ship_photo

    def next_ship(self):
        # Mostrar la siguiente imagen
        self.current_index = (self.current_index + 1) % len(self.ship_images)
        self.show_current_ship()

    def prev_ship(self):
        # Mostrar la imagen anterior
        self.current_index = (self.current_index - 1) % len(self.ship_images)
        self.show_current_ship()

    def select_photo(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo de imagen
        self.filename = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=(("Archivos de Imagen", "*.jpg;*.png;*.jpeg"), ("Todos los archivos", "*.*")))

        # Verificar si se seleccionó un archivo
        if self.filename:
            print("Ruta del archivo seleccionado:", self.filename)

    def select_music(self):
        # Abrir un cuadro de diálogo para seleccionar un archivo MP3
        self.music_file = filedialog.askopenfilename(title="Seleccionar Música", filetypes=(("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*")))

        # Verificar si se seleccionó un archivo
        if self.music_file:
            print("Archivo de música seleccionado:", self.music_file)

    def createUser(self):
        username = self.entry_username.get()
        fullname = self.entry_name.get()
        email = self.entry_email.get()
        photo = "self.filename"
        ship = self.ship_images[self.current_index]
        music = "self.music_file"
        password = self.entry_password.get()

        
        if not username or not password or not fullname or not email:
            messagebox.showwarning("Warning", "Please fill all the data to create your user")
            return
        
        # Cargar datos de usuarios desde el archivo JSON
        with open("data.json") as json_file:
            data = json.load(json_file)

        # Verificar las credenciales con los datos del archivo JSON
        for usuario in data:
            if usuario["username"] == username and usuario["password"] == password:
                messagebox.showwarning("Warning", "This user already exists")
                return
        
        user = {"username": username, 
                "password": password, 
                "full_name": fullname,
                "email": email,
                "photo": photo,
                "ship": ship,
                "music": music}
        
        # Agregar el nuevo usuario a la lista de datos existentes
        data.append(user)

        # Escribir los datos actualizados en el archivo JSON
        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

User()