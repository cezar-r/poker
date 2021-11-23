from cards import SUITS, VALUES, Card
import random


class Deck:

	def __init__(self):
		self.cards = self._init_cards()

	def _init_cards(self):
		cards = []
		for suit in SUITS:
			for value in VALUES:
				cards.append(Card(suit, value))
		return cards

	def shuffle(self):
		random.shuffle(self.cards)


	def reset(self):
		self.cards = self._init_cards()

