import tkinter as tk
import menu
from tkinter import messagebox
import json
import newUser

class login:
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

        self.lblCreateUser = tk.Label(self.window, text="If you don't own an account:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.lblCreateUser.place(relx=0.4, rely=0.2, anchor="center")

        self.btnCreateUser = tk.Button(self.window, text="Create User", font=("Fixedsys", 10), command=createUser())
        self.btnCreateUser.place(relx=0.65, rely=0.2, anchor="center") 

        # Etiqueta y campo de entrada para el nombre de usuario
        self.username = tk.Label(self.window, text="Username:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.username.place(relx=0.4, rely=0.3, anchor="center")

        self.entry_username = tk.Entry(self.window)
        self.entry_username.place(relx=0.6, rely=0.3, anchor="center", width=200)

        # Etiqueta y campo de entrada para la contraseña
        self.password = tk.Label(self.window, text="Password:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.password.place(relx=0.4, rely=0.4, anchor="center")

        self.entry_password = tk.Entry(self.window, show="*")
        self.entry_password.place(relx=0.6, rely=0.4, anchor="center", width=200)

        #Log in
        self.btnLogin = tk.Button(self.window, text=" ★ Log In ★ ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.verify)
        self.btnLogin.place(relx=0.5, rely=0.5, anchor="center") 

        #Etiqueta y boton para recuperar contraseña
        self.recover = tk.Label(self.window, text="Forgot your password?:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.recover.place(relx=0.4, rely=0.6, anchor="center")

        self.btnRecover = tk.Button(self.window, text="Recover Password", font=("Fixedsys", 10))
        self.btnRecover.place(relx=0.65, rely=0.6, anchor="center") 

        self.window.mainloop()

    def verify(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Warning", "Please fill all the data to log in")
            return
        
        # Cargar datos de usuarios desde el archivo JSON
        with open("data.json") as json_file:
            data = json.load(json_file)

        # Verificar las credenciales con los datos del archivo JSON
        for usuario in data:
            if usuario["username"] == username and usuario["password"] == password:
                self.window.destroy()
                inst_init_menu = menu.init_menu()
                return

        # Si no se encuentra el usuario en el archivo JSON o las credenciales son incorrectas
        messagebox.showerror("Error", "Wrong credentials. Please try again.")
        
    def createUser():
        inst_newUser = newUser.User(0)
         




