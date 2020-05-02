'''Classes specific to the game of Hearts'''
import pyinputplus as pyip

class Player:
	'''Represents a single player.'''

	def __init__(self, name, deck_instance, is_computer=True):
		'''
		Tracks the player's name, if they're computer, points, hand,
		discard pile, the other player's positions, lists keeping track
		of the various states of cards, and the card they played during
		a turn.
		'''
		self.name = name
		self.is_computer = is_computer
		self.points = 0
		self.round_points = 0
		self.deck_instance = deck_instance
		self.hand = []
		self.discard = []
		self.player_left = ''
		self.player_right = ''
		self.player_across = ''
		self.cards_to_pass = []
		self.viable_cards = []
		self.played_card = ''

	def assign_positions(self, player_left, player_across, player_right):
		'''Assign positions around table.'''
		self.player_left = player_left
		self.player_across = player_across
		self.player_right = player_right


class Game:			
	'''Represents the game in general.'''
	
	def __init__(self):
		'''
		Keeps track of if hearts have been broken, the hand number, and
		lists of card points and values.
		'''
		self.hearts_broken = False
		self.hand_num = 0
		self.card_points = {
			'2 of Hearts': 1, '3 of Hearts': 1, '4 of Hearts': 1,
			'5 of Hearts': 1, '6 of Hearts': 1, '7 of Hearts': 1, 
			'8 of Hearts': 1, '9 of Hearts': 1, '10 of Hearts': 1,
			'Jack of Hearts': 1, 'Queen of Hearts': 1, 'King of Hearts': 1,
			'Ace of Hearts': 1, 'Queen of Spades': 13
				}
		self.card_values = {
			'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
			'10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
				}

	def determine_winner(self, players):
		'''Determine who won the game.'''
		low_points = 100
		winner = None
		for player in players:
			if player.points < low_points:
				low_points = player.points
				winner = player
		for player in players:
			# Handles a tie; assumes only two players tied.
			if player != winner:
				if player.points == winner.points:
					print(
						f'{player.name} and {winner.name} both have '
						f'{winner.points} and have won with a tie!'
							)
					return
		print(f'{winner.name} has won with {low_points} points.')


