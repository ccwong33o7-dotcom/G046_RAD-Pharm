import pygame

def draw_menu(screen, font, mouse_pos):
    start_rect = pygame.Rect(170,340,250,60)
    setting_rect = pygame.Rect(190,440,200,60)
    exit_rect = pygame.Rect(180,540,200,60)

    normal_color = (255, 228, 196)
    hover_color  = (255, 255, 255)
    outline_color = (80, 80, 80)

    start_clr = hover_color if start_rect.collidepoint(mouse_pos) else normal_color
    setting_clr = hover_color if setting_rect.collidepoint(mouse_pos) else normal_color
    exit_clr = hover_color if exit_rect.collidepoint(mouse_pos) else normal_color

    def draw_outlined_text(text, rect, color, outline_color, offset=2):
        text_surf = font.render(text, True, color)
        outline_surf = font.render(text, True, outline_color)

        text_rect = text_surf.get_rect()
        base_x = rect.x + 5
        base_y = rect.y + 10

        for dx in (-offset, 0, offset):
            for dy in (-offset, 0, offset):
                if dx == 0 and dy == 0:
                    continue
                screen.blit(outline_surf, (base_x + dx, base_y + dy))

        screen.blit(text_surf, (base_x, base_y))

    draw_outlined_text("START GAME", start_rect, start_clr, outline_color)
    draw_outlined_text("SETTING", setting_rect, setting_clr, outline_color)
    draw_outlined_text("EXIT GAME", exit_rect, exit_clr, outline_color)

    return start_rect, setting_rect, exit_rect