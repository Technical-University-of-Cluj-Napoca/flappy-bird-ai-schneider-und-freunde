import pygame
import random
import sys
from src.settings import *
from src.bird import Bird
from src.pipe import Pipe
from src.ui import Button, draw_text, draw_medals

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI 2025")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)

        # Game State
        self.running = True
        self.game_active = False
        self.game_mode = None # 'manual' or 'auto'
        self.state = 'MENU' # MENU, TUTORIAL, GAME, GAMEOVER, HIGHSCORE

        # Groups
        self.bird_group = pygame.sprite.GroupSingle()
        self.pipe_group = pygame.sprite.Group()
        
        self.bird = Bird()
        self.bird_group.add(self.bird)

        # Background
        self.bg_img = load_image('background-day.png')
        if self.bg_img:
            self.bg_img = pygame.transform.scale(self.bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self.bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg_img.fill(SKY_BLUE)

        # Ground
        self.ground_img = load_image('base.png')
        if self.ground_img:
            self.ground_img = pygame.transform.scale2x(self.ground_img)
        else:
            self.ground_img = pygame.Surface((SCREEN_WIDTH, 100))
            self.ground_img.fill((222, 184, 135))
        self.ground_scroll = 0
        self.ground_y = SCREEN_HEIGHT - 100

        # Game Variables
        self.score = 0
        self.high_score_manual = 0
        self.high_score_auto = 0
        self.last_pipe = pygame.time.get_ticks()
        self.pass_pipe = False

        # UI Elements
        self.btn_manual = Button(SCREEN_WIDTH//2 - 100, 300, 200, 50, "Manual Mode", (200, 200, 200))
        self.btn_auto = Button(SCREEN_WIDTH//2 - 100, 370, 200, 50, "Autonomous Mode", (200, 200, 200))
        self.btn_highscore = Button(SCREEN_WIDTH//2 - 100, 440, 200, 50, "High Scores", (255, 215, 0))
        
        self.btn_replay = Button(SCREEN_WIDTH//2 - 50, 300, 100, 40, "Replay", (100, 255, 100))
        self.btn_menu = Button(SCREEN_WIDTH//2 - 50, 360, 100, 40, "Menu", (200, 200, 200))

    def reset_game(self):
        self.bird.reset()
        self.pipe_group.empty()
        self.score = 0
        self.game_active = True
        self.bird_group.add(self.bird) # Ensure bird is in group

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == 'MENU':
                        if self.btn_manual.is_clicked(pos):
                            self.game_mode = 'manual'
                            self.state = 'TUTORIAL'
                        elif self.btn_auto.is_clicked(pos):
                            self.game_mode = 'auto'
                            self.state = 'TUTORIAL'
                        elif self.btn_highscore.is_clicked(pos):
                            self.state = 'HIGHSCORE'

                    elif self.state == 'HIGHSCORE':
                        # Click anywhere to return
                        self.state = 'MENU'

                    elif self.state == 'TUTORIAL':
                        self.reset_game()
                        self.state = 'GAME'
                        if self.game_mode == 'manual':
                            self.bird.jump()

                    elif self.state == 'GAME':
                        if self.game_mode == 'manual' and self.game_active:
                            self.bird.jump()

                    elif self.state == 'GAMEOVER':
                        if self.btn_replay.is_clicked(pos):
                            self.state = 'TUTORIAL'
                        elif self.btn_menu.is_clicked(pos):
                            self.state = 'MENU'

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == 'GAME' and self.game_mode == 'manual' and self.game_active:
                        self.bird.jump()

            # Drawing Background
            self.screen.blit(self.bg_img, (0, 0))

            # State Machine
            if self.state == 'MENU':
                self.draw_menu()
            elif self.state == 'HIGHSCORE':
                self.draw_highscore()
            elif self.state == 'TUTORIAL':
                self.draw_tutorial()
            elif self.state == 'GAME':
                self.update_game()
                self.draw_game()
            elif self.state == 'GAMEOVER':
                self.draw_game_over()

            # Draw Ground
            self.screen.blit(self.ground_img, (self.ground_scroll, self.ground_y))
            if self.state == 'GAME' and self.game_active:
                self.ground_scroll -= PIPE_SPEED
                if abs(self.ground_scroll) > 35:
                    self.ground_scroll = 0

            pygame.display.update()

        pygame.quit()
        sys.exit()

    def draw_menu(self):
        draw_text(self.screen, "FLAPPY BIRD AI 2025", 30, SCREEN_WIDTH//2, 100)
        # Draw bird in midflight
        bird_rect = self.bird.image.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(self.bird.image, bird_rect)
        
        draw_text(self.screen, "© 2025 Schneider & Freunde", 15, SCREEN_WIDTH//2, SCREEN_HEIGHT - 30)
        
        self.btn_manual.draw(self.screen)
        self.btn_auto.draw(self.screen)
        self.btn_highscore.draw(self.screen)

    def draw_highscore(self):
        draw_text(self.screen, "HIGH SCORES", 30, SCREEN_WIDTH//2, 100)
        
        pygame.draw.rect(self.screen, (240, 230, 140), (40, 150, SCREEN_WIDTH-80, 200), border_radius=10)
        pygame.draw.rect(self.screen, BLACK, (40, 150, SCREEN_WIDTH-80, 200), 2, border_radius=10)
        
        draw_text(self.screen, f"Manual: {self.high_score_manual}", 25, SCREEN_WIDTH//2, 200)
        draw_text(self.screen, f"Auto: {self.high_score_auto}", 25, SCREEN_WIDTH//2, 280)
        
        draw_text(self.screen, "Click to return", 15, SCREEN_WIDTH//2, 400)

    def draw_tutorial(self):
        draw_text(self.screen, "GET READY!", 40, SCREEN_WIDTH//2, 150)
        
        if self.game_mode == 'manual':
            draw_text(self.screen, "Tap or Space to Fly", 20, SCREEN_WIDTH//2, 250)
        else:
            draw_text(self.screen, "Initializing Brain...", 20, SCREEN_WIDTH//2, 250)
            draw_text(self.screen, "Survival of the Fittest", 15, SCREEN_WIDTH//2, 280)
            
        draw_text(self.screen, "Tap to Start", 15, SCREEN_WIDTH//2, 400)
        
        # Show bird
        self.bird.rect.center = (50, SCREEN_HEIGHT // 2)
        self.screen.blit(self.bird.image, self.bird.rect)

    def update_game(self):
        if self.game_active:
            # Pipe Generation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, -1)
                top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, 1)
                self.pipe_group.add(btm_pipe)
                self.pipe_group.add(top_pipe)
                self.last_pipe = current_time

            self.bird_group.update()
            self.pipe_group.update()

            # Collision
            if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or \
               self.bird.rect.top <= 0 or self.bird.rect.bottom >= self.ground_y:
                self.game_active = False
                self.state = 'GAMEOVER'
                self.update_high_score()

            # Score - Check if bird passed pipe
            if len(self.pipe_group) > 0:
                # Get the first pipe in the group (they come in pairs)
                first_pipe = self.pipe_group.sprites()[0]
                
                # If bird is past the pipe and hasn't scored yet
                if self.bird.rect.left > first_pipe.rect.right and not self.pass_pipe:
                    self.score += 1
                    self.pass_pipe = True
                
                # Reset flag when bird is before the next pipe (ready to score again)
                if self.pass_pipe and self.bird.rect.left < first_pipe.rect.left:
                    self.pass_pipe = False

    def draw_game(self):
        self.pipe_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        
        # Draw Score
        score_surf = self.font.render(str(self.score), True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(score_surf, score_rect)

    def draw_game_over(self):
        # Draw game elements frozen
        self.pipe_group.draw(self.screen)
        self.bird_group.draw(self.screen)
        
        # Game Over Box
        box_rect = pygame.Rect(40, 150, SCREEN_WIDTH-80, 250)
        pygame.draw.rect(self.screen, (222, 216, 149), box_rect, border_radius=10)
        pygame.draw.rect(self.screen, (84, 56, 71), box_rect, 3, border_radius=10)
        
        draw_text(self.screen, "GAME OVER", 35, SCREEN_WIDTH//2, 120, (255, 100, 100))
        
        draw_text(self.screen, f"Score: {self.score}", 20, SCREEN_WIDTH//2 + 30, 190)
        draw_text(self.screen, f"Best: {self.high_score_manual if self.game_mode == 'manual' else self.high_score_auto}", 20, SCREEN_WIDTH//2 + 30, 230)
        
        draw_medals(self.screen, self.score)
        
        self.btn_replay.draw(self.screen)
        self.btn_menu.draw(self.screen)

    def update_high_score(self):
        if self.game_mode == 'manual':
            if self.score > self.high_score_manual:
                self.high_score_manual = self.score
        else:
            if self.score > self.high_score_auto:
                self.high_score_auto = self.score
