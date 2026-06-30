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

bloodstop_icon = pygame.image.load("image/icon/bloodstop_button.png").convert_alpha()
bloodstop_icon = pygame.transform.smoothscale(bloodstop_icon, (70, 70))
lungclear_icon = pygame.image.load("image/icon/lung-clear_button.png").convert_alpha()
lungclear_icon = pygame.transform.smoothscale(lungclear_icon, (92, 70))
speedserum_icon = pygame.image.load("image/icon/speedserum_button.png").convert_alpha()
speedserum_icon = pygame.transform.smoothscale(speedserum_icon, (70, 70))
radointment_icon = pygame.image.load("image/icon/rad-ointment_button.png").convert_alpha()
radointment_icon = pygame.transform.smoothscale(radointment_icon, (70, 70))
Beaker_icon = pygame.image.load("image/icon/Beaker_icon.jpeg").convert_alpha()
Beaker_icon = pygame.transform.smoothscale(Beaker_icon, (70, 70))
A_icon = pygame.image.load("image/icon/A.png").convert_alpha()
A_icon = pygame.transform.smoothscale(A_icon, (70, 70))
D_icon = pygame.image.load("image/icon/D.png").convert_alpha()
D_icon = pygame.transform.smoothscale(D_icon, (70, 70))
S_icon = pygame.image.load("image/icon/S.png").convert_alpha()
S_icon = pygame.transform.smoothscale(S_icon, (70, 70))
W_icon = pygame.image.load("image/icon/W.png").convert_alpha()
W_icon = pygame.transform.smoothscale(W_icon, (70, 70))
BioFuel_icon = pygame.image.load("image/icon/Bio_Fuel_icon.png").convert_alpha()
BioFuel_icon = pygame.transform.smoothscale(BioFuel_icon, (70, 70))
FilteredWater_icon = pygame.image.load("image/icon/Filtered_water_icon.png").convert_alpha()
FilteredWater_icon = pygame.transform.smoothscale(FilteredWater_icon, (70, 70))
GlowingAloe_icon = pygame.image.load("image/icon/Glowing_Aloe_icon.png").convert_alpha()
GlowingAloe_icon = pygame.transform.smoothscale(GlowingAloe_icon, (70, 70))
RustyThorn_icon = pygame.image.load("image/icon/Rusty_ Thorn_icon.png").convert_alpha()
RustyThorn_icon = pygame.transform.smoothscale(RustyThorn_icon, (70, 70))
ScrapFiber_icon = pygame.image.load("image/icon/Scrap_Fiber_icon.png").convert_alpha()
ScrapFiber_icon = pygame.transform.smoothscale(ScrapFiber_icon, (70, 70))



try:
    play_btn_img = pygame.image.load("image/button/Minigame_play_btn.png").convert_alpha()
    play_btn_img = pygame.transform.smoothscale(play_btn_img, (180, 80))
except:
    play_btn_img = None
    print("Warning: Play button image not found")

try:
    recipe_btn_img = pygame.image.load("image/button/Recipe_button.png").convert_alpha()
    recipe_btn_img = pygame.transform.smoothscale(recipe_btn_img, (130, 70))
except:
    recipe_btn_img = None
    print("Warning: recipe_button.png not found")

try:
    recipe_popup_img = pygame.image.load("image/icon/Recipe.png").convert_alpha()
    recipe_popup_img = pygame.transform.smoothscale(recipe_popup_img, (430, 460))
except:
    recipe_popup_img = None
    print("Warning: recipe_popup.png not found")

play_btn_rect = pygame.Rect(550, 435, 180, 80)
recipe_btn_rect = pygame.Rect(1100, 50, 130, 70)
show_recipe_popup = False
recipe_close_rect = pygame.Rect(880, 130, 45, 45)

RECIPES = {
    "Rad-Ointment": {"Filtered water": 1, "Glowing Aloe": 1 , "Scrap Fiber": 1},
    "Speed Serum": {"Bio-Fuel": 1, "Rusty Thorn": 1, "Filtered water": 1},
    "Lung-Clear": {"Filtered water":1, "Glowing Aloe": 1},
    "Blood-Stop":{"Scrap Fiber":1, "Rusty Thorn": 1},

}

inventory = {"Filtered water": "Infinite", "Bio-Fuel": "Infinite", "Scrap Fiber": "Infinite", "Glowing Aloe": 2, "Rusty Thorn":2 
             ,"Rad-Ointment": 0 , "Speed Serum": 0, "Lung-Clear": 0, "Blood-Stop": 0}
save_callback = None
message_callback = None

def set_save_callback(callback):
    global save_callback
    save_callback = callback

def set_message_callback(callback):
    global message_callback
    message_callback = callback

game_state = "MENU"
pending_item = ""

catch_started = False
falling_items = []
basket = pygame.Rect(605, 615, 70, 70)
basket_speed = 12
spawn_timer = 0
caught = {}
catch_timer = 0

