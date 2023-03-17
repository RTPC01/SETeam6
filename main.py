import pygame
from game import singleplayer
from game import main_menu


def main():
    pygame.init()

    game_mode = main_menu()

    if game_mode == 'singleplayer':
        singleplayer()

    elif game_mode == 'quit':
        pygame.quit()


if __name__ == "__main__":
    main()
