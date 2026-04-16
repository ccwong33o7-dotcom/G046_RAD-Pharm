import pygame
import sys
from menu import draw_menu

pygame.init()

Width = 1280
Height= 720

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("16;9")
font = pygame.font.SysFont("Arial",40)

current_state="MENU"

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
         if current_state == "MENU":
            s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)
            if s_btn.collidepoint(mouse_pos):
               current_state = "GAME"
            elif set_btn.collidepoint(mouse_pos):
               current_state = "SETTING"
            elif e_btn.collidepoint(mouse_pos):
               pygame.quit()
               sys.exit()

    if current_state == "MENU":
       draw_menu(screen, font, mouse_pos)
    elif current_state =="GAME":
       screen.fill((0, 100, 0))
    elif current_state == "SETTING":
       screen.fill((50, 50, 50))

    pygame.display.update()

    
         

