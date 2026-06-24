import pygame 
import random

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

}

inventory = {"Filtered water": "Infinite", "Bio-Fuel": "Infinite", "Scrap Fiber": "Infinite", "Glowing Aloe": 2, "Rusty Thorn":2 
             ,"Rad-Ointment": 0 , "Speed Serum": 0, "Lung-Clear": 0, "Blood-Stop": 0}

hidden_items = [
    "Rad-Ointment",
    "Speed Serum",
    "Lung-Clear",
    "Blood-Stop",
    
]

game_state = "MENU"
pending_item = ""

catch_started = False
falling_items = []
basket = pygame.Rect(560, 620, 160, 35)
basket_speed = 8
spawn_timer = 0
caught = {}
catch_timer = 0

mix_started = False
mix_sequence = []
player_sequence = []
mix_index = 0
mix_timer = 0

ARROWS = [
    pygame.K_w,
    pygame.K_s,
    pygame.K_a,
    pygame.K_d
]

ARROW_TEXT = {
    pygame.K_w: "w",
    pygame.K_s: "s",
    pygame.K_a: "a",
    pygame.K_d: "d"
}

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

def start_catch_game(item):

    global catch_started
    global falling_items
    global basket
    global caught
    global catch_timer

    catch_started = True

    basket.x = 560

    falling_items.clear()

    catch_timer = 30 * 15  

    caught = {}

    for ingredient in RECIPES[item]:
        caught[ingredient] = 0

WRONG_ITEMS = [
    "Toxic Waste",
    "Rock",
    "Metal Scrap",
    "Poison Mushroom"
]

def spawn_falling_item():

    global falling_items

    recipe = list(RECIPES[pending_item].keys())

    if random.random() < 0.7:
        name = random.choice(recipe)
        good = True

    else:
        name = random.choice(WRONG_ITEMS)
        good = False

    falling_items.append({

        "name": name,

        "good": good,

        "rect": pygame.Rect(
            random.randint(50,1150),
            -40,
            70,
            35
        ),

        "speed": random.randint(4,7)

    })

def update_catch_game():

    global spawn_timer
    global catch_timer
    global game_state

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:

        basket.x -= basket_speed

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

        basket.x += basket_speed

    basket.x = max(0,min(1120,basket.x))

    spawn_timer += 1

    if spawn_timer >= 30:

        spawn_timer = 0

        spawn_falling_item()

    catch_timer -= 1

    for item in falling_items[:]:

        item["rect"].y += item["speed"]

        if item["rect"].colliderect(basket):

            if item["good"]:

                caught[item["name"]] += 1

            else:

                print("Wrong ingredient!")

                game_state = "MENU"

                falling_items.clear()

                return

            falling_items.remove(item)

        elif item["rect"].y > 720:

            falling_items.remove(item)

    success = True

    for ingredient, amount in RECIPES[pending_item].items():

        if caught[ingredient] < amount:

            success = False

    if success:

        craft_success(pending_item)

        print("Medicine Crafted!")

        game_state = "MENU"

        falling_items.clear()

        return

    if catch_timer <= 0:

        print("Time Up!")

        game_state = "MENU"

        falling_items.clear()

def start_mix_game(item):

    global mix_started
    global mix_sequence
    global player_sequence
    global mix_index
    global mix_timer

    mix_started = True

    player_sequence.clear()

    mix_index = 0

    if item == "Lung-Clear":
        length = random.randint(3,4)

    else:
        length = random.randint(5,7)

    mix_sequence = [
        random.choice(ARROWS)
        for i in range(length)
    ]

    mix_timer = 30 * (length + 2)

def update_mix_game(event):

    global mix_index
    global mix_timer
    global game_state

    if event.type != pygame.KEYDOWN:
        return

    if event.key not in ARROWS:
        return

    if event.key == mix_sequence[mix_index]:

        mix_index += 1

        if mix_index >= len(mix_sequence):

            craft_success(pending_item)

            print("Medicine Crafted!")

            game_state = "MENU"

    else:

        print("Wrong Formula!")

        game_state = "MENU"      

def update_crafting(event, progress):

    global game_state
    global pending_item

    if game_state == "MENU":

        if event.type == pygame.KEYDOWN:

            selection = None

            if event.key == pygame.K_1:
                selection = "Rad-Ointment"

            elif event.key == pygame.K_2:
                if progress.get("speed_serum_recipe", False):
                    selection = "Speed Serum"
                else:
                    print("Recipe not unlocked!")

            elif event.key == pygame.K_3:
                selection = "Lung-Clear"

            elif event.key == pygame.K_4:
                if progress.get("blood_stop_recipe", False):
                    selection = "Blood-Stop"
                else:
                    print("Recipe not unlocked!")

            if selection and check_resources(selection):

                pending_item = selection

                if selection in ["Rad-Ointment", "Blood-Stop"]:
                    game_state = "CATCH"
                    start_catch_game(selection)

                else:
                    game_state = "MIX"
                    start_mix_game(selection)

                print(f"Crafting {selection}")

            elif selection:
                print("Missing ingredients!")

    elif game_state == "MIX":

        update_mix_game(event)
def animate_crafting():

    global mix_timer
    global game_state

    if game_state == "CATCH":

        update_catch_game()
    
    elif game_state == "MIX":

        mix_timer -= 1

        if mix_timer <= 0:

            print("Time Up!")

            game_state = "MENU"


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


    small_font = pygame.font.SysFont("Arial", 16, bold=True)

    visible_items = []

    for item, count in inventory.items():

        if item not in hidden_items:
            visible_items.append((item, count))

    positions = {
        "Filtered water": (255, 645),
        "Bio-Fuel": (450, 645),
        "Scrap Fiber": (650, 645),
        "Glowing Aloe": (845, 645),
        "Rusty Thorn": (1020, 645)
    }

    for item, count in visible_items:

        txt = small_font.render(
            f"{item}: {count}",
            True,
            (255, 255, 255)
        )

        if item in positions:
            screen.blit(txt, positions[item])
    
    if game_state == "CATCH":

        pygame.draw.rect(
            screen,
            (30,30,30),
            basket
        )

        font = pygame.font.SysFont("Arial",20)

        timer = font.render(
            f"Time: {catch_timer//30}",
            True,
            (255,255,255)
        )

        screen.blit(timer,(20,20))

        y = 60

        for ingredient, amount in RECIPES[pending_item].items():

            txt = font.render(

                f"{ingredient}: {caught[ingredient]}/{amount}",

                True,

                (255,255,255)

            )

            screen.blit(txt,(20,y))

            y += 25

        for item in falling_items:

            color = (0,200,0) if item["good"] else (220,50,50)

            pygame.draw.rect(

                screen,

                color,

                item["rect"]

            )

            label = font.render(

                item["name"],

                True,

                (255,255,255)

            )

            screen.blit(

                label,

                (item["rect"].x,item["rect"].y)

            )
    if game_state == "MIX":

        title = pygame.font.SysFont("Arial",32,True)

        text = title.render(

            "Enter Formula",

            True,

            (255,255,255)

        )

        screen.blit(text,(470,120))

        arrow_font = pygame.font.SysFont("Arial",60)

        x = 280

        y = 260

        next_arrow = arrow_font.render(

            ARROW_TEXT[mix_sequence[mix_index]],

            True,

            (255,255,255)

        )

        screen.blit(next_arrow,(600,260))

        small = pygame.font.SysFont("Arial",24)

        progress = small.render(

            f"{mix_index+1}/{len(mix_sequence)}",

            True,

            (255,255,255)

        )

        screen.blit(progress,(600,340))

    return play_btn_rect


 



