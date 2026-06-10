import pygame
import random

class Customer:
    def __init__(self, img_path):
        try:
            self.image = pygame.image.load(img_path).convert_alpha()
            
            target_h = 420
            w, h = self.image.get_size()
            target_w = int(w * (target_h / h))
            self.image = pygame.transform.smoothscale(self.image, (target_w, target_h))
        except pygame.error as e:
            print(f"ERROR loading customer image {img_path}: {e}")
            self.image = pygame.Surface((120, 300), pygame.SRCALPHA)
            self.image.fill((200, 0, 0, 150))

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))


class CustomerManager:
    def __init__(self):
        self.image_paths = [
            "image/Customer/buyer1.png", 
            "image/Customer/buyer2.png",
            "image/Customer/buyer3.png",
            "image/Customer/buyer4.png"
        ]
        self.active_customers = []

    def spawn_customers(self, count):
        self.active_customers.clear()
        
        available_count = min(count, len(self.image_paths))
        chosen_paths = random.sample(self.image_paths, available_count)
        
        for path in chosen_paths:
            self.active_customers.append(Customer(path))

    def draw_all(self, screen):
        if not self.active_customers:
            return

        screen_w, screen_h = screen.get_size()
        num_customers = len(self.active_customers)
        y_pos = 340 
        
        for i, customer in enumerate(self.active_customers):
            spacing = screen_w // (num_customers + 1)
            x_pos = spacing * (i + 1) - (customer.image.get_width() // 2)
            
            customer.draw(screen, x_pos, y_pos)