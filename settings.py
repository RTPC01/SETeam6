import pygame
import pickle


def settings_menu():
    color_blind_mode, current_screen_size = load_settings()
    pygame.init()
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game - Settings")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    button_font = pygame.font.Font(None, 40)

    settings_running = True
    screen_sizes = ["Large", "Medium", "Small"]
    save_button = pygame.Rect(screen.get_rect().centerx - 100, 650, 200, 60)

    while settings_running:
        screen.fill((0, 128, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    settings_running = False

                if event.key == pygame.K_c:
                    color_blind_mode = not color_blind_mode

                if event.key == pygame.K_s:
                    current_screen_size = "Small"

                if event.key == pygame.K_m:
                    current_screen_size = "Medium"

                if event.key == pygame.K_l:
                    current_screen_size = "Large"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and save_button.collidepoint(event.pos):
                    save_settings(color_blind_mode, current_screen_size)
                    settings_running = False

        draw_centered_text(screen, "Settings", font, (255, 255, 255), screen.get_rect().centerx, 100)
        draw_centered_text(screen, "Press C to toggle color blind mode", font, (255, 255, 255), screen.get_rect().centerx, 200)
        draw_centered_text(screen, "Press L, M, S to cycle through screen sizes", font, (255, 255, 255), screen.get_rect().centerx, 300)
        draw_centered_text(screen, "Press ESS to EXIT", font, (255, 255, 255), screen.get_rect().centerx, 400)

        draw_centered_text(screen, f"Color blind mode: {'ON' if color_blind_mode else 'OFF'}", font, (255, 255, 255), screen.get_rect().centerx, 500)
        draw_centered_text(screen, f"Screen size: {current_screen_size}", font, (255, 255, 255), screen.get_rect().centerx, 600)

        draw_button(screen, "Save", button_font, (255, 255, 255), save_button)

        pygame.display.flip()
        clock.tick(60)

    return color_blind_mode, current_screen_size


def save_settings(color_blind_mode, current_screen_size):
    settings = {
        'color_blind_mode': color_blind_mode,
        'screen_size': current_screen_size
    }
    print(settings)
    with open("settings.pickle", "wb") as f:
        pickle.dump(settings, f)



def load_settings():
    try:
        with open("settings.pickle", "rb") as f:
            settings = pickle.load(f)
    except FileNotFoundError:
        settings = {
            'color_blind_mode': False,
            'screen_size': "Large"
        }

    return settings


def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)


def draw_centered_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    screen.blit(text_surface, text_rect)