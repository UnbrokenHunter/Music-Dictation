import pygame
import tempfile

def play_melody(app):
    if app.melody is None:
        print("No melody to play.")
        return

    midi_path = tempfile.mktemp('.mid')
    app.melody.write('midi', fp=midi_path)

    pygame.mixer.init()
    pygame.mixer.music.load(midi_path)
    pygame.mixer.music.play()

    print("Playing Melody")
