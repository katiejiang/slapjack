import sys
from itertools import cycle

from card import Card, CARD_HEIGHT, RANKS, NUM_CARDS_IN_DECK
from player import Player, MENU_HEIGHT

class Slapjack(object):
    """
    A game of Slapjack. Keeps track of players, cards, current rank, and other
    game mechanics.
    """
    def __init__(self, player_name_0, player_name_1):
        cards = Card.generate_deck()
        self.players = (Player(player_name_0, cards[:NUM_CARDS_IN_DECK//2]), \
                        Player(player_name_1, cards[NUM_CARDS_IN_DECK//2:]))
        self.turn = 0
        self.rank_iter = cycle(RANKS)
        self.current_rank = '--'
        self.pile = []
        self.burn = None
        self.slap = None

    @property
    def current_player(self):
        """
        Returns the current player.
        Raises an error if the turn is out of bounds.
        """
        if self.turn < 0 or self.turn > 1:
            raise ValueError('Turn out of bounds: turn = {}'.format(self.turn))
        return self.players[self.turn]

    @property
    def winner(self):
        """
        Returns the winning player.
        """
        if self.players[0].num_cards == 0:
            return self.players[1]
        elif self.players[1].num_cards == 0:
            return self.players[0]
        else:
            return None

    @property
    def top_card(self):
        """
        Returns the card at the top of the pile.
        If the pile is empty, return None.
        """
        return self.pile[-1] if self.pile else None

    def slappable(self):
        """
        Return true if the card at the top of the pile can be slapped.
        """
        return self.top_card and \
               (self.top_card.rank == 'J' or self.top_card.rank == self.current_rank)

    def play_card(self, player):
        """
        Allows the given player to play a card from their deck to the pile.
        """
        self.pile.append(player.play_card())
        self.turn ^= 1
        if sys.version_info[0] < 3:
            self.current_rank = self.rank_iter.next()
        else:
            self.current_rank = next(self.rank_iter)
        self.burn = None
        self.slap = None

    def burn_card(self, player):
        """
        Burns a card from the given player's deck to the bottom of the pile.
        """
        self.pile.insert(0, player.play_card())
        self.burn = player

    def slap_card(self, player_num):
        """
        Given player attempts to slap the pile.
        If the top card is slappable, the player wins the pile.
        Otherwise, the player must burn a card.
        """
        player = self.players[player_num]
        if not self.pile:
            return
        elif self.slappable():
            self.turn = player_num
            player.cards += self.pile
            self.pile = []
            self.rank_iter = cycle(RANKS)
            self.current_rank = '--'
            self.slap = player
        else:
            self.burn_card(player)

    ######## Display string methods ########

    def top_card_str(self, screen_width):
        """
        Returns a string for the top card of the pile.
        """
        return self.top_card.display_str(screen_width) if self.top_card else '\n' * CARD_HEIGHT

    def message_str(self, screen_width):
        """
        Returns a string for messages such as:
        'Player 0 burns a card.' and 'Player 1 wins the slap!'
        If there is a player who has burned or successfully slapped the pile.
        Otherwise, returns an empty string.
        """
        if self.burn:
            message = '{} burns a card.'.format(self.burn.name.strip())
        elif self.slap:
            message = '{} wins the slap!'.format(self.slap.name.strip())
        else:
            message = ''

        padding = max(3, (screen_width - len(message))//2)
        return padding * ' ' + message if message else ''

    def player_menus_str(self, screen_width):
        """
        Returns a string with the player menus.
        """
        # Get menu for each player
        menu_0, menu_1 = self.players[0].menu(self.turn == 0), self.players[1].menu(self.turn == 1)
        # Calculate spacing between menus
        padding = max(3, screen_width - (len(menu_0[0]) + len(menu_1[0])) - 1)
        # Combine menus + padding
        return '\n'.join([menu_0[i] + (' ' * padding) + menu_1[i] for i in range(MENU_HEIGHT)])

    def current_rank_str(self):
        """
        Returns a string with the current rank (call) and instructions to quit.
        """
        space_or_empty = ' ' if len(self.current_rank) == 1 else ''
        return '\n'.join([
            '+------------------+',
            '| Current call: {} |'.format(self.current_rank + space_or_empty),
            '+------------------+',
            '',
            'Press q to quit this game.'
        ])
