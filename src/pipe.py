import pygame
import random
from src.settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = load_image('pipe-red.png')
        
        if self.image:
            self.image = pygame.transform.scale2x(self.image)
        else:
            self.image = pygame.Surface((52, 320))
            self.image.fill((0, 255, 0))

        # position 1 is from top, -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y - PIPE_GAP // 2))
        else:
            self.rect = self.image.get_rect(topleft=(x, y + PIPE_GAP // 2))

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()
