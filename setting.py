import os
import pygame
import json
import sys

def run_setting(screen, back_to): 
  title_font = pygame.font.SysFont("Arial",50,bold=True)
  UI_font = pygame.font.SysFont("Arial",30)
  clock = pygame.time.Clock()

  title_font = pygame.font.SysFont("Arial",40,bold=True)

  popup_width, popup_height = 400,500
  popup_rect = pygame.Rect((1280 - popup_width)//2, (720- popup_height)//2, popup_width, popup_height)

  overlay = pygame.Surface((1280,720), pygame.SRCALPHA)
  overlay.fill((0, 0, 0, 150))

  settings_path = "settings.json"
  music_volume, sfx_volume = 0.5, 0.5 

  if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                data = json.load(f)
                music_volume = data.get("music_volume", 0.5)
                sfx_volume = data.get("sfx_volume", 0.5)
        except: pass

  pygame.mixer.music.set_volume(music_volume)

  def save_settings():
     with open("settings.json","w") as f:
        json.dump({"music_volume": music_volume, "sfx_volume": sfx_volume},f)
        
  music_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + 150, 200, 20)
  sfx_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + 250, 200, 20)
  save_quit_rect = pygame.Rect(popup_rect.centerx - 80, popup_rect.y + 330, 160, 45)
  back_btn_rect = pygame.Rect(popup_rect.centerx - 80, popup_rect.y + 400, 160, 45)
  
  background_snapshot = screen.copy()

  setting_running = True
  while setting_running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        save_settings()
        pygame.quit()
        sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if save_quit_rect.collidepoint(mouse_pos):
          save_settings()
          pygame.quit()
          sys.exit()

        if back_btn_rect.collidepoint(mouse_pos):
          save_settings()
          setting_running = False
           

    if mouse_pressed[0]:
        if music_rect.collidepoint(mouse_pos):
           music_volume = (mouse_pos[0] - music_rect.x) / music_rect.width
           music_volume = max(0.0, min(1.0, music_volume))
           pygame.mixer.music.set_volume(music_volume)
            
        elif sfx_rect.collidepoint(mouse_pos):
           sfx_volume = (mouse_pos[0] - sfx_rect.x) / sfx_rect.width
           sfx_volume = max(0.0, min(1.0, sfx_volume))

    screen.blit(background_snapshot, (0, 0)) 
    screen.blit(overlay,(0,0))
    
    pygame.draw.rect(screen, (240, 240, 240), popup_rect, border_radius=15) 
    pygame.draw.rect(screen, (100, 100, 100), popup_rect, width=3, border_radius=15)

    title_surf = title_font.render("SETTINGS",True,(50,50,50))
    screen.blit(title_surf,(popup_rect.centerx - title_surf.get_width()//2, popup_rect.y + 40))

    label_m = UI_font.render(f"Music Volume: {int(music_volume*100)}%", True, (50, 50, 50))
    screen.blit(label_m, (music_rect.x, music_rect.y - 35))
    pygame.draw.rect(screen, (200, 200, 200), music_rect)
    pygame.draw.rect(screen, (100, 149, 237), (music_rect.x, music_rect.y, 200 * music_volume, 20))

    label_s = UI_font.render(f"Effect Volume: {int(sfx_volume*100)}%", True, (50, 50, 50))
    screen.blit(label_s, (sfx_rect.x, sfx_rect.y - 35))
    pygame.draw.rect(screen, (200, 200, 200), sfx_rect)
    pygame.draw.rect(screen, (255, 165, 0), (sfx_rect.x, sfx_rect.y, 200 * sfx_volume, 20))

    sq_color = (80,80,80) if save_quit_rect.collidepoint(mouse_pos) else (130,130,130)
    pygame.draw.rect(screen, sq_color, save_quit_rect)
    sq_surf = UI_font.render("SAVE & QUIT", True, (255,255,255))
    screen.blit(sq_surf,(save_quit_rect.centerx - sq_surf.get_width()//2, save_quit_rect.centery - sq_surf.get_height()//2))

    back_color = (120,120,120) if back_btn_rect.collidepoint(mouse_pos) else (180,180,180)
    pygame.draw.rect(screen, back_color, back_btn_rect)
    back_surf = UI_font.render("BACK", True, (255,255,255))
    screen.blit(back_surf,(back_btn_rect.centerx - back_surf.get_width()//2, back_btn_rect.centery - back_surf.get_height()//2))

    pygame.display.flip()

  return back_to