import pygame, sys
from pygame.locals import *

import shinsai

class GUIGame(shinsai.Game):
    """The settings and methods for a game using PyGame"""
    def __init__(self, caption):
        """Initialize a new PyGame game."""
        super().__init__()
        pygame.display.init()
        pygame.display.set_caption(caption)
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
                )
        self.screen_rect = self.screen.get_rect()
        self.x = self.y = -5
        self.card_selected = False

    def check_for_input(self):
        """This checks for user input without waiting for it."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    self.terminate(True)
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    return 'Enter'
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.x, self.y = event.pos

    def wait_for_input(
        self, yesno=False, numbered=False, text=False, enter_prompt=False
            ):
        """This pauses the game to wait for player input."""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: # Pressing ESC quits.
                        return 'Esc'
                    if enter_prompt:
                        if event.key == K_RETURN or event.key == K_KP_ENTER:
                            return 'Enter'
                    if yesno:
                        if event.key == K_y:
                            return 'y'
                        elif event.key == K_n:
                            return 'n'
                    if numbered:
                        if event.key == K_KP1 or event.key == K_1:
                            return 1
                        elif event.key == K_KP2 or event.key == K_2:
                            return 2
                        elif event.key == K_KP3 or event.key == K_3:
                            return 3
                        elif event.key == K_KP4 or event.key == K_4:
                            return 4
                        elif event.key == K_KP5 or event.key == K_5:
                            return 5
                        elif event.key == K_KP6 or event.key == K_6:
                            return 6
                        elif event.key == K_KP7 or event.key == K_7:
                            return 7
                        elif event.key == K_KP8 or event.key == K_8:
                            return 8
                        elif event.key == K_KP9 or event.key == K_9:
                            return 9
                        elif event.key == K_KP0 or event.key == K_0:
                            return 0
                    if text:
                        if event.key == K_RETURN or event.key == K_KP_ENTER:
                            return 'Enter'
                        elif event.key == K_BACKSPACE:
                            return 'Backspace'
                        else:
                            return str(event.unicode)
                    else:
                        return None
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.x, self.y = event.pos
                    return 'button'
                    
    def terminate(self, called=False):
        """This quits pygame and the game.
        
        If it's called from a menu, it thanks the player.
        """
        if called:
            self.screen.fill(self.settings.black)
            self.draw_large_center_text(
                'Thank you for playing!', self.settings.green
                    )
            self.update_display()
            self.wait_for_input()
        pygame.display.quit()
        pygame.font.quit()
        pygame.mixer.quit()    
        sys.exit()

    def update_display(self):
        """Updates the screen."""
        pygame.display.update()

    def draw_text(self, text, surface, x, y, font, color):  
        """Function to get text info."""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (int(x), int(y))
        surface.blit(textobj, textrect)

    def draw_bottom_text(self, text, color):
        """Draw text at the bottom of the screen."""
        self.draw_text(
            text, self.screen, self.screen_rect.width / 2, 
            self.screen_rect.height - 50, self.settings.basic_font, color
                )
    
    def draw_heading_text(self, text, color):
        """Draw heading text."""
        self.draw_text(
            text, self.screen, self.screen_rect.width /2,
            100, self.settings.large_font, color
        )

    def draw_center_text(self, text, color):
        """Draw text in the center of the screen."""
        self.draw_text(
            text, self.screen, self.screen_rect.width / 2, 
            self.screen_rect.height / 2, self.settings.basic_font, color
                )

    def draw_large_center_text(self, text, color):
        """Draw text in the center of the screen with large font."""
        self.draw_text(
            text, self.screen, self.screen_rect.width / 2, 
            self.screen_rect.height / 2, self.settings.large_font, color
                )

    def pause_game(self, seconds=0.5):
        """Pause the game briefly."""
        pygame.time.wait(int(seconds * 1000))

    def gather_names(self, num_players=1):
        """Gathers names for the number of human players.
        Returns player name if 1 player, 'players' list if more than.

        Example:
        players = gather_names(3)
        player_1 = players[0]
        player_2 = players[1]
        player_3 = players[2]
        """
        players = []
        
        for player in range(num_players):       
            finished = False
            name = ''
            while not finished:
                self.screen.fill(self.settings.black)
                self.draw_text(
                    f"What is your name? (start typing)", self.screen, 
                    self.screen_rect.left + self.screen_rect.width / 2, 
                    self.screen_rect.height / 2 - 100, 
                    self.settings.large_font, self.settings.green
                        )  
                self.draw_text(
                    name, self.screen, self.screen_rect.width / 2, 
                    self.screen_rect.height / 2, self.settings.medium_font,
                    self.settings.red
                        )
                self.update_display()
                pressed = self.wait_for_input(text=True)
                if pressed == 'Enter':
                    finished = True
                elif pressed == 'button':
                    name = name
                elif pressed == 'Backspace':
                    name = name[:-1]
                elif pressed == 'Esc':
                    finished = True
                    return None
                elif pressed != None:
                    name += pressed
            players.append(name)

        if len(players) == 1:
            return players[0]
        else:
            return players

    def create_sound(self, sound_file):
        """Set up a sound to play."""
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_file)
        return sound
     
    def play_sound(self, sound):
        """Play a sound."""
        sound.play()

    def draw_line(self, surface, start_pos, end_pos, width=1, color=(0,0,0)):
        """Draw a line."""
        pygame.draw.line(surface, color, start_pos, end_pos, width)

    def yes_no_buttons(
        self, text, game, text_color, button_color, button_text_color,
        background_color=None, bottom_text=None, new_screen=True
            ):
        """Screen with Yes and No buttons.
        Returns what was pressed.
        """
        if new_screen:
            self.screen.fill(background_color)
        self.draw_text(
            text, self.screen, self.screen_rect.width / 2, 
            self.screen_rect.height / 2 - 100, self.settings.large_font,
            text_color
                )
        yes_button = Button(
            game, "(Y)es", button_color, button_text_color, 100, 
            coords=(
                self.settings.screen_width / 2 - 100, 
                self.settings.screen_height / 2
                    )
            )
        no_button = Button(
            game, "(N)o", button_color, button_text_color, 100,
            coords=(
                self.settings.screen_width / 2 + 100, 
                self.settings.screen_height / 2
                    )
                )
        Button.draw_button(yes_button)
        Button.draw_button(no_button)
        if bottom_text:
            self.draw_bottom_text(
                bottom_text, self.settings.green
                    )
        self.update_display()
        while True:
            pressed = self.wait_for_input(yesno=True)
            if pressed == 'Esc':
                return 'Esc'
            if pressed == 'y' or yes_button.rect.collidepoint(game.x, game.y):
                return 'y'
            if pressed == 'n' or no_button.rect.collidepoint(game.x, game.y):
                return 'n'
    
    def press_any_key(self, sound, message='Press any key.'):
        """Displays at the bottom of the screen and waits for input."""
        self.draw_bottom_text(message, self.settings.green)
        self.update_display()
        self.wait_for_input()
        self.play_sound(sound)


class Settings:
    """The settings for the game."""
    def __init__(self):
        pygame.font.init()
        self.screen_width, self.screen_height = 1200, 800

        self.track_file = 'tracking.json'
        
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.lightblue = (8, 167, 236)
        self.grey = (128, 128, 128)

        self.small_font = pygame.font.SysFont(None, 30)
        self.basic_font = pygame.font.SysFont(None, 30)
        self.medium_font = pygame.font.SysFont(None, 50)
        self.large_font = pygame.font.SysFont(None, 75)


class Button:
    """Creates a button."""
    def __init__(
        self, game, msg=None, color=(128, 128, 128), font_color=(0,0,0),
        width=200, height=50, coords=(0, 0)
            ):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.x, self.y = coords
        self.x -= width / 2
        self.y -= height / 2
        self.width, self.height = width, height
        self.button_color = (color)
        self.text_color = (font_color)
        self.font = pygame.font.SysFont(None, 48)
        self.text = msg

        # Build the buttons rect object.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
         
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
                )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def __str__(self):
        """Shows the button text."""
        return self.text


class Images:
    """Adapted from SpriteSheet from Beyond PCC
    
    https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
    """
    def __init__(self, game, filename):
        """Load the spritesheet or image."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f'Unable to load spritesheet/image: {filename}')
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(
                rect[0] + rect[2] * x, rect[1], rect[2], rect[3]
                    ) for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(
        self, num_rows, num_cols, 
        x_margin=0, x_padding=0,
        y_margin=0, y_padding=0
            ):
        """Load a grid of images.
        x_margin is space between top of sheet and top of first row.
        x_padding is space between rows.
        Assumes symmetrical padding on left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images.
        """
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two
        # margins, and the padding between each row, then divide by
        # num_cols. Same reasoning for y.
        x_sprite_size = (
            sheet_width - 2 * x_margin - (num_cols - 1) * x_padding 
                ) / num_cols
        y_sprite_size = (
            sheet_height - 2 * y_margin - (num_rows - 1) * y_padding
                ) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                # and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)
            
        grid_images = self.images_at(sprite_rects)
        # print(f'Loaded {len(grid_images)} grid images.')
        # Uncomment prior line for initial testing purposes.

        return grid_images

    def display_image(self, image, image_rect, image_x=0, image_y=0):
        """Displays the image on the screen."""
        image_rect.left, image_rect.top = image_x, image_y
        self.screen.blit(image, image_rect)


class GUIDeck(shinsai.Deck):
    """A class representing a deck of cards updated for PyGame."""
    def __init__(self, card_set):
        """Initialize a new PyGame game."""
        super().__init__()
        self.card_set = card_set

    def build_decks(self, num_decks, add_jokers=False):
        """Builds a deck from specified number of decks of cards and 
        shuffles it.
        """
        cards = []
        for deck in range(num_decks):
            for card in self.card_set.cards:
                cards.append(card)
        self.shuffle_deck(cards)
        return cards