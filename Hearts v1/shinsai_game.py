"""Game classes and methods. Plan to eventually incorporate other types
of games, such as dice."""

import random
import pyinputplus as pyip

class GameMethods:
	"""Methods universal to games in general."""

	def who_goes_first(num_players=2):
		'''
		Randomly choose which player goes first.
		Returns random integer 1-number of players.
		'''
		return random.randrange(1, num_players+1)

	def play_again():
		'''
		Prompts the user if they'd like to play again. Returns 'yes' or 
		'no'.
		'''
		play_again = pyip.inputYesNo(
			'Would you like to play again? ', blank=True
				)
		if not play_again:
			play_again = 'no'
		return play_again

	def gather_names(num_players=1):
		'''
		Gathers names for the number of human players.
		Returns 'players' list.

		Example:
		players = gather_names(3)
		player_1 = players[0]
		player_2 = players[1]
		player_3 = players[2]
		'''
		players = []
		for i, player in enumerate(range(num_players)):
			player = pyip.inputStr(f'Player {i + 1}, what is your name? ')
			players.append(player)
		if len(players) == 1:
			return players[0]
		else:
			return players
	

class Cards:
	"""Card methods."""

	def __init__(self):
		self.jokers = ['Joker', 'Joker']
		self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
		self.face_cards = ('Jack', 'Queen', 'King', 'Ace')
	
	def get_suit(self, card):
		'''Returns the suit value of a particular card.'''
		for suit in self.suits:
			if card.endswith(f'{suit}'):
				return suit

	def same_suit(self, *card_list):
		'''
		Determines if all the cards in a card list are the same suit.
		'''
		suits = []
		for cards in card_list:
			for card in cards:
				suit = get_suit(card)
				suits.append(suit)
		return all(suit == suits[0] for suit in suits)

	def get_value(self, card):
		'''
		Returns the value of a particular card. (i.e. 2, Jack, Ace)
		'''
		value = card.split(' ')[0]
		return value

	def same_value(self, *card_list):
		'''
		Determines if all the cards in a card list are the same value.
		'''
		values = []
		for cards in card_list:
			for card in cards:
				value = self.get_value(card)
				values.append(value)
		return all(value == values[0] for value in values)

	def assign_ranks(self, deck, rank_list):
		'''
		Takes a deck and provided list of ranks and returns a dictionary
		with each card value (2-Ace) as a key, the value being a list of
		the cards with that card value.
		'''
		ranks = {}
		for rank in rank_list:
			ranks[rank] = []
		for card in deck:
			card_val = self.get_value(card)
			ranks[card_val].append(card)
		return ranks

	def show_hand(self, player, hand):
		'''Displays the cards in the player's hand.'''
		print(f'\n{player}\'s hand is: ')
		print(', '.join(hand))

	def show_table(self, table, player=None):
		'''
		Displays the cards on the table.
		If no player is specified, it shows everything on the table.
		'''
		if player:
			print(f'\nCards on {player}\'s table:')
			print(', '.join(table))
		else:
			print('Cards on the table:')
			print(', '.join(table))


class Deck(Cards):
	'''Methods specific to a deck.'''

	def build_decks(self, num_decks, add_jokers=False):
		'''
		Builds a deck from specified number of decks of cards and 
		shuffles it.
		'''
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
		'''Deals the top card from the deck.'''
		return deck.pop(0)
		
	def get_random_card(self, deck):
		'''Removes and returns a random card from the deck.'''
		rand_card = random.choice(deck)
		deck.remove(rand_card)
		return rand_card

	def shuffle_deck(self, deck):
		'''Shuffles the deck.'''
		random.shuffle(deck)
		return deck

	def deal_hands(self, deck, size, num_hands):
		'''
		Deals specified number of hands of specified size from the deck.
		'''
		hands = []
		for hand in range(num_hands):
			cards_hand = []
			for _ in range(size):
				card = deck.pop(0)
				cards_hand.append(card)
			hands.append(cards_hand)
		return hands