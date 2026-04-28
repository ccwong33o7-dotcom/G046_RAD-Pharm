import pygame
import os

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

        self.img_growth = []
        self.img_dead = []


        try:
            self.img_seedling = pygame.image.load("image/seedling.jpeg").convert_alpha()
            self.img_bud = pygame.image.load("image/bud.jpeg").convert_alpha()
            self.img_flower = pygame.image.load("image/flower.jpeg").convert_alpha()

            self.img_wilt_1 = pygame.image.load("image/wilt_1.jpeg").convert_alpha()
            self.img_wilt_2 = pygame.image.load("image/wilt_2.jpeg").convert_alpha()
            self.img_wilt_3 = pygame.image.load("image/wilt_3.jpeg").convert_alpha()
        
        except pygame.error as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            import sys
            sys.exit()
    
    def update(self):
        self.dust += self.dust_speed
        if self.dust > 100: 
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
        current_image = None
        if not self.is_dead:
            if self.growth < 33:
                current_image = self.img_seedling
            elif self.growth < 66:
                current_image = self.img_bud
            else:
                current_image = self.img_flower
        else:
            if self.death_timer < 300:
                current_image = self.img_wilt_1
            elif self.death_timer < 600:
                current_image = self.img_wilt_2
            else:
                current_image = self.img_wilt_3
        
        scaled_image = pygame.transform.scale(current_image, (self.rect.width, self.rect.height))
        surface.blit(scaled_image, (self.rect.x, self.rect.y))

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





