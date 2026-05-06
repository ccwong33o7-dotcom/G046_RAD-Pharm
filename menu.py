import pygame

def draw_menu(screen, font, mouse_pos):

    start_rect = pygame.Rect(170,340,250,60)
    setting_rect = pygame.Rect(190,440,200,60)
    exit_rect = pygame.Rect(180,540,200,60)

    
    start_clr = (205,133,63) if start_rect.collidepoint(mouse_pos) else (92,64,51)
    setting_clr = (205,133,63) if setting_rect.collidepoint(mouse_pos) else (92,64,51)
    exit_clr = (205,133,63) if exit_rect.collidepoint(mouse_pos) else (92,64,51)

    screen.blit(font.render("START GAME", True, start_clr),(start_rect.x + 5, start_rect.y +10))
    screen.blit(font.render("SETTING", True, setting_clr),(setting_rect.x + 10, setting_rect.y +10))
    screen.blit(font.render("EXIT GAME", True, exit_clr),(exit_rect.x + 5, exit_rect.y +10))

    return start_rect, setting_rect, exit_rect