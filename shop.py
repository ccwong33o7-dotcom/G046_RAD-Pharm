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

    return None, back_to_pharmacy_btn