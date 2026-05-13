import pygame

def draw_pharmacy(screen, font, bg_img):
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))


    settings_btn_rect = pygame.Rect(1180,20,80,40)
    pygame.draw.rect(screen,(150,50,50),settings_btn_rect)

    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Setting",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +10))

    shop_btn_rect = pygame.Rect(1180,70,80,40)
    pygame.draw.rect(screen,(50,150,50),shop_btn_rect)

    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Shop",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +55))

    greenhouse_btn_rect = pygame.Rect(1180,120,80,40)
    pygame.draw.rect(screen,(50,50,150),greenhouse_btn_rect)

    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Greenhouse",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +100))

    crafting_btn_rect = pygame.Rect(1180,170,80,40)
    pygame.draw.rect(screen,(150,150,50),crafting_btn_rect)
    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Crafting",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +150))

    return settings_btn_rect, shop_btn_rect, greenhouse_btn_rect, crafting_btn_rect