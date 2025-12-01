import pygame
from src.settings import *

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        
        # Load images or create fallbacks
        for img_name in ['bluebird-upflap.png', 'bluebird-midflap.png', 'bluebird-downflap.png']:
            img = load_image(img_name)
            if img:
                self.images.append(pygame.transform.scale2x(img)) # Usually flappy bird assets are small
            else:
                # Fallback
                surf = pygame.Surface((34, 24))
                surf.fill((255, 255, 0))
                self.images.append(surf)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=BIRD_START_POS)
        self.velocity = 0
        self.clicked = False

    def update(self, flying=True):
        if flying:
            # Gravity
            self.velocity += GRAVITY
            if self.velocity > 8:
                self.velocity = 8
            
            self.rect.y += int(self.velocity)

        # Animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

        # Rotation
        self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)

    def jump(self):
        self.velocity = BIRD_JUMP

    def reset(self):
        self.rect.center = BIRD_START_POS
        self.velocity = 0
