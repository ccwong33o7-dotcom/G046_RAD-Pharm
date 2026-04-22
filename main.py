import pygame
import sys
from menu import draw_menu
from setting import run_setting
from pharmacy import draw_pharmacy
from shop import draw_shop

pygame.init()

Width = 1280
Height= 720

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game")
font = pygame.font.SysFont("Arial",40)

current_state="MENU"
last_state = "MENU"

while True:
    mouse_pos = pygame.mouse.get_pos()

    if current_state == "MENU":
       s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)

    elif current_state == "PHARMACY":
       pharmacy_set_btn, pharmacy_to_shop_btn = draw_pharmacy(screen,font)

    elif current_state == "SHOP":
       shop_set_btn = draw_shop(screen,font)

    elif current_state == "SETTING":
       current_state = run_setting(screen, last_state)
       
       
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:         
         if current_state == "MENU":
            if s_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"  
            elif set_btn.collidepoint(mouse_pos):
               last_state = "MENU"
               current_state = "SETTING"
            elif e_btn.collidepoint(mouse_pos):
               pygame.quit()
               sys.exit()
         
         elif current_state == "PHARMACY":
            if pharmacy_set_btn.collidepoint(mouse_pos):
               last_state ="PHARMACY"
               current_state = "SETTING"
            elif pharmacy_to_shop_btn.collidepoint(mouse_pos):
               current_state = "SHOP"

         elif current_state == "SHOP":
            if shop_set_btn.collidepoint(mouse_pos):
               last_state = "SHOP"
               current_state = "SETTING"

         elif current_state == "SETTING":
            pass
 
         elif current_state in ["SHOP", "JUNKYARD", "GREENHOUSE"]:
            pass

    pygame.display.flip()
    
         

