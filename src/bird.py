import pygame
from src.settings import *
from src.neural_network import NeuralNetwork

class Bird(pygame.sprite.Sprite):
    def __init__(self, brain=None):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        
        # AI components
        self.brain = brain if brain else None
        self.fitness = 0
        self.alive = True
        
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
        self.fitness = 0
        self.alive = True
    
    def think(self, pipes):
        """
        Use neural network to decide whether to jump
        
        Args:
            pipes: Sprite group of pipes
        
        Returns:
            bool: True if decided to jump
        """
        if not self.brain or not self.alive:
            return False
        
        # Find the next pipe
        next_pipe = None
        min_distance = float('inf')
        
        for pipe in pipes:
            # Only consider pipes ahead of the bird
            if pipe.rect.right > self.rect.left:
                distance = pipe.rect.left - self.rect.left
                if distance < min_distance:
                    min_distance = distance
                    next_pipe = pipe
        
        if next_pipe is None:
            # No pipe ahead, use default values
            pipe_x = 288
            pipe_top_y = 0
            pipe_bottom_y = 512
        else:
            pipe_x = min_distance
            # Determine if this is top or bottom pipe
            if next_pipe.rect.bottom < 256:  # Top pipe
                pipe_top_y = next_pipe.rect.bottom
                # Find corresponding bottom pipe
                for pipe in pipes:
                    if pipe.rect.left == next_pipe.rect.left and pipe.rect.top > 256:
                        pipe_bottom_y = pipe.rect.top
                        break
                else:
                    pipe_bottom_y = pipe_top_y + PIPE_GAP
            else:  # Bottom pipe
                pipe_bottom_y = next_pipe.rect.top
                # Find corresponding top pipe
                for pipe in pipes:
                    if pipe.rect.left == next_pipe.rect.left and pipe.rect.bottom < 256:
                        pipe_top_y = pipe.rect.bottom
                        break
                else:
                    pipe_top_y = pipe_bottom_y - PIPE_GAP
        
        # Make decision
        should_jump = self.brain.predict(
            self.rect.centery,
            self.velocity,
            pipe_x,
            pipe_top_y,
            pipe_bottom_y
        )
        
        return should_jump
