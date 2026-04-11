import pygame

def draw_menu(screen, font, mouse_pos):
    screen.fill((40,40,40))

    start_rect = pygame.Rect(549,250,200,60)
    setting_rect = pygame.Rect(540,350,200,60)
    exit_rect = pygame.Rect(540,450,200,60)

    
    start_clr = (0,255,0) if start_rect.collidepoint(mouse_pos) else (255,255,255)
    setting_clr = (0,255,0) if setting_rect.collidepoint(mouse_pos) else (255,255,255)
    exit_clr = (0,255,0) if exit_rect.collidepoint(mouse_pos) else (255,255,255)

    screen.blit(font.render("START GAME", True, start_clr),(555,260))
    screen.blit(font.render("SETTING", True, setting_clr),(575,360))
    screen.blit(font.render("EXIT GAME", True, exit_clr),(560,460))

    return start_rect, setting_rect, exit_rect