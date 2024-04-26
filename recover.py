import tkinter as tk
from tkinter import messagebox
import AnimatedGIF
import json
import yagmail
import random
import datetime
import re

class Recover:
    def __init__(self, window, animated_gif):
        self.window = window
        self.animated_gif = animated_gif

        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry("800x600")

        self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.2, anchor="center")

        # Etiqueta y campo de entrada para el correo electronico
        self.emailLbl = tk.Label(self.window, text="E-mail:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.emailLbl.place(relx=0.35, rely=0.3, anchor="center")

        self.entry_email = tk.Entry(self.window)
        self.entry_email.place(relx=0.55, rely=0.3, anchor="center", width=200)

        self.btnCancel = tk.Button(self.window, text=" Cancel ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.cancel)
        self.btnCancel.place(relx=0.4, rely=0.4, anchor="center") 

        self.btnSend = tk.Button(self.window, text=" Send ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.verifyEmail)
        self.btnSend.place(relx=0.6, rely=0.4, anchor="center") 

        self.window.mainloop()

    def cancel(self):
        self.clear_win()
        import login
        login.login(self.window, self.animated_gif)

    def verifyWindow(self):
        self.emailLbl.destroy()
        self.entry_email.destroy()
        self.btnSend.destroy()
        self.btnCancel.destroy()

        self.code = tk.Label(self.window, text="Code:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.code.place(relx=0.35, rely=0.3, anchor="center")

        self.entry_code = tk.Entry(self.window)
        self.entry_code.place(relx=0.55, rely=0.3, anchor="center", width=200)

        self.btnSend = tk.Button(self.window, text=" Submit ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.verify_code)
        self.btnSend.place(relx=0.5, rely=0.4, anchor="center") 

    def changePasswordWindow(self):
        self.code.destroy()
        self.entry_code.destroy()
        self.btnSend.destroy()

        # Etiqueta y campo de entrada para la contraseña
        self.password = tk.Label(self.window, text="Password:", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.password.place(relx=0.35, rely=0.3, anchor="center")

        self.entry_password = tk.Entry(self.window)
        self.entry_password.place(relx=0.55, rely=0.3, anchor="center", width=200)

        self.btnSend = tk.Button(self.window, text=" Save ", font=("Fixedsys", 15), background="#52112f", fg="white", command=self.savePassword)
        self.btnSend.place(relx=0.5, rely=0.4, anchor="center") 

    def savePassword(self):
        password = self.entry_password.get()

        if self.verify_password(password) == False:
            messagebox.showwarning("Error", "Password must have:\n- Minimum 7 characters\n- You must use at least one capital letter\n- You must use at least one special symbol\n- You must use at least one number\n- You must use at least one lowercase letter")
            return

        with open("data.json") as json_file:
            data = json.load(json_file)
            
        for usuario in data:
            if usuario["email"] == self.email:
                 usuario["password"] = password

        with open("data.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

        messagebox.showinfo("Password updated", "Your password has been changed successfully")
        self.clear_win
        import login
        login.login(self.window, self.animated_gif)

    def verifyEmail(self):
        self.email = self.entry_email.get()
                
        # Cargar datos de usuarios desde el archivo JSON
        with open("data.json") as json_file:
            data = json.load(json_file)

        # Verificar si el correo esta registrado
        for usuario in data:
            if usuario["email"] == self.email:
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

        current_time = datetime.datetime.now()
        time_difference = current_time - self.timestamp
        if time_difference.total_seconds() > 300: 
            messagebox.showerror("Error", "The code has exired")
            return
        elif code != self.codeEntered:
            messagebox.showerror("Error", "The code entered is incorrect")
            return 
        else: 
            self.changePasswordWindow()

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
    
    def clear_win(self):
        for widget in self.window.winfo_children():
            if widget != self.animated_gif:
                widget.destroy()
