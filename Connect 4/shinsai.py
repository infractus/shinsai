"""
Shinsai classes and functions.

Version 1.2 - adding Pygame stuff
Version 1.1 - 5/14/2020 - Added Program class.
Version 1.0 - 5/13/2020 (Date I started tracking.)
"""

import random, json, os
import pyinputplus as pyip

from pathlib import Path

p = Path(__file__).parent
os.chdir(p)

class Program:
    """The settings and methods for a program in general."""
    def __init__(self):
        """
        Initialize a program object. 
        Settings can than be assigned as instance variables.
        """
        pass

    def write_to_tracking(self, track_file, tracking):
        """Writes changes to track file."""
        with open(track_file, 'w') as f:
            json.dump(tracking, f, indent=4)

    def get_stored_tracking(self, track_file):
        """Checks is tracking file exists, creates it if it does not."""
        try:
            with open(track_file) as f:
                tracking = json.load(f)
        except FileNotFoundError:
            tracking = {}
            self.write_to_tracking(track_file, tracking)
            with open(track_file) as f:
                tracking = json.load(f)
        return tracking


class Game(Program):
    """The settings and methods for a game in general."""
    def __init__(self):
        """
        Initialize a new game. Settings can than be assigned as instance
        variables.
        """
        self.playing = True

    def who_goes_first(self, num_players=2):
        """
        Randomly choose which player goes first.
        Returns random integer 1-number of players.
        """
        return random.randrange(1, num_players+1)

    def play_again(self):
        """
        Prompts the user if they'd like to play again. Returns 'yes' or 
        'no'.
        """
        play_again = pyip.inputYesNo(
            '\nWould you like to play again? ', blank=True
                )
        if not play_again:
            play_again = 'no'
        return play_again

    def gather_names(self, num_players=1):
        """
        Gathers names for the number of human players.
        Returns 'players' list.

        Example:
        players = gather_names(3)
        player_1 = players[0]
        player_2 = players[1]
        player_3 = players[2]
        """
        players = []
        for i, player in enumerate(range(num_players)):
            player = pyip.inputStr(f'Player {i + 1}, what is your name? ')
            players.append(player)
        if len(players) == 1:
            return players[0]
        else:
            return players

    def get_stored_tracking(self, track_file):
        """Checks is tracking file exists, creates it if it does not."""
        try:
            with open(track_file) as f:
                tracking = json.load(f)
        except FileNotFoundError:
            tracking = {}
            tracking['player_stats'] = {}
            tracking['game_stats'] = {}
            self.write_to_tracking(track_file, tracking)
            with open(track_file) as f:
                tracking = json.load(f)
        return tracking

class Tournament:
    """Represents a tournament"""
    
    def __init__(self, num_rounds = 3):
        """Tracks tournament settings."""
        self.round_number = 0
        self.tournament_over = False
        self.winner = None
        

class Player:
    """Represents a single player."""

    def __init__(self, name, is_computer=True):
        """Tracks a player's name and if they're computer or human."""
        self.name = name
        self.is_computer = is_computer

    def __str__(self):
        """Returns the player's name when printing the instance."""
        return self.name


class Cards:
    """Represents cards in general."""

    def __init__(self):
        self.jokers = ['Joker', 'Joker']
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        self.face_cards = ('Jack', 'Queen', 'King', 'Ace')
    
    def get_suit(self, card):
        """Returns the suit value of a particular card."""
        for suit in self.suits:
            if card.endswith(f'{suit}'):
                return suit
        if card == 'Joker':
            return 'Joker'

    def same_suit(self, *card_list):
        """
        Determines if all the cards in a card list are the same suit.
        Returns boolean.
        """
        suits = []
        for cards in card_list:
            for card in cards:
                suit = self.get_suit(card)
                suits.append(suit)
        return all(suit == suits[0] for suit in suits)

    def get_value(self, card):
        """
        Returns the value of a particular card. (i.e. 2, Jack, Ace)
        """
        value = card.split(' ')[0]
        return value

    def same_value(self, *card_list):
        """
        Determines if all the cards in a card list are the same value.
        Returns boolean.
        """
        values = []
        for cards in card_list:
            for card in cards:
                value = self.get_value(card)
                values.append(value)
        return all(value == values[0] for value in values)


class Deck(Cards):
    """Methods specific to a deck."""

    def build_decks(self, num_decks, add_jokers=False):
        """
        Builds a deck from specified number of decks of cards and 
        shuffles it.
        """
        cards = []
        for deck in range(num_decks):
            for suit in self.suits:
                [cards.append(f'{str(n)} of {suit}') for n in range(2, 11)]
                [cards.append(f'{face} of {suit}') for face in self.face_cards]
            if add_jokers:
                cards += self.jokers
        self.shuffle_deck(cards)
        return cards
    
    def deal_top_card(self, deck):
        """Deals the top card from the deck."""
        return deck.pop(0)
        
    def get_random_card(self, deck):
        """Removes and returns a random card from the deck."""
        rand_card = random.choice(deck)
        deck.remove(rand_card)
        return rand_card

    def shuffle_deck(self, deck):
        """Shuffles the deck."""
        random.shuffle(deck)
        return deck

    def deal_hands(self, deck, size, num_hands):
        """
        Deals specified number of hands of specified size from the deck.
        """
        hands = []
        for hand in range(num_hands):
            cards_hand = []
            for _ in range(size):
                card = deck.pop(0)
                cards_hand.append(card)
            hands.append(cards_hand)
        return hands

    def show_hand(self, player, hand):
        """Displays the cards in the player's hand."""
        print(f'\n{player}\'s hand is: ')
        print(', '.join(hand))

    def show_table(self, table, player=None):
        """
        Displays the cards on the table.
        If no player is specified, it shows everything on the table.
        """
        if player:
            print(f'\nCards on {player}\'s table:')
            print(', '.join(table))
        else:
            print('\nCards on the table:')
            print(', '.join(table))