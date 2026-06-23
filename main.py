import pygame
import sys
import os
import json
import random
import math
from menu import draw_menu
from setting import run_setting
import pharmacy
from shop import draw_shop
from greenhouse import draw_greenhouse, Plant
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
    gh_fixed_bg_img = pygame.image.load("image/background/Greenhouse2.png").convert()
    gh_fixed_bg_img = pygame.transform.smoothscale(gh_fixed_bg_img, (Width, Height))
except:
    gh_fixed_bg_img = None
    print("Warning: Fixed greenhouse background not found")
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
    crafting_bg_img = pygame.image.load("image/background/Final_Lab_Background.jpeg").convert()
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
    btn_soil = pygame.image.load("image/button/60_button2.png").convert_alpha()
    btn_soil = pygame.transform.smoothscale(btn_soil, (96, 52))
    
    btn_oxygen = pygame.image.load("image/button/65_button.png").convert_alpha()
    btn_oxygen = pygame.transform.smoothscale(btn_oxygen, (96, 52))
    
    btn_canopy = pygame.image.load("image/button/150_button.png").convert_alpha()
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

try:
    acid_buy_img = pygame.image.load("image/button/buy.png").convert_alpha()
    acid_buy_img = pygame.transform.smoothscale(acid_buy_img, (300, 105))

    acid_cancel_img = pygame.image.load("image/button/cancel.png").convert_alpha()
    acid_cancel_img = pygame.transform.smoothscale(acid_cancel_img, (300, 105))
except Exception as e:
    acid_buy_img = None
    acid_cancel_img = None
    print(f"Warning: Acid rain buttons not found: {e}")



pygame.display.set_caption("Game")
font = pygame.font.SysFont("Arial",40)
msg_font = pygame.font.SysFont("Comic Sans MS", 20)
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
        "cookies": 35,
        "saved_people": 0,
        "sedative": 0,
        "ration_pack": 0,
        "speed_serum": 0,
        "blood_stop": 0,
        "tutorial_done": False,
        "greenhouse_fixed": False,
        "canopy_fixed_day": 0,
    }

def save_game(day_num, seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_amt, saved_people_count):
    """Writes active day progression and intro milestones to disk."""
    data = {
       "current_day": day_num, 
       "has_seen_intro": seen_intro, 
       "pure_soil": pure_soil_count, 
       "has_intact_canopy": has_intact_canopy, 
       "oxygen_recycler_count": oxygen_recycler_count,
       "cookies": cookies_amt,
       "saved_people": saved_people_count,
       "sedative": progress.get("sedative", 0),
       "ration_pack": progress.get("ration_pack", 0),
       "speed_serum": inventory.get("Speed Serum", 0), 
       "blood_stop": inventory.get("Blood-Stop", 0),
       "tutorial_done": tutorial_done,
       "greenhouse_fixed": greenhouse_fixed,
       "canopy_fixed_day": canopy_fixed_day
       }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

progress = load_game()
current_day = progress["current_day"]
has_seen_intro = progress["has_seen_intro"]

pure_soil_count = progress.get("pure_soil", 0)
pure_soil_count = int(pure_soil_count) if isinstance(pure_soil_count, (int, float)) else 0

has_intact_canopy = progress.get("has_intact_canopy", False)
oxygen_recycler_count = progress.get("oxygen_recycler_count", 0)

intact_canopy_count = 1 if has_intact_canopy else 0
oxygen_recycler_count = 1 if oxygen_recycler_count > 0 else 0

cookies_count = progress.get("cookies", 35)
saved_people = progress.get("saved_people", 0)
tutorial_done = progress.get("tutorial_done", False)

inventory["Speed Serum"] = int(progress.get("speed_serum", 0))
inventory["Blood-Stop"] = int(progress.get("blood_stop", 0))
oxygen_recycler_active = 1 if oxygen_recycler_count > 0 else 0
intact_canopy_active = 1 if has_intact_canopy else 0

