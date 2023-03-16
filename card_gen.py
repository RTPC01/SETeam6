import pygame

from random import shuffle


class Card:

    def __init__(self, name, filename, owner=None):
        self.name = name
        self.card_img = pygame.image.load(filename)
        self.color = name[0]
        self.type = name[2]


def generate_cards():
    cards = []
    colors = ["blue_", "red_", "green_", "yellow_"]
    colors_name = ["b", "r", "g", "y"]
    card_type = ["picker", "skip", "reverse", "0",
                 "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    # make predefined cards
    for i in range(len(colors)):  # O(m*n)
        for ct in card_type:
            name_str = colors_name[i] + "_" + ct
            filename_str = "small_cards/" + colors[i] + ct + ".png"
            cards.append(Card(name_str, filename_str, None))

    # make four wild pick 4
    cards.append(Card(
        "w_p_f1", "small_cards/wild_pick_four.png", None))
    cards.append(Card(
        "w_p_f2", "small_cards/wild_pick_four.png", None))
    cards.append(Card(
        "w_p_f3", "small_cards/wild_pick_four.png", None))
    cards.append(Card(
        "w_p_f4", "small_cards/wild_pick_four.png", None))

    # make four wild color
    cards.append(Card(
        "w_c1", "small_cards/wild_color_changer.png", None))
    cards.append(Card(
        "w_c2", "small_cards/wild_color_changer.png", None))
    cards.append(Card(
        "w_c3", "small_cards/wild_color_changer.png", None))
    cards.append(Card(
        "w_c4", "small_cards/wild_color_changer.png", None))

    return cards


# Check_List
'''
all_cards = generate_cards()
for card in all_cards:
    print(f"Card name: {card.name}, Color: {card.color}, Type: {card.type}")
'''
