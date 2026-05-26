import pygame
import os

SETTING_ICON = None
SHOP_ICON = None

def load_assets():
    global SETTING_ICON, SHOP_ICON
    if SETTING_ICON is not None and SHOP_ICON is not None:
        return SETTING_ICON, SHOP_ICON

    base_path = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_path, "image", "setting_button.png")

    if os.path.exists(img_path):
        try:
            img = pygame.image.load(img_path).convert_alpha()
            SETTING_ICON = pygame.transform.scale(img, (42, 42))
            print("Icon Success")
        except Exception as e:
            print(f"Icon Failed: {e}")

    shop_img_path = os.path.join(base_path, "image", "shop_button.png")
    if os.path.exists(shop_img_path):
        try:
            img = pygame.image.load(shop_img_path).convert_alpha()
            SHOP_ICON = pygame.transform.scale(img, (45, 45))
            print("Icon Success")
        except Exception as e:
            print(f"Icon Failed: {e}")

    return SETTING_ICON, SHOP_ICON

def draw_pharmacy(screen, font, bg_img):
    icon_set, icon_shop = load_assets()

    if bg_img:
        screen.blit(bg_img, (0,0))
    else:
        screen.fill((255,250,200))


    settings_btn_rect = pygame.Rect(35,22,50,50)

    if SETTING_ICON:
        screen.blit(icon_set, (settings_btn_rect.x + 4, settings_btn_rect.y + 4))
    else:
        pygame.draw.rect(screen, (150, 50, 50), settings_btn_rect)
        temp_text = pygame.font.SysFont("Arial", 15).render("Set", True, (255,255,255))
        screen.blit(temp_text, (settings_btn_rect.x + 10, settings_btn_rect.y + 15))

    small_font = pygame.font.SysFont("Arial",20)

    shop_btn_rect = pygame.Rect(95,22,50,50)
    if SHOP_ICON:
        screen.blit(icon_shop, (shop_btn_rect.x + 2, shop_btn_rect.y + 2))
    else:
        pygame.draw.rect(screen,(50,150,50),shop_btn_rect)
        btn_text = small_font.render("Shop", True, (255, 255, 255))
        screen.blit(btn_text, (shop_btn_rect.x + 4, shop_btn_rect.y + 12))

    greenhouse_btn_rect = pygame.Rect(1180,130,80,40)
    pygame.draw.rect(screen,(50,50,150),greenhouse_btn_rect)
    gh_font = pygame.font.SysFont("Arial",14)
    btn_text = gh_font.render("Greenhouse",True, (255,255,255))
    screen.blit(btn_text,(greenhouse_btn_rect.x + 2, greenhouse_btn_rect.y +12))

    crafting_btn_rect = pygame.Rect(1180,180,80,40)
    pygame.draw.rect(screen,(150,150,50),crafting_btn_rect)
    btn_text = small_font.render("Crafting",True, (255,255,255))
    screen.blit(btn_text,(crafting_btn_rect.x + 5, crafting_btn_rect.y +10))

    return settings_btn_rect, shop_btn_rect, greenhouse_btn_rect, crafting_btn_rect