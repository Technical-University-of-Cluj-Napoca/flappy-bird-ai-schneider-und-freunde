import pygame
from src.settings import *

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(screen, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont('Arial', size, bold=True)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

def draw_medals(screen, score):
    medal_color = None
    if score >= 40:
        medal_color = (229, 228, 226) # Platinum
        medal_name = "Platinum"
    elif score >= 30:
        medal_color = (255, 215, 0) # Gold
        medal_name = "Gold"
    elif score >= 20:
        medal_color = (192, 192, 192) # Silver
        medal_name = "Silver"
    elif score >= 10:
        medal_color = (205, 127, 50) # Bronze
        medal_name = "Bronze"
    
    if medal_color:
        pygame.draw.circle(screen, medal_color, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 10), 20)
        draw_text(screen, medal_name, 12, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 40)
