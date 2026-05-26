import pygame
import sys

def show_intro(screen, clock):
    title_font = pygame.font.SysFont("Arial", 44, bold=True)
    text_font = pygame.font.SysFont("Arial", 24)
    tip_font = pygame.font.SysFont("Arial", 18, italic=True)

    story_scenes = [
        [
            "The world has ended.",
            "A terrible virus turned people into zombies, and hospitals are gone.",
            "The rich hoarded all the medicine, leaving regular people to die in the ruins."
        ],
        [
            "But you are a pharmacist who cares.",
            "You said no to the safe zones and came back to your family's old pharmacy.",
            "Here, you reopen the shop to help the survivors."
        ],
        [
            "You must search the ruins for supplies, mix wild herbs,",
            "and make medicine for everyone who knocks on your door.",
            "",
            "But WATCH OUT! The smell of living humans will attract hungry zombies."
        ],
        [
            "When they attack, drop your medicine, grab your gun, and shoot them down!",
            "You cannot save the whole world...",
            "But you can save the living with your medicine—and destroy the dead with your bullets.",
            "",
            "[ ARE YOU READY TO SURVIVE DAY 1? ]"
        ]
    ]

    current_scene = 0         
    char_index = 0            
    typing_speed = 1          
    frame_count = 0
    scene_complete = False    

    running = True
    while running:
        screen.fill((20, 18, 18)) 

        title_surf = title_font.render("THE LAST PHARMACIST", True, (140, 20, 20)) # Crimson Red
        screen.blit(title_surf, (50, 45))

        pygame.draw.line(screen, (70, 65, 65), (50, 110), (750, 110), 2)

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
        current_y = 160
        
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
            screen.blit(text_surf, (60, current_y))
            current_y += 40 

        if scene_complete:
            if current_scene < len(story_scenes) - 1:
                tip_text = "[ Press SPACE to continue ]"
            else:
                tip_text = "[ Press SPACE to open your pharmacy for Day 1 ]"
        else:
            tip_text = "[ Printing... Press SPACE to reveal all text ]"

        tip_surf = tip_font.render(tip_text, True, (110, 105, 105))
        screen.blit(tip_surf, (60, 520))

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