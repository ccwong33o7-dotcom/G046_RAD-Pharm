import pygame 

screen_width = 1280
screen_height = 720

RECIPES = {
    "Rad-Ointment": {"Filtered water": 1, "Glowing Aloe": 1 , "Scrap Fiber": 1},
    "Speed Serum": {"Bio-Fuel": 1, "Rusty Thorn": 1, "Filtered water": 1},
    "Lung-Clear": {"Filtered water":1, "Glowing Aloe": 1},
    "Blood-Stop":{"Scrap Fiber":1, "Rusty Thorn": 1},
    "Pain Killer":{"Bio_Fuel":1, "Glowing Aloe": 1, "Rusty Thorn": 1}
}

inventory = {"Filtered water": "Infinite", "Bio-Fuel": "Infinite", "Scrap Fiber": "Infinite", "Glowing Aloe": 2, "Rusty Thorn":2 
             ,"Rad-Ointment": 0 , "Speed Serum": 0, "Lung-Clear": 0, "Blood-Stop": 0, "Pain Killer": 0}

def try_to_craft(item_name):
    recipe = RECIPES[item_name]
    infinite_resources = ["Filtered water", "Bio-Fuel", "Scrap Fiber"]

    for ingredient, amount_needed in recipe.items():
        if ingredient not in infinite_resources:
            if inventory[ingredient] < amount_needed:
                print(f"Not enough {ingredient} to craft {item_name}!")
                return
            
    for ingredient, amount_needed in recipe.items():
        if ingredient not in infinite_resources:
            inventory[ingredient] -= amount_needed
            print(f"Ha! You crafted {item_name}!")

            inventory[item_name] += 1

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Junkyard Lab")
font = pygame.font.SysFont("Arial", 22)

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.KEYDOWN:
        if event .key == pygame.K_1:
            try_to_craft("Rad-Ointment")
        if event.key == pygame.K_2:
            try_to_craft("Speed Serum")
        if event.key == pygame.K_3:
            try_to_craft("Lung-Clear")
        if event.key == pygame.K_4:
            try_to_craft("Blood-Stop")
        if event.key == pygame.K_5:
            try_to_craft("Pain Killer")
    
            


