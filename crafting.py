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



try:
    play_btn_img = pygame.image.load("image/button/Minigame_play_btn.png").convert_alpha()
    play_btn_img = pygame.transform.smoothscale(play_btn_img, (180, 80))
except:
    play_btn_img = None
    print("Warning: Play button image not found")

play_btn_rect = pygame.Rect(550, 435, 180, 80)

RECIPES = {
    "Rad-Ointment": {"Filtered water": 1, "Glowing Aloe": 1 , "Scrap Fiber": 1},
    "Speed Serum": {"Bio-Fuel": 1, "Rusty Thorn": 1, "Filtered water": 1},
    "Lung-Clear": {"Filtered water":1, "Glowing Aloe": 1},
    "Blood-Stop":{"Scrap Fiber":1, "Rusty Thorn": 1},
    "Pain Killer":{"Bio_Fuel":1, "Glowing Aloe": 1, "Rusty Thorn": 1}
}

inventory = {"Filtered water": "Infinite", "Bio-Fuel": "Infinite", "Scrap Fiber": "Infinite", "Glowing Aloe": 2, "Rusty Thorn":2 
             ,"Rad-Ointment": 0 , "Speed Serum": 0, "Lung-Clear": 0, "Blood-Stop": 0, "Pain Killer": 0}

hidden_items = [
    "Rad-Ointment",
    "Speed Serum",
    "Lung-Clear",
    "Blood-Stop",
    "Pain Killer"
]

game_state = "MENU"
pending_item = ""
marker_pos = 0
marker_speed = 3
minigame_started = False
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
        

def update_crafting(event):

    global game_state
    global pending_item
    global marker_pos
    global marker_speed
    global minigame_started

    if game_state == "MENU":
        minigame_started = False
        if event.type == pygame.KEYDOWN:

            selection = None

            if event.key == pygame.K_1:
                selection = "Rad-Ointment"

            elif event.key == pygame.K_2:
                selection = "Speed Serum"

            elif event.key == pygame.K_3:
                selection = "Lung-Clear"

            elif event.key == pygame.K_4:
                selection = "Blood-Stop"

            elif event.key == pygame.K_5:
                selection = "Pain Killer"

            if selection:

                if check_resources(selection):

                    pending_item = selection

                    game_state = "MINIGAME"

                    minigame_started = False

                    marker_pos = 0
                    marker_speed = 3

                    print(f"Crafting {selection}")

                else:
                    print("Missing ingredients!")

    elif game_state == "MINIGAME":

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not minigame_started:

                if play_btn_rect.collidepoint(event.pos):

                    minigame_started = True

                    marker_pos = 0

                    print("Minigame Started!")

    if minigame_started:

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if target_zone[0] <= marker_pos <= target_zone[1]:

                    craft_success(pending_item)

                    print("SUCCESS!")

                else:
                    print("FAILED!")

                game_state = "MENU"

                minigame_started = False
                

    return game_state



def animate_crafting():
    global marker_pos, marker_speed

    if game_state == "MINIGAME" and minigame_started:

        marker_pos += marker_speed

        if marker_pos >= bar_width or marker_pos <= 0:
            marker_speed *= -1


def draw_crafting(screen, bg_image, font):

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOUR_BG)

    msg = get_title_font().render(
        "Press 1-5 To Craft",
        True,
        COLOR_TEXT
    )

    screen.blit(msg, (500, 40))


    small_font = pygame.font.SysFont("Arial", 22, bold=True)

    visible_items = []

    for item, count in inventory.items():

        if item not in hidden_items:
            visible_items.append((item, count))

    positions = {
        "Filtered water": (70, 665),
        "Bio-Fuel": (350, 665),
        "Scrap Fiber": (620, 665),
        "Glowing Aloe": (900, 665),
        "Rusty Thorn": (1080, 665)
    }

    for item, count in visible_items:

        txt = small_font.render(
            f"{item}: {count}",
            True,
            (255, 255, 255)
        )

        if item in positions:
            screen.blit(txt, positions[item])

    if game_state == "MINIGAME":

        bar_x = (screen.get_width() // 2) - (bar_width // 2)

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (bar_x, 350, bar_width, 50)
        )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (
                bar_x + target_zone[0],
                350,
                target_zone[1] - target_zone[0],
                50
            )
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (bar_x + marker_pos, 340, 10, 70)
        )

        # DRAW PLAY BUTTON HERE
        if not minigame_started:

            if play_btn_img:
                screen.blit(play_btn_img, play_btn_rect)

            else:
                pygame.draw.rect(
                    screen,
                    (0, 180, 0),
                    play_btn_rect,
                    border_radius=12
                )

                txt = small_font.render(
                    "PLAY",
                    True,
                    (255, 255, 255)
                )

                screen.blit(txt, (565, 585))



    return play_btn_rect


 



