import pygame
import random
from card_gen import Card, generate_cards
from card_shuffle import shuffle_and_deal_cards
play_drawn_card_button = pygame.Rect(0, 0, 430, 110)


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


def get_clicked_card(cards, x, y, max_per_row, spacing, mouse_x, mouse_y):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * spacing)
        if card_rect.collidepoint(mouse_x, mouse_y):
            return i, card
    return None, None


def draw_button(screen, text, font, color, rect):
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    lines = text.split('\n')
    line_spacing = font.get_linesize() + 5  # Add some additional space between the lines
    total_height = line_spacing * len(lines)

    for index, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = rect.centerx
        text_rect.centery = rect.centery - total_height // 2 + index * line_spacing
        screen.blit(text_surface, text_rect)


def get_top_card(deck):
    if deck:
        return deck[-1]
    return None


def draw_top_card(screen, card, x, y):
    if card:
        screen.blit(card.card_img, (x, y))


# 카드를 놓을 수 있는지 확인하는 함수
def can_play_card(card, top_card):
    return card.color == top_card.color or card.value == top_card.value or card.value in ('wild', 'wild_draw_4')


# 컴퓨터 플레이어의 턴을 처리하는 함수
def computer_turn(player2_cards, discard_pile, remaining_deck):
    top_card = get_top_card(discard_pile)
    playable_cards = [card for card in player2_cards if can_play_card(card, top_card)]

    if playable_cards:
        played_card = random.choice(playable_cards)
        discard_pile.append(played_card)
        player2_cards.remove(played_card)
    else:
        player2_cards.append(remaining_deck.pop())



def main():
    pygame.init()

    global screen, clock, font, font_big, remaining_deck
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)  # Change the size from 36 to 30
    font_big = pygame.font.Font(None, 72)

    game_mode = main_menu()

    if game_mode == 'singleplayer':
        all_cards = generate_cards()
        players_cards, remaining_deck = shuffle_and_deal_cards(all_cards, num_players=2, cards_per_player=7)
        # 카드 한 장을 뽑아서 남은 카드 덱 옆에 보이게 놓기
        discard_pile = [remaining_deck.pop()]

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

        discard_pile = [remaining_deck.pop()]

        played_card_x = screen.get_rect().centerx - 100
        played_card_y = screen.get_rect().centery - 50

        player_turn = True
        draw_requested = False
        new_drawn_card = None
        remaining_deck_rect = remaining_deck[0].card_img_back.get_rect()
        remaining_deck_rect.topleft = (screen.get_rect().centerx, screen.get_rect().centery)

        while running:
            screen.fill((0, 128, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_card_index, clicked_card = get_clicked_card(player1_cards, x, y, max_per_row, spacing,
                                                                        mouse_x, mouse_y)
                    if draw_requested and play_drawn_card_button.collidepoint(mouse_x, mouse_y):
                        draw_requested = False
                        new_drawn_card = None
                        player_turn = False
                    if clicked_card is not None:
                        top_card = get_top_card(discard_pile)
                        if draw_requested and clicked_card == new_drawn_card and can_play_card(clicked_card, top_card):
                            discard_pile.append(clicked_card)
                            player1_cards.pop(clicked_card_index)
                            player_turn = False
                            draw_requested = False
                            new_drawn_card = None
                        elif not draw_requested:
                            top_card = get_top_card(discard_pile)
                            if clicked_card is not None and can_play_card(clicked_card, top_card):
                                discard_pile.append(clicked_card)
                                player1_cards.pop(clicked_card_index)
                                player_turn = False
                            elif remaining_deck_rect.collidepoint(mouse_x, mouse_y):
                                draw_requested = True
                                new_drawn_card = remaining_deck.pop()
                                player1_cards.append(new_drawn_card)
                            else:  # 아무 카드도 클릭되지 않았다면, 카드를 드로우합니다.
                                if remaining_deck_rect.collidepoint(mouse_x, mouse_y):
                                    draw_requested = True
                                    new_drawn_card = remaining_deck.pop()
                                    player1_cards.append(new_drawn_card)
                    elif draw_requested:  # 드로우한 카드를 낼 수 없다면 턴을 마칩니다.
                        draw_requested = False
                        new_drawn_card = None
                        player_turn = False
                    elif remaining_deck_rect.collidepoint(mouse_x, mouse_y):  # 카드를 드로우합니다.
                        draw_requested = True
                        new_drawn_card = remaining_deck.pop()
                        player1_cards.append(new_drawn_card)

            # 플레이어 2 (컴퓨터) 턴 처리
            if not player_turn:
                delay_time = random.randint(1000, 3000)  # 1~3초 사이의 랜덤한 시간(밀리초 단위) 생성
                pygame.time.delay(delay_time)  # 랜덤한 지연 시간 적용
                computer_turn(player2_cards, discard_pile, remaining_deck)
                player_turn = True

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered_card_index = find_hovered_card(player1_cards, x, y, max_per_row, spacing, mouse_x, mouse_y)
            hovered_card_index2 = find_hovered_card(player2_cards, x2, y2, max_per_row, spacing2, mouse_x, mouse_y)

            draw_cards(screen, player1_cards, x, y, max_per_row, spacing, hovered_card_index)
            draw_cards(screen, player2_cards, x2, y2, max_per_row, spacing2, hovered_card_index2)

            # 남은 카드 더미 그리기
            if remaining_deck:
                screen.blit(remaining_deck[0].card_img_back, (screen.get_rect().centerx, screen.get_rect().centery))

            top_card = get_top_card(discard_pile)
            draw_top_card(screen, top_card, played_card_x, played_card_y)

            # 드로우 요청 시 버튼 표시
            if draw_requested and can_play_card(new_drawn_card, top_card):
                play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
                draw_button(screen, "Click on the remaining deck to turn.\n Or If you want to submit a drawn card,"
                                    "\nclick on the drawn card.", font, (255, 255, 255), play_drawn_card_button)
            elif draw_requested:
                play_drawn_card_button.topleft = (screen.get_rect().centerx + 100, screen.get_rect().centery)
                draw_button(screen, "Click on the remaining deck to turn.", font, (255, 255, 255),
                            play_drawn_card_button)

            # 게임 종료 조건 확인 및 메시지 출력
            if len(player1_cards) == 0:
                draw_text(screen, "Player 1 wins!", font_big, (255, 255, 255), screen.get_rect().centerx, 100)
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
            elif len(player2_cards) == 0:
                draw_text(screen, "Player 2 (Computer) wins!", font_big, (255, 255, 255), screen.get_rect().centerx,
                          100)
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False

            pygame.display.flip()
            clock.tick(60)

    elif game_mode == 'quit':
        pygame.quit()


if __name__ == "__main__":
    main()
