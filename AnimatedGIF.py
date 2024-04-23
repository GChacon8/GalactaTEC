import tkinter as tk
from PIL import Image, ImageTk

#Clase para el movimiento del fondo de pantalla del menu, imagen tipo gif
class AnimatedGIF(tk.Label):
    def __init__(self, master, path):
        super().__init__(master)
        self._master = master
        self._gif_path = path
        self._gif_frames = []
        self._index = 0
        self._delay = 100
        self._load_frames()
        self._animate()

    def _load_frames(self):
        gif = Image.open(self._gif_path)
        try:
            while True:
                self._gif_frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(self._gif_frames)) # Move to the next frame
        except EOFError:
            pass

    def _animate(self):
        self.config(image=self._gif_frames[self._index])
        self._index = (self._index + 1) % len(self._gif_frames)
        self._master.after(self._delay, self._animate)