import pygame

def draw_pharmacy(screen, bg_img):
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

   
    return True