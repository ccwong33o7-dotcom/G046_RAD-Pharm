import pygame

def draw_pharmacy(screen, bg_img):
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

    greenhouse_btn_rect = pygame.Rect(1180,130,80,40)
    pygame.draw.rect(screen,(50,50,150),greenhouse_btn_rect)
    gh_font = pygame.font.SysFont("Arial",14)
    btn_text = gh_font.render("Greenhouse",True, (255,255,255))
    screen.blit(btn_text,(greenhouse_btn_rect.x + 2, greenhouse_btn_rect.y +12))

    crafting_btn_rect = pygame.Rect(1180,180,80,40)
    pygame.draw.rect(screen,(150,150,50),crafting_btn_rect)

    small_font = pygame.font.SysFont("Arial", 20)
    btn_text = small_font.render("Crafting",True, (255,255,255))
    screen.blit(btn_text,(crafting_btn_rect.x + 5, crafting_btn_rect.y +10))

    shop_btn_rect = pygame.Rect(1180,230,80,40) 
    pygame.draw.rect(screen,(180,100,50),shop_btn_rect) 

    shop_text = small_font.render("Shop",True, (255,255,255))
    screen.blit(shop_text,(shop_btn_rect.x + 18, shop_btn_rect.y +10))

    return greenhouse_btn_rect, crafting_btn_rect, shop_btn_rect