


class WinnerCalculator():
	
	def __init__(self, players, community):
		self.players = players
		self.community = community
		self.winning_hand = ''
		self.winners = []
		self.scores = []
		self.best_score_per_player = {}
		self.check()


	def check(self):
		self.get_best_hands()
		self.compare()


	def compare(self):
		best_hands = dict(sorted(list(self.best_score_per_player.items()), key = lambda x: x[1])[::-1])
		best_score = list(best_hands.values())[0]
		print(best_hands)
		for player, score in list(best_hands.items()):
			if score == best_score:
				self.winners.append(player)
				self.scores.append(score)
		


	def print_winners(self):
		score_hand_dict = {10 : 'Royal Flush',
						9 : 'Straight Flush',
						8 : 'Four of a Kind',
						7 : 'Full House',
						6 : 'Flush',
						5 : 'Straight',
						4 : 'Three of a Kind',
						3 : 'Two Pair',
						2 : 'One Pair',
						1 : 'High Card'}

		print(score_hand_dict[sorted(list(self.best_score_per_player.values()))[-1] // 14])
		for winner, score in list(zip(self.winners, self.scores)):
			print(winner.name, winner.hand, score)
		print(self.community)



	def get_best_hands(self, players = None):
		if not players:
			players = self.players

		for player in players:
			self.high_card(player)
			self.one_pair(player)
			self.two_pair(player)
			self.three_of_a_kind(player)
			self.straight(player)
			self.flush(player)
			self.full_house(player)
			self.four_of_a_kind(player)
			self.straight_flush(player)
			self.royal_flush(player)
		



	def royal_flush(self, player):
		best_hand = self._suit_dict(player)
		for suit in best_hand:
			if sorted(best_hand[suit]) == [10, 11, 12, 13, 14]:
				self.best_score_per_player[player] = 10 * 14 
				self.winning_hand = 'Royal Flush'
				return


	def straight_flush(self, player):
		best_hand = self._suit_dict(player)
		for suit in best_hand:
			straight = self._check_straight(best_hand[suit])
			if straight:
				self.best_score_per_player[player] = 9 * 14 + straight - 1
				self.winning_hand = 'Straight Flush'
				return


	def four_of_a_kind(self, player):
		best_hand = self._value_dict(player)
		for value in best_hand:
			if len(best_hand[value]) == 4:
				self.best_score_per_player[player] = 8 * 14 + value - 1
				self.winning_hand = 'Four of a Kind'
				return

	def full_house(self, player):
		best_hand = self._value_dict(player)
		has_3 = False
		has_2 = False
		biggest_value = 0
		for value in best_hand:
			if len(best_hand[value]) >= 3:
				if not has_3:
					has_3 = True
				else:
					has_2 = True
				if value > biggest_value:
					biggest_value = value
			elif len(best_hand[value]) >= 2:
				has_2 = True

		if has_3 and has_2:
			self.best_score_per_player[player] = 7 * 14 + biggest_value - 1
			self.winning_hand = 'Full House'
			return


	def flush(self, player):
		best_hand = self._suit_dict(player)
		for suit in best_hand:
			if len(best_hand[suit]) == 5:
				self.best_score_per_player[player] = 6 * 14 + max(best_hand[suit]) - 1
				self.winning_hand = 'Flush'
				return



	def straight(self, player): # 
		values = [card.int_value for card in player.hand + self.community]
		straight = self._check_straight(values)
		if straight:
			self.best_score_per_player[player] = 5 * 14 + straight - 1
			self.winning_hand = 'Straight'
			return



	def three_of_a_kind(self, player):
		best_hand = self._value_dict(player)
		for value in best_hand:
			if len(best_hand[value]) == 3:
				self.best_score_per_player[player] = 4 * 14 + value - 1
				self.winning_hand = 'Three of a Kind'
				return



	def two_pair(self, player):
		best_hand = self._value_dict(player)
		has_two = False
		for value in best_hand:
			if len(best_hand[value]) == 2:
				if has_two:
					self.best_score_per_player[player] = score 
					self.winning_hand = 'Two Pair'
					return
				has_two = True
				score = 3 * 14 + value - 1


	def one_pair(self, player):
		best_hand = self._value_dict(player)
		for value in best_hand:
			if len(best_hand[value]) == 2:
				self.best_score_per_player[player] = 2 * 14 + value - 1
				self.winning_hand = 'One Pair'
				return

	def high_card(self, player):
		self.best_score_per_player[player] = 1 * 14 + max([card.int_value for card in player.hand + self.community]) - 1
		self.winning_hand = 'High Card'
		return



	def _value_dict(self, player):
		suits = [card.suit for card in player.hand]
		values = [card.int_value for card in player.hand]
		best_hand = {}
		for suit, value in list(zip(suits, values)):
			if value in best_hand:
				best_hand[value].append(suit)
			else:
				best_hand[value] = [suit]
		for card in self.community:
			if card.int_value in best_hand:
				best_hand[card.int_value].append(card.suit)
			else:
				best_hand[card.int_value] = [card.suit]
		best_hand = dict(sorted(list(best_hand.items()), key = lambda x: x[0])[::-1])
		return best_hand



	def _suit_dict(self, player):
		suits = [card.suit for card in player.hand]
		values = [card.int_value for card in player.hand]
		best_hand = {}
		for suit, value in list(zip(suits, values)):
			if suit in best_hand:
				best_hand[suit].append(value)
			else:
				best_hand[suit] = [value]
		for card in self.community:
			if card.suit in best_hand:
				best_hand[card.suit].append(card.int_value)
			else:
				best_hand[card.suit] = [card.int_value]
		return best_hand



	def _check_straight(self, values):
		prev_value = 0
		in_a_row = 1
		straight = []
		if 14 in values:
			values.append(1)
		values = sorted(values)
		for value in values:
			if value - prev_value == 1:
				in_a_row += 1
				straight.append(value)
				if in_a_row == 5:
					return max(straight)
			elif value != prev_value:
				in_a_row = 1
			prev_value = value
		return False


if __name__ == '__main__':
	from cards import Card 
	from player import Player

	player1 = Player("Bob", 1)
	card1 = Card("clubs", 8)
	card2 = Card("diamonds", 6)
	player1.hand = [card1, card2]



	player2 = Player("Mel", 1)
	card9 = Card("clubs", 5)
	card8 = Card("diamonds", 6)
	player2.hand = [card9, card8]

	card3 = Card("clubs", 4)
	card4 = Card("hearts", 3)
	card5 = Card("diamonds", 2)
	card6 = Card("diamonds", 7)
	card7 = Card("clubs", 5)

	community = [card3, card4, card5, card6, card7]

	calc = WinnerCalculator([player1, player2], community)
	calc.print_winners()





