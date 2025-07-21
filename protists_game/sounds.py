import pygame
import os
import random

def load_sounds():
    """Load and return a dictionary of game sounds."""
    sounds = {
        "collect": pygame.mixer.Sound(os.path.join("music", "food", "acquire.wav")),
        "damage": pygame.mixer.Sound(os.path.join("music", "damage", "damage-sound.wav")),
        "defence": pygame.mixer.Sound(os.path.join("music", "level_up", "defence.ogg")),
        "levelup": pygame.mixer.Sound(os.path.join("music", "level_up", "levelup.wav")),
        "gameover": pygame.mixer.Sound(os.path.join("music", "game_over", "GameOver.ogg")),
        "select": pygame.mixer.Sound(os.path.join("music", "select", "menu-click.ogg")),
        "protist_select": pygame.mixer.Sound(os.path.join("music", "select", "protists_selection.wav")),
        # Add more as needed
    }
    return sounds

def get_intro_music_path():
    """Return the path to the intro music."""
    return os.path.join("music", "intro", "the_eternal_sandsmix2.ogg")


def get_bg_music_path():
    """Return a random background music track."""
    bg_tracks = [
        os.path.join("music", "background", "TremLoadingloopl.wav"),
        os.path.join("music", "background", "Underwater-Ambient-Pad.ogg"),
        os.path.join("music", "background", "unknown_space_bassed.wav"),
    ]
    return random.choice(bg_tracks)

def get_gameover_music_path():
    """Return the path to the game over music."""
    return os.path.join("music", "game_over", "GameOver.wav")