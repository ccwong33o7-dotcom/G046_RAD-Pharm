import pygame
import sys
import math
from customer import CustomerManager
from crafting import inventory

inventory_bar_img = None
gun_icon_img = None
cookie_icon_img = None

try:
    inventory_bar_img_original = pygame.image.load("image/button/inventory_bar.png") 
    original_width, original_height = inventory_bar_img_original.get_size()
    inventory_bar_img = pygame.transform.smoothscale(inventory_bar_img_original, (int(original_width * 0.5), int(original_height * 0.5)))
except Exception as e:
    print(f"ERROR inventory bar picture: {e}")

try:
    gun_ori = pygame.image.load("image/button/handgun.png").convert_alpha()
    gun_icon_img = pygame.transform.smoothscale(gun_ori, (120, 120))
except Exception as e:
    print(f"ERROR loading handgun.jpg: {e}")

try:
    cookie_ori = pygame.image.load("image/button/CookiesforPharmacy.png").convert_alpha()
    cookie_icon_img = pygame.transform.smoothscale(cookie_ori, (100, 100))  
except Exception as e:
    print(f"ERROR loading CookiesforPharmacy.jpg: {e}")

customer_manager = CustomerManager()

def change_customer_count(count):
    customer_manager.spawn_customers(count)

def draw_pharmacy(screen, bg_img, counter_img, money_waiting_to_collect):
    screen_w, screen_h = screen.get_size()
    bg_rect = pygame.Rect(0, 0, 1280, 720)
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

    customer_manager.draw_all(screen)

    if counter_img:
        target_width = 1280
        target_height = 340
        
        scaled_counter = pygame.transform.smoothscale(counter_img, (target_width, target_height))
        
        pos_x = 0
        pos_y = 380  
        
        screen.blit(scaled_counter, (pos_x, pos_y))

    gun_rect = pygame.Rect(100, 400, 140, 140)       
    cookie_rect = pygame.Rect(350, 420, 110, 110)    

    if gun_icon_img:
        screen.blit(gun_icon_img, (gun_rect.x, gun_rect.y))
    else:
        pygame.draw.rect(screen, (150, 50, 50), gun_rect, 2)
    
    if money_waiting_to_collect:
        if cookie_icon_img:
            screen.blit(cookie_icon_img, (cookie_rect.x, cookie_rect.y))
        else:
            pygame.draw.rect(screen, (220, 160, 40), cookie_rect, 2) 
        tip_font = pygame.font.SysFont("Arial", 20, bold=True)
        tip_text = tip_font.render("CLICK TO COLLECT", True, (0, 255, 0))
        screen.blit(tip_text, (cookie_rect.x - 30, cookie_rect.y - 25))
    
    font = pygame.font.SysFont("Arial", 28)

    rad_text = font.render(f"Rad-Ointment: {inventory['Rad-Ointment']}", True, (255,255,255))
    speed_text = font.render(f"Speed Serum: {inventory['Speed Serum']}", True, (255,255,255))
    blood_text = font.render(f"Blood-Stop: {inventory['Blood-Stop']}", True, (255,255,255))

    screen.blit(rad_text, (960, 220))
    screen.blit(speed_text, (960, 260))
    screen.blit(blood_text, (960, 300))

    if inventory_bar_img:
        x_pos = -275
        y_pos = 170
        screen.blit(inventory_bar_img, (x_pos, y_pos))
    
    sell_rad_btn = pygame.Rect(960, 350, 180, 45)

    pygame.draw.rect(screen, (0,180,0), sell_rad_btn)

    btn_text = font.render("Sell Rad", True, (255,255,255))
    screen.blit(btn_text, (1005, 358))

    return {
        "sell_rad": sell_rad_btn,
        "gun": gun_rect,
        "money": cookie_rect
    }