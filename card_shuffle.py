# card_shuffle.py
from card_gen import Card, generate_cards
from random import shuffle
from typing import List


# 이전에 작성한 shuffle_and_deal_cards 함수를 여기에 붙여넣기
def shuffle_and_deal_cards(all_cards: List[Card], num_players: int, cards_per_player: int):
    # 카드를 셔플한다
    shuffle(all_cards)

    # 플레이어들의 카드 목록을 초기화한다
    players_cards = [[] for _ in range(num_players)]

    # 카드를 플레이어들에게 나눠준다
    for i in range(num_players * cards_per_player):
        player_index = i % num_players
        card = all_cards.pop()
        players_cards[player_index].append(card)

    return players_cards


'''
# 카드 생성
all_cards = generate_cards()

# Set_Player_Num and Set_Cards_Per_Player
num_players = 4
cards_per_player = 7
players_cards = shuffle_and_deal_cards(all_cards, num_players, cards_per_player)

# Print Card
for i, player_cards in enumerate(players_cards):
    print(f"Player {i + 1}'s cards:")
    for card in player_cards:
        print(card.name)
    print()
'''