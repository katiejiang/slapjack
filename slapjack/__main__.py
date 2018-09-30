import curses
from curses import wrapper

from card import CARD_HEIGHT
from player import MENU_HEIGHT
from slapjack import Slapjack

MESSAGE_HEIGHT = 1
CURRENT_CALL_HEIGHT = 5

REQUIRED_HEIGHT = CARD_HEIGHT               \
              + 1                           \
              + MESSAGE_HEIGHT              \
              + 1                           \
              + MENU_HEIGHT                 \
              + 1                           \
              + CURRENT_CALL_HEIGHT

def play(game, screen):
    while True:
        # Clear screen
        screen.clear()

        # Check if screen is large enough to play game
        screen_height, screen_width = screen.getmaxyx()
        if screen_height < REQUIRED_HEIGHT:
            window.addstr(0, 0, "Please make your terminal screen larger.")
            continue

        # Check if a player has won.
        if game.winner:
            break

        # Calculate y-values for the strings we want to display
        # We want 1 newline between each of the strings
        message_y = CARD_HEIGHT + 1
        player_menus_y = message_y + MESSAGE_HEIGHT + 1
        current_call_y = player_menus_y + MENU_HEIGHT + 1

        # Display information strings on screen
        screen.addstr(0, 0, game.top_card_str(screen_width))
        screen.addstr(message_y, 0, game.message_str(screen_width))
        screen.addstr(player_menus_y, 0, game.player_menus_str(screen_width))
        screen.addstr(current_call_y, 0, game.current_rank_str())

        # Get user input
        c = screen.getch()

        if c in [ord('z'), ord('x'), ord('c')] and game.turn == 0:
            # Player 0's turn to place a card on the pile
            game.play_card(game.current_player)
        elif c in [ord(','), ord('.'), ord('/')] and game.turn == 1:
            # Player 1's turn to place a card on the pile
            game.play_card(game.current_player)
        elif c in [ord('a'), ord('s'), ord('d')]:
            # Player 0 wants to slap the pile
            game.slap_card(0)
        elif c in [ord('l'), ord(';'), ord("'")]:
            # Player 1 wants to slap the pile
            game.slap_card(1)
        elif c == ord('q'):
            # Quit this game
            return

def main(screen):
    print("Playing Slapjack...")
    # Clear screen
    screen.clear()
    # Initialize the game
    game = Slapjack("Katie", "Stephanie")

    while True:
        slapjack_str = '#####################################\n' \
                     + '#        WELCOME TO SLAPJACK        #\n' \
                     + '#####################################\n\n'
        instructions_str = 'Press p to play a new game.\nPress q to quit.'
        # Set winner message if player 0 or player 1 won
        winner_str = '{} is the winner!\n'.format(game.winner.name.strip()) if game.winner else ''

        # Display instructions and winner message on screen
        screen.clear()
        screen.addstr(0, 0, slapjack_str + winner_str + instructions_str)

        # Get user input
        c = screen.getch()
        if c == ord('q'):
            # Quit the game
            return
        elif c == ord('p'):
            # Play a new game
            game = Slapjack("Katie", "Stephanie")
            play(game, screen)


if __name__ == "__main__":
    wrapper(main)
