import time
import pyinputplus as pyip

import shinsai_game

CARD_POINTS = {
'2 of Hearts': 1, '3 of Hearts': 1, '4 of Hearts': 1, '5 of Hearts': 1,
'6 of Hearts': 1, '7 of Hearts': 1, '8 of Hearts': 1, '9 of Hearts': 1, 
'10 of Hearts': 1, 'Jack of Hearts': 1, 'Queen of Hearts': 1,
'King of Hearts': 1, 'Ace of Hearts': 1, 'Queen of Spades': 13
	}
CARD_VALUES = {
'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
	}

def game_setup():
	'''Setup for game.'''

	p1_name = the_game.gather_names()

	player_1 = shinsai_game.Player(p1_name, is_computer=False)
	player_2 = shinsai_game.Player('Luna')
	player_3 = shinsai_game.Player('Marina')
	player_4 = shinsai_game.Player('Ariel')
		
	# Create a list of players to work with.
	players = [player_1, player_2, player_3, player_4]

	# Assign players their positions relative to other players.
	assign_positions(player_1, player_2, player_3, player_4)
	assign_positions(player_2, player_3, player_4, player_1)
	assign_positions(player_3, player_4, player_1, player_2)
	assign_positions(player_4, player_1, player_2, player_3)

	
	# Create dictionary for point tracking.
	point_tracking = {}
	for player in players:
		point_tracking[player.name] = 0

	return player_1, player_2, player_3, player_4, players, point_tracking


def assign_positions(player, player_left, player_across, player_right):
	'''Assign positions around table.'''
	player.player_left = player_left
	player.player_across = player_across
	player.player_right = player_right


def start_play():
	'''Play the game.'''
	while True:
		print('\nWelcome to Shinsai\'s Hearts!!')
		input('Press ENTER to start.')
		play_game()
		play_again = the_game.play_again()
		if play_again == 'no':
			print('\nThanks for playing!')
			break


def play_game():
	'''Set up a new game.'''
	the_game.max_points = 0
	the_game.hand_num = 0
	the_game.hearts_broken = False
	for player in players:
		player.points = 0
		player.round_points = 0
	begin_hand()
	determine_winner()


def begin_hand():
	'''Start playing a hand.'''
	while True:
		playing_hand = set_up_hand()
		if not playing_hand:
			break
		passing_cards()
		play_hand()


def set_up_hand():
	'''Sets up each hand.'''
	the_game.hand_num += 1
	the_game.round_num = 0
	the_game.hearts_broken = False
	
	set_points()
	
	if the_game.max_points >= 100:
		# Stop playing the hand if someone breaks 100 points.
		return False
		
	for player in players:
		# Empty each players discard pile to start a new hand.
		player.discard = []

	print(f'\nThis is hand number {the_game.hand_num}.')
	
	deck = the_deck.build_decks(1)
	player_1.hand, player_2.hand, player_3.hand, player_4.hand = \
		the_deck.deal_hands(deck, 13, 4)

	for player in players:
		# Sort hands, show human players their cards.
		player.hand = sort_hand(player, player.hand)
		if not player.is_computer:
			the_deck.show_hand(player.name, player.hand)
	
	return True


def set_points():
	'''	Adds points for the round to total points for the hand.'''
	print()
	for player in players:
		player.points += player.round_points
		print(f'{player.name} has {player.points} total points.')
	for player in players:
		if player.points > the_game.max_points:
			the_game.max_points = player.points


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
		if the_deck.get_value(card) == 'Jack']
	[new_hand.append(card) for card in hand \
		if the_deck.get_value(card) == 'Queen']
	[new_hand.append(card) for card in hand \
		if the_deck.get_value(card) == 'King']
	[new_hand.append(card) for card in hand \
		if the_deck.get_value(card) == 'Ace']

	# Sort new_hand by suit to create final_hand.
	[final_hand.append(card) for card in new_hand \
		if the_deck.get_suit(card) == 'Hearts']
	[final_hand.append(card) for card in new_hand \
		if the_deck.get_suit(card) == 'Spades']
	[final_hand.append(card) for card in new_hand \
		if the_deck.get_suit(card) == 'Diamonds']
	[final_hand.append(card) for card in new_hand \
		if the_deck.get_suit(card) == 'Clubs']

	return final_hand


