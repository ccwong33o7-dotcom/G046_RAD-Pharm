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
img_tire = None
img_drum1 = None
img_drum2 = None
img_drum3 = None
img_tire2 = None
img_drum4 = None
    
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
        self.planted = False

        self.img_growth = []
        self.img_dead = []

        self.is_dead = False
        self.death_timer = 0
        self.delete_btn_rect = None


        try:
            if self.name == "Glowing Aloe":

              self.img_seedling = pygame.image.load(
                "image/plant/Seedling aloe.png"
              ).convert_alpha()

              self.img_bud = pygame.image.load(
                "image/plant/Growing aloe.png"
              ).convert_alpha()

              self.img_flower = pygame.image.load(
                 "image/plant/Aloe.png"
              ).convert_alpha()

              self.img_wilt_1 = pygame.image.load(
                  "image/plant/Aloe.png"
              ).convert_alpha()

              self.img_wilt_2 = pygame.image.load(
                  "image/plant/Aloe wilt1.png"
              ).convert_alpha()

              self.img_wilt_3 = pygame.image.load(
                 "image/plant/Aloe wilt2.png"
              ).convert_alpha()


            elif self.name == "Rusty Thorn":

              self.img_seedling = pygame.image.load(
                 "image/plant/seedling thorn.png"
              ).convert_alpha()

              self.img_bud = pygame.image.load(
                 "image/plant/Growing thorn.png"
              ).convert_alpha()

              self.img_flower = pygame.image.load(
                 "image/plant/Mature thorn.png"
              ).convert_alpha()

              self.img_wilt_1 = pygame.image.load(
                 "image/plant/Mature thorn.png"
              ).convert_alpha()

              self.img_wilt_2 = pygame.image.load(
                 "image/plant/Thorn wilt1.png"
              ).convert_alpha()

              self.img_wilt_3 = pygame.image.load(
                "image/plant/Thorn wilt2.png"
              ).convert_alpha()

        except pygame.error as e:
            print(f"Error loading images for {self.name}: {e}")

    def update(self):
     if not self.planted:
        return

     self.dust += self.dust_speed
     if self.dust >= 100:
        self.dust = 100
        if not self.is_dead:
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

        if not self.planted:
          return

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

        if self.is_dead:
            self.delete_btn_rect = pygame.Rect(self.rect.x + 35, self.rect.y - 60, 50, 30)
            pygame.draw.rect(surface, (139, 69, 19), self.delete_btn_rect) 
            
            small_font = pygame.font.SysFont("Arial", 12, bold=True)
            txt = small_font.render("Clear", True, (255, 255, 255))
            surface.blit(txt, (self.delete_btn_rect.x + 10, self.delete_btn_rect.y + 8))
        else:
            self.delete_btn_rect = None
     

def draw_greenhouse(screen, font, plant_list, bg_image=None, pure_soil_count=0, oxygen_count=0, canopy_count=0, has_intact_canopy=False, has_oxygen_recycler=False, ready_to_craft=False, locked_plots=None):
    global img_pure_soil, img_intact_canopy, img_oxygen_recycler, img_plant_seed, img_harvest
    global img_tire, img_drum1, img_drum2, img_drum3, img_tire2, img_drum4
    small_font = pygame.font.SysFont("Arial", 20)

    aloe_btn_rect = pygame.Rect(25, 630, 120, 65)
    thorn_btn_rect = pygame.Rect(160, 630, 120, 65)
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
    
    if img_tire is None and os.path.exists("image/Obstacles/Tires.png"):
        img_tire = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Tires.png").convert_alpha(), (170, 120))
    if img_drum1 is None and os.path.exists("image/Obstacles/Drum1.png"):
        img_drum1 = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Drum1.png").convert_alpha(), (115, 155))
    if img_drum2 is None and os.path.exists("image/Obstacles/Drum 2.png"):
        img_drum2 = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Drum 2.png").convert_alpha(), (100, 140))
    if img_drum3 is None and os.path.exists("image/Obstacles/Drum 3.png"):
        img_drum3 = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Drum 3.png").convert_alpha(), (100, 140))
    if img_tire2 is None and os.path.exists("image/Obstacles/Tires 2.png"):
        img_tire2 = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Tires 2.png").convert_alpha(), (120, 110))
    if img_drum4 is None and os.path.exists("image/Obstacles/Drum 4.png"):
        img_drum4 = pygame.transform.smoothscale(pygame.image.load("image/Obstacles/Drum 4.png").convert_alpha(), (100, 140))


    if bg_image:
        screen.blit(bg_image, (0,0))
    else:
        screen.fill(COLOR_BG)
    
    if locked_plots:
        for plot in locked_plots:
            img = None
            if plot['type'] == 'tire': img = img_tire
            elif plot['type'] == 'drum1': img = img_drum1
            elif plot['type'] == 'drum2': img = img_drum2
            elif plot['type'] == 'drum3': img = img_drum3
            elif plot['type'] == 'tire2': img = img_tire2
            elif plot['type'] == 'drum4': img = img_drum4
            if img: screen.blit(img, (plot['x'], plot['y']))
    
    for p in plant_list:
        p.update()
        p.draw(screen)
    
    small_font = pygame.font.SysFont("Arial", 16)
    pygame.draw.rect(screen, (0, 100, 0), aloe_btn_rect, border_radius=10)
    screen.blit(small_font.render("Plant Aloe", True, (255, 255, 255)), (aloe_btn_rect.x + 20, aloe_btn_rect.y + 20))
    
    pygame.draw.rect(screen, (100, 0, 0), thorn_btn_rect, border_radius=10)
    screen.blit(small_font.render("Plant Thorn", True, (255, 255, 255)), (thorn_btn_rect.x + 20, thorn_btn_rect.y + 20))

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

    return canopy_btn_rect, pure_soil_btn_rect, oxygen_btn_rect, harvest_btn_rect, aloe_btn_rect, thorn_btn_rect