mix_started = False
mix_sequence = []
player_sequence = []
mix_index = 0
mix_timer = 0
lab_tutorial_step = 0

ARROWS = [
    pygame.K_w,
    pygame.K_s,
    pygame.K_a,
    pygame.K_d
]

KEY_TO_ARROW = {
    pygame.K_w: pygame.K_w,
    pygame.K_UP: pygame.K_w,

    pygame.K_s: pygame.K_s,
    pygame.K_DOWN: pygame.K_s,

    pygame.K_a: pygame.K_a,
    pygame.K_LEFT: pygame.K_a,

    pygame.K_d: pygame.K_d,
    pygame.K_RIGHT: pygame.K_d,
}

ARROW_TEXT = {
    pygame.K_w: "W / ↑",
    pygame.K_s: "S / ↓",
    pygame.K_a: "A / ←",
    pygame.K_d: "D / →"
}

KEY_ICONS = {
    pygame.K_w: W_icon,
    pygame.K_a: A_icon,
    pygame.K_s: S_icon,
    pygame.K_d: D_icon
}

def check_resources(item_name):
    recipe = RECIPES[item_name]
    infinite_resources = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]
    for ingredient, amount_needed in recipe.items():
        if ingredient not in infinite_resources:
            if inventory[ingredient] < amount_needed:
                return False
    return True

def get_missing_ingredients(item_name):
    recipe = RECIPES[item_name]
    infinite_resources = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]
    missing = []

    for ingredient, amount_needed in recipe.items():
        if ingredient in infinite_resources:
            continue

        have = inventory.get(ingredient, 0)

        if have < amount_needed:
            missing.append(f"{ingredient} x{amount_needed - have}")

    return missing

def craft_success(item_name):
    recipe = RECIPES[item_name]
    infinites = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]

    for ingredient, amount in recipe.items():
        if ingredient not in infinites:
            inventory[ingredient] -= amount

    inventory[item_name] += 1

    if save_callback:
        save_callback()

def start_catch_game(item):

    global catch_started
    global falling_items
    global basket
    global caught
    global catch_timer

    catch_started = True

    basket.centerx = screen_width // 2
    basket.y = 535

    falling_items.clear()

    catch_timer = 30 * 25  

    caught = {}

    for ingredient in RECIPES[item]:
        caught[ingredient] = 0

WRONG_ITEMS = [
    "Toxic",
    "Rock",
    "Metal Scrap",
    "Poison Mushroom"
]

ITEM_ICONS = {
    "Filtered water": FilteredWater_icon,
    "Bio-Fuel": BioFuel_icon,
    "Scrap Fiber": ScrapFiber_icon,
    "Glowing Aloe": GlowingAloe_icon,
    "Rusty Thorn": RustyThorn_icon,

}
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

    basket.x = max(0, min(screen_width - basket.width, basket.x))

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
                if message_callback:
                    message_callback("Craft Failed! Wrong ingredient collected.")
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

        if message_callback:
            message_callback(f"{pending_item} crafted successfully!")
        game_state = "MENU"
        falling_items.clear()
        return

    if catch_timer <= 0:
        if message_callback:
            message_callback("Craft Failed! Time ran out.")
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

    mix_timer = 30 * (length + 6)

def update_mix_game(event):

    global mix_index
    global mix_timer
    global game_state

    if event.type != pygame.KEYDOWN:
        return

    pressed_key = KEY_TO_ARROW.get(event.key)

    if pressed_key is None:
        return

    if pressed_key == mix_sequence[mix_index]:

        mix_index += 1

        if mix_index >= len(mix_sequence):

            craft_success(pending_item)

            if message_callback:
                message_callback(f"{pending_item} crafted successfully!")

            game_state = "MENU"

    else:

        if message_callback:
            message_callback("Craft Failed! Wrong formula entered.")

        game_state = "MENU"  

def update_crafting(event, progress):

    global game_state
    global pending_item
    global show_recipe_popup

    if event.type == pygame.MOUSEBUTTONDOWN:
        if recipe_btn_rect.collidepoint(event.pos):
            show_recipe_popup = True
            return

        if show_recipe_popup and recipe_close_rect.collidepoint(event.pos):
            show_recipe_popup = False
            return

    if game_state == "MENU":

        if event.type == pygame.KEYDOWN:

            selection = None

            if event.key == pygame.K_1:
                selection = "Rad-Ointment"

            elif event.key == pygame.K_2:
                if progress.get("speed_serum_recipe", False):
                    selection = "Speed Serum"
                else:
                    if message_callback:
                        message_callback("Speed Serum recipe locked! Unlock it in Shop with cookies.")

            elif event.key == pygame.K_3:
                selection = "Lung-Clear"

            elif event.key == pygame.K_4:
                if progress.get("blood_stop_recipe", False):
                    selection = "Blood-Stop"
                else:
                    if message_callback:
                        message_callback("Blood-Stop recipe locked! Unlock it in Shop with cookies.")

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
                missing = get_missing_ingredients(selection)

                if message_callback:
                    message_callback("Missing: " + ", ".join(missing))

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

            if message_callback:
                message_callback("Craft Failed! Time ran out.")

            game_state = "MENU"
