import random
from enum import Enum

CARD_HEIGHT = 9
CARD_WIDTH = 15
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
NUM_CARDS_IN_DECK = 52
NUM_SUITS = 4

class Card(object):
    """
    A card in the game of Slapjack.
    """
    def __init__(self, rank):
        self.rank = rank

    def display_str(self, screen_width):
        """
        Returns a display string for the card.
        """
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
            for i in range(NUM_SUITS):
                deck.append(Card(rank))
        random.shuffle(deck)
        return deck
