import pygame
import os

class TaskBar:
    def __init__(self, screen_width):
        self.screen_width = screen_width

        self.setting_icon = None
        self.cookies_icon = None
        self.load_assets()
        self.settings_btn_rect = pygame.Rect(45,20,48,48)

        self.font = pygame.font.SysFont("Agency FB", 34, bold=True) 
        self.money_font = pygame.font.SysFont("Agency FB", 38, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14)

    def load_assets(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        setting_path = os.path.join(base_path, "image", "button", "setting_button.png")
        if os.path.exists(setting_path):
            try:
                img = pygame.image.load(setting_path).convert_alpha()
                self.setting_icon = pygame.transform.smoothscale(img, (48, 48))
                print("TaskBar: Setting Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Setting Icon Failed: {e}")

        cookie_path = os.path.join(base_path, "image", "Cookies_currency.png")
        if os.path.exists(cookie_path):
            try:
                c_img = pygame.image.load(cookie_path).convert_alpha()
                self.cookie_icon = pygame.transform.smoothscale(c_img, (48, 48))
                print("TaskBar: Cookies Currency Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Setting Icon Failed: {e}")

    def draw(self, screen, current_day,cookies):
        if self.setting_icon:
            screen.blit(self.setting_icon, (self.settings_btn_rect.x, self.settings_btn_rect.y))
        else:
            pygame.draw.circle(screen, (150, 50, 50), self.settings_btn_rect.center, 20)

        day_text = f"DAY {current_day}"
        day_surf = self.font.render(day_text, True, (200, 204, 207))
        day_x = 612 - (day_surf.get_width() // 2)
        day_y = 35
        screen.blit(day_surf, (day_x, day_y))

        money_text = f"{cookies}"
        money_surf = self.money_font.render(money_text, True, (230, 230, 230))
        cookie_w, cookie_h = 37, 37 
        if self.cookie_icon and self.cookie_icon.get_size() != (cookie_w, cookie_h):
            self.cookie_icon = pygame.transform.smoothscale(self.cookie_icon, (cookie_w, cookie_h))

        base_x = 960
        cookie_y = 25

        if self.cookie_icon:
            screen.blit(self.cookie_icon, (base_x, cookie_y))

        text_x = base_x + cookie_w + 15
        text_y = 33

        screen.blit(money_surf, (text_x, text_y))

    def check_click(self, mouse_pos):
        if self.settings_btn_rect.collidepoint(mouse_pos):
            return "settings"
        return None