def draw_lab_tutorial(screen):
    global lab_tutorial_step

    hints = [
        "Step 1: Press 1-4 to choose a medicine.",
        "Step 2: Click the Recipe button to view all crafting recipes.",
        "Step 3: Rad-Ointment and Blood-Stop use the Catch Game (1 & 4).",
        "Step 4: Use A/D or Left/Right to move the beaker and catch only the correct ingredients.",
        "Step 5: Speed Serum and Lung-Clear use the Mixing Game (2 & 3).",
        "Step 6: Press W/A/S/D or Arrow Keys to match the formula shown.",
        "Step 7: Blood-Stop and Speed Serum recipes must be unlocked in the Shop using cookies.",
        "Step 8: Press SPACE to continue through the tutorial."
    ]

    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 80))
    screen.blit(overlay, (0, 0))

    box_width = 760
    box_height = 95
    box_x = (1280 - box_width) // 2
    box_y = 95

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, (15, 25, 55), box_rect, border_radius=14)
    pygame.draw.rect(screen, (240, 230, 200), box_rect, 2, border_radius=14)

    tut_font = pygame.font.SysFont("Segoe UI", 18, bold=True)
    small_font = pygame.font.SysFont("Segoe UI", 13, bold=True)

    text = tut_font.render(hints[lab_tutorial_step], True, (255, 245, 210))
    text_rect = text.get_rect(center=(1280 // 2, box_y + 35))
    screen.blit(text, text_rect)

    skip_text = small_font.render("Press SPACE to continue / skip", True, (190, 200, 220))
    skip_rect = skip_text.get_rect(center=(1280 // 2, box_y + 68))
    screen.blit(skip_text, skip_rect)
def draw_crafting(screen, bg_image, font):

    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOUR_BG)

    msg = get_title_font().render(
        "Press 1-4 To Craft",
        True,
        COLOR_TEXT
    )

    screen.blit(msg, (500, 55))
    if recipe_btn_img:
        screen.blit(recipe_btn_img, recipe_btn_rect)
    else:
        pygame.draw.rect(screen, (80, 55, 35), recipe_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (230, 200, 150), recipe_btn_rect, 2, border_radius=10)
        recipe_text = font.render("RECIPE", True, (255, 255, 255))
        screen.blit(recipe_text, recipe_text.get_rect(center=recipe_btn_rect.center))

    screen.blit(bloodstop_icon, (33, 510))
    screen.blit(lungclear_icon, (33, 397))
    screen.blit(speedserum_icon, (33, 290))
    screen.blit(radointment_icon, (33, 185))

    small_font = pygame.font.SysFont("Arial", 12, bold=True)

    visible_items = []

    for item, count in inventory.items():
            visible_items.append((item, count))

    positions = {
        "Filtered water": (255, 645),
        "Bio-Fuel": (450, 645),
        "Scrap Fiber": (650, 645),
        "Glowing Aloe": (845, 645),
        "Rusty Thorn": (1020, 645),

        "Rad-Ointment": (29, 260),
        "Speed Serum": (29, 370),
        "Lung-Clear": (32, 480),
        "Blood-Stop": (31, 590)
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

        beaker_rect = Beaker_icon.get_rect(center=basket.center)
        screen.blit(Beaker_icon, basket.topleft)

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

            icon = ITEM_ICONS.get(item["name"])

            if icon is not None:
                screen.blit(icon, item["rect"])

            label = font.render(
                item["name"],
                True,
                color
            )

            screen.blit(
                label,
                (item["rect"].x, item["rect"].y)
        )
    if game_state == "MIX":

        title = pygame.font.SysFont("Arial",32,True)

        text = title.render(

            "Enter Formula",

            True,

            (255,255,255)

        )

        screen.blit(text,(470,120))

        icon = KEY_ICONS[mix_sequence[mix_index]]

        icon_rect = icon.get_rect(center=(640, 300))

        screen.blit(icon, icon_rect)

        small = pygame.font.SysFont("Arial",24)

        progress = small.render(

            f"{mix_index+1}/{len(mix_sequence)}",

            True,

            (255,255,255)

        )

        screen.blit(progress,(600,340))

    if show_recipe_popup:
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(450, 120, 620, 460)

        if recipe_popup_img:
            screen.blit(recipe_popup_img, popup_rect)
        else:
            pygame.draw.rect(screen, (230, 200, 150), popup_rect, border_radius=15)
            pygame.draw.rect(screen, (70, 45, 25), popup_rect, 4, border_radius=15)

        pygame.draw.circle(screen, (180, 50, 45), recipe_close_rect.center, 24)
        pygame.draw.circle(screen, (255, 230, 200), recipe_close_rect.center, 24, 3)

        close_text = font.render("X", True, (255, 255, 255))
        screen.blit(close_text, close_text.get_rect(center=recipe_close_rect.center))

    return play_btn_rect


 



