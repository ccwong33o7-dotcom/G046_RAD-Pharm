import pygame
import os

class TaskBar:
    def __init__(self, screen_width):
        self.screen_width = screen_width

        self.setting_icon = None
        self.load_assets()
        self.settings_btn_rect = pygame.Rect(28, 20, 40, 40)

        self.font = pygame.font.SysFont("Arial", 30, bold=True) 
        self.small_font = pygame.font.SysFont("Arial", 14)

    def load_assets(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        setting_path = os.path.join(base_path, "image", "setting_button.png")
        if os.path.exists(setting_path):
            try:
                img = pygame.image.load(setting_path).convert_alpha()
                self.setting_icon = pygame.transform.scale(img, (40, 40))
                print("TaskBar: Setting Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Setting Icon Failed: {e}")

    def draw(self, screen, current_day):
        if self.setting_icon:
            screen.blit(self.setting_icon, (self.settings_btn_rect.x, self.settings_btn_rect.y))
        else:
            pygame.draw.circle(screen, (150, 50, 50), self.settings_btn_rect.center, 20)

        day_text = f"DAY {current_day}"
        
        day_surf = self.font.render(day_text, True, (210, 70, 50)) 
        
        day_x = 515 - (day_surf.get_width() // 2)
        day_y = 22 
        
        screen.blit(day_surf, (day_x, day_y))

    def check_click(self, mouse_pos):
        if self.settings_btn_rect.collidepoint(mouse_pos):
            return "settings"
        return None