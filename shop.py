import pygame

def draw_shop(screen, font, bg_img=None,btn_soil=None, btn_oxygen=None, btn_canopy=None,btn_30=None):
    if bg_img:
        screen.blit(bg_img, (0, 0))  
    else:
        screen.fill((200, 230, 255))

    back_to_pharmacy_btn = pygame.Rect(1180, 140, 80, 40)
    pygame.draw.rect(screen, (100, 100, 250), back_to_pharmacy_btn)

    small_font = pygame.font.SysFont("Arial", 20)
    back_text = small_font.render("Back", True, (255, 255, 255))
    screen.blit(back_text, (back_to_pharmacy_btn.x + 20, back_to_pharmacy_btn.y + 10))

    force_small_font = pygame.font.SysFont("Arial", 20, bold=True)

    buy_sedative_btn = pygame.Rect(277, 210, 147, 80)
    if btn_30:
        screen.blit(btn_30, (buy_sedative_btn.x, buy_sedative_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_sedative_btn)

    buy_ration_btn = pygame.Rect(277, 365, 147, 80)
    if btn_30:
        screen.blit(btn_30, (buy_ration_btn.x, buy_ration_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_ration_btn)

    buy_soil_btn = pygame.Rect(720, 210, 160, 50)
    if btn_soil:
        screen.blit(btn_soil, (buy_soil_btn.x, buy_soil_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_soil_btn)
        buy_text = force_small_font.render("195", True, (255, 255, 255))
        screen.blit(buy_text, (buy_soil_btn.x + 55, buy_soil_btn.y + 12))

    buy_canopy_btn = pygame.Rect(720, 513, 160, 50)
    if btn_canopy:
        screen.blit(btn_canopy, (buy_canopy_btn.x, buy_canopy_btn.y))
    else:
        pygame.draw.rect(screen, (50, 150, 50), buy_canopy_btn)
        canopy_text = force_small_font.render("225", True, (255, 255, 255))
        screen.blit(canopy_text, (buy_canopy_btn.x + 55, buy_canopy_btn.y + 12))

    buy_oxygen_btn = pygame.Rect(720, 361, 160, 50)
    if btn_oxygen:
        screen.blit(btn_oxygen, (buy_oxygen_btn.x, buy_oxygen_btn.y))
    else:
        pygame.draw.rect(screen, (70, 70, 150), buy_oxygen_btn)
        oxygen_text = force_small_font.render("200", True, (255, 255, 255))
        screen.blit(oxygen_text, (buy_oxygen_btn.x + 55, buy_oxygen_btn.y + 12))

    return buy_soil_btn, buy_canopy_btn, buy_oxygen_btn, back_to_pharmacy_btn