class Hand:
	'''The methods for a hand.'''

	def sort_hand(player, hand):
		'''Sorts the hand first by suit then by rank.'''
		new_hand = []
		final_hand = []

		# Sort hand by value and create new_hand list.
		for v in range(2, 11):
			for card in hand:
				if card.startswith(str(v)):
					new_hand.append(card)
		[new_hand.append(card) for card in hand \
			if player.deck_instance.get_value(card) == 'Jack']
		[new_hand.append(card) for card in hand \
			if player.deck_instance.get_value(card) == 'Queen']
		[new_hand.append(card) for card in hand \
			if player.deck_instance.get_value(card) == 'King']
		[new_hand.append(card) for card in hand \
			if player.deck_instance.get_value(card) == 'Ace']

		# Sort new_hand by suit to create final_hand.
		[final_hand.append(card) for card in new_hand \
			if player.deck_instance.get_suit(card) == 'Hearts']
		[final_hand.append(card) for card in new_hand \
			if player.deck_instance.get_suit(card) == 'Spades']
		[final_hand.append(card) for card in new_hand \
			if player.deck_instance.get_suit(card) == 'Diamonds']
		[final_hand.append(card) for card in new_hand \
			if player.deck_instance.get_suit(card) == 'Clubs']

		return final_hand
	
	def cards_to_pass(player, game_instance, hand):
		'''
		Determines where each player will pass cards, then calls
		choose_pass() to choose which cards to pass between players.
		'''
		if not player.is_computer:
			if game_instance.hand_num % 4 == 1:
				print(
					f'\nChoose 3 cards to pass left to'
					f' {player.player_left.name}.'
						)
				new_hand = Hand.choose_pass(player, hand)
			if game_instance.hand_num % 4 == 2:
				print(
					f'\nChoose 3 cards to pass right to'
					f' {player.player_right.name}.'
						)
				new_hand = Hand.choose_pass(player, hand)
			if game_instance.hand_num % 4 == 3:
				print(
					'\nChoose 3 cards to pass across to ' 
					f'{player.player_across.name}.'
						)	
				new_hand = Hand.choose_pass(player, hand)
		else:
			if game_instance.hand_num % 4 == 1:
				new_hand = Hand.choose_pass(player, hand, 'left')
			if game_instance.hand_num % 4 == 2:
				new_hand = Hand.choose_pass(player, hand, 'right')
			if game_instance.hand_num % 4 == 3:
				new_hand = Hand.choose_pass(player, hand, 'across')
		return new_hand
		
	def choose_pass(player, hand, passing_to=None):
		'''
		Decide which cards to pass. Returns the players hand without the
		chosen cards.
		'''
		if not player.is_computer:
			# Prompt user for which cards to pass.
			while True:
				new_hand = hand[:]
				cards = []
				print('\nFirst card:')
				choice = pyip.inputMenu(new_hand, numbered=True)
				new_hand.remove(str(choice))
				cards.append(choice)
				print('\nSecond card:')
				choice = pyip.inputMenu(new_hand, numbered=True)
				new_hand.remove(choice)
				cards.append(choice)
				print('\nThird card:')
				choice = pyip.inputMenu(new_hand, numbered=True)
				new_hand.remove(choice)
				cards.append(choice)
				print(f"\nThe cards you have chosen are: {', '.join(cards)}")
				verify = pyip.inputYesNo('Do you want to pass these cards? ')
				if verify == 'yes':
					break
		else:
			# Logic for computer to decide which cards to pass.
			new_hand = hand[::-1]
			cards = []
			suits = {'Hearts': [], 'Clubs': [], 'Spades': [], 'Diamonds': []}
			for suit in suits.keys():
			# Create a dictionary of the cards in the hand to easily
			# determine how many of each card is in the hand.
				for card in new_hand:
					if card.endswith(suit):
						suits[suit].append(card)
			for card in new_hand:
				# Always pass the 2 of Clubs
				if card == '2 of Clubs':
					cards.append(card)
					new_hand.remove(card)
					suits['Clubs'].remove(card)
			if passing_to == 'right':
				# Always pass the Queen of Spades right.
				for card in new_hand:
					if card == 'Queen of Spades':
						cards.append(card)
						new_hand.remove(card)
						suits['Spades'].remove(card)
			while len(cards) < 3:
				for card in new_hand[:]:
					# Create variables for how many cards of each suit
					# in hand for easier readability of the following 
					# code.
					clubs = len(suits['Clubs'])
					hearts = len(suits['Hearts'])
					diamonds = len(suits['Diamonds'])
					spades = len(suits['Spades'])
					if len(cards) < 3:
						if clubs > 1 and clubs < 5:
							# If less than 5 clubs void clubs keeping 
							# one for first round
							if card.endswith('Clubs'):
								cards.append(card)
								new_hand.remove(card)
								suits['Clubs'].remove(card)
						elif diamonds > 0 and diamonds < 4:
							# If less than 4 diamonds void diamonds.
							if card.endswith('Diamonds'):
								cards.append(card)
								new_hand.remove(card)
								suits['Diamonds'].remove(card)
						elif spades > 0 and spades < 4 and suits['Spades'] !=\
									['Queen of Spades']:
								# If less than 4 spades void spades but 
								# keep the Queen
								if card.endswith('Spades'):
									cards.append(card)
									new_hand.remove(card)
									suits['Spades'].remove(card)
						elif diamonds <= clubs and diamonds > 0:
							# If less or same diamonds to clubs and
							# more than zero diamonds use diamond
							if card.endswith('Diamonds'):
								cards.append(card)
								new_hand.remove(card)
								suits['Diamonds'].remove(card)
						elif clubs <= diamonds and clubs > 1:
							# If less or same clubs to diamonds and more
							# than one clubs use clubs
							if card.endswith('Clubs'):
								cards.append(card)
								new_hand.remove(card)
								suits['Clubs'].remove(card)
						else:
							if clubs > 1:
								if card.endswith('Clubs'):
									cards.append(card)
									new_hand.remove(card)
									suits['Clubs'].remove(card)
							elif diamonds > 0:
								if card.endswith('Diamonds'):
									cards.append(card)
									new_hand.remove(card)
									suits['Diamonds'].remove(card)
							elif spades > 0:
								if spades > 1 and card == 'Queen of Spades':
									continue
								else:
									if card.endswith('Spades'):
										cards.append(card)
										new_hand.remove(card)
										suits['Spades'].remove(card)
							elif hearts > 0:
								if card.endswith('Hearts'):
									cards.append(card)
									new_hand.remove(card)
									suits['Hearts'].remove(card)
		player.cards_to_pass = cards
		new_hand = new_hand[::-1]
		return new_hand					

	def pass_cards(player, game_instance):
		'''
		Actually pass the cards and display results to human players.
		'''
		if game_instance.hand_num % 4 == 1:
			player.player_left.hand.extend(player.cards_to_pass)
			if not player.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to ' 
					f'{player.player_left.name}.'
						)
			if not player.player_left.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to '
					f'{player.player_left.name}.'
						)
		if game_instance.hand_num % 4 == 2:
			player.player_right.hand.extend(player.cards_to_pass)
			if not player.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to ' 
					f'{player.player_right.name}.'
						)
			if not player.player_right.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to '
					f'{player.player_right.name}.'
						)
		if game_instance.hand_num % 4 == 3:
			player.player_across.hand.extend(player.cards_to_pass)
			if not player.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to ' 
					f'{player.player_across.name}.'
						)
			if not player.player_across.is_computer:
				print(
					f'\n{player.name} passed the cards '
					f'{", ".join(player.cards_to_pass)} to '
					f'{player.player_across.name}.'
						)

	def set_points(players, max_points):
		'''
		Adds points for the round to the total points for the hand for 
		each player. Rechecks max_points and returns that number.
		'''
		print()
		for player in players:
			player.points += player.round_points
			print(f'{player.name} has {player.points} total points.')
		for player in players:
			if player.points > max_points:
				max_points = player.points
		return max_points


