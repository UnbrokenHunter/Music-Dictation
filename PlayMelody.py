import pygame
import tempfile

def play_melody(melody):
    midi_path = tempfile.mktemp('.mid')
    melody.write('midi', fp=midi_path)

    pygame.mixer.init()
    pygame.mixer.music.load(midi_path)
    pygame.mixer.music.play()
