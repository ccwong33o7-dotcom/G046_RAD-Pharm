import pygame
from customer import CustomerManager
from crafting import inventory

inventory_bar_img_original = None

try:
    inventory_bar_img_original = pygame.image.load("image/button/inventory_bar.png") 
except pygame.error as e:
    print(f"ERROR inventory bar picture: {e}")
    inventory_bar_img_original = None
    
SCALE_FACTOR = 0.5 

if inventory_bar_img_original:
    original_width, original_height = inventory_bar_img_original.get_size()
    scaled_width = int(original_width * SCALE_FACTOR)
    scaled_height = int(original_height * SCALE_FACTOR)
    inventory_bar_img = pygame.transform.smoothscale(inventory_bar_img_original, (scaled_width, scaled_height))
else:
    inventory_bar_img = None

customer_manager = CustomerManager()

def change_customer_count(count):
    customer_manager.spawn_customers(count)

def draw_pharmacy(screen, bg_img):
    
    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))

    customer_manager.draw_all(screen)
    
    font = pygame.font.SysFont("Arial", 28)

    rad_text = font.render(f"Rad-Ointment: {inventory['Rad-Ointment']}", True, (255,255,255))
    speed_text = font.render(f"Speed Serum: {inventory['Speed Serum']}", True, (255,255,255))
    blood_text = font.render(f"Blood-Stop: {inventory['Blood-Stop']}", True, (255,255,255))

    screen.blit(rad_text, (850, 250))
    screen.blit(speed_text, (850, 300))
    screen.blit(blood_text, (850, 350))

    if inventory_bar_img:
        x_pos = -275
        y_pos = 170
        screen.blit(inventory_bar_img, (x_pos, y_pos))
    
        sell_rad_btn = pygame.Rect(850, 450, 200, 50)

    pygame.draw.rect(screen, (0,200,0), sell_rad_btn)

    btn_text = font.render("Sell Rad", True, (255,255,255))
    screen.blit(btn_text, (890, 460))

    return sell_rad_btn

   
    