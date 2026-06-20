import pygame
import sys
import math
import os
import random
from crafting import inventory


class Customer:
    def __init__(self, img_path):
        try:
            self.image = pygame.image.load(img_path).convert_alpha()

            target_h = 340
            w, h = self.image.get_size()
            target_w = int(w * (target_h / h))
            self.image = pygame.transform.smoothscale(self.image, (target_w, target_h))
        except pygame.error as e:
            print(f"ERROR loading customer image {img_path}: {e}")
            self.image = pygame.Surface((120, 300), pygame.SRCALPHA)
            self.image.fill((200, 0, 0, 150))

        try:
            self.bubble_image = pygame.image.load("image/Customer/CI_bubblerequest.png").convert_alpha()
            bubble_h = 215
            bw, bh = self.bubble_image.get_size()
            bubble_w = int(bw * (bubble_h / bh))
            self.bubble_image = pygame.transform.smoothscale(self.bubble_image, (bubble_w, bubble_h))
        except pygame.error as e:
            print(f"ERROR loading bubble image: {e}")
            self.bubble_image = pygame.Surface((100, 150), pygame.SRCALPHA)
            self.bubble_image.fill((255, 255, 255, 200))

        self.current_x = 1280
        self.target_x = 1280
        self.speed = 8
        self.sell_btn_rect = pygame.Rect(0, 0, 0, 0)

        self.possible_requests = ["ration_pack", "sedative", "blood_stop", "speed_serum"]
        self.requested_item = random.choice(self.possible_requests[:4])
        self.item_icon = None
        icon_paths = {
            "ration_pack": "image/Customer/CI_rationpack.png",
            "sedative": "image/Customer/CI_sedative.png",
            "blood_stop": "image/Customer/CI_bloodstop.png",
            "speed_serum": "image/Customer/CI_speedserum.png"
        }
        try:
            icon_img = pygame.image.load(icon_paths[self.requested_item]).convert_alpha()
            target_icon_h = 55
            orig_w, orig_h = icon_img.get_size()
            target_icon_w = int(orig_w * (target_icon_h / orig_h))
            self.item_icon = pygame.transform.smoothscale(icon_img, (target_icon_w, target_icon_h))
        except Exception as e:
            print(f"ERROR loading icon for {self.requested_item}: {e}")
            self.item_icon = pygame.Surface((55, 55))
            self.item_icon.fill((0, 200, 200))

        self.is_satisfied = False

    def set_requested_item(self, item):
        self.requested_item = item
        icon_paths = {
            "ration_pack": "image/Customer/CI_rationpack.png",
            "sedative": "image/Customer/CI_sedative.png",
            "blood_stop": "image/Customer/CI_bloodstop.png",
            "speed_serum": "image/Customer/CI_speedserum.png"
        }
        try:
            icon_img = pygame.image.load(icon_paths[item]).convert_alpha()
            target_icon_h = 55
            orig_w, orig_h = icon_img.get_size()
            target_icon_w = int(orig_w * (target_icon_h / orig_h))
            self.item_icon = pygame.transform.smoothscale(icon_img, (target_icon_w, target_icon_h))
        except Exception as e:
            print(f"ERROR loading icon for {item}: {e}")
            self.item_icon = pygame.Surface((55, 55))
            self.item_icon.fill((0, 200, 200))

    def update(self):
        if self.current_x > self.target_x:
            self.current_x -= self.speed
            if self.current_x < self.target_x:
                self.current_x = self.target_x

    def draw(self, screen, y_pos, selected_item=None):
        self.rect = pygame.Rect(self.current_x, y_pos, self.image.get_width(), self.image.get_height())
        screen.blit(self.image, (self.current_x, y_pos))

        if self.current_x <= self.target_x:
            bubble_x = self.current_x - self.bubble_image.get_width() + 10
            bubble_y = y_pos - 40
            screen.blit(self.bubble_image, (bubble_x, bubble_y))

            if self.item_icon:
                icon_x = bubble_x + (self.bubble_image.get_width() - self.item_icon.get_width()) // 2
                icon_y = bubble_y + 65
                screen.blit(self.item_icon, (icon_x, icon_y))

            btn_w, btn_h = 70, 25
            btn_x = bubble_x + (self.bubble_image.get_width() - btn_w) // 2
            btn_y = bubble_y + 130
            self.sell_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

            if selected_item is not None and selected_item == self.requested_item:
                btn_color = (46, 204, 113)  
            else:
                btn_color = (128, 128, 128)  

            pygame.draw.rect(screen, btn_color, self.sell_btn_rect, border_radius=4)
            btn_font = pygame.font.SysFont("Arial", 13, bold=True)
            text_surf = btn_font.render("SELL", True, (255, 255, 255))
            screen.blit(text_surf, (btn_x + (btn_w - text_surf.get_width()) // 2,
                                    btn_y + (btn_h - text_surf.get_height()) // 2))
        else:
            self.sell_btn_rect = pygame.Rect(0, 0, 0, 0)

    def check_click(self, mouse_pos, selected_item, progress_dict):
        if self.current_x > self.target_x or self.is_satisfied:
            return False, "Not ready"

        if self.sell_btn_rect.collidepoint(mouse_pos):
            if selected_item is None:
                return False, "Please select an item from your hotbar first!"
            if selected_item != self.requested_item:
                return False, f"Wrong item! This customer requested {self.requested_item.replace('_', ' ').title()}."

            target_dict = progress_dict
            dict_key = selected_item

            if selected_item == "blood_stop":
                target_dict = inventory
                dict_key = "Blood-Stop"
            elif selected_item == "speed_serum":
                target_dict = inventory
                dict_key = "Speed Serum"

            if target_dict.get(dict_key, 0) <= 0:
                item_name = dict_key.replace('_', ' ').title()
                if selected_item in ["ration_pack", "sedative"]:
                    return False, f"{item_name} is out of stock! Go to the SHOP to buy more."
                elif selected_item in ["blood_stop", "speed_serum"]:
                    return False, f"{item_name} is out of stock! Go to the LAB to craft it."
                else:
                    return False, "Out of stock!"

            target_dict[dict_key] -= 1
            self.is_satisfied = True
            return True, "Trade successful!"

        return False, "No click"


class CustomerManager:
    def __init__(self):
        self.image_paths = [
            "image/Customer/buyer1.png",
            "image/Customer/buyer2.png",
            "image/Customer/buyer3.png",
            "image/Customer/buyer4.png"
        ]
        self.active_customers = []

        pygame.font.init()
        self.feedback_font = pygame.font.SysFont("Comic Sans MS", 20, bold=True)
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = (255, 50, 50)

    def spawn_customers(self, count,force_ration=False):
        self.active_customers.clear()

        available_count = min(count, len(self.image_paths))
        chosen_paths = random.sample(self.image_paths, available_count)

        screen_w = pygame.display.get_surface().get_width() if pygame.display.get_surface() else 1280

        for i, path in enumerate(chosen_paths):
            customer = Customer(path)
            if force_ration and i == 0: 
                customer.set_requested_item("ration_pack")
            spacing = screen_w // (available_count + 1)
            target_x = spacing * (i + 1) - (customer.image.get_width() // 2)
            target_x += -150

            customer.target_x = target_x
            customer.current_x = screen_w + (i * 80)

            self.active_customers.append(customer)

    def update_all(self):
        self.active_customers = [c for c in self.active_customers if not c.is_satisfied]
        for customer in self.active_customers:
            customer.update()

    def show_message(self, text, is_success=False):
        self.feedback_text = text
        self.feedback_timer = 120
        self.feedback_color = (50, 255, 50) if is_success else (255, 50, 50)

    def draw_all(self, screen, selected_item=None):
        y_pos = 177
        self.update_all()

        for customer in self.active_customers:
            customer.draw(screen, y_pos,selected_item)

        if self.feedback_timer > 0 and self.feedback_text:
            text_surf = self.feedback_font.render(self.feedback_text, True, self.feedback_color)
            text_surf = text_surf.convert_alpha()

            if self.feedback_timer < 60:
                alpha = int((self.feedback_timer / 60) * 255)
            else:
                alpha = 255
            text_surf.set_alpha(alpha)

            text_rect = text_surf.get_rect(center=(screen.get_width() // 2, 695))
            screen.blit(text_surf, text_rect)

            self.feedback_timer -= 1

    def handle_click(self, mouse_pos, current_selected_item, merged_inventory):
        if not self.active_customers:
            return False, "No active customer"

        current_customer = self.active_customers[0]
        if current_customer.requested_item == current_selected_item:
            if merged_inventory.get(current_selected_item, 0) > 0:
                if hasattr(current_customer, 'state'):
                    current_customer.state = "leaving"
                self.active_customers.pop(0)

                return True, "Success"
            else:
                return False, "No stock"
        else:
            return False, "Medicine does not match what customer wants!"


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

_global_manager_ref = None

def change_customer_count(count):
    if _global_manager_ref:
        _global_manager_ref.spawn_customers(count)

def draw_pharmacy(screen, bg_img, counter_img, money_waiting_to_collect, progress_dict=None, external_manager=None, selected_item=None):
    global _global_manager_ref
    if external_manager:
        _global_manager_ref = external_manager
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

    if external_manager:
        external_manager.draw_all(screen, selected_item)

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
    
    cookie_rect = pygame.Rect(720, 430, 100, 100)

    if money_waiting_to_collect:
        if cookie_icon_img:
            screen.blit(cookie_icon_img, (cookie_rect.x, cookie_rect.y))
        else:
            pygame.draw.circle(screen, (240, 200, 20), cookie_rect.center, 40)

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
        blood_count = label_font.render(f"Count: {inventory.get('Blood-Stop', 0)}", True, (255, 255, 255))
        screen.blit(blood_count, (bloodstop_rect.x + 12, bloodstop_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (180, 60, 60), bloodstop_rect, 2)

    if speedserum_icon_img:
        scaled_img = pygame.transform.smoothscale(speedserum_icon_img, (BTN_W, BTN_H))
        screen.blit(scaled_img, (speedserum_rect.x, speedserum_rect.y))
        speed_count = label_font.render(f"Count: {inventory.get('Speed Serum', 0)}", True, (255, 255, 255))
        screen.blit(speed_count, (speedserum_rect.x + 12, speedserum_rect.y + BTN_H + 5))
    else:
        pygame.draw.rect(screen, (60, 120, 180), speedserum_rect, 2)
    
    font = pygame.font.SysFont("Arial", 28)
    rad_val = inventory.get('Rad-Ointment', 0)
    rad_text = font.render(f"Rad-Ointment: {rad_val}", True, (255,255,255))
    screen.blit(rad_text, (960, 220))
    
    sell_rad_btn = pygame.Rect(0, 0, 0, 0)
    if external_manager and external_manager.active_customers:
        sell_rad_btn = external_manager.active_customers[0].sell_btn_rect

    return {
        "sell_rad": sell_rad_btn,
        "gun": gun_rect,
        "money": cookie_rect,
        "ration_pack": ration_pack_rect,
        "sedative": sedative_rect,
        "blood_stop": bloodstop_rect,
        "speed_serum": speedserum_rect
    }