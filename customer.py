import pygame
import random
from crafting import inventory as crafting_inventory

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
            self.item_icon = pygame.transform.smoothscale(icon_img, (55, 55))
        except Exception as e:
            print(f"ERROR loading icon for {self.requested_item}: {e}")
            self.item_icon = pygame.Surface((55, 55))
            self.item_icon.fill((0, 200, 200))

        self.is_satisfied = False

    def update(self):
        if self.current_x > self.target_x:
            self.current_x -= self.speed
            if self.current_x < self.target_x:
                self.current_x = self.target_x

    def draw(self, screen, y_pos):
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
            btn_y = bubble_y + 145  
 
            self.sell_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            
            pygame.draw.rect(screen, (46, 204, 113), self.sell_btn_rect, border_radius=4)
            
            btn_font = pygame.font.SysFont("Arial", 13, bold=True)
            text_surf = btn_font.render("SELL", True, (255, 255, 255))
            text_x = btn_x + (btn_w - text_surf.get_width()) // 2
            text_y = btn_y + (btn_h - text_surf.get_height()) // 2
            screen.blit(text_surf, (text_x, text_y))
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
                target_dict = crafting_inventory
                dict_key = "Blood-Stop"
            elif selected_item == "speed_serum":
                target_dict = crafting_inventory
                dict_key = "Speed Serum"

            if target_dict.get(dict_key, 0) <= 0:
                return False, "Out of stock! You don't have enough items to sell."
            
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
        self.font = pygame.font.SysFont("Arial", 17, bold=True)
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = (255, 50, 50)

    def spawn_customers(self, count):
        self.active_customers.clear()
        
        available_count = min(count, len(self.image_paths))
        chosen_paths = random.sample(self.image_paths, available_count)
        
        screen_w = pygame.display.get_surface().get_width() if pygame.display.get_surface() else 1280
        
        for i, path in enumerate(chosen_paths):
            customer = Customer(path)
            
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

    def draw_all(self, screen):
        y_pos = 177
        self.update_all()
        
        for customer in self.active_customers:
            customer.draw(screen, y_pos)

        if self.feedback_timer > 0 and self.feedback_text:
            text_surf = self.font.render(self.feedback_text, True, self.feedback_color)
            text_surf = text_surf.convert_alpha()  

            if self.feedback_timer < 60:
                alpha = int((self.feedback_timer / 60) * 255)
            else:
                alpha = 255
            text_surf.set_alpha(alpha)  
            x = (screen.get_width() - text_surf.get_width()) // 2
            y = 695
            screen.blit(text_surf, (x, y))
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