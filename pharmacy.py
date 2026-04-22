import pygame

def draw_pharmacy(screen, font):
    screen.fill((255,250,200))

    text = font.render("Pharmacy Room", True,(0,0,0))
    screen.blit(text,(1280//2-100,720//2))

    settings_btn_rect = pygame.Rect(1180,20,80,40)
    pygame.draw.rect(screen,(150,50,50),settings_btn_rect)

    small_font = pygame.font.SysFont("Arial",20)
    btn_text = small_font.render("Set",True, (255,255,255))
    screen.blit(btn_text,(settings_btn_rect.x + 15, settings_btn_rect.y +10))

    return settings_btn_rect