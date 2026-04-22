import pygame
import sys
from menu import draw_menu
from setting import run_setting
from pharmacy import draw_pharmacy

pygame.init()

Width = 1280
Height= 720

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game")
font = pygame.font.SysFont("Arial",40)

current_state="MENU"

while True:
    mouse_pos = pygame.mouse.get_pos()

    if current_state == "MENU":
       s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)
    elif current_state == "PHARMACY":
       pharmacy_set_btn = draw_pharmacy(screen,font)
    elif current_state == "SETTING":
       back_btn = run_setting(screen)
       
       
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
         if current_state == "MENU":
            if s_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"  
            elif set_btn.collidepoint(mouse_pos):
               current_state = "SETTING"
            elif e_btn.collidepoint(mouse_pos):
               pygame.quit()
               sys.exit()
         
         elif current_state == "PHARMACY":
            if pharmacy_set_btn.collidepoint(mouse_pos):
               run_setting(screen)

         elif current_state == "SETTING":
            pass
 
         elif current_state in ["SHOP", "JUNKYARD", "GREENHOUSE"]:
            pass

    pygame.display.flip()
    
         

