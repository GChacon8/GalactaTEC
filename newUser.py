import tkinter as tk
from tkinter import filedialog, messagebox
import AnimatedGIF
from PIL import Image, ImageTk
import json
import re
import yagmail
import login
import menu

class newUser:
    def __init__(self, window, animated_gif, key):
        self.key = key
        self.window = window
        self.animated_gif = animated_gif

        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry("800x600")

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
        if(self.key == 0):
            self.btnCreate = tk.Button(self.window, text=" ★ Create User ★ ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.createUser)
            self.btnCreate.place(relx=0.5, rely=0.8, anchor="center") 

        else:
            self.setOriginalValues()
            self.btnCancel = tk.Button(self.window, text=" Cancel ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.createUser)
            self.btnCancel.place(relx=0.35, rely=0.8, anchor="center") 
            
            self.btnCreate = tk.Button(self.window, text=" ★ Save Changes ★ ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.saveChanges)
            self.btnCreate.place(relx=0.6, rely=0.8, anchor="center")

        self.btnBack = tk.Button(self.window, text=" Go Back ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.goBack)
        self.btnBack.place(relx=0.5, rely=0.9, anchor="center") 


        self.window.mainloop()

    def clear_win(self):
        for widget in self.window.winfo_children():
            if widget != self.animated_gif:
                widget.destroy()

    def goBack(self):
        if self.key == 0:
            self.clear_win()
            login.login(self.window, self.animated_gif)
        else:
            self.clear_win()
            menu.init_menu(self.window, self.animated_gif, self.key)

    def setOriginalValues(self):

        with open("data.json") as json_file:
            data = json.load(json_file)

        self.photo = ""
        self.music = ""
            
        for usuario in data:
            if usuario["key"] == self.key:
                self.entry_username.insert(0, usuario["username"])
                self.entry_name.insert(0, usuario["full_name"])
                self.entry_email.insert(0, usuario["email"])
                self.entry_password.insert(0,usuario ["password"])
                self.photo = usuario["photo"]
                self.music = usuario["music"]

        self.OgPhoto = tk.Label(self.window, text=self.photo, font=("Fixedsys", 5), bg="#120043", fg="white")
        self.OgPhoto.place(relx=0.4, rely=0.48, anchor="center")

        self.music = tk.Label(self.window, text=self.music, font=("Fixedsys", 5), bg="#120043", fg="white")
        self.music.place(relx=0.4, rely=0.73, anchor="center")

        # Mostrar la foto de perfil actual
        self.pic = tk.Label(self.window, background="#2b5a81")
        self.pic.grid(row=0, column=0, padx=0, pady=0)
        self.pic.place(relx=0.25, rely=0.25, anchor="center")

        self.OgPhoto = tk.Label(self.window, text="Me", font=("Fixedsys", 10), bg="#120043", fg="white")
        self.OgPhoto.place(relx=0.25, rely=0.33, anchor="center")

        ppImage = Image.open(self.photo).resize((70,70))
        ppPhoto = ImageTk.PhotoImage(ppImage)

        self.pic.config(image=ppPhoto)
        self.pic.image = ppPhoto

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
        ship = self.ship_images[self.current_index]
        password = self.entry_password.get()

        if not self.filename:
            photo = None
        else:
            photo = self.filename

        if not self.music:
            music = None
        else:
            music = self.music_file

        
        if not username or not password or not fullname or not email:
            messagebox.showwarning("Warning", "Please fill all the data to create your user")
            return
        
        if self.validateEmail(email) == False:
            messagebox.showwarning("Error", "The email address entered is not valid, please try again")
            return
        
        if self.verify_password(password) == False:
            messagebox.showwarning("Error", "Password must have:\n- Minimum 7 characters\n- You must use at least one capital letter\n- You must use at least one special symbol\n- You must use at least one number\n- You must use at least one lowercase letter")
            return
        
        # Cargar datos de usuarios desde el archivo JSON
        with open("data.json") as json_file:
            data = json.load(json_file)

        # Verificar las credenciales con los datos del archivo JSON
        for usuario in data:
            if usuario["username"] == username or  usuario["email"] == email:
                messagebox.showwarning("Warning", "This user already exists")
                return
        
        user = {"key": len(data)+1,
            "username": username, 
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
            

    def saveChanges(self):
        username = self.entry_username.get()
        fullname = self.entry_name.get()
        email = self.entry_email.get()
        ship = self.ship_images[self.current_index]
        password = self.entry_password.get()
        
        if not self.filename:
            photo = self.photo #Si no ingresa un nuevo valor permanece el original
        else:
            photo = self.filename

        if not self.music:
            music = self.music
        else:
            music = self.music_file

        
        if not username or not password or not fullname or not email:
            messagebox.showwarning("Warning", "Please fill all the data to create your user")
            return
        
        if self.validateEmail(email) == False:
            messagebox.showwarning("Error", "The email address entered is not valid, please try again")
            return
        
        if self.verify_password(password) == False:
            messagebox.showwarning("Error", "Password must have:\n- Minimum 7 characters\n- You must use at least one capital letter\n- You must use at least one special symbol\n- You must use at least one number\n- You must use at least one lowercase letter")
            return
        
        user = {"key": self.key,
                "username": username, 
                "password": password, 
                "full_name": fullname,
                "email": email,
                "photo": photo,
                "ship": ship,
                "music": music}
        
        with open("data.json") as json_file:
            data = json.load(json_file)
            
        for usuario in data:
            if usuario["key"] == self.key:
                usuario.update(user) 

        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        

    def verify_password(self, password):
        # Verificar la longitud mínima de 7 caracteres
        if len(password) < 7:
            return False

        # Verificar al menos una mayúscula, una minúscula, un número y un símbolo especial
        if not re.search(r"[A-Z]", password):  # Al menos una mayúscula
            return False
        if not re.search(r"[a-z]", password):  # Al menos una minúscula
            return False
        if not re.search(r"\d", password):     # Al menos un número
            return False
        if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", password):  # Al menos un símbolo especial
            return False

        return True
    
    
    def validateEmail(self, destination):
        try:
            # Inicializar Yagmail con tu dirección de correo electrónico y contraseña
            yag = yagmail.SMTP('galactatec@gmail.com', 'twklqtltylscbvnz')

            # Enviar el correo electrónico
            yag.send(to=destination, subject='Welcome to GalactaTEC', contents='This email is a confirmation of your new user for GalactaTEC.')

            print("El correo electrónico fue enviado exitosamente.")
            return True

        except Exception as e:
            print("Error al enviar el correo electrónico:", e)
            return False