has_seen_intro = False

current_state="MENU"
last_state = "MENU"

plants = []

plot_positions = [
    {'x': 990, 'y': 380, 'unlock_day': 1}, 
    {'x': 710, 'y': 380, 'unlock_day': 1},  
    {'x': 450, 'y': 380, 'unlock_day': 3},  
    {'x': 200, 'y': 380, 'unlock_day': 3},  

    {'x': 290, 'y': 230, 'unlock_day': 6},
    {'x': 490, 'y': 230, 'unlock_day': 6},
    {'x': 685, 'y': 230, 'unlock_day': 8},
    {'x': 870, 'y': 230, 'unlock_day': 8}
]

locked_plots = [
    {'type': 'tire', 'x': 440, 'y': 420, 'unlock_day': 3},
    {'type': 'drum1', 'x': 200, 'y': 380, 'unlock_day': 3},
    {'type': 'drum2', 'x': 290, 'y': 250, 'unlock_day': 6},
    {'type': 'drum3', 'x': 500, 'y': 250, 'unlock_day': 6},
    {'type': 'tire2', 'x': 690, 'y': 290, 'unlock_day': 8},
    {'type': 'drum4', 'x': 870, 'y': 250, 'unlock_day': 8}
]



def get_free_plot():
    for plot in plot_positions:

        if current_day < plot['unlock_day']:
            continue

        x = plot['x']
        y = plot['y']

        occupied = False

        for p in plants:
            if p.planted and p.rect.x == x and p.rect.y == y:
                occupied = True
                break

        if not occupied:
            return x, y

    return None

pygame.event.pump()
pygame.event.clear()

clock= pygame.time.Clock()

task_bar = TaskBar(Width)
weather_sys = WeatherSystem()
weather_sys.update_weather(current_day)

flash_message = ""
flash_message_timer = 0

acid_rain_days = [3, 8]
shown_acid_rain_days = []
show_acid_rain_popup = False
greenhouse_fixed = progress.get("greenhouse_fixed", False)
canopy_fixed_day = progress.get("canopy_fixed_day", 0)
if current_day in [6, 7]:
    greenhouse_fixed = False
    canopy_fixed_day = 0

if current_day in [3, 8] and intact_canopy_count > 0:
    greenhouse_fixed = False
    canopy_fixed_day = 0

acid_buy_rect = pygame.Rect(0, 0, 0, 0)
acid_cancel_rect = pygame.Rect(0, 0, 0, 0)

try:
    acid_rain_popup_img = pygame.image.load("image/background/acid rain.png").convert_alpha()
    acid_rain_popup_img = pygame.transform.smoothscale(acid_rain_popup_img, (760, 530))
except:
    acid_rain_popup_img = None
    print("Warning: Acid rain popup image not found")

def trigger_message(text):
    global flash_message, flash_message_timer
    flash_message = text
    flash_message_timer = 180

show_plant_menu = False
plant_menu_rect = pygame.Rect(0, 0, 0, 0)
aloe_btn_rect = pygame.Rect(0, 0, 0, 0)  
thorn_btn_rect = pygame.Rect(0, 0, 0, 0)

customer_manager = pharmacy.CustomerManager()
initial_count = random.randint(1, 2)
force_ration = not tutorial_done
customer_manager.spawn_customers(initial_count, force_ration=force_ration)
print(f"Game Started: Initialized {initial_count} customers for Day {current_day}")

has_money_on_table = False
current_selected_item = None

pharmacy_buttons = {
    "money": pygame.Rect(720, 430, 100, 100),
    "ration_pack": pygame.Rect(25, 532, 90, 90),
    "sedative": pygame.Rect(131, 532, 90, 90),
    "blood_stop": pygame.Rect(237, 532, 90, 90),
    "speed_serum": pygame.Rect(343, 532, 90, 90),
    "sell_rad": pygame.Rect(850, 450, 200, 50)
}

