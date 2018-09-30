MENU_HEIGHT = 5

class Player(object):
    """
    A player for the game of Slapjack. Keeps track of name and cards.
    """

    def __init__(self, name, cards):
        # padding is for formatting & alignment reasons
        padding = max(0, len('XX cards') - len(name)) * ' '
        self.name = name + padding
        self.cards = cards

    @property
    def num_cards(self):
        return len(self.cards)

    def play_card(self):
        return self.cards.pop(0)

    def __repr__(self):
        return "Player(name={}, cards=)".format(self.name, self.cards)

    ######## Display string methods ########

    @property
    def num_cards_str(self):
        """
        Returns a string for the number of cards a player has.
        The format is 'XX cards' with extra whitespace to match the length of
        the player's name.
        """
        space_or_empty = ' ' if self.num_cards < 10 else ''
        padding = space_or_empty + max(0, len(self.name) - len('XX cards')) * ' '
        return '{} cards{}'.format(self.num_cards, padding)

    def menu(self, is_turn):
        """
        Displays a menu for the player with their name and number of cards.
        """
        if is_turn:
            # Add a box around current player to indicate it is their turn
            return [
                '+-{}----+'.format(len(self.name) * '-'),
                '| {}    |'.format(self.name),
                '| {}--- |'.format(len(self.name) * '-'),
                '| {}    |'.format(self.num_cards_str),
                '+-{}----|'.format(len(self.name) * '-')
            ]
        else:
            return [
                ' {}    '.format(len(self.name) * ' '),
                ' {}    '.format(self.name),
                ' {}--- '.format(len(self.name) * '-'),
                ' {}    '.format(self.num_cards_str),
                ' {}    '.format(len(self.name) * ' ')
            ]
