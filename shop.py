import pygame

def draw_shop(screen, font):
    screen.fill((200,230,255))

    text = font.render("Welcome to the SHOP", True,(0,0,0))
    screen.blit(text,(1280//2-100,720//2))

    settings_btn_rect = pygame.Rect(1150,30,100,40)
    pygame.draw.rect(screen,(150,50,50),settings_btn_rect)

    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Setting",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +10))

    back_to_pharmacy_btn = pygame.Rect(1180,70,80,40)
    pygame.draw.rect(screen,(100,100,250),back_to_pharmacy_btn)

    back_text = small_font.render("Back",True, (255,255,255))
    screen.blit(back_text,(back_to_pharmacy_btn.x + 20, back_to_pharmacy_btn.y + 10))

    return settings_btn_rect, back_to_pharmacy_btn