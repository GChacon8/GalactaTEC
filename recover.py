import tkinter as tk
from tkinter import filedialog, messagebox
import menu
import json
import yagmail
import random
import datetime

class Recover:
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
        self.etiqueta.place(relx=0.5, rely=0.2, anchor="center")

        # Etiqueta y campo de entrada para el correo electronico
        self.email = tk.Label(self.window, text="E-mail:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.email.place(relx=0.35, rely=0.3, anchor="center")

        self.entry_email = tk.Entry(self.window)
        self.entry_email.place(relx=0.55, rely=0.3, anchor="center", width=200)

        self.btnCancel = tk.Button(self.window, text=" Cancel ", font=("Fixedsys", 15), background="#52112f", fg="white")
        self.btnCancel.place(relx=0.4, rely=0.4, anchor="center") 

        self.btnSend = tk.Button(self.window, text=" Send ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.verifyEmail)
        self.btnSend.place(relx=0.6, rely=0.4, anchor="center") 

        self.window.mainloop()

    def verifyWindow(self):
        self.email.destroy()
        self.entry_email.destroy()
        self.btnSend.destroy()
        self.btnCancel.destroy()

        self.code = tk.Label(self.window, text="Code:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.code.place(relx=0.35, rely=0.3, anchor="center")

        self.entry_code = tk.Entry(self.window)
        self.entry_code.place(relx=0.55, rely=0.3, anchor="center", width=200)

        self.btnSend = tk.Button(self.window, text=" Submit ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.verify_code)
        self.btnSend.place(relx=0.6, rely=0.4, anchor="center") 

    def changePasswordWindow(self):
        self.code.destroy()
        self.entry_code.destroy()
        self.btnSend.destroy()

    def verifyEmail(self):
        email = self.entry_email.get()
                
        # Cargar datos de usuarios desde el archivo JSON
        with open("data.json") as json_file:
            data = json.load(json_file)

        # Verificar si el correo esta registrado
        for usuario in data:
            if usuario["email"] == email:
                self.sendEmail()
            
    def generate_code(self):
        # Generar un código de 5 dígitos aleatorio
        code = ''.join(random.choices('0123456789', k=5))
        self.timestamp = datetime.datetime.now()
        return code

    def sendEmail(self):
        self.codeEntered = self.generate_code()
        content = 'Your recovery code is: ' + self.codeEntered
        try:
            # Inicializar Yagmail con tu dirección de correo electrónico y contraseña
            yag = yagmail.SMTP('galactatec@gmail.com', 'twklqtltylscbvnz')

            # Enviar el correo electrónico
            yag.send(to=self.entry_email.get(), subject='★ Recover your GalactaTEC password ★', contents=content)
            print("El correo electrónico fue enviado exitosamente.")
            self.verifyWindow()
            return True

        except Exception as e:
            print("Error al enviar el correo electrónico:", e)
            return False
        
    def verify_code(self):
        code = self.entry_code.get()
        print(code)
        print(self.codeEntered)

        current_time = datetime.datetime.now()
        time_difference = current_time - self.timestamp
        if time_difference.total_seconds() > 300: 
            messagebox.showwarning("Error", "The code has exired")
            return
        elif code != self.codeEntered:
            messagebox.showwarning("Error", "The code entered is incorrect")
            return 
        else: 
            self.changePasswordWindow()

Recover()