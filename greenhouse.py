import pygame

COLOR_BG = (30, 30, 30)
COLOR_PLANT= (50, 200, 50)
COLOR_DUST = (150, 150, 100)
COLOR_TEXT = (200, 200, 200)

class Plant:
    def __init__(self):
        self.rect = pygame.Rect(590, 500, 100, 100)
        self.growth = 0
        self.dust = 0
        self.is_dead = False
    
    def update(self):
        if self.is_dead: return

        self.dust += 0.1
        if self.dust > 100: 
            self.dust = 100

        if self.dust < 70:
            self.growth += 0.05

        if self.dust >= 100:
            self.is_dead = True
    
    def clean(self):
        self.dust -= 20
        
        if self.dust < 0: 
            self.dust = 0
    
    def draw(self, surface):
        current_height = (self.growth / 100) * 150
        plant_rect = pygame.Rect(self.rect.x, self.rect.bottom - current_height, self.rect.width, current_height)
        color = (100, 100, 100) if self.is_dead else COLOR_PLANT
        pygame.draw.rect(surface, color, plant_rect)



def draw_greenhouse(screen, font, my_plant):
    screen.fill(COLOR_BG)
    my_plant.update()
    my_plant.draw(screen)

    status_text = font.render(f"Growth: {int(my_plant.growth)}%  Dust: {int(my_plant.dust)}%", True, COLOR_TEXT)
    screen.blit(status_text, (20,20))

    if my_plant.is_dead:
       death_text = font.render("PLANT DIED! (Too much radiation)", True, (255, 0, 0))
       screen.blit(death_text, (1280 // 2 - 150, 720 // 2))

    small_font = pygame.font.SysFont("Arial", 20)

    setting_btn_rect = pygame.Rect(1150, 30, 100, 40)
    pygame.draw.rect(screen, (150, 50, 50), setting_btn_rect)
    set_text = small_font.render("Setting", True, (255, 255, 255))
    screen. blit(set_text, (setting_btn_rect.x +15, setting_btn_rect.y + 10))
    
    back_btn_rect = pygame.Rect(1150, 80, 100, 40)
    pygame.draw.rect(screen, (100, 100, 250), back_btn_rect)
    btn_text = small_font.render("Back", True, (255, 255, 255))
    screen.blit(btn_text, (back_btn_rect.x + 25, back_btn_rect.y + 10))

    return setting_btn_rect, back_btn_rect





