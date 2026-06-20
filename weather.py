import pygame
import os

SUNNY = "SUNNY"
CLOUDY = "CLOUDY"
STORMY = "STORMY"

WEATHER_SCHEDULE = {
    1: SUNNY,
    2: CLOUDY,
    3: STORMY,
    4: CLOUDY,
    5: SUNNY,
    6: SUNNY,
    7: STORMY,
    8: SUNNY,
    9: CLOUDY,
    10: SUNNY
}

class WeatherSystem:
    def __init__(self):
        self.current_weather = SUNNY
        self.weather_icons = {}
        self.load_icons()
        
        self.title_font = pygame.font.SysFont("Agency FB", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 18, bold=False)

    def load_icons(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        weather_files = {
            SUNNY: "Sunny_icon.png",    
            CLOUDY: "Cloudy_icon.png", 
            STORMY: "storm_icon.png"  
        }
        
        for w_type, filename in weather_files.items():
            path = os.path.join(base_path, "image", "icon", filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    self.weather_icons[w_type] = pygame.transform.smoothscale(img, (48, 48))
                except Exception as e:
                    print(f"Weather: Failed to load {w_type} icon: {e}")

    def update_weather(self, day):
        """Updates the weather based on the current day."""
        self.current_weather = WEATHER_SCHEDULE.get(day, SUNNY)

    def show_weather_explanation(self, screen, clock):
        """Runs a loop to explain the weather mechanics after the intro."""
        explaining = True

        intro_text = [
            "[ DOOMSDAY WEATHER OBSERVER SYSTEM ]",
            "In this harsh world, weather directly affects plant growth and outside dangers.",
            "There are 3 types of weather conditions you will encounter:",
            "  1. SUNNY: Plentiful sunlight. Plants grow much faster.",
            "  2. CLOUDY: Overcast skies. Plant growth speed might slow down.",
            "  3. STORMY: Severe weather! Dust accumulation spikes. Protect your greenhouse!",
            "",
            "[ HOW TO PROGRESS TO THE NEXT DAY ]",
            "Every day, you must brave the wasteland to rescue survivors.",
            "Successfully rescue 25 PEOPLE to clear the day and unlock the next level!",
            "",
            "--- Click anywhere or press any key to start Day 1 ---"
        ]

        while explaining:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys; sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    explaining = False  
                    print("Weather System acknowledged. Transitioning to PHARMACY...")
                    return "PHARMACY"  

            box_rect = pygame.Rect(200, 80, 880, 560)
            pygame.draw.rect(screen, (30, 28, 25), box_rect)
            pygame.draw.rect(screen, (180, 140, 70), box_rect, 3) 

            title_surf = self.title_font.render(intro_text[0], True, (240, 190, 80))
            screen.blit(title_surf, (1280 // 2 - title_surf.get_width() // 2, 110))

            start_y = 190
            for line in intro_text[1:]:
                if "SUNNY" in line: color = (255, 215, 0)    
                elif "CLOUDY" in line: color = (170, 190, 210)  
                elif "STORMY" in line: color = (240, 90, 80)     
                elif "25 PEOPLE" in line: color = (100, 255, 100) 
                else: color = (220, 220, 220)                   
                
                text_surf = self.text_font.render(line, True, color)
                screen.blit(text_surf, (240, start_y))
                start_y += 34

            pygame.display.flip()
            clock.tick(60)