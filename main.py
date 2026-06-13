import pygame
import sys
import os
import json
from menu import draw_menu
from setting import run_setting
import pharmacy 
from shop import draw_shop
from greenhouse import draw_greenhouse, Plant, draw_plant_menu
from crafting import draw_crafting, update_crafting, animate_crafting, inventory 
from intro import show_intro
from taskbar import TaskBar
from map import draw_map
from weather import WeatherSystem

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("music/background_music.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

Width = 1280
Height= 720

screen = pygame.display.set_mode((Width, Height))
try:
   gh_bg_img = pygame.image.load("image/background/greenhouse_3.png").convert()
   gh_bg_img = pygame.transform.smoothscale(gh_bg_img, (Width, Height))
except:
   gh_bg_img = None
   print("Warning: Greenhouse background image not fount")
try:
   menu_bg_img = pygame.image.load("image/background/mainmenu.png").convert()
   menu_bg_img = pygame.transform.smoothscale(menu_bg_img, (Width, Height))
except:
   menu_bg_img = None
   print("Warning: MainMenu image not found")
try:
   pharmacy_bg_img = pygame.image.load("image/background/Pharmacy_bg.png").convert()
   pharmacy_bg_img = pygame.transform.smoothscale(pharmacy_bg_img, (Width, Height))
   pharmacy_counter_img = pygame.image.load("image/button/counterbgnew.png").convert_alpha()
except:
   pharmacy_bg_img = None
   pharmacy_counter_img = None
   print("Warning: Pharmacy scene image not found")
try:
   shop_bg_img = pygame.image.load("image/background/shopwithouttb.png").convert()
   shop_bg_img = pygame.transform.smoothscale(shop_bg_img, (Width, Height))
except:
   shop_bg_img = None
   print("Warning: Shop scene image not found")
try:
    crafting_bg_img = pygame.image.load("image/background/lab_without_taskbar.png").convert()
    crafting_bg_img = pygame.transform.smoothscale(crafting_bg_img, (Width, Height))
except:
    crafting_bg_img = None
    print("Warning: Crafting background image not found")
try:
    map_bg_img = pygame.image.load("image/background/Map background.png").convert()
    map_bg_img = pygame.transform.smoothscale(map_bg_img, (Width, Height))
except:
    map_bg_img = None
    print("Warning: Map background image not found")
try:
    survivor_icon_img = pygame.image.load("image/icon/survivor.jpg").convert_alpha()
    survivor_icon_img = pygame.transform.smoothscale(survivor_icon_img, (50, 50))
except Exception as e:
    survivor_icon_img = None
    print(f"Warning: Failed to load survivor kit icon: {e}")
try:
    btn_soil = pygame.image.load("image/button/195_button.png").convert_alpha()
    btn_soil = pygame.transform.smoothscale(btn_soil, (96, 52))
    
    btn_oxygen = pygame.image.load("image/button/200_button.png").convert_alpha()
    btn_oxygen = pygame.transform.smoothscale(btn_oxygen, (96, 52))
    
    btn_canopy = pygame.image.load("image/button/225_button.png").convert_alpha()
    btn_canopy = pygame.transform.smoothscale(btn_canopy, (96, 52))
    
    btn_30 = pygame.image.load("image/button/30_button.png").convert_alpha()
    btn_30 = pygame.transform.smoothscale(btn_30, (96,52))

    btn_50 = pygame.image.load("image/button/50_button.png").convert_alpha()
    btn_50 = pygame.transform.smoothscale(btn_50, (96,52))

    btn_60 = pygame.image.load("image/button/60_button.png").convert_alpha()    
    btn_60 = pygame.transform.smoothscale(btn_60, (96,52))
except Exception as e:
    btn_soil = btn_oxygen = btn_canopy = btn_30 = btn_50 = btn_60 = None
    print(f"Warning: Failed to load price button images: {e}")

try:
    img_pharmacy = pygame.image.load("image/button/PH_button.png").convert_alpha()
    img_pharmacy = pygame.transform.smoothscale(img_pharmacy, (270, 200))

    img_lab = pygame.image.load("image/button/Lab_button.png").convert_alpha()
    img_lab = pygame.transform.smoothscale(img_lab, (280, 210))

    img_shop = pygame.image.load("image/button/Shop_button.png").convert_alpha()
    img_shop = pygame.transform.smoothscale(img_shop, (260, 190))

    img_greenhouse = pygame.image.load("image/button/GH_button.png").convert_alpha()
    img_greenhouse = pygame.transform.smoothscale(img_greenhouse, (270, 200))
except Exception as e:
    img_pharmacy = img_lab = img_shop = img_greenhouse = None
    print(f"Warning: Failed to load map building buttons: {e}")



pygame.display.set_caption("Game")
font = pygame.font.SysFont("Arial",40)
msg_font = pygame.font.SysFont("Comic Sans MS", 26)
ui_font = pygame.font.SysFont("Agency FB", 36, bold=True)

SAVE_FILE = "save_data.json"

def load_game():
    """Reads saved progression data or establishes defaults."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "current_day": 1, 
        "has_seen_intro": False, 
        "pure_soil": 0, 
        "has_intact_canopy": False, 
        "has_oxygen_recycler": False,
        "cookies": 5,
        "saved_people": 0,
        "sedative": 0,
        "ration_pack": 0,
        "speed_serum": 0,
        "blood_stop": 0
    }

def save_game(day_num, seen_intro, pure_soil_count, has_intact_canopy, has_oxygen_recycler, cookies_amt, saved_people_count):
    """Writes active day progression and intro milestones to disk."""
    data = {
       "current_day": day_num, 
       "has_seen_intro": seen_intro, 
       "pure_soil": pure_soil_count, 
       "has_intact_canopy": has_intact_canopy, 
       "has_oxygen_recycler": has_oxygen_recycler,
       "cookies": cookies_amt,
       "saved_people": saved_people_count,
       "sedative": progress.get("sedative", 0),
       "ration_pack": progress.get("ration_pack", 0),
       "speed_serum": int(has_Speed_Serum),
       "blood_stop": int(has_Blood_Stop)
       }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

progress = load_game()
current_day = progress["current_day"]
has_seen_intro = progress["has_seen_intro"]

pure_soil_count = progress.get("pure_soil", 0)
pure_soil_count = int(pure_soil_count) if isinstance(pure_soil_count, (int, float)) else 0

has_intact_canopy = progress.get("has_intact_canopy", False)
has_oxygen_recycler = progress.get("has_oxygen_recycler", False)

intact_canopy_count = 1 if has_intact_canopy else 0
oxygen_recycler_count = 1 if has_oxygen_recycler else 0

cookies_count = progress.get("cookies", 5)
saved_people = progress.get("saved_people", 0)

has_Speed_Serum = bool(progress.get("speed_serum", 0))
has_Blood_Stop = bool(progress.get("blood_stop", 0))
oxygen_recycler_active = 1 if has_oxygen_recycler else 0
intact_canopy_active = 1 if has_intact_canopy else 0

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
weather_sys = WeatherSystem()
weather_sys.update_weather(current_day)

flash_message = ""
flash_message_timer = 0

def trigger_message(text):
    global flash_message, flash_message_timer
    flash_message = text
    flash_message_timer = 180

show_plant_menu = False
plant_menu_rect = pygame.Rect(0, 0, 0, 0)
aloe_btn_rect = pygame.Rect(0, 0, 0, 0)  
thorn_btn_rect = pygame.Rect(0, 0, 0, 0)

initial_count = min(current_day, 4)
pharmacy.change_customer_count(initial_count)
print(f"Game Started: Initialized {initial_count} customers for Day {current_day}")

has_money_on_table = False

pharmacy_buttons = {
    "sell_rad": pygame.Rect(850, 450, 200, 50),
    "gun": pygame.Rect(180, 480, 120, 120),
    "money": pygame.Rect(720, 430, 100, 100)
}

while True:
    mouse_pos = pygame.mouse.get_pos()

    if saved_people >= 25:
        current_day += 1
        saved_people = 0 
        print(f"Day Cleared! Welcome to Day {current_day}!")
        
        if current_day > 10:
            print("Victory! You survived all 10 days!")
            current_day = 1 
            
        weather_sys.update_weather(current_day) 
        next_day_customers = min(current_day, 4)
        pharmacy.change_customer_count(next_day_customers)
        print(f"New Day! Spawned {next_day_customers} customers.")
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, has_oxygen_recycler, cookies_count, saved_people)

    if current_state == "MENU":
       screen.fill((0, 0, 0))
       if menu_bg_img:
          screen.blit(menu_bg_img, (0,0))
       s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)

    elif current_state == "INTRO":
        show_intro(screen, clock)
        has_seen_intro = True
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, has_oxygen_recycler, cookies_count, saved_people)
        current_state = "WEATHER_EXPLAIN" 

    elif current_state == "WEATHER_EXPLAIN":
        if pharmacy_bg_img:
            screen.blit(pharmacy_bg_img, (0, 0))
        else:
            screen.fill((50, 50, 50))
            
        overlay = pygame.Surface((Width, Height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180) 
        screen.blit(overlay, (0, 0))
        
        next_state = weather_sys.show_weather_explanation(screen, clock)
        if next_state:
            current_state = next_state
            
    elif current_state == "PHARMACY":
        screen.fill((0, 0, 0))
        pharmacy_buttons = pharmacy.draw_pharmacy(screen, pharmacy_bg_img, pharmacy_counter_img, has_money_on_table, progress)
    
    elif current_state == "MAP":
       screen.fill((0, 0, 0))
       to_gh_btn, to_shop_btn, to_craft_btn, to_pharmacy_btn = draw_map(screen, map_bg_img, font, mouse_pos, img_greenhouse, img_shop, img_lab, img_pharmacy)
       
    elif current_state == "SHOP":
       screen.fill((0, 0, 0))
       (shop_buy_soil_btn, shop_buy_canopy_btn, shop_buy_oxygen_btn, 
        shop_buy_speed_serum_btn, shop_buy_blood_stop_btn, 
        shop_buy_sedative_btn, shop_buy_ration_btn) = draw_shop(
            screen, font, shop_bg_img, btn_soil, btn_oxygen, btn_canopy, btn_30, btn_50, btn_60
        )

    elif current_state == "GREENHOUSE":
       screen.fill((0, 0, 0))
       ready_to_craft = all(p.growth >= 100 and not p.is_dead for p in plants)
       any_dead = any(p.is_dead for p in plants)
       gh_upgrade_btn, pure_soil_btn, oxygen_btn, plant_seed_btn, harvest_btn = draw_greenhouse(screen, font, plants,gh_bg_img, pure_soil_count, oxygen_recycler_count, intact_canopy_count, has_intact_canopy, has_oxygen_recycler, ready_to_craft)

       if ready_to_craft:
            msg = font.render("HARVEST AVAILABLE!", True, (0, 255, 0))
            screen.blit(msg, (Width//2 - 150, 50))
       elif any_dead:
            msg = font.render("CRAFTING FAILED (Plant Died)", True, (255, 0, 0))
            screen.blit(msg, (Width//2 - 200, 50))
       if show_plant_menu:
           plant_menu_rect, aloe_btn_rect, thorn_btn_rect = draw_plant_menu(screen)
           
    elif current_state == "CRAFTING":
      screen.fill((0, 0, 0))
      _, crafting_back_btn = draw_crafting(screen, crafting_bg_img, font)
      animate_crafting()

    elif current_state == "SETTING":
       current_state = run_setting(screen, last_state)
       pygame.event.clear()

    if current_state not in ["MENU", "SETTING", "INTRO", "WEATHER_EXPLAIN"]:
        task_bar.draw(screen, current_day, cookies_count, saved_people, weather_sys)

    if flash_message_timer > 0:
        flash_message_timer -= 1

        text_surf = msg_font.render(flash_message, True, (160, 160, 160))
        text_surf = text_surf.convert_alpha()  

        if flash_message_timer < 60:
            alpha = int((flash_message_timer / 60) * 255)
        else:
            alpha = 255
        text_surf.set_alpha(alpha)

        text_rect = text_surf.get_rect(center=(Width // 2, Height - 50))
        
        screen.blit(text_surf, text_rect)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, has_oxygen_recycler, cookies_count, saved_people)
        pygame.quit()
        sys.exit()
        
      if current_state == "CRAFTING":
         update_crafting(event)

      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_k:
              saved_people += 1
              print(f"Test: Saved 1 person. Progress: {saved_people}/25") 
          if event.key == pygame.K_h:
              for p in plants:
                  p.growth = 100
                  p.is_dead = False
                  p.harvested = False
              print("Test: All plants are now fully grown! Press Harvest Button now!")

          if event.key == pygame.K_1:
              pharmacy.change_customer_count(1)
              print("Test Key: Switched to 1 customer")
          if event.key == pygame.K_2:
              pharmacy.change_customer_count(2)
              print("Test Key: Switched to 2 customers")
          if event.key == pygame.K_3:
              pharmacy.change_customer_count(3)
              print("Test Key: Switched to 3 customers")
          if event.key == pygame.K_4:
              pharmacy.change_customer_count(4)
              print("Test Key: Switched to 4 customers")

      if event.type == pygame.MOUSEBUTTONDOWN: 
         if current_state not in ["MENU", "SETTING","INTRO", "WEATHER_EXPLAIN"]:
            clicked_top = task_bar.check_click(mouse_pos)
            if clicked_top == "settings":
               last_state = current_state 
               current_state = "SETTING"
               continue 
            elif clicked_top == "map":
               current_state = "MAP"
               continue
            elif clicked_top == "weather":
               print(f"TaskBar: Weather Icon Clicked! Current weather is {weather_sys.current_weather}")
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
                   save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, has_oxygen_recycler, cookies_count, saved_people)
                   pygame.quit()
                   sys.exit()
         elif current_state == "PHARMACY":

             if pharmacy_buttons["sell_rad"].collidepoint(mouse_pos):

                 if inventory.get("Rad-Ointment", 0) > 0:
                        inventory["Rad-Ointment"] -= 1
                        has_money_on_table = True 
                        trigger_message("Buyer left cookies on the counter! Click it to collect!")
                 else:
                     trigger_message("No Rad-Ointment left to sell!")

             elif pharmacy_buttons["gun"].collidepoint(mouse_pos):
                print("Gun clicked!")
                trigger_message("You grabbed the Gun! Ready to shoot.")
                    
             elif has_money_on_table and pharmacy_buttons["money"].collidepoint(mouse_pos):
                cookies_count += 20
                saved_people += 1
                has_money_on_table = False 
                print("Cookies collected!")
                trigger_message("+20 Cookies collected into wallet!")
         
         elif current_state == "MAP":
            if to_gh_btn.collidepoint(mouse_pos):
               current_state = "GREENHOUSE"
               print("Entering to Greenhouse...")
            elif to_shop_btn.collidepoint(mouse_pos):
               current_state = "SHOP"
               print("Entering to Shop...")
            elif to_craft_btn.collidepoint(mouse_pos):
               current_state = "CRAFTING"
               print("Entering to Crafting...")
            elif to_pharmacy_btn.collidepoint(mouse_pos):
               current_state = "PHARMACY"
               print("Entering to Pharmacy...")

         elif current_state == "SHOP":
             if shop_buy_sedative_btn.collidepoint(mouse_pos):
                 if cookies_count >= 30:
                     cookies_count -= 30
                     progress["sedative"] += 1
                     trigger_message("Sedative purchased! Pharmacy updated.")
                 else:
                     trigger_message("Not enough Cookies for Sedative!")

             elif shop_buy_ration_btn.collidepoint(mouse_pos):
                 if cookies_count >= 30:
                     cookies_count -= 30
                     progress["ration_pack"] += 1
                     trigger_message("Ration Pack purchased! Pharmacy updated.")
                 else:
                     trigger_message("Not enough Cookies for Ration Pack!")

             elif shop_buy_soil_btn and shop_buy_soil_btn.collidepoint(mouse_pos):
                 if cookies_count >= 195:
                     cookies_count -= 195
                     pure_soil_count += 1
                     trigger_message("Pure Soil purchased!")
                 else:
                     trigger_message("Not enough Cookies for Pure Soil!")

             elif shop_buy_canopy_btn and shop_buy_canopy_btn.collidepoint(mouse_pos):
                 print(f"DEBUG: Clicked Canopy Button! Current status: {has_intact_canopy}")
                 if has_intact_canopy:
                     trigger_message("You already own Intact Canopy!")
                 elif cookies_count >= 225:
                     cookies_count -= 225
                     has_intact_canopy = True
                     intact_canopy_count = 1
                     trigger_message("Intact Canopy purchased!")
                 else:
                     trigger_message("Not enough Cookies for Intact Canopy!")

             elif shop_buy_oxygen_btn and shop_buy_oxygen_btn.collidepoint(mouse_pos):
                 print(f"DEBUG: Clicked Oxygen Button! Current status: {has_oxygen_recycler}")
                 if has_oxygen_recycler:
                     trigger_message("You already own Oxygen Recycler!")
                 elif cookies_count >= 200:
                     cookies_count -= 200
                     has_oxygen_recycler = True
                     oxygen_recycler_count = 1
                     trigger_message("Oxygen Recycler purchased!")
                 else:
                     trigger_message("Not enough Cookies for Oxygen Recycler!")

             elif shop_buy_speed_serum_btn and shop_buy_speed_serum_btn.collidepoint(mouse_pos):
                 if cookies_count >= 50:
                     cookies_count -= 50
                     has_Speed_Serum = True
                     trigger_message("Speed Serum purchased!")
                 else:
                     trigger_message("Not enough Cookies for Speed Serum!")

             elif shop_buy_blood_stop_btn and shop_buy_blood_stop_btn.collidepoint(mouse_pos):
                 if cookies_count >= 60:
                     cookies_count -= 60
                     has_Blood_Stop = True
                     trigger_message("Blood Stop purchased!")
                 else:
                     trigger_message("Not enough Cookies for Blood Stop!")
 
         elif current_state == "GREENHOUSE":
            if show_plant_menu:
                if aloe_btn_rect.collidepoint(mouse_pos):
                    print("Clicked Aloe Vera! Planting Aloe Vera seed...")

                    plant_a.growth = 0
                    plant_a.dust = 0
                    plant_a.is_dead = False
                    show_plant_menu = False
                    trigger_message("Aloe Vera planted!")
                    
                elif thorn_btn_rect.collidepoint(mouse_pos):
                    print("Clicked Rusty Thorn! Planting Rusty Thorn seed...")
                    plant_b.growth = 0
                    plant_b.dust = 0
                    plant_b.is_dead = False
                    show_plant_menu = False 
                    trigger_message("Rusty Thorn planted!")
                    
                elif not plant_menu_rect.collidepoint(mouse_pos):
                    show_plant_menu = False
                    print("Closed Plant Menu")
                continue
            if plant_seed_btn.collidepoint(mouse_pos):
               print("Opening Plant Seed Menu...")
               show_plant_menu = True  
            elif harvest_btn.collidepoint(mouse_pos):
                harvested_something = False
                for p in plants:
                     if p.growth >= 100 and not p.harvested and not p.is_dead:
                           
                           if p.name in inventory:
                               inventory[p.name] += 1
                           else:
                               inventory[p.name] = 1
                           
                           p.growth = 0
                           p.dust = 0
                           p.harvested = False
                           harvested_something = True
                           print(f"Harvested {p.name} added to lab!")
                           print(f"Current amount: {inventory[p.name]}")

                if harvested_something:
                    print("Harvest successful!")    
                else:
                     print("No plants ready to harvest!")
                

            elif gh_upgrade_btn.collidepoint(mouse_pos):
               if has_intact_canopy:
                  print("You clicked the Intact Canopy! Now you can implement its effect.")

            elif pure_soil_btn and pure_soil_btn.collidepoint(mouse_pos) and pure_soil_count > 0:
               pure_soil_count -= 1
               for p in plants:
                   if not p.is_dead:
                      p.dust = 0
                      p.growth += 20
                      if p.growth > 100: p.growth = 100
            
            elif oxygen_btn and oxygen_btn.collidepoint(mouse_pos) and has_oxygen_recycler:
               has_oxygen_recycler = False
               oxygen_recycler_count = 0

               for p in plants:
                     if not p.is_dead:
                        p.growth += 30
                        if p.growth >100: p.growth = 100
            
            else:
             for p in plants:
                if p.rect.collidepoint(mouse_pos):
                    p.clean()

         elif current_state == "CRAFTING":
            if crafting_back_btn.collidepoint(mouse_pos):
               current_state = "MAP"

         


    pygame.display.flip()
    clock.tick(60)
    