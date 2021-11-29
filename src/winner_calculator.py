 
from deck import Deck
from itertools import permutations

deck = Deck()
deck.shuffle()
deck = deck.cards

class WinnerCalculator():
	
	def __init__(self, players, community, verbose = True):
		self.players = players
		self.community = community
		self.winning_hand = ''
		self.winners = []
		self.scores = []
		self.best_score_per_player = {}
		self.verbose = verbose
		self.check()


	def check(self):
		self.get_best_hands()
		self.compare()
		if self.verbose:
			self.print_winners()


	def compare(self):
		best_hands = dict(sorted(list(self.best_score_per_player.items()), key = lambda x: x[1])[::-1])
		best_score = list(best_hands.values())[0]
		if self.verbose:
			print("Scores:")
			print(best_hands, "\n")
		self.player_scores = best_hands
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

		# print(list(self.best_score_per_player.values()))

		self.winning_hand = score_hand_dict[sorted(list(self.best_score_per_player.values()))[-1] // 14]
		if self.verbose:
			for winner, score in list(zip(self.winners, self.scores)):
				print("Winner:" + "\n" + winner.name, winner.hand)
			print("Board:", self.community)
			print(self.winning_hand)
			print()



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
		values = []
		for value in best_hand:
			if len(best_hand[value]) == 2:
				if has_two:
					self.best_score_per_player[player] = score + round(value / 14, 2)
					self.winning_hand = 'Two Pair'
					break
				has_two = True
				score = 3 * 14 + value - 1
		if has_two:
			for value in best_hand:
				if len(best_hand[value]) == 1:
					self.best_score_per_player[player] += (value - 1) / 1400
					return


	def one_pair(self, player):
		best_hand = self._value_dict(player)
		score = 0
		has_pair = False
		for value in best_hand:
			if len(best_hand[value]) == 2:
				self.best_score_per_player[player] = 2 * 14 + value - 1
				self.winning_hand = 'One Pair'
				has_pair = True
				break
		num_cards = 0
		if has_pair:
			for value in best_hand:
				if len(best_hand[value]) == 1 and num_cards <= 2:
					num_cards += 1
					self.best_score_per_player[player] += (value-1) / 390
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
		prev_value = -1
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



class OddsCalculator:

	def __init__(self, players, board, deck):
		self.players = players
		self.board = board
		self.deck = deck

	def calculate_odds(self):

		burned = [card for player in self.players for card in player.hand] + [card for card in self.board]

		# # to calculate only from its own hand
		# if len(self.players) == 1:
		# 	self._simulate_all_other_hands()

		# to calculate everyones
		# else:
		combinations = self.create_combinations()
		wins = {}
		hand_scores = {}
		for hand in combinations:
			calculator = WinnerCalculator(self.players, hand, verbose = False)
			scores = calculator.player_scores
			winner = list(scores.keys())[0]
			if winner in wins:
				wins[winner] += 1
			else:
				wins[winner] = 1
			if winner in hand_scores:
				hand_scores[winner].append(list(scores.values())[0])
			else:
				hand_scores[winner] = [list(scores.values())[0]]
		for player in self.players:
			if player not in list(wins.keys()):
				wins[player] = 0
		self.scores = hand_scores
		self.odds = dict([(name, round(win/(sum(list(wins.values()))), 2)) for name, win in list(wins.items())])


	def create_combinations(self):
		deck_copy = self.deck.copy()
		board_copy = self.board.copy()
		if len(board_copy) == 5:
			return [board_copy]
		combinations = []
		for comb in permutations(deck_copy, 5 - len(board_copy)):
			for card in comb:
				board_copy.append(card)
			combinations.append(board_copy)
			board_copy = self.board.copy()
		return combinations
			
	def _create_combinations(self, board, deck, boards = []):
		if len(deck) == 0:
			return [board]
		if len(deck) < (5 - len(self.board)):
			return boards
		temp_board = self.board.copy()
		# for i in range(5 - len(self.board)):
		temp_board.append(deck[0])
		# boards.append(temp_board)
		return self._create_combinations(temp_board, deck[1:], boards)


def create_board():
	board = []
	for i in range(3):
		board.append(deck[0])
		del deck[0]
	return board


def create_players(num_players):
	players = []
	for i in range(num_players):
		players.append(Player())
	for player in players:
		player.hand = [deck[0], deck[1]]
		del deck[0]
		del deck[0]
	return players


def print_odds(players, board):
	odds = OddsCalculator(players, board, deck)
	odds.calculate_odds()
	_odds = odds.odds
	if len(board) == 3:
		print("Flop")
	elif len(board) == 4:
		print("Turn")
	elif len(board) == 5:
		print("River")
	for player in _odds:
		for player1 in players:
			if player.name == player1.name:
				print(player.name, player.hand, ":", _odds[player])
	print("\n", "Board: ", board, "\n")
	print("------------------\n")


if __name__ == '__main__':
	from player import Player

	players = create_players(2)
	board = create_board()

	print_odds(players, board)
	board.append(deck[0])
	del deck[0]


	print_odds(players, board)
	board.append(deck[0])
	del deck[0]


	print_odds(players, board)



'''
BOARDS TO TEST

 A 8 
 2 K
 A Q Q Q


3 4
4 9 4 2 A -> should not be straight

 '''