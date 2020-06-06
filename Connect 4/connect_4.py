#! python3
"""This is the Python with Friends Coding Challenge - Week 1"""

import random

import shinsai, shinsai_pygame, shinsai_token_set, make_sets

# Create lists of winning combinations and slots in each column.
WIN_COMBOS = make_sets.win_combos()
COLUMN_LISTS = make_sets.column_lists()

class Connect4:
    """Class to manage game and behavior."""
    def __init__(self):
        """Initialize a game of Connect 4."""                 
        self.the_game = shinsai_pygame.GUIGame("rshinsai's Connect 4")
        self.tokens = shinsai_token_set.TokenSet(self.the_game)
        self.tracking = self.the_game.get_stored_tracking(
            self.the_game.settings.track_file
                )
        self.menu_sound = self.the_game.create_sound('sounds/switch7.wav')
        self.the_game.settings.bg_color = self.the_game.settings.white
        self.the_game.settings.board_text_color = self.the_game.settings.black
        self.the_game.settings.menu_text_color = self.the_game.settings.green

    def run_game(self):
        """Start the main loop for the game."""
        while the_game.playing:
            self.game_setup()
            self.check_tracking()
            self.display_menu()

    def game_setup(self):
        """Set up the game.
        
        Displays the welcome screen, gathers player number and player
        information, sets various game settings.
        """
        while True:
            button_clicked = self.display_welcome_screen()
            p1_name, p2_name = None, None

            while True:
                pressed = the_game.wait_for_input()
                if button_clicked.rect.collidepoint(the_game.x, the_game.y):
                    the_game.x = the_game.y = -5
                    the_game.play_sound(self.menu_sound)
                    break
                elif pressed == 'Esc':
                    the_game.terminate(True)
                else:
                    the_game.play_sound(self.menu_sound)
                    break

            num_players = self.select_num_players()
            if num_players == 1:
                the_game.num_players = 1
                p1_name = self.select_player(1)
                p2_name = 'Luna'

            if num_players == 2:
                the_game.num_players = 2
                p1_name = self.select_player(1)
                p2_name = self.select_player(2)
                the_game.update_display()
                
            if p1_name and p2_name:
                if p1_name == 'Marina (PC)':
                    self.player_1 = shinsai.Player('Marina')
                    self.player_2 = shinsai.Player('Luna')
                else:
                    self.player_1 = shinsai.Player(p1_name, is_computer=False)
                    self.player_2 = shinsai.Player('Luna')    
                if the_game.num_players == 2:
                    self.player_2 = shinsai.Player(p2_name, is_computer=False)

                self.players = [self.player_1, self.player_2]
                self.player_1.opponent = self.player_2
                self.player_2.opponent = self.player_1
                self.player_1.token = self.tokens.player1lastplayed
                self.player_2.token = self.tokens.player2lastplayed

                the_game.round_num = 0
                the_game.game_over = False
                the_game.tournament_over = False
                break
    
    def display_welcome_screen(self):
        """The first screen the player sees."""
        the_game.screen.fill(settings.black)
        con_4 = shinsai_pygame.Images(the_game, 'images/connect_4.jpg')
        con_4_rect = con_4.sheet.get_rect()
        con_4_image = con_4.image_at(con_4_rect)
        con_4.display_image(
            con_4_image, con_4_rect, con_4_rect.width / 2 + 200, 125
                )
        the_game.draw_text(
            "Welcome to rshinsai's Connect 4!", the_game.screen,
            screen_rect.width / 2, screen_rect.height / 2 + 100,
            settings.large_font, settings.menu_text_color
                )
        the_game.draw_bottom_text(
            "Press ESC to quit.", settings.menu_text_color
                )

        button = shinsai_pygame.Button(
            the_game, "Press to Begin", settings.green, settings.blue, 240, 
            coords=(
                settings.screen_width / 2, settings.screen_height / 2 + 200
                    )
                )
        shinsai_pygame.Button.draw_button(button)
        the_game.update_display()
        return button

    def select_num_players(self):
        """Select the number of players."""
        the_game.screen.fill(settings.black)

        the_game.draw_text(
            "How many players will be playing?", the_game.screen, 
            screen_rect.width / 2, screen_rect.height / 2 - 100,
            settings.large_font, settings.menu_text_color
                )

        button_1 = shinsai_pygame.Button(
            the_game, "(1)", settings.blue, settings.menu_text_color, 100, 
            coords=(
                settings.screen_width / 2 - 100, settings.screen_height / 2
                    )
            )
        button_2 = shinsai_pygame.Button(
            the_game, "(2)", settings.blue, settings.menu_text_color, 100, 
            coords=(
                settings.screen_width / 2 + 100, settings.screen_height / 2
                    )
            )
        
        shinsai_pygame.Button.draw_button(button_1)
        shinsai_pygame.Button.draw_button(button_2)

        the_game.draw_bottom_text(
            "Press ESC to return to welcome screen.", settings.menu_text_color
                )

        the_game.update_display()
        while True:
            pressed = the_game.wait_for_input(numbered=True)
            if pressed == 'Esc':
                the_game.play_sound(self.menu_sound)
                return
            if pressed == '1' or button_1.rect.collidepoint(
                    the_game.x, the_game.y
                ):
                the_game.x = the_game.y = -5
                the_game.play_sound(self.menu_sound)
                return 1
            if pressed == '2' or button_2.rect.collidepoint(
                    the_game.x, the_game.y
                ):
                the_game.x = the_game.y = -5
                the_game.play_sound(self.menu_sound)
                return 2      

    def select_player(self, player_num):
        """Asks if player has played before."""        
        if player_num == 1:
            text = 'Player 1'
        else:
            text = 'Player 2'

        if the_game.num_players == 1:
            pressed = the_game.yes_no_buttons(
                "Are you an existing player?", the_game,
                settings.menu_text_color, settings.green, settings.blue,
                settings.black, "Press ESC to return to title screen."
                    )
        else:
            pressed = the_game.yes_no_buttons(
                f"{text}, are you an existing player?", the_game,
                settings.menu_text_color, settings.green, settings.blue,
                settings.black, "Press ESC to return to title screen."
                        )

        if pressed == 'Esc':
            the_game.play_sound(self.menu_sound)
            return
        if pressed == 'y':
            the_game.x = the_game.y = -5
            the_game.play_sound(self.menu_sound)
            name = self.returning_user()
            return name
        if pressed == 'n':
            the_game.x = the_game.y = -5
            the_game.play_sound(self.menu_sound)
            name = the_game.gather_names()
            return name      

    def returning_user(self):
        """Select a returning user.
        
        Creates and displays a list of saved players (and the PC player)
        to select from.
        """
        the_game.screen.fill(settings.black)
        human_players = ['Marina (PC)']
        players = tracking["player_stats"].keys()
        for player in players:
            if not tracking["player_stats"][f'{player}']["is_computer"]:
                human_players.append(player)
        the_game.draw_text(
            "Select a player using the number listed:", the_game.screen,
            screen_rect.width / 2, 100, settings.large_font,
            settings.menu_text_color
                )

        text_y = 200
        buttons = []
        for i, choice in enumerate(human_players):
            text_y += 50
            button = shinsai_pygame.Button(
                the_game, f"{i+1}) {choice}", color=settings.lightblue,
                width = 400, height=40, coords=(
                    screen_rect.width / 2, text_y
                        )
                    )
            button.draw_button()
            buttons.append(button)

        the_game.draw_bottom_text(
            "Press ESC to return to title screen.", settings.menu_text_color
                )
        name = self.select_name(buttons, human_players)
        return name
    
    def select_name(self, buttons, human_players):
        """Select a name from the list."""
        while True:
            the_game.update_display()
            pressed = the_game.wait_for_input(numbered=True)
            if pressed:
                if pressed == 'Esc':
                    the_game.play_sound(self.menu_sound)
                    break
                if pressed == 'button':
                    for i, button in enumerate(buttons):
                        if button.rect.collidepoint(the_game.x, the_game.y):
                            the_game.x = the_game.y = -5
                            the_game.play_sound(self.menu_sound)
                            name = f'{button}'.split(None, 1)[1]
                            return name
                try:
                    for _ in human_players:
                        name = human_players[pressed-1]
                    the_game.play_sound(self.menu_sound)        
                    return name
                except:
                    pressed = None
        
    def check_tracking(self):
        """Creates appropriate key/value pairs in tracking file."""
        player_stats = tracking['player_stats']
        game_stats = tracking['game_stats']

        for player in self.players:
            # Check if player exists, if not, creates initial values.
            if f'{player}' in player_stats.keys():
                continue
            player_stats[f'{player}'] = {}
            player_stats[f'{player}'][f'{player.opponent}'] = [0, 0]
            player_stats[f'{player}']['is_computer'] = player.is_computer
            player_stats[f'{player}']['total_games'] = 0
            player_stats[f'{player}']['total_wins'] = 0
            player_stats[f'{player}']['total_losses'] = 0
            player_stats[f'{player}']['total_draws'] = 0
            player_stats[f'{player}']['total_turns'] = 0
            player_stats[f'{player}']['total_rounds'] = 0
            player_stats[f'{player}']['total_tournaments'] = 0
            player_stats[f'{player}']['tournament_wins'] = 0
            player_stats[f'{player}']['tournament_losses'] = 0
                            
        for player in self.players:
            # Checks if the player has played against this opponent.
            if f'{player.opponent}' in player_stats[f'{player}'].keys():
                continue
            # Creates win/loss tally for specific opponent.
            player_stats[f'{player}'][f'{player.opponent}'] = [0,0]

        if game_stats == {}:
            # Creates initial values if first time running game.
            game_stats.update(
                {
                    'total_tournaments': 0, 'total_games': 0,
                    'total_rounds': 0, 'total_turns': 0, 'num_ties': 0
                    }
                )

        the_game.write_to_tracking(settings.track_file, tracking)

    def display_menu(self):
        """Display the main menu."""
        while True:
            the_game.screen.fill(settings.black)
            the_game.draw_text(
                f"Welcome, {self.player_1}!", the_game.screen, 
                screen_rect.width / 2, 100, settings.large_font,
                settings.menu_text_color

                    )
            the_game.draw_text(
                "Select an option:", the_game.screen,
                screen_rect.width / 2, 200, settings.large_font,
                settings.menu_text_color
                    )
            menu_choices = [
                'Start a tournament', 'Start a game', 'View game stats',
                'View players stats', 'Switch player', 'Quit'
                    ]
            if tracking["game_stats"]["total_games"] == 0:
                # Only show game stats option if a game's been played.
                menu_choices.remove('View game stats')
            the_game.draw_bottom_text(
                "Press ESC to return to title screen.",
                settings.menu_text_color
                    )

            text_y = 300
            buttons = []
            for i, choice in enumerate(menu_choices):
                text_y += 50
                button = shinsai_pygame.Button(
                    the_game, f"{i+1}) {choice}", color=settings.lightblue,
                    width = 400, height=40, coords=(
                        screen_rect.width / 2, text_y
                            )
                        )
                button.draw_button()
                buttons.append(button)
            
            choice = None
            the_game.update_display()
            pressed = the_game.wait_for_input(numbered=True)
            if pressed == 'Esc':
                the_game.play_sound(self.menu_sound)
                break
            if pressed == 'button':
                for i, button in enumerate(buttons):
                    if button.rect.collidepoint(the_game.x, the_game.y):
                        the_game.x = the_game.y = -5
                        the_game.play_sound(self.menu_sound)
                        choice = menu_choices[i]
            else:
                try:
                    for i in menu_choices:
                        choice = menu_choices[pressed-1]
                        the_game.play_sound(self.menu_sound)
                except:
                    pressed = None
            if pressed:
                if choice == 'Start a tournament':
                    the_game.is_tournament = True
                    the_game.game_over = False                       
                    self.the_tournament = shinsai.Tournament()
                    self.the_tournament.players = self.players
                    for player in self.the_tournament.players:
                        player.round_wins = 0
                    self.start_tournament()
                if choice == 'Start a game':
                    the_game.is_tournament = False
                    the_game.game_over = False
                    self.start_play()
                elif choice == 'View game stats':
                    self.view_game_stats()
                elif choice == 'View players stats':
                    self.view_player_stats()
                elif choice == 'Switch player':
                    break
                elif choice == 'Quit':
                    the_game.playing = False
                    the_game.terminate(True)
    
    def start_tournament(self):
        """Starts the tournament loop"""
        while True:
            if not self.the_tournament.tournament_over:
                self.show_tournament_record()
                self.start_play()
            else:
                play_again = the_game.yes_no_buttons(
                    "Would you like to play another tournament?", the_game,
                    settings.menu_text_color, settings.green, settings.blue,
                    settings.black
                        )
                if play_again == 'n':
                    self.show_tournament_record()
                    break
                else:
                    self.the_tournament.tournament_over = False
                    self.the_tournament.winner = None
                    the_game.game_over = False
                    self.start_play()

    def show_tournament_record(self):
        """Shows the players tournament record."""
        the_game.screen.fill(settings.black)
        player_stats = tracking["player_stats"]
        p1_stats = player_stats[f"{self.player_1}"]

        total_tournaments = p1_stats["total_tournaments"]
        total_rounds = p1_stats["total_rounds"]
        tournament_wins = p1_stats["tournament_wins"]
        tournament_losses = p1_stats["tournament_losses"]

        the_game.draw_heading_text(
            f'Tournament Stats for {self.player_1}', settings.menu_text_color
                )
        the_game.draw_text(
            f'{self.player_1} has played {total_tournaments} tournaments.',
            the_game.screen, screen_rect.width / 2, 
            screen_rect.height / 2 - 100, settings.medium_font,
            settings.menu_text_color
                )
        the_game.draw_text(
            f'Rounds: {total_rounds}',
            the_game.screen, screen_rect.width / 2,
            screen_rect.height / 2 - 50, settings.medium_font,
            settings.menu_text_color
                )
        the_game.draw_text(
            f'Wins: {tournament_wins}', the_game.screen, screen_rect.width / 2, 
            screen_rect.height / 2, settings.medium_font,
            settings.menu_text_color
                )
        the_game.draw_text(
            f'Losses: {tournament_losses}', the_game.screen,
            screen_rect.width / 2, screen_rect.height / 2 + 50,
            settings.medium_font, settings.menu_text_color
                )
        
        the_game.press_any_key(self.menu_sound)

    def start_play(self):
        """Starts the game loop"""
        if the_game.is_tournament:
            the_tournament = self.the_tournament
            the_tournament.win_count = [0, 0]
            the_tournament.draw_count = 0
            the_tournament.round_num = 0
            the_game.tournament_over = False
            for player in self.players:
                player.round_wins = 0
        while True:
            if the_game.is_tournament:
                if the_tournament.win_count[0] == 2 or\
                        the_tournament.win_count[1] == 2:
                    the_tournament.tournament_over = True
                    self.show_tournament_results()
                    break
            if not the_game.game_over:
                if the_game.is_tournament:
                    the_tournament.round_num += 1
                self.new_game()
            else:
                play_again = the_game.yes_no_buttons(
                    "Would you like to play another game?", the_game,
                    settings.menu_text_color, settings.green, settings.blue,
                    settings.black
                        )
                if play_again == 'n':
                    self.show_record()
                    if the_game.is_tournament:
                        the_tournament.tournament_over = True
                    break
                else:
                    if the_game.is_tournament:
                        the_tournament.round_num += 1
                    self.new_game()
    
    def show_tournament_results(self):
        """Show the results of the tournament."""
        the_tournament = self.the_tournament
        player_stats = tracking['player_stats']
        winning_rounds = 0 
        for player in the_tournament.players:
            if player.round_wins > winning_rounds:
                winning_rounds = player.round_wins
                the_tournament.winner = player
        
        winner_stats = player_stats[f'{the_tournament.winner}']
        opponent_stats = player_stats[f'{the_tournament.winner.opponent}']
        game_stats = tracking['game_stats']

        winner_stats['total_tournaments'] += 1
        winner_stats['tournament_wins'] += 1
        opponent_stats['total_tournaments'] += 1
        opponent_stats['tournament_losses'] += 1
        game_stats['total_tournaments'] += 1

        the_game.write_to_tracking(settings.track_file, tracking)

        the_game.screen.fill(settings.black)
        the_game.draw_heading_text(
            'Tournament Results', settings.menu_text_color
                )
        the_game.draw_text(
            f'After {the_tournament.round_num} rounds,', the_game.screen,
            screen_rect.width / 2, screen_rect.height / 2 - 50,
            settings.medium_font, settings.menu_text_color
                )
        the_game.draw_text(
            f'{the_tournament.winner} is the winner!', the_game.screen,
            screen_rect.width / 2, screen_rect.height / 2, settings.large_font,
            settings.menu_text_color
                )

        the_game.press_any_key(self.menu_sound)
        
    def new_game(self):
        """Create new game.
        
        Creates the_board, a dictionary tracking states of every piece.
        """
        the_game.turn_num = 0
        the_game.game_over = False
        the_game.the_board = {}
        the_game.tokens_left = 42
        tokens = self.tokens
        
        for row in range(0, 7):
            for column in range(0, 6):
                the_game.the_board[str(row)+str(column)] = {
                    "token": tokens.empty, "state": "empty", "player": None,
                    "x": tokens.empty.rect.width * row + 375,
                    "y": tokens.empty.rect.height * column + 200,
                    "button": shinsai_pygame.Button(
                        the_game, width=tokens.empty.rect.width, 
                        height=tokens.empty.rect.height, coords=(
                            tokens.empty.rect.width * row + 375 + \
                                (tokens.empty.rect.width * 1/2),
                            tokens.empty.rect.height * column + 200 + \
                                (tokens.empty.rect.height * 1/2),
                                )
                            )
                        }

        the_game.turn = the_game.who_goes_first()
        self.show_record()
        self.show_who_first()
        self.play_game()

    def show_who_first(self):
        """Display who is going first."""
        the_game.screen.fill(settings.black)        
        if the_game.turn == 1:
            the_game.turn = self.player_1
            the_game.draw_center_text(
                f'{self.player_1} goes first.', settings.menu_text_color
                    )
        else:
            the_game.turn = self.player_2
            the_game.draw_center_text(
                f'{self.player_2} goes first.', settings.menu_text_color
                    )

        the_game.press_any_key(self.menu_sound)

    def play_game(self):
        """Play the game."""
        the_game.x, the_game.y = -5, -5
        the_board = the_game.the_board
        while True:
            while not the_game.game_over:
                the_game.check_for_input()
                self.update_screen()
                the_game.turn_num += 1
                        
                for player in self.players:
                    if the_game.turn == player:
                        self.take_turn(player)
                        the_game.tokens_left -= 1
                        for combo in WIN_COMBOS:
                            # Check for a win.
                            for i in combo:
                                if the_game.the_board[i]['player'] != player:
                                    break
                            else:
                                # If a win is found, highlight the
                                # winning pieces, and pause 2 seconds.
                                for i in combo:
                                    the_board[i]['token'] = the_game.turn.token
                                    the_board[i]['token'].x = the_board[i]['x']
                                    the_board[i]['token'].y = the_board[i]['y']
                                    the_board[i]['token'].blitme()
                                the_game.update_display()
                                the_game.pause_game(2)
                                the_game.game_over = True
                                the_game.winner = player
                        the_game.turn = player.opponent
                        break 

                if the_game.tokens_left == 0:
                    the_game.game_over = True
                    the_game.winner = None
                    if the_game.is_tournament:
                        self.the_tournament.draw_count += 1
                    
            
            if the_game.is_tournament:
                if the_game.winner:
                    the_game.winner.round_wins += 1
                    if the_game.winner == self.player_1:
                        self.the_tournament.win_count[0] += 1
                    if the_game.winner == self.player_2:
                        self.the_tournament.win_count[1] += 1
            self.game_over(the_game.winner)
            break
    
    def update_screen(self):
        """Updates the screen."""
        self.check_for_clicks()
        self.draw_board()
        the_game.update_display()

    def check_for_clicks(self):
        """Checks if a button has been clicked."""
        try:
            if the_game.exit_button.rect.collidepoint(the_game.x, the_game.y):
                the_game.terminate(True)
        except:
            return

    def draw_board(self):
        """Draw the board."""
        the_board = the_game.the_board

        the_game.screen.fill(settings.bg_color)
        the_game.draw_text(
            f'Turn: {the_game.turn_num}', the_game.screen, 120, 50,
            settings.medium_font, settings.board_text_color
                )
        the_game.draw_text(
            f'{self.player_1}:', the_game.screen, screen_rect.width * 1/3, 50,
            settings.medium_font, settings.board_text_color
                )

        the_game.draw_text(
            f'{self.player_2}:', the_game.screen, screen_rect.width * 2/3, 50,
            settings.medium_font, settings.board_text_color
                )

        self.tokens.player1.x = screen_rect.width * 1/3
        self.tokens.player2.x = screen_rect.width * 2/3
        self.tokens.player1.y = self.tokens.player2.y = 75
        self.tokens.player1.blitme()
        self.tokens.player2.blitme()

        num_x = screen_rect.width * 1/4 + self.tokens.player1.rect.width + 40

        for i in range(1, 8):
            # Draw numbers at bottom of board.
            the_game.draw_text(
                f'{i}', the_game.screen, num_x, screen_rect.height * 3/4, 
                settings.medium_font, settings.board_text_color
                    )
            num_x += self.tokens.player1.rect.width

        the_game.draw_text(
            'Press a numbered key or click on a column to drop a piece.', 
            the_game.screen, screen_rect.width * 1/2, screen_rect.height - 100,
            settings.medium_font, settings.board_text_color
                )
        the_game.draw_text(
            f"It is {self.the_game.turn}'s turn.", the_game.screen,
            screen_rect.width / 2, screen_rect.height - 150,
            settings.medium_font, settings.board_text_color
                )

        the_game.exit_button = shinsai_pygame.Button(
            the_game, "Quit (ESC)", settings.blue, settings.white,
            coords=(1050, 50)
                )

        if the_game.is_tournament:
            # Show round information if tournament.
            the_game.draw_text(
                f'Round: {self.the_tournament.round_num}', the_game.screen,
                120, 100, settings.medium_font, settings.board_text_color
                    )
            the_game.draw_text(
                f'{self.player_1}: {self.the_tournament.win_count[0]}',
                the_game.screen, 120, 150, settings.medium_font,
                settings.board_text_color
                    )
            the_game.draw_text(
                f'{self.player_2}: {self.the_tournament.win_count[1]}',
                the_game.screen, 120, 200, settings.medium_font,
                settings.board_text_color
                    )
            the_game.draw_text(
                f'Draws: {self.the_tournament.draw_count}', the_game.screen,
                120, 250, settings.medium_font, settings.board_text_color
                    )       

        for k in the_board.keys():
            # Draw the board itself.
            the_board[k]['token'].x = the_board[k]['x']
            the_board[k]['token'].y = the_board[k]['y']
            the_board[k]['token'].blitme()

        the_game.exit_button.draw_button()

    def take_turn(self, player):
        """Take a turn."""
        the_board = the_game.the_board
        while True:
            if player.is_computer:
                column_selected = self.take_turn_computer()
            else:
                column_selected = self.take_turn_human()

            for k in the_board.keys():
                # Switch from the "last played" token to the standard
                if the_board[k]['token'] == self.tokens.player1lastplayed:
                    the_board[k]['token'] = self.tokens.player1
                if the_board[k]['token'] == self.tokens.player2lastplayed:
                    the_board[k]['token'] = self.tokens.player2                                     
            for xy in reversed(COLUMN_LISTS[column_selected - 1]):
                # Take the turn and "animate" the results.
                if the_board[xy]['state'] == 'taken':
                    continue
                elif the_board[xy]['state'] == 'empty':
                    the_board[xy]['token'] = the_game.turn.token
                    self.animate_result(xy)
                    the_board[xy]['state'] = "taken"
                    the_board[xy]['player'] = the_game.turn
                    return xy

    def take_turn_computer(self):
        """Take a turn if player is computer."""
        the_board = the_game.the_board
        # Take the center column if it's not taken.
        if the_game.turn_num == 1:
            return 4
        if the_game.turn_num == 2 and the_board['35']['state'] == 'empty':
            return 4

        column_selected = self.check_for_wins(the_board, the_game.turn)
        # Check for winning moves.
        if not column_selected:
            # Check if the opponent will win next turn and block.
            column_selected = self.check_for_wins(
                the_board, the_game.turn.opponent
                    )
        if not column_selected:
            # Pick a random column with at least 1 empty slot.
            empty_slots = []
            col_number = 0
            for column in COLUMN_LISTS:
                col_number += 1
                for xy in reversed(column):
                    if the_board[xy]['state'] == 'empty':
                        empty_slots.append(col_number)
                        break
            chosen = random.choice(empty_slots)
            column_selected = chosen
        return column_selected

    def check_for_wins(self, the_board, player):
        """Check if any winning combos."""
        for combo in WIN_COMBOS:
            empty_slots = []
            piece_count = 0
            for i in combo:
                if the_board[i]['player'] == player:
                    piece_count += 1
                if the_board[i]['state'] == 'empty':
                    empty_slots.append(i)
            if piece_count == 3 and empty_slots:
                col_number = 0
                for column in COLUMN_LISTS:
                    col_number += 1
                    if empty_slots[0] in column:
                        check_empty = []
                        for xy in column:
                            if the_board[xy]['state'] == 'empty':
                                check_empty.append(xy)
                        if check_empty[-1] == empty_slots[0]:
                          column_selected = col_number
                          return column_selected 
                        else:
                            continue
    
    def take_turn_human(self):
        """Take a turn if player is human."""
        the_board = the_game.the_board
        while True:        
            column_selected = None
            pressed = the_game.wait_for_input(numbered=True)

            if pressed in range(1, 8):
                column_selected = pressed
            if pressed == 'button':  
                for k in the_board.keys():
                    if the_board[k]['button'].rect.collidepoint(
                        the_game.x, the_game.y
                            ):
                        the_game.x = the_game.y = -5
                        for i, column in enumerate(COLUMN_LISTS):
                            if k in column:
                                pressed = i+1
                                column_selected = pressed
            if the_game.exit_button.rect.collidepoint(the_game.x, the_game.y):
                the_game.terminate(True)
            if pressed == "Esc":
                the_game.terminate(True)
            return column_selected
    
    def animate_result(self, xy):
        """Animate the results of a choice."""
        the_board = the_game.the_board
        tokens = self.tokens
        for column in COLUMN_LISTS:
            if xy in column:
                for xyz in column:
                    if the_board[xyz]['state'] == 'empty':
                        if the_game.turn == self.player_1:
                            tokens.falling_token.image = tokens.player1.image
                        else:
                            tokens.falling_token.image = tokens.player2.image
                        tokens.falling_token.x = the_board[xyz]['x']
                        tokens.falling_token.y = the_board[xyz]['y']
                        tokens.falling_token.blitme()
                        the_game.update_display()
                        the_game.pause_game(.20)
                        tokens.falling_token.image = tokens.empty.image
                        tokens.falling_token.blitme()
                        the_game.update_display()
                    else:
                        return

    def game_over(self, player):
        """Actions to take if the game is over.

        Displays results and updates the tracking.
        """        
        game_stats = tracking['game_stats']
        player_stats = tracking['player_stats']
        
        the_game.screen.fill(settings.black)
        the_game.draw_text(
            f'After {the_game.turn_num} turns,', the_game.screen, 
            screen_rect.width / 2, 250, settings.medium_font, 
            settings.menu_text_color
                )

        if player:
            the_game.draw_text(
                f'{player} is the winner!', the_game.screen, 
                screen_rect.width / 2, 300, settings.medium_font,
                settings.menu_text_color
                    )
            p_stats = player_stats[f'{player}']
            opponent_stats = player_stats[f'{player.opponent}']
        
            p_stats[f'{player.opponent}'][0] += 1
            opponent_stats[f'{player}'][1] += 1
            p_stats['total_wins'] += 1
            opponent_stats['total_losses'] += 1
        else:
            the_game.draw_text(
                'The game has ended in a draw!', the_game.screen, 
                screen_rect.width / 2, 300, settings.medium_font,
                settings.menu_text_color
                    )
            for player in self.players:
                p_stats = player_stats[f'{player}']
                p_stats['total_draws'] += 1
            game_stats['num_ties'] += 1
        
        if the_game.is_tournament:
            game_stats['total_rounds'] += 1
        game_stats['total_games'] += 1
        game_stats['total_turns'] += the_game.turn_num
        for i in self.players:
            player_stats[f'{i}']["total_turns"] += the_game.turn_num
            player_stats[f'{i}']["total_games"] += 1
            if the_game.is_tournament:
                    player_stats[f'{i}']['total_rounds'] += 1
        the_game.write_to_tracking(settings.track_file, tracking)
        the_game.press_any_key(self.menu_sound)

    def show_record(self):
        """Shows the record of wins/losses."""
        the_game.screen.fill(settings.black)
    
        track_list = tracking["player_stats"][f"{self.player_1}"]\
            [f"{self.player_2}"]
        the_game.draw_center_text(
            f'{self.player_1} has {track_list[0]} wins and {track_list[1]}'
            f' losses against {self.player_2}.', settings.menu_text_color
                )

        the_game.press_any_key(self.menu_sound)

    def view_game_stats(self):
        """View the stats of the game in general."""
        game_stats = tracking['game_stats']
        total_games = game_stats["total_games"]
        total_turns = game_stats["total_turns"]
        num_ties = game_stats["num_ties"]

        the_game.screen.fill(settings.black)
        
        the_game.draw_text(
            'Game Stats', the_game.screen, screen_rect.width / 2, 150,
            settings.large_font, settings.menu_text_color
                )
        
        if total_games == 1:
            the_game.draw_text(
                f'Out of {total_games} total game:', the_game.screen, 
                screen_rect.width / 2, 250, settings.basic_font, 
                settings.menu_text_color
                    ) 
        else:
            the_game.draw_text(
                f'Out of {total_games} total games:', the_game.screen, 
                screen_rect.width / 2, 250, settings.basic_font, 
                settings.menu_text_color
                    )    
        the_game.draw_text(
            f'There have been {num_ties} tied games - '
            f'{round(num_ties / total_games * 100, 2)}%', the_game.screen,
            screen_rect.width / 2, 300, settings.basic_font,
            settings.menu_text_color
                )
        the_game.draw_text(
            'The average number of turns per game: '
            f'{round(total_turns / total_games, 2)}', the_game.screen,
            screen_rect.width / 2, 350, settings.basic_font,
            settings.menu_text_color
                )
        the_game.draw_text(
            'The total number of tournaments played: '
            f'{game_stats["total_tournaments"]}', the_game.screen,
            screen_rect.width / 2, 400, settings.basic_font,
            settings.menu_text_color
                )
        the_game.press_any_key(self.menu_sound)
        
    def view_player_stats(self):
        """View stats for each current player."""
        the_game.screen.fill(settings.black)
        
        self.player_1.y = 75
        self.player_2.y = 400

        for player in self.players:
            player_stats = tracking['player_stats'][f'{player}']
            total_games = player_stats['total_games']
            total_tournaments = player_stats['total_tournaments']
            total_turns = player_stats['total_turns']
            total_rounds = player_stats['total_rounds']
            games_won = player_stats['total_wins']
            games_lost = player_stats['total_losses']
            games_drawn = player_stats['total_draws']
            tournament_wins = player_stats['tournament_wins']

            if not total_games:
                the_game.draw_text(
                    f'No stats for {player} - no games played.', 
                    the_game.screen, screen_rect.width / 2, player.y + 50, 
                    settings.basic_font, settings.menu_text_color
                        ) 
                continue
            the_game.draw_text(
                f'Stats for {player}:', the_game.screen, screen_rect.width / 2,
                player.y, settings.medium_font, settings.menu_text_color
                        )
            the_game.draw_text(
                '--------------------', the_game.screen, screen_rect.width / 2,
                player.y + 20, settings.medium_font, settings.menu_text_color
                        )
            the_game.draw_text(
                f'Total games played - {total_games}', the_game.screen, 
                screen_rect.width / 2, player.y + 50, settings.basic_font,
                settings.menu_text_color
                        )
            try:
                the_game.draw_text(
                    f'Wins: {games_won} - '
                    f'{round(games_won / total_games * 100, 2)}%', 
                    the_game.screen, screen_rect.width / 2, player.y + 80,
                    settings.basic_font, settings.menu_text_color
                        )
            except:
                the_game.draw_text(
                    'Wins: 0 - 0%', the_game.screen, screen_rect.width / 2,
                    player.y + 80, settings.basic_font, settings.menu_text_color
                        )
            try:
                the_game.draw_text(
                    f'Losses: {games_lost} - '
                    f'{round(games_lost / total_games * 100, 2)}%', 
                    the_game.screen, screen_rect.width / 2, player.y + 110,
                    settings.basic_font, settings.menu_text_color
                        )
            except:
                the_game.draw_text(
                    'Losses: 0 - 0%', the_game.screen, screen_rect.width / 2,
                    player.y + 110, settings.basic_font,
                    settings.menu_text_color
                        )
            try:
                the_game.draw_text(
                    f'Draws: {games_drawn} - '
                    f'{round(games_drawn / total_games * 100, 2)}%', 
                    the_game.screen, screen_rect.width / 2, player.y + 140,
                    settings.basic_font, settings.menu_text_color
                        )
            except:
                the_game.draw_text(
                    'Draws: 0 - 0%', the_game.screen, screen_rect.width / 2,
                    player.y + 140, settings.basic_font,
                    settings.menu_text_color
                        )           
            the_game.draw_text(
                f'Average turns per game: '
                f'{round(total_turns / total_games, 1)}', the_game.screen,
                screen_rect.width / 2, player.y + 170, settings.basic_font,
                settings.menu_text_color
                    )
            the_game.draw_text(
                f'Total tournaments played: {total_tournaments}',
                the_game.screen, screen_rect.width / 2, player.y + 200, 
                settings.basic_font, settings.menu_text_color
                    )
            try:                
                the_game.draw_text(
                    'The average number of rounds per tournament: '
                    f'{round(total_rounds / total_tournaments, 1)}',
                    the_game.screen, screen_rect.width / 2, player.y + 230, 
                    settings.basic_font, settings.menu_text_color
                        )
            except:
                the_game.draw_text(
                    'The average number of rounds per tournament: 0',
                    the_game.screen, screen_rect.width / 2, player.y + 230, 
                    settings.basic_font, settings.menu_text_color
                        )
            try:                
                the_game.draw_text(
                    f'Tournaments won: {tournament_wins} - '
                    f'{round(tournament_wins / total_tournaments * 100, 1)}%',
                    the_game.screen, screen_rect.width / 2, player.y + 260, 
                    settings.basic_font, settings.menu_text_color
                        )
            except:
                the_game.draw_text(
                    'Tournaments won: 0 - 0%',
                    the_game.screen, screen_rect.width / 2, player.y + 260, 
                    settings.basic_font, settings.menu_text_color
                        )
        the_game.press_any_key(self.menu_sound)


if __name__ == '__main__':
    connect_4 = Connect4()
    the_game = connect_4.the_game
    settings = the_game.settings
    screen_rect = the_game.screen_rect
    tracking = connect_4.tracking
    connect_4.run_game()