show_day_transition = False
transition_day = 0
transition_anim_timer = 0

tutorial_active = False
tutorial_step = 0 
tutorial_skip_rect = pygame.Rect(0, 0, 0, 0)
tutorial_done_timer = 0
tutorial_show_skip = True

def start_tutorial():
    global tutorial_active, tutorial_step, tutorial_done_timer
    if progress.get("ration_pack", 0) == 0:
        progress["ration_pack"] = 1
        print("[Tutorial] Gave 1 Ration Pack for tutorial.")
    tutorial_active = True
    tutorial_step = 0
    tutorial_done_timer = 0
    print("[Tutorial] Started.")

def draw_tutorial(screen, pharmacy_buttons):
    global tutorial_skip_rect, tutorial_done_timer, tutorial_active, tutorial_done
    
    if not tutorial_active:
        return
    
    if tutorial_step == 0:
        if customer_manager.active_customers:
            customer = customer_manager.active_customers[0]
            if customer.current_x > customer.target_x:  
                return  
        else:
            return
    
    hint_text = ""

    if tutorial_step == 0:
        hint_text = "Step 1: Click on Ration Pack to select it."
    elif tutorial_step == 1:
        hint_text = "Step 2: Click the SELL button to trade with customer."
    elif tutorial_step == 2:
        hint_text = "Step 3: Click the cookies on the counter to collect reward!"
    else:
        hint_text = "Tutorial Complete! You're ready to help survivors."
        if tutorial_done_timer == 0:
            trigger_message("Tutorial complete! Buy supplies at SHOP or craft medicine at LAB to save survivors.")
        tutorial_done_timer += 1
        if tutorial_done_timer > 180:
            tutorial_active = False
            tutorial_done = True
            save_game(current_day, has_seen_intro, pure_soil_count,
                     has_intact_canopy, oxygen_recycler_count,
                     cookies_count, saved_people)
            print("[Tutorial] Finished and saved.")
        return
    
    box_width = 480
    box_height = 60
    box_x = (Width - box_width) // 2
    box_y = Height - 110
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    
    pygame.draw.rect(screen, (20, 30, 60, 200), box_rect, border_radius=14)
    pygame.draw.rect(screen, (255, 255, 255, 60), box_rect, width=2, border_radius=14)
    
    font_tut = pygame.font.SysFont("Segoe UI", 18, bold=True)
    text_surf = font_tut.render(hint_text, True, (255, 255, 220))
    text_rect = text_surf.get_rect(center=(Width // 2, box_y + box_height // 2))
    screen.blit(text_surf, text_rect)

    dot_y = box_y - 18
    for i in range(3):
        dot_x = Width // 2 - 24 + i * 24
        if i == tutorial_step:
            color = (0, 200, 255)
            pygame.draw.circle(screen, color, (dot_x, dot_y), 7)
            pygame.draw.circle(screen, (0, 200, 255, 80), (dot_x, dot_y), 11, 2)
        else:
            color = (160, 160, 160)
            pygame.draw.circle(screen, color, (dot_x, dot_y), 5)
    
    tutorial_skip_rect = pygame.Rect(0, 0, 0, 0)

def handle_tutorial_click(mouse_pos):
    global tutorial_step, tutorial_active, tutorial_done
    
    if not tutorial_active:
        return False
    
    return False

def advance_tutorial():
    global tutorial_step, tutorial_active, tutorial_done
    
    if not tutorial_active:
        return
    
    if tutorial_step < 2:
        tutorial_step += 1
        print(f"[Tutorial] Advanced to step {tutorial_step}")
    else:
        tutorial_step = 3
        trigger_message("Tutorial complete! Buy medicines at the Shop or craft in the Lab. Start saving survivors!")

        print("[Tutorial] All steps completed!")

while True:
    mouse_pos = pygame.mouse.get_pos()

    if greenhouse_fixed:
      if current_day - canopy_fixed_day >= 3:
        greenhouse_fixed = False
        canopy_fixed_day = 0
        trigger_message("The canopy has broken down!")

    if saved_people >= 25:
        current_day += 1
        saved_people = 0 
        if current_day in [6, 8]:
           greenhouse_fixed = False
           canopy_fixed_day = 0
           trigger_message("The canopy has broken down!")

        show_day_transition = True
        transition_day = current_day
        transition_anim_timer = 0
        
        print(f"Day Cleared! Welcome to Day {current_day}!")
        
        if current_day > 10:
            print("Victory! You survived all 10 days!")
            trigger_message("You survived all 10 days! Victory!")
            current_day = 1
            
        weather_sys.update_weather(current_day) 
        next_day_customers = random.randint(1, 2)
        customer_manager.spawn_customers(next_day_customers, force_ration=False)
        print(f"New Day! Spawned {next_day_customers} customers.")
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_count, saved_people)

    if current_state == "MENU":
       screen.fill((0, 0, 0))
       if menu_bg_img:
          screen.blit(menu_bg_img, (0,0))
       s_btn, set_btn, e_btn = draw_menu(screen, font, mouse_pos)

    elif current_state == "INTRO":
        show_intro(screen, clock)
        has_seen_intro = True
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_count, saved_people)
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
        if not tutorial_done and not tutorial_active:
            start_tutorial()
        if len(customer_manager.active_customers) == 0 and not has_money_on_table:
            spawn_num =random.randint(1, 2)
            customer_manager.spawn_customers(spawn_num, force_ration=False)
            
        pharmacy_buttons = pharmacy.draw_pharmacy(screen, pharmacy_bg_img, pharmacy_counter_img, has_money_on_table, progress, customer_manager, selected_item=current_selected_item)
        draw_tutorial(screen, pharmacy_buttons)

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
       ready_to_craft = len(plants) > 0 and all(
           p.growth >= 100 and not p.is_dead for p in plants
       )
       any_dead = any(p.is_dead for p in plants)

       active_locked_plots = [
          plot for plot in locked_plots
          if current_day < plot['unlock_day']
       ]

       print(
          "DAY =", current_day,
          "FIXED =", greenhouse_fixed,
          "FIX DAY =", canopy_fixed_day
       ) 

       roof_fixed_today = (
          (current_day == 3 and greenhouse_fixed and canopy_fixed_day == 3)
          or (current_day in [4, 5] and canopy_fixed_day == 3)
          or (current_day == 8 and greenhouse_fixed and canopy_fixed_day == 8)
          or (current_day in [9, 10] and canopy_fixed_day == 8)
       )

       if roof_fixed_today and gh_fixed_bg_img:
          current_gh_bg = gh_fixed_bg_img
       else:
          current_gh_bg = gh_bg_img

       gh_upgrade_btn, pure_soil_btn, oxygen_btn, harvest_btn, aloe_btn, thorn_btn = draw_greenhouse(screen, font, plants,current_gh_bg, pure_soil_count, oxygen_recycler_count, intact_canopy_count, has_intact_canopy, oxygen_recycler_count > 0, ready_to_craft, locked_plots=active_locked_plots)

       acid_rain_protected_now = (
           current_day in [3, 8]
           and greenhouse_fixed
           and canopy_fixed_day == current_day
       )

       if current_day in acid_rain_days and not acid_rain_protected_now:
           acid_overlay = pygame.Surface((Width, Height))
           acid_overlay.fill((40, 70, 35))
           acid_overlay.set_alpha(90)
           screen.blit(acid_overlay, (0, 0))

       if ready_to_craft:
            msg = font.render("HARVEST AVAILABLE!", True, (0, 255, 0))
            screen.blit(msg, (Width//2 - 150, 50))
       elif any_dead:
            msg = font.render("CRAFTING FAILED (Plant Died)", True, (255, 0, 0))
            screen.blit(msg, (Width//2 - 200, 50))
           
    elif current_state == "CRAFTING":
      screen.fill((0, 0, 0))
      draw_crafting(screen, crafting_bg_img, font)
      animate_crafting()

    elif current_state == "SETTING":
       current_state = run_setting(screen, last_state)
       pygame.event.clear()

    if current_state not in ["MENU", "SETTING", "INTRO", "WEATHER_EXPLAIN"]:
        task_bar.draw(screen, current_day, cookies_count, saved_people, weather_sys)

    if flash_message_timer > 0:
        flash_message_timer -= 1
        text_surf = msg_font.render(flash_message, True, (200, 200, 200))
        text_surf = text_surf.convert_alpha()

        alpha = int((flash_message_timer / 60) * 255) if flash_message_timer < 60 else 255
        text_surf.set_alpha(alpha)

        text_rect = text_surf.get_rect(center=(Width // 2, 695))
        screen.blit(text_surf, text_rect)
    
    if show_acid_rain_popup:
      overlay = pygame.Surface((Width, Height))
      overlay.fill((0, 0, 0))
      overlay.set_alpha(170)
      screen.blit(overlay, (0, 0))

      if acid_rain_popup_img:
          popup_rect = acid_rain_popup_img.get_rect(center=(Width // 2, Height // 2 - 35))
          screen.blit(acid_rain_popup_img, popup_rect)

      acid_buy_rect = pygame.Rect(330, 540, 260, 90)
      acid_cancel_rect = pygame.Rect(690, 540, 260, 90)

      if acid_buy_img:
         buy_scaled = pygame.transform.smoothscale(acid_buy_img, (260, 90))
         screen.blit(buy_scaled, acid_buy_rect)

      if acid_cancel_img:
         cancel_scaled = pygame.transform.smoothscale(acid_cancel_img, (260, 90))
         screen.blit(cancel_scaled, acid_cancel_rect)

    if show_day_transition:
        transition_anim_timer += 1
        overlay = pygame.Surface((Width, Height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        box_width = 700
        box_height = 240
        box_rect = pygame.Rect(
            (Width - box_width) // 2,
            (Height - box_height) // 2 - 20,
            box_width, box_height
        )
        pygame.draw.rect(screen, (20, 20, 40, 220), box_rect, border_radius=24)
        pygame.draw.rect(screen, (100, 200, 255, 120), box_rect, width=3, border_radius=24)
        
        font_title = pygame.font.SysFont("Arial", 52, bold=True)
        title_text = f"Welcome to Day {transition_day}!"
        
        shadow_surf = font_title.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(Width//2 + 2, Height//2 - 25 + 2))
        screen.blit(shadow_surf, shadow_rect)
        
        main_surf = font_title.render(title_text, True, (255, 255, 255))
        main_rect = main_surf.get_rect(center=(Width//2, Height//2 - 25))
        screen.blit(main_surf, main_rect)
        
        line_y = Height // 2 + 20
        for i in range(300):
            alpha = int(200 * (1 - abs(i - 150) / 150))
            pygame.draw.rect(screen, (100, 200, 255, alpha),
                           (Width//2 - 150 + i, line_y, 1, 2))
        
        breath = int(150 + 105 * (0.5 + 0.5 * math.sin(transition_anim_timer * 0.04)))
        font_sub = pygame.font.SysFont("Arial", 26)
        sub_text = "Press any key to continue your journey."
        sub_surf = font_sub.render(sub_text, True, (220, 220, 220))
        sub_surf.set_alpha(breath)
        sub_rect = sub_surf.get_rect(center=(Width//2, Height//2 + 65))
        screen.blit(sub_surf, sub_rect)
        
        arrow_color = (100, 200, 255, breath)
        arrow_points = [
            (Width//2 + 160, Height//2 + 65 - 8),
            (Width//2 + 160, Height//2 + 65 + 8),
            (Width//2 + 160 + 16, Height//2 + 65)
        ]
        pygame.draw.polygon(screen, arrow_color, arrow_points)
        
        date_font = pygame.font.SysFont("Arial", 16)
        date_text = f"Day {transition_day}  •  RAD-Pharm"
        date_surf = date_font.render(date_text, True, (150, 150, 150))
        date_rect = date_surf.get_rect(center=(Width//2, Height - 35))
        screen.blit(date_surf, date_rect)

    for event in pygame.event.get():
      if show_acid_rain_popup:
         if event.type == pygame.MOUSEBUTTONDOWN:
            if acid_buy_rect.collidepoint(event.pos):
              show_acid_rain_popup = False
              current_state = "SHOP"

            elif acid_cancel_rect.collidepoint(event.pos):
              show_acid_rain_popup = False

         continue
      
      if show_day_transition:
          if event.type == pygame.KEYDOWN:
              show_day_transition = False
              continue 
          if event.type == pygame.QUIT:
              save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_count, saved_people)
              pygame.quit()
              sys.exit()
          continue
      
      if event.type == pygame.QUIT:
        save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_count, saved_people)
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

      if event.type == pygame.MOUSEBUTTONDOWN: 
         if tutorial_active:
                if handle_tutorial_click(mouse_pos):
                    continue

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
            
            if current_state == "GREENHOUSE":
              clicked_clear = False
              for p in plants:

                if p.is_dead and p.delete_btn_rect and p.delete_btn_rect.collidepoint(mouse_pos):

                    plants.remove(p)

                    trigger_message("Plant discarded into bin!")

                    clicked_clear = True
                    break

              if not clicked_clear:
                  if show_plant_menu:

                      if aloe_btn_rect.collidepoint(mouse_pos):
                          show_plant_menu = False
                      elif thorn_btn_rect.collidepoint(mouse_pos):
                          show_plant_menu = False
                      elif not plant_menu_rect.collidepoint(mouse_pos):
                          show_plant_menu = False

                  elif harvest_btn.collidepoint(mouse_pos):
                      pass
                  elif gh_upgrade_btn.collidepoint(mouse_pos):

                       print("CANOPY BUTTON CLICKED")

                       if intact_canopy_count > 0:

                         print("CANOPY AVAILABLE")

                         intact_canopy_count -= 1
                         has_intact_canopy = False

                         greenhouse_fixed = True
                         canopy_fixed_day = current_day
                         save_game(
                           current_day,
                           has_seen_intro,
                           pure_soil_count,
                           has_intact_canopy,
                           oxygen_recycler_count,
                           cookies_count,
                           saved_people
                         )

                         trigger_message("Greenhouse repaired!")

                  elif pure_soil_btn and pure_soil_btn.collidepoint(mouse_pos):
                      pass
                  elif oxygen_btn and oxygen_btn.collidepoint(mouse_pos):
                      pass
                  else:
                      pass

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
                   save_game(current_day, has_seen_intro, pure_soil_count, has_intact_canopy, oxygen_recycler_count, cookies_count, saved_people)
                   pygame.quit()
                   sys.exit()
                   
         elif current_state == "PHARMACY":   
             clicked_ui = False

             item_configs = [
                 ("ration_pack", "progress", "ration_pack", "Ration Pack"),
                 ("sedative", "progress", "sedative", "Sedative"),
                 ("blood_stop", "inventory", "Blood-Stop", "Blood Stop"),
                 ("speed_serum", "inventory", "Speed Serum", "Speed Serum")
             ]
             
             for ui_key, source, stock_key, display_name in item_configs:
                 rect = pharmacy_buttons.get(ui_key)
                 if rect and rect.collidepoint(mouse_pos):
                     clicked_ui = True
                     if source == "progress":
                         stock = progress.get(stock_key, 0)
                     else:  # inventory
                         stock = inventory.get(stock_key, 0)
                     
                     if stock <= 0:
                         if source == "progress":
                             msg = f"{display_name} out of stock! Go to SHOP to buy."
                         else:
                             msg = f"{display_name} out of stock! Go to LAB to craft."
                         trigger_message(msg) 
                         customer_manager.show_message(msg, is_success=False)
                         current_selected_item = None 
                     else:
                         current_selected_item = ui_key
                         trigger_message(f"Held: {display_name}")
                         if tutorial_active and tutorial_step == 0 and ui_key == "ration_pack":
                             advance_tutorial()
                     break  
             else:       
                 if has_money_on_table and pharmacy_buttons.get("money") and pharmacy_buttons["money"].collidepoint(mouse_pos):
                     clicked_ui = True
                     cookies_count += 45
                     saved_people += 1
                     has_money_on_table = False 
                     trigger_message("+45 Cookies collected into wallet!")
                     if tutorial_active and tutorial_step == 2:
                         advance_tutorial()

                 elif pharmacy_buttons.get("sell_rad") and pharmacy_buttons["sell_rad"].collidepoint(mouse_pos):
                     clicked_ui = True
                     
                     if current_selected_item is None:
                         customer_manager.show_message("Hold a medicine from the hotbar first!", is_success=False)
                         trigger_message("Please select an item first.")
                     else:
                         stock_available = False
                         if current_selected_item == "ration_pack":
                             stock_available = progress.get("ration_pack", 0) > 0
                         elif current_selected_item == "sedative":
                             stock_available = progress.get("sedative", 0) > 0
                         elif current_selected_item == "blood_stop":
                             stock_available = inventory.get("Blood-Stop", 0) > 0
                         elif current_selected_item == "speed_serum":
                             stock_available = inventory.get("Speed Serum", 0) > 0
                         
                         if not stock_available:
                             item_name = current_selected_item.replace('_', ' ').title()
                             if current_selected_item in ["ration_pack", "sedative"]:
                                 msg = f"{item_name} is out of stock! Available in SHOP."
                             else:
                                 msg = f"{item_name} is out of stock! Craft it in LAB."
                             trigger_message(msg)
                             customer_manager.show_message(msg, is_success=False)
                             current_selected_item = None 
                         else:
                             if customer_manager.active_customers:
                                 current_customer = customer_manager.active_customers[0]
                                 if current_selected_item == current_customer.requested_item:
                                     if current_selected_item == "ration_pack":
                                         progress["ration_pack"] -= 1
                                     elif current_selected_item == "sedative":
                                         progress["sedative"] -= 1
                                     elif current_selected_item == "blood_stop":
                                         inventory["Blood-Stop"] -= 1
                                     elif current_selected_item == "speed_serum":
                                         inventory["Speed Serum"] -= 1
                                     
                                     current_customer.is_satisfied = True
                                     has_money_on_table = True
                                     current_selected_item = None
                                     customer_manager.show_message("Trade successful! Click cookies to collect!", is_success=True)
                                     trigger_message("Buyer left cookies on the counter!")
                                     save_game(current_day, has_seen_intro, pure_soil_count,
                                             has_intact_canopy, oxygen_recycler_count,
                                             cookies_count, saved_people)
                                     if tutorial_active and tutorial_step == 1:
                                         advance_tutorial()
                                 else:
                                     customer_manager.show_message("Medicine does not match what customer wants!", is_success=False)
                                     trigger_message("Wrong medicine!")

         elif current_state == "MAP":
            if to_gh_btn.collidepoint(mouse_pos):
               current_state = "GREENHOUSE"
               print("Entering to Greenhouse...")

               if current_day in acid_rain_days and current_day not in shown_acid_rain_days:
                 show_acid_rain_popup = True
                 shown_acid_rain_days.append(current_day)
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
                 if cookies_count >= 60:
                     cookies_count -= 60
                     pure_soil_count += 1
                     trigger_message("Pure Soil purchased!")
                 else:
                     trigger_message("Not enough Cookies for Pure Soil!")

             elif shop_buy_canopy_btn and shop_buy_canopy_btn.collidepoint(mouse_pos):
                 print(f"DEBUG: Clicked Canopy Button! Current status: {has_intact_canopy}")
                 if has_intact_canopy:
                     trigger_message("You already own Intact Canopy!")
                 elif cookies_count >= 150:
                     cookies_count -= 150
                     has_intact_canopy = True
                     intact_canopy_count = 1
                     trigger_message("Intact Canopy purchased!")
                 else:
                     trigger_message("Not enough Cookies for Intact Canopy!")

             elif shop_buy_oxygen_btn and shop_buy_oxygen_btn.collidepoint(mouse_pos):
                 print(f"DEBUG: Clicked Oxygen Button! Current status: {oxygen_recycler_count}")
                 if cookies_count >= 65:
                     cookies_count -= 65
                     oxygen_recycler_count += 1
                     trigger_message("Oxygen Recycler purchased!")
                 else:
                     trigger_message("Not enough Cookies for Oxygen Recycler!")

             elif shop_buy_speed_serum_btn and shop_buy_speed_serum_btn.collidepoint(mouse_pos):
                  if cookies_count >= 50:
                      cookies_count -= 50
                      inventory["Speed Serum"] += 1 
                      trigger_message("Speed Serum purchased!")
                  else:
                      trigger_message("Not enough Cookies for Speed Serum!")

             elif shop_buy_blood_stop_btn and shop_buy_blood_stop_btn.collidepoint(mouse_pos):
                  if cookies_count >= 60:
                      cookies_count -= 60
                      inventory["Blood-Stop"] += 1 
                      trigger_message("Blood Stop purchased!")
                  else:
                      trigger_message("Not enough Cookies for Blood Stop!")
 
         elif current_state == "GREENHOUSE":
            if aloe_btn.collidepoint(mouse_pos):
                pos = get_free_plot()

                if pos:
                   x, y = pos
                   new_plant = Plant(x, y, "Glowing Aloe", 0.02)
                   new_plant.planted = True
                   plants.append(new_plant)
                   trigger_message("Aloe planted!")
                else:
                   trigger_message("No empty plot!")
            
            elif thorn_btn.collidepoint(mouse_pos):
                pos = get_free_plot()

                if pos:
                   x, y = pos
                   new_plant = Plant(x, y, "Rusty Thorn", 0.02)
                   new_plant.planted = True
                   plants.append(new_plant)
                   trigger_message("Rusty Thorn planted!")
                else:
                   trigger_message("No empty plot!")


            elif harvest_btn.collidepoint(mouse_pos):
                harvested_something = False
                for p in plants:
                     if p.growth >= 100 and not p.harvested and not p.is_dead:
                           
                           if p.name in inventory:
                               inventory[p.name] += 1
                           else:
                               inventory[p.name] = 1
                           
                           p.planted = False
                           p.growth = 0
                           p.dust = 0
                           p.is_dead = False
                           p.harvested = False

                           harvested_something = True
                           print(f"Harvested {p.name} added to lab!")

                if harvested_something:
                    print("Harvest successful!")
                    trigger_message("Harvest successful!")   
                else:
                     print("No plants ready to harvest!")
                     trigger_message("No plants ready to harvest!")

            elif pure_soil_btn and pure_soil_btn.collidepoint(mouse_pos) and pure_soil_count > 0:
               pure_soil_count -= 1
               for p in plants:
                   if not p.is_dead:
                      p.dust = 0
                      p.growth += 20
                      if p.growth > 100: p.growth = 100
            
            elif oxygen_btn and oxygen_btn.collidepoint(mouse_pos) and oxygen_recycler_count > 0:
               oxygen_recycler_count -= 1

               for p in plants:
                     if not p.is_dead:
                        p.growth += 30
                        if p.growth >100: p.growth = 100
            
            else:
               pass

    pygame.display.flip()
    clock.tick(60)