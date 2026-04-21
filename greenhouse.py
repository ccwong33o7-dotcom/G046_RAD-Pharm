import pygame
import sys

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

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Hazard Greenhouse - Survival Alpha")
clock = pygame.time.Clock() 


my_plant = Plant(270, 250)




