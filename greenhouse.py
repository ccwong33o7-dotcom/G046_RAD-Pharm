import pygame

COLOR_BG = (30, 30, 30)
COLOR_TEXT = (200, 200, 200)

class Plant:
    def __init__(self, x_pos, name, dust_speed):
        self.rect = pygame.Rect(x_pos, 400, 150, 200)
        self.name = name
        self.growth = 0
        self.dust = 0
        self.dust_speed = dust_speed 
        self.is_dead = False
        self.death_timer = 0

        try:
            self.img_seedling = pygame.image.load("image/seedling.png").convert_alpha()
            self.img_bud = pygame.image.load("image/bud.png").convert_alpha()
            self.img_flower = pygame.image.load("image/flower.png").convert_alpha()

            self.img_wilt_1 = pygame.image.load("image/wilt_1.png").convert_alpha()
            self.img_wilt_2 = pygame.image.load("image/wilt_2.png").convert_alpha()
        
        except pygame.erroe as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            import sys
            sys.exit()
    
    def update(self):
        if self.is_dead: return

        self.dust += self.dust_speed
        if self.dust > 100: 
            self.dust = 100

        if self.dust < 70:
            self.growth += 0.05
            if self.growth > 100:
                self.growth = 100

        if self.dust >= 100:
            self.is_dead = True

        def clean(self):
         self.dust -= 20
        if self.dust < 0:
            self.dust = 0

    
    def draw(self, surface):
        current_height = (self.growth / 100) * 150
        plant_rect = pygame.Rect(self.rect.x, self.rect.bottom - current_height, self.rect.width, current_height)
        color = COLOR_DEAD if self.is_dead else COLOR_PLANT
        pygame.draw.rect(surface, color, plant_rect)

        font_small = pygame.font.SysFont("Arial", 18)
        name_txt = font_small.render(f"{self.name}", True, COLOR_TEXT)
        stats_txt = font_small.render(f"D:{int(self.dust)}% G:{int(self.growth)}%", True, COLOR_TEXT)
        surface.blit(name_txt, (self.rect.x, self.rect.y - 40))
        surface.blit(stats_txt, (self.rect.x, self.rect.y - 20))

def draw_greenhouse(screen, font, plant_list):
    screen.fill(COLOR_BG)

    for p in plant_list:
        p.update()
        p.draw(screen)


    small_font = pygame.font.SysFont("Arial", 20)
    setting_btn_rect = pygame.Rect(1150, 30, 100, 40)
    back_btn_rect = pygame.Rect(1150, 80, 100, 40)
    
    pygame.draw.rect(screen, (150, 50, 50), setting_btn_rect)
    pygame.draw.rect(screen, (100, 100, 250), back_btn_rect)
    
    screen.blit(small_font.render("Setting", True, (255, 255, 255)), (1165, 40))
    screen.blit(small_font.render("Back", True, (255, 255, 255)), (1175, 90))

    return setting_btn_rect, back_btn_rect





