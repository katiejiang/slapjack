import random
from enum import Enum

CARD_HEIGHT = 9
CARD_WIDTH = 15
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

class Card:
    """
    A card in the game of Slapjack.
    """
    def __init__(self, rank):
        self.rank = rank

    def display_str(self, screen_width):
        padding = ' ' * max(0, (screen_width - CARD_WIDTH)//2)
        rank_left = self.rank if len(self.rank) == 2 else self.rank + ' '
        rank_right = self.rank if len(self.rank) == 2 else ' ' + self.rank
        return ('\n' + padding).join([
            padding + '+-------------+',
            '| {}          |'.format(rank_left),
            '|             |',
            '|             |',
            '|             |',
            '|             |',
            '|             |',
            '|          {} |'.format(rank_right),
            '+-------------+'
        ])

    def __repr__(self):
        return "Card(rank={})".format(self.rank)

    @staticmethod
    def generate_deck():
        """
        Returns a list of shuffled Cards.
        """
        deck = []
        for rank in RANKS:
            for i in range(4): # 4 suits
                deck.append(Card(rank))
        random.shuffle(deck)
        return deck