def passing_cards():
	'''Pass cards between players.'''
	if the_game.hand_num % 4:
		# Passing cards if the game number is not divisible by 4.
		for player in players:
			# Determine which cards to pass for each player.
			player.hand = cards_to_pass(player, player.hand)
		for player in players:
			# Pass the cards between hands.
			pass_cards(player)
		
		for player in players:
			# Sort the hands again and show human players their cards.
			player.hand = sort_hand(player, player.hand)
			if not player.is_computer:
				the_deck.show_hand(player.name, player.hand)


def cards_to_pass(player, hand):
	'''
	Determines where each player will pass cards, then calls
	choose_pass() to choose which cards to pass between players.
	'''
	if not player.is_computer:
		if the_game.hand_num % 4 == 1:
			print(
				f'\nChoose 3 cards to pass left to {player.player_left.name}.'
					)
			new_hand = choose_pass(player, hand)
		if the_game.hand_num % 4 == 2:
			print(
				f'\nChoose 3 cards to pass right to '
				f'{player.player_right.name}.'
					)
			new_hand = choose_pass(player, hand)
		if the_game.hand_num % 4 == 3:
			print(
				'\nChoose 3 cards to pass across to '
				f'{player.player_across.name}.'
					)	
			new_hand = choose_pass(player, hand)
	else:
		if the_game.hand_num % 4 == 1:
			new_hand = choose_pass(player, hand, 'left')
		if the_game.hand_num % 4 == 2:
			new_hand = choose_pass(player, hand, 'right')
		if the_game.hand_num % 4 == 3:
			new_hand = choose_pass(player, hand, 'across')
	return new_hand


def choose_pass(player, hand, passing_to=None):
	'''
	Decide which cards to pass. Returns the players hand without the
	chosen cards.
	'''
	if not player.is_computer:
		new_hand, cards = pick_cards_prompts(hand)
	else:
		new_hand, cards = pick_cards_pc(hand, passing_to)
		
	player.cards_to_pass = cards
	new_hand = new_hand[::-1]
	return new_hand


def pick_cards_prompts(hand):
	'''Prompt human player to pick cards.'''
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
	return new_hand, cards


def pick_cards_pc(hand, passing_to):
	'''Logic for computer to decide which cards to pass.'''
	new_hand = hand[::-1]
	cards = []
	suits = {'Hearts': [], 'Clubs': [], 'Spades': [], 'Diamonds': []}
	for suit in suits.keys():
	# Create a dictionary of the cards in the hand to easily determine
	# how many of each suit is in the hand.
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
			if len(cards) < 3:
				pick_3_cards(cards, suits, new_hand, card)
				
	return new_hand, cards


def pick_3_cards(cards, suits, new_hand, card):
	'''Logic to pick 3 cards to pass.'''
	clubs, hearts, diamonds, spades = \
		len(suits['Clubs']), len(suits['Hearts']), \
		len(suits['Diamonds']), len(suits['Spades'])
	if 1 < clubs < 5:
		# If less than 5 clubs void clubs keeping one for first round
		if card.endswith('Clubs'):
			cards.append(card)
			new_hand.remove(card)
			suits['Clubs'].remove(card)
	elif 0 < diamonds < 4:
		# If less than 4 diamonds void diamonds.
		if card.endswith('Diamonds'):
			cards.append(card)
			new_hand.remove(card)
			suits['Diamonds'].remove(card)
	elif 0 < spades < 4 and suits['Spades'] != ['Queen of Spades']:
			# If less than 4 spades void spades but keep the Queen
			if card.endswith('Spades'):
				cards.append(card)
				new_hand.remove(card)
				suits['Spades'].remove(card)
	elif 0 < diamonds <= clubs:
		# If less or same diamonds to clubs and more than zero diamonds
		# use diamond
		if card.endswith('Diamonds'):
			cards.append(card)
			new_hand.remove(card)
			suits['Diamonds'].remove(card)
	elif 1 < clubs <= diamonds:
		# If less or same clubs to diamonds and more than one clubs use
		# clubs
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
				return
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


def pass_cards(player):
	'''Pass the cards.'''
	if the_game.hand_num % 4 == 1:
		pass_left(player)
		
	if the_game.hand_num % 4 == 2:
		pass_right(player)

	if the_game.hand_num % 4 == 3:
		pass_across(player)


def pass_left(player):
	'''Pass cards left and display results to human players.'''
	player.player_left.hand.extend(player.cards_to_pass)
	if not player.is_computer:
		print(
			f'\n{player.name} passed the cards ' 
			f'{", ".join(player.cards_to_pass)} to {player.player_left.name}.'
				)
	if not player.player_left.is_computer:
		print(
			f'\n{player.name} passed the cards '
			f'{", ".join(player.cards_to_pass)} to {player.player_left.name}.'
				)


