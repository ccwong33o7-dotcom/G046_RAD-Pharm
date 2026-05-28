import pygame

def draw_map(screen, map_bg_img, font, mouse_pos, img_greenhouse, img_shop, img_lab, img_pharmacy):
    if map_bg_img:
        screen.blit(map_bg_img, (0, 0))
    else:
       screen.fill((50, 50, 50))
       error_txt = font.render("Map background not found", True, (255, 0, 0))
       screen.blit(error_txt, (1280 // 2 - 150, 720 // 2))
    
    shop_rect = pygame.Rect(180, 130, 220, 160)
    greenhouse_rect = pygame.Rect(820, 140, 220, 160)
    pharmacy_rect = pygame.Rect(530, 280, 220, 160)
    lab_rect = pygame.Rect(220, 430, 220, 160)

    if img_shop:
        screen.blit(img_shop, (shop_rect.x, shop_rect.y))
    if img_greenhouse:
        screen.blit(img_greenhouse, (greenhouse_rect.x, greenhouse_rect.y))
    if img_pharmacy:
        screen.blit(img_pharmacy, (pharmacy_rect.x, pharmacy_rect.y))
    if img_lab:
        screen.blit(img_lab, (lab_rect.x, lab_rect.y))
    
    if shop_rect.collidepoint(mouse_pos):
        label = font.render("Shop", True, (240, 1920, 60))
        screen.blit(label, (shop_rect.x + 30, shop_rect.y - 40))
    elif greenhouse_rect.collidepoint(mouse_pos):
        label = font.render("Greenhouse", True, (240, 190, 60))
        screen.blit(label, (greenhouse_rect.x + 30, greenhouse_rect.y - 40))
    elif pharmacy_rect.collidepoint(mouse_pos):
        label = font.render("Pharmacy", True, (255, 100, 100))
        screen.blit(label, (pharmacy_rect.x + 10, pharmacy_rect.y - 40))
    elif lab_rect.collidepoint(mouse_pos):
        label = font.render("Junkyard Lab", True, (150, 200, 255))
        screen.blit(label, (lab_rect.x + 20, lab_rect.y - 40))

    return greenhouse_rect, shop_rect, lab_rect, pharmacy_rect

