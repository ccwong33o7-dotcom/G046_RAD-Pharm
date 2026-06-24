import pygame

def draw_menu(screen, font, mouse_pos):

    start_rect = pygame.Rect(170,340,250,60)
    setting_rect = pygame.Rect(190,440,200,60)
    exit_rect = pygame.Rect(180,540,200,60)

    
    start_clr = (255,255,255) if start_rect.collidepoint(mouse_pos) else (181, 101, 29)
    setting_clr = (255,255,255) if setting_rect.collidepoint(mouse_pos) else (181, 101, 29)
    exit_clr = (255,255,255) if exit_rect.collidepoint(mouse_pos) else (181, 101, 29)

    shadow_clr = (80, 80, 80)

    offset_x = 2
    offset_y = 2

    start_text_shadow = font.render("START GAME", True, shadow_clr)
    start_text_front = font.render("START GAME", True, start_clr)
    screen.blit(start_text_shadow, (start_rect.x + 5 + offset_x, start_rect.y + 10 + offset_y))
    screen.blit(start_text_front, (start_rect.x + 5, start_rect.y + 10))

    setting_text_shadow = font.render("SETTING", True, shadow_clr)
    setting_text_front = font.render("SETTING", True, setting_clr)
    screen.blit(setting_text_shadow, (setting_rect.x + 10 + offset_x, setting_rect.y + 10 + offset_y))
    screen.blit(setting_text_front, (setting_rect.x + 10, setting_rect.y + 10))

    exit_text_shadow = font.render("EXIT GAME", True, shadow_clr)
    exit_text_front = font.render("EXIT GAME", True, exit_clr)
    screen.blit(exit_text_shadow, (exit_rect.x + 5 + offset_x, exit_rect.y + 10 + offset_y))
    screen.blit(exit_text_front, (exit_rect.x + 5, exit_rect.y + 10))

    return start_rect, setting_rect, exit_rect