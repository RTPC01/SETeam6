import pygame

colors = ['red', 'green', 'blue', 'yellow']
values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'skip', 'reverse', 'draw_2', 'wild', 'wild_draw_4']


class Card:
    def __init__(self, color, value, card_img, card_img_back):
        self.color = color
        self.value = value
        self.card_img = card_img
        self.card_img_back = card_img_back  # 추가된 코드

    def __str__(self):
        return f"{self.color} {self.value}"

    def __repr__(self):
        return self.__str__()

    def is_special(self):
        return self.value in ["skip", "reverse", "draw_2", "wild", "wild_draw_4"]


def generate_cards():
    cards = []
    card_back_image = pygame.image.load("card_images/card_back.png")  # 카드 뒷면 이미지를 로드합니다.

    for color in colors:
        for value in values:
            card_image = pygame.image.load(f"card_images/{color}_{value}.png")
            card = Card(color, value, card_image, card_back_image)  # card_img_back 인수를 추가합니다.
            cards.append(card)
    return cards
