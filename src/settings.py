import pygame
import os

# Screen dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 191, 255)

# Physics
GRAVITY = 0.25
BIRD_JUMP = -5
BIRD_START_POS = (50, SCREEN_HEIGHT // 2)
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Asset Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SPRITES_DIR = os.path.join(BASE_DIR, 'sprites')

# Load helper
def load_image(filename):
    path = os.path.join(SPRITES_DIR, filename)
    if os.path.exists(path):
        return pygame.image.load(path)
    return None