def pass_right(player):
	'''Pass cards right and display results to human players.'''
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


def pass_across(player):
	'''Pass cards across and display results to human players.'''
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


def play_hand():
	'''Play through a hand.'''
	whose_turn = ''
	while True:
		# This is the round loop.
		the_game.round_num += 1
		on_table = []
		for player in players:
			# Reset the played_card variable.
			player.played_card = ''

		whose_turn, suit_led = lead_round(on_table, whose_turn)
		whose_turn = continue_round(on_table, whose_turn, suit_led)	
		whose_turn, on_table = resolve_round(on_table, suit_led)
		check_shoot_the_moon()

		if not player_1.hand:
			# If the hand is empty, stop playing the hand.
			break


def lead_round(on_table, whose_turn):
	'''The first turn of a round.'''
	if the_game.round_num == 1:
		# Always play 2 of Clubs on first round.
		played_first = first_turn()
		on_table.append('2 of Clubs')
		played_first.hand.remove('2 of Clubs')
		whose_turn = played_first.player_left
		suit_led = 'Clubs'
		played_first.played_card = '2 of Clubs'
		time.sleep(.5)
	else:
		print(f'\nIt is now {whose_turn.name}\'s turn.\n')
		card = take_turn(whose_turn, leading=True)
		suit_led = the_deck.get_suit(card)
		whose_turn = resolve_turn(whose_turn, card, on_table)
		time.sleep(.5)
	return whose_turn, suit_led


def first_turn():
	'''2 of Clubs goes first in first round.'''
	for player in players:
		if '2 of Clubs' in player.hand:
			print(
				f'\n{player.name} has the 2 of Clubs and will go first. ' 
				f'\n{player.name} lays the 2 of Clubs.'
					)
			return player


def take_turn(player, suit_led=None, leading=False, table=None):
	'''Take a turn.'''
	viable_cards = choose_viable_cards(player, suit_led)
	
	if player.is_computer:
		card = take_turn_pc(suit_led, leading, viable_cards, table)
		
	else:
		card = take_turn_human(suit_led, leading, viable_cards)

	if card.endswith('Hearts'):
		if not the_game.hearts_broken:
			the_game.hearts_broken = True
			print('\nHearts have been broken!')
			input('Press ENTER to continue.')
	return card


def choose_viable_cards(player, suit_led):
	'''Make a list of viable cards to play.'''
	viable_cards = []
	for card in player.hand:
		if not the_game.hearts_broken:
			# Hearts not viable until broken.
			if card.endswith('Hearts'):
				continue
		if the_game.round_num == 1:
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
			if not player.is_computer:
				# All cards viable for human players.
				viable_cards.append(card)
			else:
				# Only points cards viable for computer players.
				if card.endswith('Hearts') or card == 'Queen of Spades':
					viable_cards.append(card)
				if not viable_cards:
					# If no points card in hand, all cards viable.
					viable_cards.append(card)
	return viable_cards


def take_turn_pc(suit_led, leading, viable_cards, table):
	'''Logic for choosing which card to play.'''
	if len(viable_cards) == 1:
		card = viable_cards[0]
		return card
	if leading:
		card = pc_leading(viable_cards)
	else:
		card = pc_not_leading(suit_led, viable_cards, table)		
	return card		


def pc_leading(viable_cards):
	'''Choose which card to play if leading.'''
	card_vals = ('2', '3', '4')
	for choice in viable_cards:
		# Lead first with low value hearts.
		if choice.endswith('Hearts') and choice.startswith(card_vals):
			card = choice
			return card
	else:
		current_lowest = 15
		lowest_card, choice = '', ''	
		for choice in viable_cards[::-1]:
			val = int(CARD_VALUES[the_deck.get_value(choice)])
			if not choice.endswith('Hearts') and choice != 'Queen of Spades':
				# Play lowest non-heart card.
				if val < current_lowest:
					current_lowest = val
					lowest_card = choice
			if lowest_card == '' or lowest_card.endswith('Hearts')\
					and choice != 'Queen of Spades':
				# If there are only hearts cards, play the lowest.
				if val < current_lowest:
					current_lowest = val
					lowest_card = choice
		card = lowest_card				
		return card


