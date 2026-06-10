import pygame
import os

COLOR_BG = (30, 30, 30)
COLOR_TEXT = ( 0, 255, 0)

img_pure_soil = None
img_intact_canopy = None
img_oxygen_recycler = None
img_plant_seed = None
img_harvest = None
img_plant_menu_bg = None
img_thorn_btn = None
img_aloe_btn = None
    
class Plant:
    def __init__(self, x_pos, y_pos, name, dust_speed, width=120, height=160):
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.name = name
        self.growth = 0
        self.dust = 0
        self.dust_speed = dust_speed 
        self.is_dead = False
        self.death_timer = 0
        self.harvested = False

        self.img_growth = []
        self.img_dead = []


        try:
            self.img_seedling = pygame.image.load("image/plant/Aloe1.png").convert_alpha()
            self.img_bud = pygame.image.load("image/plant/Aloe2.png").convert_alpha()
            self.img_flower = pygame.image.load("image/plant/Aloe3.png").convert_alpha()

            self.img_wilt_1 = pygame.image.load("image/plant/wilt_1.png").convert_alpha()
            self.img_wilt_2 = pygame.image.load("image/plant/wilt_2.png").convert_alpha()
            self.img_wilt_3 = pygame.image.load("image/plant/wilt_3.png").convert_alpha()
        
        except pygame.error as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            import sys
            sys.exit()
        
    def update(self):
        self.dust += self.dust_speed
        if self.dust > 100: 
            self.dust = 100
            if not self.is_dead and self.growth < 100:
                self.is_dead = True
                self.death_timer = 0

        if not self.is_dead and self.dust < 70:
            self.growth += 0.03
            if self.growth > 100:
                self.growth = 100

        if self.is_dead:
            self.death_timer += 1

    def clean(self):
     if not self.is_dead:
         self.dust -= 20
     if self.dust < 0:
        self.dust = 0

    
    def draw(self, surface):

        if self.growth >= 100:
            current_image = self.img_flower
        
        elif self.is_dead:
            if self.death_timer < 400:
                current_image = self.img_wilt_1
            elif self.death_timer < 800:
                current_image = self.img_wilt_2
            else:
                current_image = self.img_wilt_3
        
        else:
            if self.growth < 33:
                current_image = self.img_seedling
            else:
                current_image = self.img_bud
        
        orig_w, orig_h = current_image.get_size()
        scale_factor = 160 / orig_h
        new_w = int(orig_w * scale_factor)
        new_h = int(orig_h * scale_factor)
        scaled_image = pygame.transform.scale(current_image, (self.rect.width, self.rect.height))
        surface.blit(scaled_image, (self.rect.x, self.rect.y))

        font_small = pygame.font.SysFont("Arial", 18)
        name_txt = font_small.render(f"{self.name}", True, COLOR_TEXT)
        stats_txt = font_small.render(f"D:{int(self.dust)}% G:{int(self.growth)}%", True, COLOR_TEXT)
        surface.blit(name_txt, (self.rect.x, self.rect.y - 30))
        surface.blit(stats_txt, (self.rect.x, self.rect.y - 10))
     

