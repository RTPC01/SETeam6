import pygame
from game_utils import draw_text
from main_menu import main_menu
from singleplayer import singleplayer


def main():
    pygame.init()

    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 72)

    game_mode = main_menu(screen, clock, font, font_big)

    if game_mode == 'singleplayer':
        singleplayer(screen, clock, font, font_big)
    elif game_mode == 'quit':
        pygame.quit()


if __name__ == "__main__":
    main()
