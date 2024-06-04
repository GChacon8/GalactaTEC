import pygame
import sys

class MusicGame:
    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Pygame Music Player")

        # Diccionario de teclas y sus respectivas pistas de música
        self.music_tracks = {
            pygame.K_1: 'Songs/music_1.mp3',
            pygame.K_2: 'Songs/music_2.mp3',
            pygame.K_3: 'Songs/music_3.mp3',
        }

    def play_music(self, file_path):
        """Reproduce una pista de música, deteniendo la anterior si es necesario."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)

    def run_game(self):
        """Bucle principal del juego."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.music_tracks:
                        self.play_music(self.music_tracks[event.key])

        pygame.quit()
        sys.exit()

# Crear una instancia del juego y correrlo
if __name__ == "__main__":
    mg = MusicGame()
    mg.run_game()
