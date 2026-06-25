import pygame
import sys
import os

def show_intro(screen, clock):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    title_font = pygame.font.SysFont("Arial", 44, bold=True)
    text_font = pygame.font.SysFont("Arial", 24)
    tip_font = pygame.font.SysFont("Arial", 18, italic=True)

    bg_path = os.path.join("image", "background", "intro_bg.jpeg")

    try:
        intro_bg = pygame.image.load(bg_path).convert()
        intro_bg = pygame.transform.scale(intro_bg, (screen_width, screen_height))
    except pygame.error as e:
        print(f"[ERROR] Cannot find or load image: {bg_path}. Details: {e}")
        intro_bg = pygame.Surface((screen_width, screen_height))
        intro_bg.fill((20, 18, 18))

    story_scenes = [
    [
        "The world ended in a flash of fire.",
        "Radiation dust covers the sky, water sources are poisoned, and crops are dead.",
        "Few survivors hide underground, but radiation sickness is slowly killing them."
    ],
    [
        "You were a pharmacist who knows how to compound anti radiation drugs.",
        "You returned to that abandoned pharmacy, where some raw materials and recipes remain.",
        "You decide to set up a clinic here, offering hope to the irradiated."
    ],
    [
        "Every day you put on your protective suit and scavenge the ruins for herbs and purifiers.",
        "Dosage must be precise – one mistake can kill instead of cure.",
        "Your pharmacy is the only light in the wasteland."
    ],
    [
        "You cannot clear all the radiation...",
        "But you can give each person who comes to you a chance to survive.",
        "With your hands, you brew the antidote against death.",
        "",
        "[ ARE YOU READY TO BEGIN YOUR FIRST DAY? ]"
    ]
]

    current_scene = 0         
    char_index = 0            
    typing_speed = 1          
    frame_count = 0
    scene_complete = False    

    running = True
    while running:
        screen.blit(intro_bg, (0, 0)) 

        title_surf = title_font.render("Welcome to RAD-PHARM", True, (140, 20, 20)) # Crimson Red
        title_x = (screen_width - title_surf.get_width()) // 2  
        screen.blit(title_surf, (title_x, 45))

        pygame.draw.line(screen, (70, 65, 65), (140, 110), (screen_width - 140, 110), 2)

        lines = story_scenes[current_scene]
        total_text_len = sum(len(line) for line in lines)
        
        frame_count += 1
        if frame_count >= typing_speed:
            frame_count = 0
            if char_index < total_text_len:
                char_index += 1
            else:
                scene_complete = True

        chars_to_show = char_index
        current_y = 180
        
        for line in lines:
            if chars_to_show <= 0:
                break
            if chars_to_show >= len(line):
                display_line = line
                chars_to_show -= len(line)
            else:
                display_line = line[:chars_to_show]
                chars_to_show = 0
            
            upper_line = display_line.upper()
            if any(word in upper_line for word in ["ZOMBIE", "GUN", "BULLET", "ATTACK", "WATCH OUT"]):
                text_color = (220, 60, 60) 
            else:
                text_color = (210, 210, 210) 
            
            text_surf = text_font.render(display_line, True, text_color)
            text_x = (screen_width - text_surf.get_width()) // 2  
            screen.blit(text_surf, (text_x, current_y))
            current_y += 45 

        if scene_complete:
            if current_scene < len(story_scenes) - 1:
                tip_text = "[ Press SPACE to continue ]"
            else:
                tip_text = "[ Press SPACE to open your pharmacy for Day 1 ]"
        else:
            tip_text = "[ Printing... Press SPACE to reveal all text ]"

        tip_surf = tip_font.render(tip_text, True, (110, 105, 105))
        tip_x = (screen_width - tip_surf.get_width()) // 2  
        screen.blit(tip_surf, (tip_x, 580))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not scene_complete:
                        char_index = total_text_len
                        scene_complete = True
                    else:
                        if current_scene < len(story_scenes) - 1:
                            current_scene += 1
                            char_index = 0
                            scene_complete = False
                        else:
                            running = False

        pygame.display.flip()
        clock.tick(60)