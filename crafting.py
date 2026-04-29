import pygame 

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 32, bold=True)

RECIPES = {
    "Rad-Ointment": {"Filtered water": 1, "Glowing Aloe": 1 , "Scrap Fiber": 1},
    "Speed Serum": {"Bio-Fuel": 1, "Rusty Thorn": 1, "Filtered water": 1},
    "Lung-Clear": {"Filtered water":1, "Glowing Aloe": 1},
    "Blood-Stop":{"Scrap Fiber":1, "Rusty Thorn": 1},
    "Pain Killer":{"Bio_Fuel":1, "Glowing Aloe": 1, "Rusty Thorn": 1}
}

inventory = {"Filtered water": "Infinite", "Bio-Fuel": "Infinite", "Scrap Fiber": "Infinite", "Glowing Aloe": 2, "Rusty Thorn":2 
             ,"Rad-Ointment": 0 , "Speed Serum": 0, "Lung-Clear": 0, "Blood-Stop": 0, "Pain Killer": 0}

game_state = "MENU"
pending_item = ""
marker_pos = 0
marker_speed = 8
bar_width = 400
bar_x = (screen_width // 2) - (bar_width // 2)
target_zone = (150, 250)
            
def check_resources(item_name):
    recipe = RECIPES[item_name]
    infinite_resources = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]
    for ingredient, amount_needed in recipe.items():
        if ingredient not in infinite_resources:
            if inventory[ingredient] < amount_needed:
                return False
    return True

def craft_success(item_name):
    recipe = RECIPES[item_name]
    infinites = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]
    for ingredient, amount in recipe.items():
        if ingredient not in infinites:
            inventory[ingredient] -= amount
    inventory[item_name] += 1
        
running = True
while running:
    screen.fill((30, 30, 30))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "MENU":
            if event.type == pygame.KEYDOWN:
                selection = None
                if event.key == pygame.K_1: selection = "Rad-Ointment"
                elif event.key == pygame.K_2: selection = "Speed Serum"
                elif event.key == pygame.K_3: selection = "Lung-Clear"
                elif event.key == pygame.K_4: selection = "Blood-Stop"
                elif event.key == pygame.K_5: selection = "Pain Killer"

                if selection:
                    if check_resources(selection):
                        pending_item = selection
                        game_state = "MINIGAME"
                        marker_pos = 0 
                    else:
                        print(f"Missing ingredients for {selection}!")

        elif game_state == "MINIGAME":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if target_zone[0] <= marker_pos <= target_zone[1]:
                    craft_success(pending_item)
                    print("SUCCESS!")
                else:
                    print("FAILED!")
                game_state = "MENU"

    
    if game_state == "MENU":
        y_offset = 50
        for item, count in inventory.items():
            color = (0, 255, 0) if count != "Infinite" else (200, 200, 200)
            txt = font.render(f"{item}: {count}", True, color)
            screen.blit(txt, (50, y_offset))
            y_offset += 35
        instr = title_font.render("Press 1-5 to Craft", True, (255, 255, 255))
        screen.blit(instr, (500, 50))

    elif game_state == "MINIGAME":
        marker_pos += marker_speed
        if marker_pos >= bar_width or marker_pos <= 0:
            marker_speed *= -1
        
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, 350, bar_width, 50))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x + target_zone[0], 350, target_zone[1]-target_zone[0], 50))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x + marker_pos, 340, 10, 70))
        
        msg = font.render(f"Crafting {pending_item}: Press SPACE in Green!", True, (255, 255, 255))
        screen.blit(msg, (bar_x, 300)) 

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


