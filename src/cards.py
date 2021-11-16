SUITS = ['clubs', 'hearts', 'spades', 'diamonds']
VALUES = ['2', '3', '4', '5', '6', '7' ,'8', '9', '10', 'J', 'Q', 'K', 'A']


class Card:

	def __init__(self, suit, value):
		self.suit = suit
		self.value = value
		self.int_value = self._calc_value()


	def __str__(self):
		return f'{self.value} {self.suit}'

	def __repr__(self):
		return f'{self.value} {self.suit}'


	def _calc_value(self):
		if self.value == 'J':
			return 11
		elif self.value == 'Q':
			return 12
		elif self.value == 'K':
			return 13
		elif self.value == 'A':
			return 14
		else:
			return int(self.value)
