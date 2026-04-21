import pygame

def run_pharmacy(screen):
    font = pygame.font.SysFont("Arial",30)
    settings_btn_rect = pygame.Rect(700,20,80,40)

    running = True
    while running:
        screen.fill((255,250,200))
        text = font.render("Settings", True, (0,0,0))
        screen.blit(text,(320,250))

        pygame.draw.rect(screen, (150,50,50), back_btn_rect)
        btn_text = font.render("Back", True, (255,255,255))
        screen.blit(btn_text,(back_btn_rect.x + 10, back_btn_rect.y +5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn_rect.collidepoint(event.pos):
                    return "BACK_TO_PHARMACY" 
                
        pygame.display.flip()