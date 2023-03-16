from random import shuffle


def shuffle_cards(cards):
    shuffled_cards = cards.copy()
    shuffle(shuffled_cards)
    return shuffled_cards


def shuffle_and_deal_cards(cards, num_players, cards_per_player):
    shuffled_cards = shuffle_cards(cards)
    players_cards = [shuffled_cards[i * cards_per_player:(i + 1) * cards_per_player] for i in range(num_players)]
    remaining_deck = shuffled_cards[num_players * cards_per_player:]
    return players_cards, remaining_deck


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