class Turn:
	'''The methods for a turn.'''

	def first_turn(players):
		'''2 of Clubs goes first in first round.'''
		for player in players:
			if '2 of Clubs' in player.hand:
				print(
					f'\n{player.name} has the 2 of Clubs and will go'
					f' first. \n{player.name} lays the 2 of Clubs.'
						)
				return player
	
	def take_turn(
		player, round_num, game_instance, suit_led=None, 
		leading=False, table=None
			):
		'''Take a turn.'''
		for card in player.hand:
			# Make list of viable cards in hand.
			viable_cards = []
			for card in player.hand:
				if not game_instance.hearts_broken:
					# Hearts not viable until broken.
					if card.endswith('Hearts'):
						continue
				if round_num == 1:
					# Cannot play Queen of Spades on first round.
					if card == 'Queen of Spades':
						continue
				if suit_led:
					# If a suit was led, only viable cards are suit.
					if card.endswith(suit_led):
						viable_cards.append(card)
				else:			
					# If player leading, all cards are viable.
					viable_cards.append(card)
		if not viable_cards:
			# If no possible cards, all cards are viable.
			for card in player.hand:
				# All cards viable for human players.
				if not player.is_computer:
					viable_cards.append(card)
				else:
					if card.endswith('Hearts') or card == 'Queen of Spades':
					# Only points cards viable for computer players.
						viable_cards.append(card)
					if not viable_cards:
						# If no points card in hand, all cards viable.
						viable_cards.append(card)
		if player.is_computer:
			# AI for choosing which card to play.
			if len(viable_cards) == 1:
				card = viable_cards[0]
				return card
			if leading:
				# What card to play if leading.
				card_vals = ('2', '3', '4')
				for choice in viable_cards:
					# Lead first with low value hearts.
					if choice.endswith('Hearts') \
							and choice.startswith(card_vals):
						card = choice
						return card
				else:
					current_lowest = 15
					lowest_card, choice = '', ''				
					for choice in viable_cards[::-1]:
						if not choice.endswith('Hearts') and \
								choice != 'Queen of Spades':
							# Play lowest non-heart card.
							if int(game_instance.card_values[
								player.deck_instance.get_value(choice)
									]) < current_lowest:
								current_lowest = int(game_instance.card_values[
										player.deck_instance.get_value(choice)
											])
								lowest_card = choice
						if lowest_card == '' or lowest_card.endswith('Hearts')\
								and choice != 'Queen of Spades':
							if int(game_instance.card_values[
								player.deck_instance.get_value(choice)
									]) < current_lowest:
								current_lowest = int(game_instance.card_values[
										player.deck_instance.get_value(choice)
											])
								lowest_card = choice
					card = lowest_card				
					return card	
			else:			
				# What card to play if not leading.
				if 'Queen of Spades' in viable_cards and suit_led != 'Spades':
					return 'Queen of Spades'

				if suit_led != 'Hearts':
					# Break hearts if no other choice, playing highest.
					if viable_cards[-1].endswith('Hearts'):
						if not game_instance.hearts_broken:
							game_instance.hearts_broken = True
							print('\nHearts have been broken!')
							input('Press ENTER to continue.')
						return viable_cards[-1]

				current_highest = 0
				for crd in table:
					# Determine highest value of cards on table with led
					# suit.
					if crd.endswith(suit_led):
						if int(game_instance.card_values[
								player.deck_instance.get_value(crd)
									]) > current_highest:
							current_highest = int(game_instance.card_values[
								player.deck_instance.get_value(crd)
									])			
				highest_card, choice = '', ''
				for choice in viable_cards:
					# Play the next lowest card of led suit without
					# going over. 
					if current_highest > int(game_instance.card_values[
							player.deck_instance.get_value(choice)
								]):
						highest_card = choice
					if highest_card: 
						if current_highest > \
								int(game_instance.card_values[
									player.deck_instance.get_value(choice)
										]) and int(game_instance.card_values[
									player.deck_instance.get_value(choice)
										]) > int(game_instance.card_values[
								player.deck_instance.get_value(highest_card)
										]):	
							highest_card = choice
					card = highest_card
				if not highest_card:
					# Play the next lowest, but not Queen of Spades.
					for choice in viable_cards:	
						if choice != 'Queen of Spades':
							card = viable_cards[0]
							return card
						else:
							card = viable_cards[1]
							return card
				else:
					return card			
		else:
			# Display choices for human players.
			if leading == True:
				print('Choose a card to lead:')
			else:
				print('Choose a card to play:')
				print(f'\n{suit_led} is the leading suit.\n')
			if len(viable_cards) == 1:
				print(f'\nOnly one card in viable cards: {viable_cards[0]}')
				input()
				card = viable_cards[0]
			else:	
				card = pyip.inputMenu(viable_cards, numbered=True)
		if card.endswith('Hearts'):
			if not game_instance.hearts_broken:
				game_instance.hearts_broken = True
				print('\nHearts have been broken!')
				input('Press ENTER to continue.')
		return card

	def resolve_turn(whose_turn, card, on_table):
		'''Resolves a turn, returns whose turn is next.'''
		print(f'{whose_turn.name} played the {card}.')
		on_table.append(card)
		whose_turn.hand.remove(card)
		whose_turn.played_card = card
		whose_turn = whose_turn.player_left
		return whose_turn