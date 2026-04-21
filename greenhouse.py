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
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 100)
        self.growth = 0
        self.dust = 0
        self.alive = True
    
    def update(self):
        if self.alive:
            self.dust += 0.2
            if self.dust < 80:
                self.growth += 0.1
            if self.dust >= 100:
                self.alive = False
    
    def clean(self):
        self.dust -=30
        
        if self.dust < 0: 
            self.dust = 0






