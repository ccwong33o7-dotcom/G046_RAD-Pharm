import pygame
import os
import sys

class TaskBar:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.background_img = None
        self.setting_icon = None
        self.cookie_icon = None
        self.map_icon = None
        self.weather_icon = None
        self.survivor_icon = None
        self.bar_height = 65
        self.y_offset = 0
        self.load_assets()

        self.settings_btn_rect = pygame.Rect(50, 10 + self.y_offset, 42, 42)
        self.map_btn_rect = pygame.Rect(115, 10 + self.y_offset, 42, 42)
        self.weather_btn_rect = pygame.Rect(175, 10 + self.y_offset, 42, 42)

        self.font = pygame.font.SysFont("Agency FB", 32, bold=True) 
        self.money_font = pygame.font.SysFont("Agency FB", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 12)

        self.button_infos = [
            (self.settings_btn_rect, "Settings"),
            (self.map_btn_rect, "Map"),
            (self.weather_btn_rect, "Weather")
        ]
        self.tooltip_font = pygame.font.SysFont("Arial", 18, bold=True)

    def load_assets(self):
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        bg_path = os.path.join(base_path, "image", "background", "taskbarbg.png")  
        if os.path.exists(bg_path):
            try:
                img = pygame.image.load(bg_path).convert_alpha()
                self.background_img = pygame.transform.smoothscale(img, (self.screen_width, self.bar_height))
                print("TaskBar: Background Image Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Background Image Failed: {e}")
        else:
            print(f"TaskBar: taskbarbg.jpg not found at {bg_path}")
        
        setting_path = os.path.join(base_path, "image", "button", "setting_button.png")
        if os.path.exists(setting_path):
            try:
                img = pygame.image.load(setting_path).convert_alpha()
                self.setting_icon = pygame.transform.smoothscale(img, (42, 42))
                print("TaskBar: Setting Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Setting Icon Failed: {e}")
        
        map_path = os.path.join(base_path, "image", "button", "Map button.png")
        if os.path.exists(map_path):
            try:
                img = pygame.image.load(map_path).convert_alpha()
                self.map_icon = pygame.transform.smoothscale(img, (42, 42))
                print("TaskBar: Map Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Map Icon Failed: {e}")

        weather_path = os.path.join(base_path, "image", "icon", "Sunny_icon.png")
        if os.path.exists(weather_path):
            try:
                img = pygame.image.load(weather_path).convert_alpha()
                self.weather_icon = pygame.transform.smoothscale(img, (42, 42))
                print("TaskBar: Weather Icon Loaded Successfully")
            except Exception as e:
                print(f"TaskBar: Weather Icon Failed: {e}")
        else:
            print(f"TaskBar: weather icon not found at {weather_path}")

        cookie_path = os.path.join(base_path, "image", "icon", "Cookies_currency.png")
        if os.path.exists(cookie_path):
            try:
                c_img = pygame.image.load(cookie_path).convert_alpha()
                self.cookie_icon = pygame.transform.smoothscale(c_img, (42, 42))
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
                self.survivor_icon = pygame.transform.smoothscale(s_img, (36, 36))
                print("TaskBar: Survivor Icon Loaded Successfully")
            except Exception as e:
                self.survivor_icon = None
                print(f"TaskBar: Survivor Icon Failed: {e}")
        else:
            self.survivor_icon = None
            print(f"TaskBar: survivor.jpg not found at {survivor_path}")

    def draw(self, screen, current_day, cookies, saved_people=0, weather_sys_param=None, mouse_pos=None):
        if self.background_img:
            screen.blit(self.background_img, (0, self.y_offset))
        else:
            debug_bar = pygame.Surface((self.screen_width, self.bar_height))
            debug_bar.fill((255, 0, 0)) 
            screen.blit(debug_bar, (0, 0))

        if self.setting_icon:
            screen.blit(self.setting_icon, (self.settings_btn_rect.x, self.settings_btn_rect.y))
        
        if self.map_icon:
            screen.blit(self.map_icon, (self.map_btn_rect.x, self.map_btn_rect.y))
        else:
            pygame.draw.circle(screen, (50, 100, 150), self.map_btn_rect.center, 20)

        dynamic_icon = None
        if weather_sys_param and hasattr(weather_sys_param, 'current_weather'):
            if weather_sys_param.current_weather in weather_sys_param.weather_icons:
                dynamic_icon = weather_sys_param.weather_icons[weather_sys_param.current_weather]

        if dynamic_icon:
            dynamic_icon = pygame.transform.smoothscale(dynamic_icon, (42, 42))
            screen.blit(dynamic_icon, (self.weather_btn_rect.x, self.weather_btn_rect.y))

        elif self.weather_icon:
            screen.blit(self.weather_icon, (self.weather_btn_rect.x, self.weather_btn_rect.y))

        else:
            pygame.draw.circle(screen, (120, 90, 40), self.weather_btn_rect.center, 20)

        day_text = f"DAY {current_day}"
        day_surf = self.font.render(day_text, True, (220, 204, 207))
        day_x = (self.screen_width // 2) - (day_surf.get_width() // 2)
        day_y = 14 + self.y_offset
        screen.blit(day_surf, (day_x, day_y))

        money_text = f"{cookies}"
        money_surf = self.money_font.render(money_text, True, (230, 230, 230))
        cookie_w, cookie_h = 37, 37 
        if self.cookie_icon and self.cookie_icon.get_size() != (cookie_w, cookie_h):
            self.cookie_icon = pygame.transform.smoothscale(self.cookie_icon, (cookie_w, cookie_h))

        base_x = 992
        cookie_y = 14 + self.y_offset

        if self.cookie_icon:
            screen.blit(self.cookie_icon, (base_x, cookie_y))

        text_x = base_x + 34 + 10
        text_y = 17 + self.y_offset

        screen.blit(money_surf, (text_x, text_y))

        survivor_x = text_x + money_surf.get_width() + 55
        survivor_y = 13 + self.y_offset

        if self.survivor_icon:
            screen.blit(self.survivor_icon, (survivor_x, survivor_y))

        people_text = f"{saved_people} / 25"
        people_surf = self.money_font.render(people_text, True, (230, 230, 230))
        people_text_x = survivor_x + 28 + 10
        people_text_y = 17 + self.y_offset
        screen.blit(people_surf, (people_text_x, people_text_y))

        if mouse_pos:
            hovered_rect = None
            hovered_name = None
            for rect, name in self.button_infos:
                if rect.collidepoint(mouse_pos):
                    hovered_rect = rect
                    hovered_name = name
                    break

            if hovered_rect and hovered_name:
                text_surf = self.tooltip_font.render(hovered_name, True, (255, 255, 255))
                text_surf.set_alpha(180)
                text_rect = text_surf.get_rect()
                tip_x = hovered_rect.centerx - text_rect.width // 2
                tip_y = hovered_rect.top - text_rect.height + 62
                if tip_x < 0:
                    tip_x = 0
                if tip_x + text_rect.width > self.screen_width:
                    tip_x = self.screen_width - text_rect.width
                screen.blit(text_surf, (tip_x, tip_y))

    def check_click(self, mouse_pos):
        if self.settings_btn_rect.collidepoint(mouse_pos):
            return "settings"
        if self.map_btn_rect.collidepoint(mouse_pos):
            return "map"
        if self.weather_btn_rect.collidepoint(mouse_pos): 
            return "weather"
        return None