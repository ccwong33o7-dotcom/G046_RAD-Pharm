import os
import pygame
import json

def run_setting(screen, back_to): 
  title_font = pygame.font.SysFont("Arial",50,bold=True)
  UI_font = pygame.font.SysFont("Arial",30)
  clock = pygame.time.Clock()

  settings_path = "settings.json"
  music_volume, sfx_volume = 0.5, 0.5 
  if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                data = json.load(f)
                music_volume = data.get("music_volume", 0.5)
                sfx_volume = data.get("sfx_volume", 0.5)
        except: pass

  music_rect = pygame.Rect(540, 280, 200, 20)
  sfx_rect = pygame.Rect(540, 360, 200, 20)
  save_btn_rect = pygame.Rect(540, 450, 200, 50)
  
  setting_running = True
  while setting_running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if save_btn_rect.collidepoint(mouse_pos):
          with open("settings.json", "w") as f:
            json.dump({"music_volume":music_volume, "sfx_volume" : sfx_volume}, f)
          setting_running = False

    if mouse_pressed[0]:
        if music_rect.collidepoint(mouse_pos):
           music_volume = (mouse_pos[0] - music_rect.x) / music_rect.width
           music_volume = max(0.0, min(1.0, music_volume))
            
        elif sfx_rect.collidepoint(mouse_pos):
           sfx_volume = (mouse_pos[0] - sfx_rect.x) / sfx_rect.width
           sfx_volume = max(0.0, min(1.0, sfx_volume))

    screen.fill((255,255,255))
    title_surf = title_font.render("SETTINGS",True,(50,50,50))
    screen.blit(title_surf,(540,180))

    label_m = UI_font.render(f"Music Volume: {int(music_volume*100)}%", True, (50, 50, 50))
    screen.blit(label_m, (540, 250))
    pygame.draw.rect(screen, (200, 200, 200), music_rect)
    pygame.draw.rect(screen, (100, 149, 237), (music_rect.x, music_rect.y, 200 * music_volume, 20))

    label_s = UI_font.render(f"Effect Volume: {int(sfx_volume*100)}%", True, (50, 50, 50))
    screen.blit(label_s, (540, 330))
    pygame.draw.rect(screen, (200, 200, 200), sfx_rect)
    pygame.draw.rect(screen, (255, 165, 0), (sfx_rect.x, sfx_rect.y, 200 * sfx_volume, 20))

    btn_color = (120,120,120) if save_btn_rect.collidepoint(mouse_pos) else (180,180,180)
    pygame.draw.rect(screen, btn_color, save_btn_rect)

    save_surf = UI_font.render("SAVE & QUIT",True, (255,255,255))
    screen.blit(save_surf,(save_btn_rect.x +20, save_btn_rect.y +10))

    pygame.display.flip()

  return back_to