def draw_greenhouse(screen, font, plant_list, bg_image=None, pure_soil_count=0, oxygen_count=0, canopy_count=0, has_intact_canopy=False, has_oxygen_recycler=False, ready_to_craft=False):
    global img_pure_soil, img_intact_canopy, img_oxygen_recycler, img_plant_seed, img_harvest
    small_font = pygame.font.SysFont("Arial", 20)

    plant_seed_btn_rect = pygame.Rect(25, 630, 215, 65)
    harvest_btn_rect = pygame.Rect(315, 630, 260, 65)

    if img_pure_soil is None:
        for ext in [".jpg", ".png", ".JPG", ".PNG"]:
            possible_path = f"image/button/PureSoil{ext}"
            if os.path.exists(possible_path):
                try:
                    img_pure_soil = pygame.image.load(possible_path).convert_alpha()
                    img_pure_soil = pygame.transform.scale(img_pure_soil, (100, 100))
                    break
                except pygame.error as e:
                    print(f"Error loading pure soil image: {e}")
                    img_pure_soil = None
    
    if img_intact_canopy is None:
        for ext in [".jpg", ".png", ".JPG", ".PNG"]:
            possible_path = f"image/button/IntactCanopy{ext}"
            if os.path.exists(possible_path):
                try:
                    img_intact_canopy = pygame.image.load(possible_path).convert_alpha()
                    img_intact_canopy = pygame.transform.scale(img_intact_canopy, (100, 100))
                    break
                except pygame.error as e:
                    print(f"Error loading intact canopy image: {e}")
                    img_intact_canopy = None
    
    if img_oxygen_recycler is None:
        for ext in [".jpg", ".png", ".JPG", ".PNG"]:
            possible_path = f"image/button/OxygenRecycler{ext}"
            if os.path.exists(possible_path):
                try:
                    img_oxygen_recycler = pygame.image.load(possible_path).convert_alpha()
                    img_oxygen_recycler = pygame.transform.scale(img_oxygen_recycler, (100, 100))
                    break
                except pygame.error as e:
                    print(f"Error loading oxygen recycler image: {e}")
                    img_oxygen_recycler = None
    
    if img_plant_seed is None:
        for ext in [".jpg", ".png", ".JPG", ".PNG"]:
            possible_path = f"image/button/Plant Seed button{ext}"
            if os.path.exists(possible_path):
                try:
                    img_plant_seed = pygame.image.load(possible_path).convert_alpha()
                    img_plant_seed = pygame.transform.scale(img_plant_seed, (240, 65))
                    break
                except pygame.error as e:
                    print(f"Error loading plant seed image: {e}")
                    img_plant_seed = None


    if img_harvest is None:
        for ext in [".jpg", ".png", ".JPG", ".PNG"]:
            possible_path = f"image/button/Harvest button{ext}"
            if os.path.exists(possible_path):
                try:
                    img_harvest = pygame.image.load(possible_path).convert_alpha()
                    img_harvest = pygame.transform.scale(img_harvest, (260, 65))
                    break
                except pygame.error as e:
                    print(f"Error loading harvest image: {e}")
                    img_harvest = None



    if bg_image:
        screen.blit(bg_image, (0,0))
    else:
        screen.fill(COLOR_BG)
    
    for p in plant_list:
        p.update()
        p.draw(screen)
    
    if img_plant_seed:
        screen.blit(img_plant_seed, (plant_seed_btn_rect.x, plant_seed_btn_rect.y))
    else:
        pygame.draw.rect(screen, (0, 255, 0), plant_seed_btn_rect, 2)
        txt = small_font.render("Plant Seed", True, (0, 255, 0))
        screen.blit(txt, (plant_seed_btn_rect.x + 50, plant_seed_btn_rect.y + 20))

    any_plant_ready = any(p.growth >= 100 and not p.harvested and not p.is_dead for p in plant_list)

    if img_harvest:
        screen.blit(img_harvest, (harvest_btn_rect.x, harvest_btn_rect.y))

    else:
        if any_plant_ready:
            pygame.draw.rect(screen, (255, 0, 0), harvest_btn_rect, 2)
            txt = small_font.render("Harvest", True, (255, 0, 0))
        else:
            pygame.draw.rect(screen, (100, 100, 100), harvest_btn_rect, 2)
            txt = small_font.render("Harvest", True, (100, 100, 100))
        screen.blit(txt, (harvest_btn_rect.x + 100, harvest_btn_rect.y + 20))
        
    canopy_btn_rect = pygame.Rect(1120, 615, 100, 100)
    if img_intact_canopy:
        screen.blit(img_intact_canopy, (canopy_btn_rect.x, canopy_btn_rect.y))
    else:  
        if has_intact_canopy:
            pygame.draw.rect(screen, (34, 139, 34), canopy_btn_rect)
            screen.blit(font.render("Canopy", True, (255, 255, 255)), (canopy_btn_rect.x + 15, canopy_btn_rect.y + 40))
        else:  
            pygame.draw.rect(screen, (80, 80, 80), canopy_btn_rect, 2)
            screen.blit(small_font.render("Locked", True, (120, 120, 120)), (canopy_btn_rect.x + 20, canopy_btn_rect.y + 40))


    pure_soil_btn_rect = pygame.Rect(700, 615, 100, 100)
    if img_pure_soil:
            screen.blit(img_pure_soil,(pure_soil_btn_rect.x, pure_soil_btn_rect.y))
    else:
            pygame.draw.rect(screen, (139, 69, 19), pure_soil_btn_rect)
    
    oxygen_btn_rect = pygame.Rect(900, 615, 100, 100)
    if img_oxygen_recycler:
        screen.blit(img_oxygen_recycler, (oxygen_btn_rect.x, oxygen_btn_rect.y))
    else:
        pygame.draw.rect(screen, (70, 70, 150), oxygen_btn_rect)
    

    circle_radius = 13
    badge_font = pygame.font.SysFont("Arial", 12, bold=True)

    buttons_with_counts = [
        (pure_soil_btn_rect, pure_soil_count),
        (oxygen_btn_rect, oxygen_count),
        (canopy_btn_rect, canopy_count)
    ]

    for btn_rect, count in buttons_with_counts:
        circle_center = (btn_rect.x + 90, btn_rect.y + 5)
        
        pygame.draw.circle(screen, (185, 25, 15), circle_center, circle_radius)
        
        count_txt = badge_font.render(f"x{count}", True, (255, 255, 255))
        txt_rect = count_txt.get_rect(center=circle_center)
        screen.blit(count_txt, txt_rect)

    return canopy_btn_rect, pure_soil_btn_rect, oxygen_btn_rect, plant_seed_btn_rect, harvest_btn_rect

