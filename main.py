from menu import main_menu
from game import game_loop
from settings import settings_menu, load_settings
import pygame


def main():
    while True:
        settings = load_settings()
        color_blind_mode, screen_size = settings
        screen_size_map = {
            "Small": (800, 600),
            "Medium": (1200, 800),
            "Large": (1400, 800)
        }
        print(screen_size_map)
        print(screen_size)
        screen = pygame.display.set_mode(screen_size_map[settings['screen_size']])

        mode = main_menu(settings['screen_size'])
        if mode == 'singleplayer':
            color_blind_mode, current_screen_size = settings_menu()
            game_loop(color_blind_mode, current_screen_size)
        elif mode == 'quit':
            break

if __name__ == "__main__":
    main()

