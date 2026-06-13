import pygame
import random

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

        self.current_x = 1280  
        self.target_x = 1280   
        self.speed = 5

    def update(self):
        if self.current_x > self.target_x:
            self.current_x -= self.speed
            if self.current_x < self.target_x:
                self.current_x = self.target_x

    def draw(self, screen, y_pos):
        screen.blit(self.image, (self.current_x, y_pos))


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
        for customer in self.active_customers:
            customer.update()

    def draw_all(self, screen):
        if not self.active_customers:
            return

        y_pos = 177
        
        self.update_all()
        
        for customer in self.active_customers:
            customer.draw(screen, y_pos)