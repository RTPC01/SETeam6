import pygame
from game_utils import draw_text


def main_menu(screen, clock, font, font_big):
    menu_running = True
    game_mode = None

    while menu_running:
        screen.fill((0, 128, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                game_mode = 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = 'singleplayer'
                    menu_running = False
                elif event.key == pygame.K_3:
                    menu_running = False
                    game_mode = 'quit'

        draw_text(screen, "UNO Game", font_big, (255, 255, 255), screen.get_rect().centerx, 100)
        draw_text(screen, "Press 1 for Singleplayer", font, (255, 255, 255), screen.get_rect().centerx, 300)
        draw_text(screen, "Press 3 to Quit", font, (255, 255, 255), screen.get_rect().centerx, 400)

        pygame.display.flip()
        clock.tick(60)

    return game_mode
