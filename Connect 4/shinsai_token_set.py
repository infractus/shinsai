from shinsai_pygame import Images

"""Module for a set of tokens, and images of tokens in various state."""

class TokenSet:
	"""Represents a set of tokens for Connect 4.

	Each token is an object of the Token class.
	"""
	def __init__(self, game):
		"""
		Initialize attributes to represent the overall set of tokens.
		"""
		self.game = game
		self._load_tokens()
		
	def _load_tokens(self):
		"""Builds the overall set.

		- Loads images from the sprite sheet.
		- Creates a Token object for each token type, and sets
			appropriate attributes for that token.
		- Adds each token to the list self.tokens.
		"""
		filename = 'images/connect_4_sprite_sheet.png'
		token_ss = Images(self.game, filename)

		# Load all card images.
		token_images = token_ss.load_grid_images(4, 3)

		# Creates the Token objects, assigns names, images and rects.
		self.empty = Token(self.game)
		self.empty.name = 'empty'
		self.empty.image = token_images[0]
		self.empty.rect = self.empty.image.get_rect()

		self.player1 = Token(self.game)
		self.player1.name = 'player1'
		self.player1.image = token_images[1]
		self.player1.rect = self.player1.image.get_rect()
		
		self.player2 = Token(self.game)
		self.player2.name = 'player2'
		self.player2.image = token_images[2]
		self.player2.rect = self.player2.image.get_rect()
		
		self.player1lastplayed = Token(self.game)
		self.player1lastplayed.name = 'player1lastplayed'
		self.player1lastplayed.image = token_images[-2]
		self.player1lastplayed.rect = self.player1lastplayed.image.get_rect()

		self.player2lastplayed = Token(self.game)
		self.player2lastplayed.name = 'player2lastplayed'
		self.player2lastplayed.image = token_images[-1]
		self.player2lastplayed.rect = self.player2lastplayed.image.get_rect()

		# A falling token takes on the image of the player's token.
		self.falling_token = Token(self.game)
		self.falling_token.name = 'falling_token'
		self.falling_token.rect = self.empty.image.get_rect()

class Token:
	"""Represents a token."""
	def __init__(self, game):
		"""Initialize attributes to represent a token."""
		self.image = None
		self.name = ''
		self.screen = game.screen
		self.x, self.y = 0.0, 0.0

	def blitme(self):
		"""Draw a token."""
		self.rect = self.image.get_rect()
		self.rect.topleft = self.x, self.y
		self.screen.blit(self.image, self.rect)

	def __str__(self):
		"""Returns the name attribute of the token."""
		return self.name