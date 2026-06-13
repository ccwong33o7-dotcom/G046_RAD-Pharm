import pygame
import sys
import math
import os
from customer import CustomerManager
from crafting import inventory


gun_icon_img = None
cookie_icon_img = None
ration_pack_icon_img = None
sedative_icon_img = None
bloodstop_icon_img = None
speedserum_icon_img = None

def load_and_scale(path, size, name_for_error):
    if not os.path.exists(path):
        print(f"ERROR: Image file not found: {path}. Please ensure the 'image/button/' directory and images exist.")
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)
    except Exception as e:
        print(f"ERROR loading {name_for_error}: {e}")
        return None
    
ICON_SIZE = (95, 95)

gun_icon_img = load_and_scale("image/button/handgun.png", (120, 120), "handgun.png")
cookie_icon_img = load_and_scale("image/button/CookiesforPharmacy.png", (100, 100), "CookiesforPharmacy.png")

ration_pack_icon_img = load_and_scale("image/button/rationpack_button.png", ICON_SIZE, "rationpack_button.png")
sedative_icon_img = load_and_scale("image/button/sedative_button.png", ICON_SIZE, "sedative_button.png")
bloodstop_icon_img = load_and_scale("image/button/bloodstop_button.png", ICON_SIZE, "bloodstop_button.png")
speedserum_icon_img = load_and_scale("image/button/speedserum_button.png", ICON_SIZE, "speedserum_button.png")

customer_manager = CustomerManager()

def change_customer_count(count):
    customer_manager.spawn_customers(count)

def draw_pharmacy(screen, bg_img, counter_img, money_waiting_to_collect, progress_dict=None):
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

    gun_rect = pygame.Rect(50, 395, 120, 120)
    if gun_icon_img:
        screen.blit(gun_icon_img, (gun_rect.x, gun_rect.y))
    else:
        pygame.draw.rect(screen, (150, 50, 50), gun_rect, 2)

    BTN_W, BTN_H = 90, 90
    START_X = 25
    START_Y = 532
    SPACING_X = 106

    ration_pack_rect = pygame.Rect(START_X + 0 * SPACING_X, START_Y, BTN_W, BTN_H)
    sedative_rect    = pygame.Rect(START_X + 1 * SPACING_X, START_Y, BTN_W, BTN_H)
    bloodstop_rect   = pygame.Rect(START_X + 2 * SPACING_X, START_Y, BTN_W, BTN_H)
    speedserum_rect  = pygame.Rect(START_X + 3 * SPACING_X, START_Y, BTN_W, BTN_H)
    
    cookie_rect = None

    label_font = pygame.font.SysFont("Arial", 16, bold=True)

    ration_val = progress_dict.get("ration_pack", 0) if progress_dict else 0
    sedative_val = progress_dict.get("sedative", 0) if progress_dict else 0

    if ration_pack_icon_img:
        scaled_img = pygame.transform.smoothscale(ration_pack_icon_img, (BTN_W, BTN_H))
        screen.blit(scaled_img, (ration_pack_rect.x, ration_pack_rect.y))
        qty_text = label_font.render(f"Count: {ration_val}", True, (255, 255, 255))
        screen.blit(qty_text, (ration_pack_rect.x + 12, ration_pack_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (100, 100, 150), ration_pack_rect, 2)

    if sedative_icon_img:
        scaled_img = pygame.transform.smoothscale(sedative_icon_img, (BTN_W, BTN_H))
        screen.blit(scaled_img, (sedative_rect.x, sedative_rect.y))
        qty_text = label_font.render(f"Count: {sedative_val}", True, (255, 255, 255)) 
        screen.blit(qty_text, (sedative_rect.x + 12, sedative_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (100, 150, 100), sedative_rect, 2)

    if bloodstop_icon_img:
        scaled_img = pygame.transform.smoothscale(bloodstop_icon_img, (BTN_W, BTN_H))
        screen.blit(scaled_img, (bloodstop_rect.x, bloodstop_rect.y))
        blood_count = label_font.render(f"Count: {inventory['Blood-Stop']}", True, (255, 255, 255))
        screen.blit(blood_count, (bloodstop_rect.x + 12, bloodstop_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (180, 60, 60), bloodstop_rect, 2)

    if speedserum_icon_img:
        scaled_img = pygame.transform.smoothscale(speedserum_icon_img, (BTN_W, BTN_H))
        screen.blit(scaled_img, (speedserum_rect.x, speedserum_rect.y))
        speed_count = label_font.render(f"Count: {inventory['Speed Serum']}", True, (255, 255, 255))
        screen.blit(speed_count, (speedserum_rect.x + 12, speedserum_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (60, 120, 180), speedserum_rect, 2)
    
    font = pygame.font.SysFont("Arial", 28)
    rad_text = font.render(f"Rad-Ointment: {inventory['Rad-Ointment']}", True, (255,255,255))
    screen.blit(rad_text, (960, 220))
    
    sell_rad_btn = pygame.Rect(960, 350, 180, 45)
    pygame.draw.rect(screen, (0,180,0), sell_rad_btn)
    btn_text = font.render("Sell Rad", True, (255,255,255))
    screen.blit(btn_text, (1005, 358))

    return {
        "sell_rad": sell_rad_btn,
        "gun": gun_rect,
        "money": cookie_rect,
        "ration_pack": ration_pack_rect,
        "sedative": sedative_rect,
        "blood_stop": bloodstop_rect,
        "speed_serum": speedserum_rect
    }