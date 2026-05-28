import os
import pygame
import json
import sys

def run_setting(screen, back_to): 
  UI_font = pygame.font.SysFont("Arial",30)
  clock = pygame.time.Clock()

  popup_width, popup_height = 400,600
  popup_rect = pygame.Rect((1280 - popup_width)//2, (720- popup_height)//2, popup_width, popup_height)

  image_path = "image/Setting_bg.png" 

  try:
        scroll_bg = pygame.image.load(image_path).convert_alpha()
        scroll_bg = pygame.transform.smoothscale(scroll_bg, (popup_width, popup_height))
        print(f"[SUCCESS] Loaded settings background image: {image_path}")
        
  except pygame.error as e:
        print(f"[ERROR] Cannot find or load image: {image_path}. Details: {e}")
        print("Fallback: Using default gray rectangle background.")
        scroll_bg = None

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
        
  music_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + 170, 200, 20)
  sfx_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + 270, 200, 20)
  save_quit_rect = pygame.Rect(popup_rect.centerx - 80, popup_rect.y + 350, 160, 42)
  back_btn_rect = pygame.Rect(popup_rect.centerx - 80, popup_rect.y + 420, 160, 42)
  
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
    
    if scroll_bg:
            screen.blit(scroll_bg, (popup_rect.x, popup_rect.y))
    else:
      pygame.draw.rect(screen, (240, 240, 240), popup_rect, border_radius=15) 
      pygame.draw.rect(screen, (100, 100, 100), popup_rect, width=3, border_radius=15)
      title_font = pygame.font.SysFont("Arial", 40, bold=True)
      title_surf = title_font.render("SETTINGS", True, (50, 50, 50))
      screen.blit(title_surf, (popup_rect.centerx - title_surf.get_width()//2, popup_rect.y + 40))

    text_color = (60, 40, 20)

    label_m = UI_font.render(f"Music Volume: {int(music_volume*100)}%", True, text_color)
    screen.blit(label_m, (music_rect.x, music_rect.y - 35))
    pygame.draw.rect(screen, (210, 190, 160), music_rect)
    pygame.draw.rect(screen, (100, 149, 237), (music_rect.x, music_rect.y, 200 * music_volume, 20))

    label_s = UI_font.render(f"Effect Volume: {int(sfx_volume*100)}%", True, text_color)
    screen.blit(label_s, (sfx_rect.x, sfx_rect.y - 35))
    pygame.draw.rect(screen, (210, 190, 160), sfx_rect)
    pygame.draw.rect(screen, (255, 165, 0), (sfx_rect.x, sfx_rect.y, 200 * sfx_volume, 20))

    sq_color = (60,50,40) if save_quit_rect.collidepoint(mouse_pos) else (90,80,70)
    pygame.draw.rect(screen, sq_color, save_quit_rect, border_radius=5)
    pygame.draw.rect(screen, (50, 40, 30), save_quit_rect, width=2, border_radius=5) 
    sq_surf = UI_font.render("SAVE & QUIT", True, (240, 230, 210))
    screen.blit(sq_surf,(save_quit_rect.centerx - sq_surf.get_width()//2, save_quit_rect.centery - sq_surf.get_height()//2))

    back_color = (80,70,60) if back_btn_rect.collidepoint(mouse_pos) else (110,100,90)
    pygame.draw.rect(screen, back_color, back_btn_rect, border_radius=5)
    pygame.draw.rect(screen, (60, 50, 40), back_btn_rect, width=2, border_radius=5)
    back_surf = UI_font.render("BACK", True, (240, 230, 210))
    screen.blit(back_surf,(back_btn_rect.centerx - back_surf.get_width()//2, back_btn_rect.centery - back_surf.get_height()//2))

    pygame.display.flip()

  return back_to