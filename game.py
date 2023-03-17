import pygame
import random
from card_gen import Card, generate_cards
from card_shuffle import shuffle_and_deal_cards
from game_utils import (
    draw_cards,
    find_hovered_card,
    draw_text,
    get_clicked_card,
    draw_button,
    get_top_card,
    draw_top_card,
    can_play_card,
    computer_turn,
    process_special_card,
)
from menu import main_menu
FPS = 60

play_drawn_card_button = pygame.Rect(0, 0, 430, 110)


def game_loop(color_blind_mode, screen_size):
    pygame.init()

    screen_size_map = {
        "Large": (1400, 800),
        "Medium": (1000, 600),
        "Small": (800, 480)
    }

    screen = pygame.display.set_mode(screen_size_map[screen_size])
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 128, 0))

        # Render game elements here
        # Apply color_blind_mode if necessary

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def singleplayer():
    global FPS
    computer_action_time = None
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("UNO Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    font_big = pygame.font.Font(None, 72)

    all_cards = generate_cards()
    players_cards, remaining_deck = shuffle_and_deal_cards(all_cards, num_players=2, cards_per_player=7)


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
            clock.tick(FPS) #FPS를 조절하여 루프 속도를 제한한다.
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
                                if clicked_card.is_special():
                                    player_turn = process_special_card(clicked_card, player1_cards, player2_cards,
                                                                       remaining_deck)
                                else:
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
                if computer_action_time is None:
                    delay_time = random.randint(1000, 3000)  # 1~3초 사이의 랜덤한 시간(밀리초 단위) 생성
                    computer_action_time = pygame.time.get_ticks() + delay_time  # 현재 시간에 랜덤한 지연 시간을 더합니다.

                if pygame.time.get_ticks() >= computer_action_time:  # 설정한 시간이 되면 컴퓨터가 행동을 취합니다.
                    player_turn = computer_turn(player2_cards, player1_cards, discard_pile, remaining_deck)
                    computer_action_time = None  # 행동을 완료한 후, 다음 행동 시간을 초기화합니다.

            mouse_x, mouse_y = pygame.mouse.get_pos()
            hovered_card_index = find_hovered_card(player1_cards, x, y, max_per_row, spacing, mouse_x, mouse_y)

            draw_cards(screen, player1_cards, x, y, max_per_row, spacing, hovered_card_index)
            draw_cards(screen, player2_cards, x2, y2, max_per_row, spacing2, hovered_card_index2, show_back=True)

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