'''
Card
	.name
	.suit
	.value
Player()
	.name
	.hand # list of cards
	.amount
	.decision()
	.raise()
	.call()
	.fold()
	.is_big_blind()
	.is_little_blind()
Deck
	cards[]
	burned_cards[]
	.reshuffle()
Table
	.deck # private
	players[]
	.pot_value
	.check_winner()
	.deal()






deck = Deck() # initalize list of cards

player1 = Player("Bob")
player2 = Player("Joe")

table = Table([player1, player2], deck)

while len(table.players > 2):
	table.play() # each player gets dealt cards from the deck




class Table:

	def __init__(self, players, deck):
		self.players = players
		self.players_in_hand = players
		self._cards = self._init_deck(deck)
		self.pot_value = 0
		self.big_blind_position = 0
		self.community_cards = []
		self.call_amount = BIG_BLIND_AMOUNT

	def _init_deck(self):
		cards = []
		for card in list(zip(CARD_VALUE, SUIT)):
			cards.append(card)
		return cards

	def play(self):
		self.community_cards = []
		self.move_blinds()
		self.players_in_hand = self.players
		cards = self.shuffle()
		self.pot_value = BIG_BLIND_AMOUNT + SMALL_BLIND_AMOUNT

		# deal cards
		for player in self.players_in_hand:
			if player.is_big_blind:
				player.amount -= BIG_BLIND_AMOUNT
			elif player.is_little_blind:
				player.amount -= LITTLE_BLIND_AMOUNT
			player.hand.append(cards[0])
			remove card from cards
		for player in self.players_in_hand:
			player.hand.append(cards[1])
			remove card from cards

		# first round of betting // pre-flop
		first_to_go = self.big_blind_position + 2
		if first_to_go > len(self.players):
			first_to_go = 0

		self._bet(first_to_go)

		# flop
		remove first card from deck
		for i in range(3):
			self.community_cards.append(cards[i])
			remove ith card

		# secound round of betting // post-flop
		self._bet(first_to_go)

		# turn
		remove first card from deck
		self.community_card.append(cards[0])
		remove 0th card from cards

		# fourth round of betting // post-turn
		self._bet(first_to_go)

		# river 
		remove first card from deck
		self.community_card.append(cards[0])
		remove 0th card from cards

		# fifth round of betting // post-river
		self._bet(first_to_go)

		self.calculate_winner()


	def _bet(self, i):
		betting_list = self._resort_players(i)
		for player in betting_list:
			decision = player.decision()
			if decision[0] == 'raise':
				amount = decision[1]
				self.pot_value += amount
				self.call_amount = amount
				player.amount -= amount
			elif decision[0] == 'call':
				self.pot_value += self.call_amount
				player.amount -= self.call_amount
			else:
				remove player from self.players_in_hand
		self.call_amount = 0
	
	
	def calculate_winner(self, ):
		winner = self._find_winner(self.players_in_hand)
		winner.amount += self.pot_value

	
	def _resort_players(self, i):
		return self.players_in_hand[i:] + self.players_in_hand[:i]
	

	def move_blinds(self):
		self.players[self.big_blind_position].is_big_blind = False
		self.players[self.big_blind_position + 1].is_little_blind = False

		if self.big_blind_position >= len(self.players - 1):
			self.big_blind_position = 0
		else:
			self.big_blind_position += 1

		self.players[self.big_blind_position].is_big_blind = True
		self.players[self.big_blind_position + 1].is_little_blind = True
	

	def shuffle(self):
		# randomize list of self._cards, return list
	

	def _rotate_blinds(self):


	def _init_deck(self):
		return deck.cards

'''