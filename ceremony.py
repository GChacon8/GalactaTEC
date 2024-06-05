import tkinter as tk
import json
from PIL import Image, ImageTk
from tkinter import filedialog
import pygame

class ceremony:
    def __init__(self, window, animated_gif, key1, key2):
        self.window = window
        self.animated_gif = animated_gif
        self.key1 = key1 # llave del jugador 1
        self.key2 = key2 # llave del jugador 2

        pygame.mixer.init()
        song_list = "Songs/Victory FFI.mp3"

        self.window.title("GalactaTEC")
        self.window.configure(bg="#120043")
        self.window.geometry("800x600")

        self.etiqueta = tk.Label(self.window, text="¡GalactaTEC!", font=("Fixedsys", 30, "italic"), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.1, anchor="center")

        self.etiqueta = tk.Label(self.window, text="✶ Award Ceremony ✶", font=("Fixedsys", 20), bg="#120043", fg="white")
        self.etiqueta.place(relx=0.5, rely=0.2, anchor="center")

        with open("data.json") as json_file:
            self.data = json.load(json_file)

        for user in self.data:
            if(user["key"] == self.key1):
                self.score1 = user["highscore"]
                self.pp1 = user["photo"] #profile picture
                self.user1 = user["username"]
            elif(user["key"] == self.key2):
                self.score2 = user["highscore"]
                self.pp2 = user["photo"]
                self.user2 = user["username"]

        if(self.score1 < self.score2):
            self.score1, self.score2 = self.score2, self.score1
            self.pp1, self.pp2 = self.pp2, self.pp1
            self.user1, self.user2 = self.user2, self.user1

        # Primer lugar
        self.lbl_first = tk.Label(self.window, text="┌── •✧• ──┐\n1st\n└── •✧• ──┘", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.lbl_first.place(relx=0.35, rely=0.65, anchor="center")

        self.lbl_user1 = tk.Label(self.window, text= self.user1, font=("Fixedsys", 15), bg="#120043", fg="white")
        self.lbl_user1.place(relx=0.35, rely=0.5, anchor="center")

        self.lbl_score1 = tk.Label(self.window, text= self.score1, font=("Fixedsys", 20), bg="#120043", fg="white")
        self.lbl_score1.place(relx=0.35, rely=0.55, anchor="center")

        self.pic1 = tk.Label(self.window, background="#2b5a81")
        self.pic1.grid(row=0, column=0, padx=0, pady=0)
        self.pic1.place(relx=0.35, rely=0.4, anchor="center")

        ppImage1 = Image.open(self.pp1).resize((100,100))
        ppPhoto1 = ImageTk.PhotoImage(ppImage1)

        self.pic1.config(image=ppPhoto1)
        self.pic1.image = ppPhoto1

        #Second place
        self.lbl_second = tk.Label(self.window, text="┌── •✧• ──┐\n2nd\n└── •✧• ──┘", font=("Fixedsys", 15), bg="#120043", fg="white")
        self.lbl_second.place(relx=0.65, rely=0.65, anchor="center")

        self.lbl_user2 = tk.Label(self.window, text= self.user2, font=("Fixedsys", 15), bg="#120043", fg="white")
        self.lbl_user2.place(relx=0.65, rely=0.5, anchor="center")

        self.lbl_score2 = tk.Label(self.window, text= self.score2, font=("Fixedsys", 20), bg="#120043", fg="white")
        self.lbl_score2.place(relx=0.65, rely=0.55, anchor="center")

        self.pic2 = tk.Label(self.window, background="#2b5a81")
        self.pic2.grid(row=0, column=0, padx=0, pady=0)
        self.pic2.place(relx=0.65, rely=0.4, anchor="center")

        ppImage2 = Image.open(self.pp2).resize((100,100))
        ppPhoto2 = ImageTk.PhotoImage(ppImage2)

        self.pic2.config(image=ppPhoto2)
        self.pic2.image = ppPhoto2

        self.play_music(song_list)
        self.window.mainloop()
        pygame.mixer.quit()
        

    # Función para reproducir música
    def play_music(self, song):
        if song:
            pygame.mixer.music.load(song)  
            pygame.mixer.music.play(-1)  # Reproducir en bucle




            

        

