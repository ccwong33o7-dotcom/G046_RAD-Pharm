import pygame
import os

class TaskBar:
    def __init__(self, screen_width):
        self.screen_width = screen_width

        self.setting_icon = None
        self.cookie_icon = None
        self.map_icon = None
        self.weather_icon = None
        self.survivor_icon = None
        self.load_assets()

        self.settings_btn_rect = pygame.Rect(57,21,47,47)
        self.map_btn_rect = pygame.Rect(130,21,48,48)
        self.weather_btn_rect = pygame.Rect(203, 21, 48, 48)

        self.font = pygame.font.SysFont("Agency FB", 34, bold=True) 
        self.money_font = pygame.font.SysFont("Agency FB", 38, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 14)

    def load_assets(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        setting_path = os.path.join(base_path, "image", "button", "setting_button.png")
        if os.path.exists(setting_path):
            try:
                img = pygame.image.load(setting_path).convert_alpha()
                self.setting_icon = pygame.transform.smoothscale(img, (47, 47))
                print("TaskBar: Setting Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Setting Icon Failed: {e}")
        
        map_path = os.path.join(base_path, "image", "button", "Map button.png")
        if os.path.exists(map_path):
            try:
                img = pygame.image.load(map_path).convert_alpha()
                self.map_icon = pygame.transform.smoothscale(img, (48, 48))
                print("TaskBar: Map Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Map Icon Failed: {e}")

        weather_path = os.path.join(base_path, "image", "icon", "Sunny_icon.png")
        if os.path.exists(weather_path):
            try:
                img = pygame.image.load(weather_path).convert_alpha()
                self.weather_icon = pygame.transform.smoothscale(img, (48, 48))
                print("TaskBar: Weather Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Weather Icon Failed: {e}")
        else:
            print(f"TaskBar: weather icon not found at {weather_path}")

        cookie_path = os.path.join(base_path, "image", "icon", "Cookies_currency.png")
        if os.path.exists(cookie_path):
            try:
                c_img = pygame.image.load(cookie_path).convert_alpha()
                self.cookie_icon = pygame.transform.smoothscale(c_img, (48, 48))
                print("TaskBar: Cookies Currency Icon Loaded Successfully")
            except Exception as e:
                self.cookie_icon = None
                print(f"TaskBar: Cookie Icon Failed: {e}")
        else:
            self.cookie_icon = None
            print("TaskBar: Cookie_currency.png not found at path")

        survivor_path = os.path.join(base_path, "image", "icon", "survivor.png")
        if os.path.exists(survivor_path):
            try:
                s_img = pygame.image.load(survivor_path).convert_alpha()
                self.survivor_icon = pygame.transform.smoothscale(s_img, (37, 37))
                print("TaskBar: Survivor Icon Loaded Successfully")
            except Exception as e:
                self.survivor_icon = None
                print(f"TaskBar: Survivor Icon Failed: {e}")
        else:
            self.survivor_icon = None
            print(f"TaskBar: survivor.jpg not found at {survivor_path}")

    def draw(self, screen, current_day, cookies, saved_people=0, weather_sys_param=None):
        if self.setting_icon:
            screen.blit(self.setting_icon, (self.settings_btn_rect.x, self.settings_btn_rect.y))
        else:
            pygame.draw.circle(screen, (150, 50, 50), self.settings_btn_rect.center, 20)
        
        if self.map_icon:
            screen.blit(self.map_icon, (self.map_btn_rect.x, self.map_btn_rect.y))
        else:
            pygame.draw.circle(screen, (50, 100, 150), self.map_btn_rect.center, 20)

        dynamic_icon = None
        if weather_sys_param and hasattr(weather_sys_param, 'current_weather'):
            if weather_sys_param.current_weather in weather_sys_param.weather_icons:
                dynamic_icon = weather_sys_param.weather_icons[weather_sys_param.current_weather]

        if dynamic_icon:
            screen.blit(dynamic_icon, (self.weather_btn_rect.x, self.weather_btn_rect.y))
        else:
            pygame.draw.circle(screen, (220, 180, 50), self.weather_btn_rect.center, 20)

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

        base_x = 940
        cookie_y = 25

        if self.cookie_icon:
            screen.blit(self.cookie_icon, (base_x, cookie_y))

        text_x = base_x + cookie_w + 15
        text_y = 33

        screen.blit(money_surf, (text_x, text_y))

        survivor_x = text_x + money_surf.get_width() + 40
        survivor_y = 25

        if self.survivor_icon:
            screen.blit(self.survivor_icon, (survivor_x, survivor_y))
        else:
            pygame.draw.rect(screen, (50, 150, 50), (survivor_x, survivor_y, 37, 37), border_radius=5)

        people_text = f"{saved_people} / 25"
        people_surf = self.money_font.render(people_text, True, (230, 230, 230))
        people_text_x = survivor_x + 37 + 12
        people_text_y = 33
        screen.blit(people_surf, (people_text_x, people_text_y))

    def check_click(self, mouse_pos):
        if self.settings_btn_rect.collidepoint(mouse_pos):
            return "settings"
        if self.map_btn_rect.collidepoint(mouse_pos):
            return "map"
        if self.weather_btn_rect.collidepoint(mouse_pos): 
            return "weather"
        return None