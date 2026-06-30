import pygame

def draw_shop(screen, font, bg_img=None,
              btn_soil=None, btn_oxygen=None,
              btn_canopy=None, btn_30=None,
              btn_50=None, btn_60=None):
    if bg_img:
        screen.blit(bg_img, (0, 0))  
    else:
        screen.fill((200, 230, 255))

    force_small_font = pygame.font.SysFont("Arial", 20, bold=True)

    buy_sedative_btn = pygame.Rect(325, 230, 96, 52)
    if btn_30:
        screen.blit(btn_30, (buy_sedative_btn.x, buy_sedative_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_sedative_btn)

    buy_ration_btn = pygame.Rect(325, 387, 96, 52)
    if btn_30:
        screen.blit(btn_30, (buy_ration_btn.x, buy_ration_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_ration_btn)

    buy_soil_btn = pygame.Rect(718, 230, 96, 52)
    if btn_soil:
        screen.blit(btn_soil, (buy_soil_btn.x, buy_soil_btn.y))
    else:
        pygame.draw.rect(screen, (139, 69, 19), buy_soil_btn)
        buy_text = force_small_font.render("60", True, (255, 255, 255))
        screen.blit(buy_text, (buy_soil_btn.x + 55, buy_soil_btn.y + 12))

    buy_canopy_btn = pygame.Rect(718, 555, 96, 52)
    if btn_canopy:
        screen.blit(btn_canopy, (buy_canopy_btn.x, buy_canopy_btn.y))
    else:
        pygame.draw.rect(screen, (50, 150, 50), buy_canopy_btn)
        canopy_text = force_small_font.render("200", True, (255, 255, 255))
        screen.blit(canopy_text, (buy_canopy_btn.x + 55, buy_canopy_btn.y + 12))

    buy_oxygen_btn = pygame.Rect(718, 387, 96, 52)
    if btn_oxygen:
        screen.blit(btn_oxygen, (buy_oxygen_btn.x, buy_oxygen_btn.y))
    else:
        pygame.draw.rect(screen, (70, 70, 150), buy_oxygen_btn)
        oxygen_text = force_small_font.render("65", True, (255, 255, 255))
        screen.blit(oxygen_text, (buy_oxygen_btn.x + 55, buy_oxygen_btn.y + 12))

    buy_speed_serum_btn = pygame.Rect(1020, 230, 96, 52)
    if btn_50:
        screen.blit(btn_50, buy_speed_serum_btn)
    else:
        pygame.draw.rect(screen, (50, 200, 50), buy_speed_serum_btn)

    buy_blood_stop_btn = pygame.Rect(1020, 387, 96, 52)
    if btn_60:
        screen.blit(btn_60, buy_blood_stop_btn)
    else:
        pygame.draw.rect(screen, (50, 200, 50), buy_blood_stop_btn)

    return (buy_soil_btn, buy_canopy_btn, buy_oxygen_btn, buy_speed_serum_btn, buy_blood_stop_btn, buy_sedative_btn, buy_ration_btn)