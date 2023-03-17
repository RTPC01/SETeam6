import pygame
from settings import settings_menu


def draw_centered_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    screen.blit(text_surface, text_rect)


def main_menu(screen):
    pygame.init()

    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    font_big = pygame.font.Font(None, 72)

    menu_running = True
    game_mode = None

    while menu_running:
        screen.fill((0, 128, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                game_mode = 'quit'

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            game_mode = 'singleplayer'
            menu_running = False
        elif keys[pygame.K_2]:
            color_blind_mode, current_screen_size = settings_menu()
        elif keys[pygame.K_3]:
            menu_running = False
            game_mode = 'quit'

        draw_centered_text(screen, "UNO Game", font_big, (255, 255, 255), screen.get_rect().centerx, 100)
        draw_centered_text(screen, "Press 1 for Singleplayer", font, (255, 255, 255), screen.get_rect().centerx, 300)
        draw_centered_text(screen, "Press 2 for Settings", font, (255, 255, 255), screen.get_rect().centerx, 400)
        draw_centered_text(screen, "Press 3 to Quit", font, (255, 255, 255), screen.get_rect().centerx, 500)

        pygame.display.flip()
        clock.tick(60)

    return game_mode