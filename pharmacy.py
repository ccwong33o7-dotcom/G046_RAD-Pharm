import pygame

def draw_pharmacy(screen, bg_img):
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

    greenhouse_btn_rect = pygame.Rect(1180,130,80,40)
    crafting_btn_rect = pygame.Rect(1180,180,80,40)
    shop_btn_rect = pygame.Rect(1180,230,80,40) 
   
    return greenhouse_btn_rect, crafting_btn_rect, shop_btn_rect