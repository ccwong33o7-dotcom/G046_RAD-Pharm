import pygame

def draw_shop(screen, font, bg_img=None):
    if bg_img:
        screen.blit(bg_img, (0, 0))  
    else:
        screen.fill((200, 230, 255))

    back_to_pharmacy_btn = pygame.Rect(1180, 140, 80, 40)
    pygame.draw.rect(screen, (100, 100, 250), back_to_pharmacy_btn)

    small_font = pygame.font.SysFont("Arial", 20)
    back_text = small_font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, (back_to_pharmacy_btn.x + 20, back_to_pharmacy_btn.y + 10))

    but_soil_btn = pygame.Rect(200, 300, 200, 60)
    pygame.draw.rect(screen, (139, 69, 19), but_soil_btn)
    but_text = font.render("Buy Pure Soil", True, (255, 255, 255))
    screen.blit(but_text, (but_soil_btn.x + 10, but_soil_btn.y + 10))

    return but_soil_btn, back_to_pharmacy_btn