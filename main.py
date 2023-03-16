import pygame
from card_gen import Card, generate_cards
from card_shuffle import shuffle_and_deal_cards


def draw_cards(screen, cards, x, y, spacing, hovered_card_index=None):
    for i, card in enumerate(cards):
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + i * spacing, y)
        if i == hovered_card_index:
            card_rect.y -= 110  # 카드를 위로 올립니다.
        screen.blit(card.card_img, card_rect)


def find_hovered_card(cards, x, y, spacing, mouse_x, mouse_y):
    for i, card in enumerate(cards):
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + i * spacing, y)
        if card_rect.collidepoint(mouse_x, mouse_y):
            return i
    return None


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("UNO Game")

    clock = pygame.time.Clock()

    all_cards = generate_cards()
    players_cards = shuffle_and_deal_cards(all_cards, num_players=4, cards_per_player=7)

    player1_cards = players_cards[0]

    x = 50
    y = 600
    spacing = 60

    running = True
    hovered_card_index = None

    while running:
        screen.fill((0, 128, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                hovered_card_index = find_hovered_card(player1_cards, x, y, spacing, mouse_x, mouse_y)

        draw_cards(screen, player1_cards, x, y, spacing, hovered_card_index)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
