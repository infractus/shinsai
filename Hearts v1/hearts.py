import time
import pyinputplus as pyip

from shinsai_game import GameMethods, Deck
from hearts_classes import Player, Hand, Turn, Game

the_deck = Deck()
the_game = Game()

def play_game():
	'''This is the game loop.'''
	max_points = 0
	while True:
		the_game.hand_num += 1
		round_num = 0
		the_game.hearts_broken = False
		
		max_points = Hand.set_points(players, max_points)

		for player in players:
			# Empty each players discard pile to start a new hand.
			player.discard = []

		if max_points >= 100:
			# Stops the loop if someone breaks 100 points.
			playing_hand = False
			break

		print(f'\nThis is hand number {the_game.hand_num}.')
		
		deck = the_deck.build_decks(1)

		player_1.hand, player_2.hand, player_3.hand, player_4.hand = \
			the_deck.deal_hands(deck, 13, 4)

		for player in players:
			# Sort hands, show human players their cards.
			player.hand = Hand.sort_hand(player, player.hand)
			if not player.is_computer:
				the_deck.show_hand(player.name, player.hand)

		if the_game.hand_num % 4:
			# Passing cards if the game number is not divisible by 4.
			for player in players:
				# Determine which cards to pass for each player.
				player.hand = Hand.cards_to_pass(player, the_game, player.hand)
			for player in players:
				# Pass the cards between hands.
				Hand.pass_cards(player, the_game)
			
			for player in players:
				# Sort the hands again and show human players their cards.
				player.hand = Hand.sort_hand(player, player.hand)
				if not player.is_computer:
					the_deck.show_hand(player.name, player.hand)
				
		while True:
			# This is the hand loop.
			round_num += 1
			on_table = []
			for player in players:
				# Reset the played_card variable.
				player.played_card = ''
			if round_num == 1:
				# Always play 2 of Clubs on first round.
				played_first = Turn.first_turn(players)
				on_table.append('2 of Clubs')
				played_first.hand.remove('2 of Clubs')
				whose_turn = played_first.player_left
				suit_led = 'Clubs'
				played_first.played_card = '2 of Clubs'
				time.sleep(.5)
			else:
				print(f'\nIt is now {whose_turn.name}\'s turn.')
				card = Turn.take_turn(
					whose_turn, round_num, the_game, leading=True
						)
				suit_led = the_deck.get_suit(card)
				whose_turn = Turn.resolve_turn(whose_turn, card, on_table)
				time.sleep(.5)

			while len(on_table) < 4:
				if len(on_table) > 0:
					the_deck.show_table(on_table)
				print(f'\nIt is now {whose_turn.name}\'s turn.')
				card = Turn.take_turn(
					whose_turn, round_num, the_game, suit_led, table=on_table
						)
				whose_turn = Turn.resolve_turn(whose_turn, card, on_table)
				time.sleep(.5)
			
			winning_value = 0
			winning_card = ''
			print(f'\nCurrently on the table:\n{", ".join(on_table)}')
			for card in on_table:
				if card.endswith(suit_led):
					if the_game.card_values[the_deck.get_value(card)]\
							> winning_value:
						winning_value = \
							the_game.card_values[the_deck.get_value(card)]
						winning_card = card
			for player in players:
				if winning_card == player.played_card:
					winner = player
					print(
						f'\n{winner.name} takes the cards with the '
						f'{winning_card}.')
					time.sleep(.5)
			whose_turn = winner

			winner.discard.extend(on_table)
			on_table = []
			for player in players:
				# Adds points for each card player has taken this hand.
				player.round_points = 0
				for card in player.discard:
					if card in the_game.card_points.keys():
						player.round_points += the_game.card_points[card]
				if not player.is_computer:				
					print(f'\n{player.name} has {player.round_points} points '
					'in their discard pile.')
			for player in players:
				# If player shoots the moon.
				if player.round_points == 26:
					player.round_points = 0
					player.player_across.round_points = 26
					player.player_left.round_points = 26
					player.player_right.round_points = 26
					print(f'\n{player.name} SHOT THE MOON!!!')
					input()
					break
			
			if not player_1.hand:
				# If the hand is empty, stop playing the hand.
				break

	the_game.determine_winner(players)				


def game_setup():
	'''Setup for game.'''
	
	p1_name = GameMethods.gather_names()

	player_1 = Player(p1_name, the_deck, is_computer=False)
	player_2 = Player('Luna', the_deck)
	player_3 = Player('Ariel', the_deck)
	player_4 = Player('Marina', the_deck)
		
	player_1.assign_positions(player_2, player_3, player_4)
	player_2.assign_positions(player_3, player_4, player_1)
	player_3.assign_positions(player_4, player_1, player_2)
	player_4.assign_positions(player_1, player_2, player_3)

	players = [player_1, player_2, player_3, player_4]

	point_tracking = {}
	for player in players:
		point_tracking[player.name] = 0

	print('Welcome to Shinsai\'s Hearts!!')
	input('Press ENTER to start.')

	return player_1, player_2, player_3, player_4, players, point_tracking


player_1, player_2, player_3, player_4, players, point_tracking = game_setup()
while True:
	play_game()
	play_again = GameMethods.play_again()
	if play_again == 'no':
		print('Thanks for playing!')
		break