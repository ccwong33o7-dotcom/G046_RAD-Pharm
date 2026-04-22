import pygame
import json

def run_setting(screen): 
  title_font = pygame.font.SysFont("Arial",50,bold=True)
  UI_font = pygame.font.SysFont("Arial",30)

  volume = 0.5
  slider_rect = pygame.Rect(540,300,200,20)
  save_btn_rect = pygame.Rect(540,400,200,50)

  setting_running = True
  while setting_running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if slider_rect.collidepoint(mouse_pos):
          volume = (mouse_pos[0] - slider_rect.x) / slider_rect.width 
          volume = max(0.0, min(1.0, volume))
        if save_btn_rect.collidepoint(mouse_pos):
          with open("settings.json", "w") as f:
            json.dump({"volume":volume}, f)
          setting_running = False

    screen.fill((255,255,255))
    title_surf = title_font.render("SETTINGS",True,(50,50,50))
    screen.blit(title_surf,(540,200))

    pygame.draw.rect(screen,(200,200,200),slider_rect)
    pygame.draw.rect(screen,(100,149,237),(slider_rect.x, slider_rect.y,200*volume,20))

    btn_color = (120,120,120) if save_btn_rect.collidepoint(mouse_pos) else (180,180,180)
    pygame.draw.rect(screen, btn_color, save_btn_rect)

    save_surf = UI_font.render("SAVE & QUIT",True, (255,255,255))
    screen.blit(save_surf,(save_btn_rect.x +20, save_btn_rect.y +10))

  pygame.display.flip()