def pc_not_leading(suit_led, viable_cards, table):
	'''Determine card to play if not leading.'''
	if 'Queen of Spades' in viable_cards and suit_led != 'Spades':
		return 'Queen of Spades'

	if suit_led != 'Hearts':
		# Break hearts if no other choice, playing highest.
		if viable_cards[-1].endswith('Hearts'):
			if not the_game.hearts_broken:
				the_game.hearts_broken = True
				print('\nHearts have been broken!')
				input('Press ENTER to continue.')
			return viable_cards[-1]
	
	card = determine_highest_card(suit_led, viable_cards, table)
	
	return card


def determine_highest_card(suit_led, viable_cards, table):
	'''
	Determines the highest card on the table and chooses what card to play.
	'''
	current_highest = 0
	for crd in table:
		# Determine highest value of cards on table with led suit.
		val = int(CARD_VALUES[the_deck.get_value(crd)])
		if crd.endswith(suit_led):
			if val > current_highest:
				current_highest = val

	highest_card, choice = '', ''
	for choice in viable_cards:
		# Play the next lowest card of led suit without going over.
		val = int(CARD_VALUES[the_deck.get_value(choice)]) 
		if current_highest > val:
			highest_card = choice
		if highest_card:
			high_val = int(CARD_VALUES[the_deck.get_value(highest_card)])
			if current_highest > val > high_val:	
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
	return card


def take_turn_human(suit_led, leading, viable_cards):
	'''
	Displays choices of viable cards for human players and prompts to
	choose.
	'''
	if leading == True:
		print('Choose a card to lead:')
	else:
		print('Choose a card to play:')
		print(f'{suit_led} is the leading suit.\n')
	if len(viable_cards) == 1:
		print(f'\nOnly one card in viable cards: {viable_cards[0]}')
		input()
		card = viable_cards[0]
	else:	
		card = pyip.inputMenu(viable_cards, numbered=True)
	return card


def resolve_turn(whose_turn, card, on_table):
	'''Resolves a turn, returns whose turn is next.'''
	print(f'{whose_turn.name} played the {card}.')
	on_table.append(card)
	whose_turn.hand.remove(card)
	whose_turn.played_card = card
	whose_turn = whose_turn.player_left
	return whose_turn


def continue_round(on_table, whose_turn, suit_led):
	'''The remaining turns of a round.'''
	while len(on_table) < 4:
		if len(on_table) > 0:
			the_deck.show_table(on_table)
		print(f'\nIt is now {whose_turn.name}\'s turn.')
		card = take_turn(whose_turn, suit_led, table=on_table)
		whose_turn = resolve_turn(whose_turn, card, on_table)
		time.sleep(.5)
	return whose_turn


def resolve_round(on_table, suit_led):
	'''Resolve a round.'''
	winning_value = 0
	winning_card = ''
	print(f'\nCurrently on the table:\n{", ".join(on_table)}')
	for card in on_table:
		# Determine which card of the suit led is highest.
		if card.endswith(suit_led):
			if CARD_VALUES[the_deck.get_value(card)] > winning_value:
				winning_value = CARD_VALUES[the_deck.get_value(card)]
				winning_card = card
	for player in players:
		# The player with the highest card "wins" the round.
		if winning_card == player.played_card:
			winner = player
			print(
				f'\n{winner.name} takes the cards with the {winning_card}.')
			time.sleep(.5)

	whose_turn = winner
	winner.discard.extend(on_table)
	on_table = []
	
	add_points()

	return whose_turn, on_table


def add_points():
	'''Adds points for each card player has taken this hand.'''
	for player in players:
		player.round_points = 0
		for card in player.discard:
			if card in CARD_POINTS.keys():
				player.round_points += CARD_POINTS[card]
		if not player.is_computer:				
			print(
				f'\n{player.name} has {player.round_points} points in their '
				'discard pile.'
					)


def check_shoot_the_moon():
	'''Check if any players shot the moon.'''
	for player in players:
		if player.round_points == 26:
			player.round_points = 0
			player.player_across.round_points = 26
			player.player_left.round_points = 26
			player.player_right.round_points = 26
			print(f'\n{player.name} SHOT THE MOON!!!')
			input('Press ENTER to continue.')
			return True


def determine_winner():
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
					f'\nAfter {the_game.hand_num} hands, {player.name} and '
					f'{winner.name} both have {winner.points} points and have '
					'won with a tie!'
						)
				return
	print(
		f'\nAfter {the_game.hand_num} hands, {winner.name} has won with '
		f'{low_points} points.'
			)


the_deck = shinsai_game.Deck()
the_game= shinsai_game.Game()
player_1, player_2, player_3, player_4, players, point_tracking = game_setup()
start_play()