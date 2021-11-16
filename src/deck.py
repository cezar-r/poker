from cards import SUITS, VALUES, Card


class Deck:

	def __init__(self):
		self.cards = self._init_cards()

	def _init_cards(self):
		cards = []
		for suit in SUITS:
			for value in VALUES:
				cards.append(Card(suit, value))
		return cards