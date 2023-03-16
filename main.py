import pygame
from card_gen import Card, generate_cards
from card_shuffle import shuffle_and_deal_cards


def draw_cards(screen, cards, x, y, max_per_row, spacing, hovered_card_index=None):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * spacing)
        if i == hovered_card_index:
            card_rect.y -= 50
        screen.blit(card.card_img, card_rect)


def find_hovered_card(cards, x, y, max_per_row, spacing, mouse_x, mouse_y):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * spacing)
        if card_rect.collidepoint(mouse_x, mouse_y):
            return i
    return None


def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def main_menu():
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


def main():
    pygame.init()

    global screen, clock, font, font_big
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font_big = pygame.font.Font(None, 72)

    game_mode = main_menu()

    if game_mode == 'singleplayer':
        all_cards = generate_cards()
        players_cards, remaining_deck = shuffle_and_deal_cards(all_cards, num_players=4, cards_per_player=7)

        player1_cards = players_cards[0]
        player2_cards = players_cards[1]

        x = 50
        y = 600
        spacing = 80

        x2 = 800
        y2 = 50
        spacing2 = 80

        max_per_row = 5

        running = True
        hovered_card_index = None
        hovered_card_index2 = None

        while running:
            screen.fill((0, 128, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    hovered_card_index = find_hovered_card(player1_cards, x, y, max_per_row, spacing, mouse_x, mouse_y)
                    hovered_card_index2 = find_hovered_card(player2_cards, x2, y2, max_per_row, spacing2, mouse_x, mouse_y)

            draw_cards(screen, player1_cards, x, y, max_per_row, spacing, hovered_card_index)
            draw_cards(screen, player2_cards, x2, y2, max_per_row, spacing2, hovered_card_index2)

            # 남은 카드 더미 그리기
            if remaining_deck:
                screen.blit(remaining_deck[0].card_img_back, (screen.get_rect().centerx, screen.get_rect().centery))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    elif game_mode == 'quit':
        pygame.quit()


if __name__ == "__main__":
    main()