def draw_plant_menu(screen):
    global img_plant_menu_bg, img_aloe_btn, img_thorn_btn
    
    menu_w, menu_h = 550, 425
    rect = pygame.Rect((1280 - menu_w) // 2, (720 - menu_h) // 2, menu_w, menu_h)
    
    if img_plant_menu_bg is None:
        possible_path = "image/background/PlantSeed_bg.png"
        
        if os.path.exists(possible_path):
            try:
                img_plant_menu_bg = pygame.image.load(possible_path).convert_alpha()
                img_plant_menu_bg = pygame.transform.smoothscale(img_plant_menu_bg, (menu_w, menu_h))
                print("[SUCCESS] PlantSeed_bg.jpg loaded successfully into memory!")
            except Exception as e:
                print(f"[ERROR] File exists, but Pygame failed to read it: {e}")
        else:
            print(f"[ERROR] Cannot find image file! Expected absolute path: {os.path.abspath(possible_path)}")

    
    if img_plant_menu_bg:
        screen.blit(img_plant_menu_bg, rect)
    else:
        overlay = pygame.Surface((menu_w, menu_h), pygame.SRCALPHA)
        overlay.fill((0, 255, 0, 200)) # Green with 200 alpha transparency
        screen.blit(overlay, rect)
        
        debug_font = pygame.font.SysFont("Arial", 24)
        error_txt = debug_font.render("ERROR: PlantSeed_bg.jpg missing!", True, (255, 0, 0))
        screen.blit(error_txt, (rect.x + 50, rect.y + 50))
    
    if img_aloe_btn is None:
        for ext in [".png", ".jpg", ".PNG", ".JPG"]:
            possible_path = f"image/button/AloeVera_button{ext}"
            if os.path.exists(possible_path):
                try:
                    img_aloe_btn = pygame.image.load(possible_path).convert_alpha()
                    img_aloe_btn = pygame.transform.smoothscale(img_aloe_btn, (150, 200)) # 缩放到合适大小
                    break
                except pygame.error as e:
                    print(f"Error loading AloeVera button: {e}")

    if img_thorn_btn is None:
        for ext in [".png", ".jpg", ".PNG", ".JPG"]:
            possible_path = f"image/button/Thorn_button{ext}"
            if os.path.exists(possible_path):
                try:
                    img_thorn_btn = pygame.image.load(possible_path).convert_alpha()
                    img_thorn_btn = pygame.transform.smoothscale(img_thorn_btn, (150, 200))
                    break
                except pygame.error as e:
                    print(f"Error loading Thorn button: {e}")

    aloe_btn_rect = pygame.Rect(rect.x + 70, rect.y + 110, 150, 200)
    thorn_btn_rect = pygame.Rect(rect.x + 330, rect.y + 110, 150, 200)

    if img_aloe_btn:
        screen.blit(img_aloe_btn, (aloe_btn_rect.x, aloe_btn_rect.y))
    else:
        pygame.draw.rect(screen, (0, 255, 0), aloe_btn_rect, 2) 

    if img_thorn_btn:
        screen.blit(img_thorn_btn, (thorn_btn_rect.x, thorn_btn_rect.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), thorn_btn_rect, 2) 
        
   
    return rect, aloe_btn_rect, thorn_btn_rect