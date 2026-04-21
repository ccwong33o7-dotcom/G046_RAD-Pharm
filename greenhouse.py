import pygame
import sys

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hazard Greenhouse Prototype")
clock = pygame.time.Clock()

COLOR_BG = (30, 30, 30)
COLOR_PLANT= (50, 200, 50)
COLOR_DUST = (150, 150, 100)
COLOR_TEXT = (200, 200, 200)

class Plant:
    def __init__(self):
        self.rect = pygame.Rect(350, 400, 100, 100)
        self.growth = 0
        self.dust = 0
        self.is_dead = False
    
    def update(self):
        if self.is_dead: return

        self.dust += 0.1
        if self.dust > 100: 
            self.dust = 100

        if self.dust < 70:
            self.growth += 0.05

        if self.dust <= 100:
            self.is_dead = True
    
    def clean(self):
        self.dust -= 20
        
        if self.dust < 0: 
            self.dust = 0
    
    def draw(self, surface):
        current_height = (self.growth / 100) * 150
        plant_rect = pygame.Rect(self.rect.x, self.rect.buttom - current_height, self.rect.width, current_height)

        color = (100, 100, 100) if self.is_dead else COLOR_PLANT
        pygame.draw.rect(surface, color, plant_rect)

        if self.dust > 0:
            dust_overlay = pygame.Surface((self.rect.width, current_height))
            dust_overlay.set_alpha(int((self.dust / 100) * 200)) 
            dust_overlay.fill(COLOR_DUST)
            surface.blit(dust_overlay, (self.rect.x, self.rect.bottom - current_height))







