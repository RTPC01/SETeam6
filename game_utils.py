import random
import pygame


def draw_cards(screen, cards, x, y, max_per_row, spacing, hovered_card_index=None, show_back=False):
    for i, card in enumerate(cards):
        row = i // max_per_row
        column = i % max_per_row
        card_rect = card.card_img.get_rect()
        card_rect.topleft = (x + column * spacing, y + row * spacing)
        if i == hovered_card_index:
            card_rect.y -= 50
        if show_back:
            screen.blit(card.card_img_back, card_rect)
        else:
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


def can_play_card(card, top_card):
    return (card.color == top_card.color or
            card.value == top_card.value or
            card.value in ('wild', 'wild_draw_4') or
            (top_card.value in ('skip', 'reverse', 'draw_2') and card.value == top_card.value))


def computer_turn(player_cards, opponent_cards, discard_pile, remaining_deck):
    top_card = get_top_card(discard_pile)
    playable_cards = [card for card in player_cards if can_play_card(card, top_card)]

    if playable_cards:
        selected_card = random.choice(playable_cards)
        discard_pile.append(selected_card)
        player_cards.remove(selected_card)

        # 특수 카드 처리
        if selected_card.is_special():
            return process_special_card(selected_card, player_cards, opponent_cards, remaining_deck)
    else:
        if remaining_deck:
            drawn_card = remaining_deck.pop()
            if can_play_card(drawn_card, top_card):
                discard_pile.append(drawn_card)
            else:
                player_cards.append(drawn_card)
    return True  # 다음 턴에 플레이어의 차례를 알리기 위해 True 반환


def process_special_card(played_card, player, opponent, remaining_deck):
    if played_card.value == "skip":
        return True  # 턴을 넘깁니다.

    if played_card.value == "reverse":
        pass  # 현재 게임에서는 무시됩니다. 2명 플레이어일 때는 효과가 없습니다.

    if played_card.value == "draw_2":
        for _ in range(2):
            if remaining_deck:
                opponent.append(remaining_deck.pop())
            else:
                break
        return False  # 턴을 넘깁니다.

    if played_card.value == "wild":
        played_card.color = random.choice(['red', 'blue', 'green', 'yellow'])

    if played_card.value == "wild_draw_4":
        for _ in range(4):
            if remaining_deck:
                opponent.append(remaining_deck.pop())
            else:
                break
        played_card.color = random.choice(['red', 'blue', 'green', 'yellow'])

    return True