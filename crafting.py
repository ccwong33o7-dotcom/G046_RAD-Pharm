import pygame 


screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
COLOUR_BG = (244, 194, 194)
COLOR_TEXT = (255, 255, 255)

font = None
title_font = None

def get_title_font():
    
    if not pygame.font.get_init():
        pygame.font.init()
    return pygame.font.SysFont("Arial", 32, bold=True)

crafting_btn_set_btn = pygame.Rect(1080, 50, 150, 50)
crafting_back_btn = pygame.Rect(1080, 150, 150, 50)


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
marker_speed = 3
bar_width = 400
bar_x = (screen_width // 2) - (bar_width // 2)
target_zone = (100, 300)


       
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
        

    screen.fill(COLOUR_BG)

def update_crafting(event):
    global game_state, pending_item, marker_pos, marker_speed

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos

        if crafting_back_btn.collidepoint(mouse_pos):
            return "PHARMACY"
        
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
                    print("Missing ingredients!")

    elif game_state == "MINIGAME":
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if target_zone[0] <= marker_pos <= target_zone[1]:
                craft_success(pending_item)
                print("SUCCESS!")
            else:
                print("FAILED!")
            game_state = "MENU"

    return game_state

def animate_crafting():
    global marker_pos, marker_speed

    if game_state == "MINIGAME":
        marker_pos += marker_speed
        if marker_pos >= bar_width or marker_pos <= 0:
            marker_speed *= -1

def draw_crafting(screen, font):
    screen.fill(COLOUR_BG)


    msg = get_title_font().render("Press 1-5 to Craft", True, COLOR_TEXT)
    screen.blit(msg, (500, 50))


    y_offset = 150
    for item, count in inventory.items():
        color = (0, 255, 0) if count != "Infinite" else (255, 255, 255)
        txt = font.render(f"{item}: {count}", True, color)
        screen.blit(txt, (100, y_offset))
        y_offset += 40


    if game_state == "MINIGAME":
        bar_x = (screen.get_width() // 2) - (bar_width // 2)

        pygame.draw.rect(screen, (80, 80, 80), (bar_x, 350, bar_width, 50))
        pygame.draw.rect(screen, (0, 255, 0),
                         (bar_x + target_zone[0], 350,
                          target_zone[1] - target_zone[0], 50))
        pygame.draw.rect(screen, (255, 255, 255),
                         (bar_x + marker_pos, 340, 10, 70))

    # Buttons
    pygame.draw.rect(screen, (100, 100, 100), crafting_back_btn)

    screen.blit(font.render("Back", True, (255, 255, 255)), (1080, 150))

    return crafting_btn_set_btn, crafting_back_btn
 



