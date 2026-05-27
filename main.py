import pygame
import sys
import os
import json
from menu import draw_menu
from setting import run_setting
from pharmacy import draw_pharmacy
from shop import draw_shop
from greenhouse import draw_greenhouse, Plant
from crafting import draw_crafting, update_crafting, animate_crafting
from intro import show_intro
from taskbar import TaskBar

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("music/background_music.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

Width = 1280
Height= 720

screen = pygame.display.set_mode((Width, Height))
try:
   gh_bg_img = pygame.image.load("image/greenhouse_3.png").convert()
   gh_bg_img = pygame.transform.scale(gh_bg_img, (Width, Height))
except:
   gh_bg_img = None
   print("Warning: Greenhouse background image not fount")
try:
   menu_bg_img = pygame.image.load("image/mainmenu.png").convert()
   menu_bg_img = pygame.transform.scale(menu_bg_img, (Width, Height))
except:
   menu_bg_img = None
   print("Warning: MainMenu image not found")
try:
   pharmacy_bg_img = pygame.image.load("image/pharmacy scene.png").convert()
   pharmacy_bg_img = pygame.transform.scale(pharmacy_bg_img, (Width, Height))
except:
   pharmacy_bg_img = None
   print("Warning: Pharmacy scene image not found")
try:
   shop_bg_img = pygame.image.load("image/shop_bg.jpeg").convert()
   shop_bg_img = pygame.transform.scale(shop_bg_img, (Width, Height))
except:
   shop_bg_img = None
   print("Warning: Shop scene image not found")

pygame.display.set_caption("Game")
font = pygame.font.SysFont("Arial",40)

SAVE_FILE = "save_data.json"

def load_game():
    """Reads saved progression data or establishes defaults."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"current_day": 1, "has_seen_intro": False, "pure_soil": 0}

def save_game(day_num, seen_intro, pure_soil_count):
    """Writes active day progression and intro milestones to disk."""
    data = {"current_day": day_num, "has_seen_intro": seen_intro, "pure_soil": pure_soil_count}
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

progress = load_game()
current_day = progress["current_day"]
has_seen_intro = progress["has_seen_intro"]
pure_soil_count = progress.get("pure_soil", 0)
pure_soil_count = 1

has_seen_intro = False

current_state="MENU"
last_state = "MENU"

plant_a = Plant(950, 400, "Glowing Aloe", 0.05)
plant_b = Plant(710, 400, "Rusty Thorn", 0.4)
plants = [plant_a, plant_b]

pygame.event.pump()
pygame.event.clear()

clock= pygame.time.Clock()

task_bar = TaskBar(Width)

while True:
    mouse_pos = pygame.mouse.get_pos()

    if current_state == "MENU":
       screen.fill((0, 0, 0))
       if menu_bg_img:
          screen.blit(menu_bg_img, (0,0))
       s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)

    elif current_state == "INTRO":
        show_intro(screen, clock)
        has_seen_intro = True
        save_game(current_day, has_seen_intro, pure_soil_count)  
        current_state = "PHARMACY" 

    elif current_state == "PHARMACY":
       screen.fill((0, 0, 0))
       greenhouse_btn, crafting_btn, shop_btn = draw_pharmacy(screen, pharmacy_bg_img)

       task_bar.draw(screen, current_day)
       
    elif current_state == "SHOP":
       screen.fill((0, 0, 0))
       shop_buy_soil_btn, shop_back_btn = draw_shop(screen,font, shop_bg_img)
       task_bar.draw(screen,current_day)

    elif current_state == "GREENHOUSE":
       screen.fill((0, 0, 0))
       gh_set_btn, gh_back_btn, gh_upgrade_btn, pure_soil_btn = draw_greenhouse(screen, font, plants,gh_bg_img, pure_soil_count)

       ready_to_craft = all(p.growth >= 100 and not p.is_dead for p in plants)
       any_dead = any(p.is_dead for p in plants)

       if ready_to_craft:
            msg = font.render("MEDICINE READY!", True, (0, 255, 0))
            screen.blit(msg, (Width//2 - 150, 50))
       elif any_dead:
            msg = font.render("CRAFTING FAILED (Plant Died)", True, (255, 0, 0))
            screen.blit(msg, (Width//2 - 200, 50))

       task_bar.draw(screen,current_day)

    elif current_state == "CRAFTING":
      screen.fill((0, 0, 0))
      crafting_btn_set_btn, crafting_back_btn = draw_crafting(screen, font)
      animate_crafting()

      task_bar.draw(screen,current_day)

    elif current_state == "SETTING":
       current_state = run_setting(screen, last_state)
       pygame.event.clear()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        save_game(current_day, has_seen_intro, pure_soil_count)
        pygame.quit()
        sys.exit()
        
      if current_state == "CRAFTING":
         update_crafting(event) 

      if event.type == pygame.MOUSEBUTTONDOWN: 
         if current_state not in ["MENU", "SETTING"]:
            clicked_top = task_bar.check_click(mouse_pos)
            if clicked_top == "settings":
               last_state = current_state 
               current_state = "SETTING"
               continue 
            elif clicked_top == "shop":
               current_state = "SHOP"
               continue
            
         if current_state == "MENU":
             if s_btn.collidepoint(mouse_pos):
                  if not has_seen_intro:
                        current_state = "INTRO"
                  else:
                        current_state = "PHARMACY"  
             elif set_btn.collidepoint(mouse_pos):
                  last_state = "MENU"
                  current_state = "SETTING"
             elif e_btn.collidepoint(mouse_pos):
                   save_game(current_day, has_seen_intro, pure_soil_count)
                   pygame.quit()
                   sys.exit()
         
         elif current_state == "PHARMACY":
            if greenhouse_btn.collidepoint(mouse_pos):
               current_state = "GREENHOUSE"
            elif crafting_btn.collidepoint(mouse_pos):
               current_state = "CRAFTING"
            elif shop_btn.collidepoint(mouse_pos):
               current_state = "SHOP"

         elif current_state == "SHOP":
            if shop_back_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"
            elif shop_buy_soil_btn and shop_buy_soil_btn.collidepoint(mouse_pos):
               pure_soil_count += 1

         elif current_state == "GREENHOUSE":
            if gh_back_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"
            elif gh_upgrade_btn.collidepoint(mouse_pos):
               pass
            elif pure_soil_btn and pure_soil_btn.collidepoint(mouse_pos) and pure_soil_count > 0:
               pure_soil_count -= 1
               for p in plants:
                   if not p.is_dead:
                      p.dust = 0
                      p.growth += 20
                      if p.growth > 100: p.growth = 100
            
            else:
             for p in plants:
                if p.rect.collidepoint(mouse_pos):
                    p.clean()

         elif current_state == "CRAFTING":
            if crafting_back_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"


    pygame.display.flip()
    clock.tick(60)
    