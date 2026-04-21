import pygame
import json

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Settings")
title_font = pygame.font.SysFont("Arial",50,bold=True)
UI_font = pygame.font.SysFont("Arial",30)

volume = 0.5
slider_rect = pygame.Rect(300,250,200,20)
save_btn_rect = pygame.Rect(300,350,200,50)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if slider_rect.collidepoint(mouse_pos):
          volume = (mouse_pos[0] - slider_rect.x) / slider_rect.width 
          volume = max(0.0, min(1.0, volume))
        if save_btn_rect.collidepoint(mouse_pos):
          with open("settings.json", "w") as f:
            json.dump({"volume":volume}, f)
          running = False