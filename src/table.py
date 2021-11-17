import random
import os

# from poker import Range 
# from poker.hand import Combo

# import holdem_calc
# import holdem_functions

from deck import Deck
from player import Player
from winner_calculator import WinnerCalculator


class Table:

	def __init__(self, players, deck, buyin):
		self.players = players
		for player in self.players:
			player.buyin(buyin)
		self.players_in_hand = players
		self._cards = self._init_deck(deck)
		self.pot_value = 0
		self.big_blind_position = 0
		self.community_cards = []
		self.big_blind_amount = buyin // 100
		self.little_blind_amount = self.big_blind_amount // 2
		self.call_amount = self.big_blind_amount
		self.turn = "Pre-Flop"


	def play(self):
		self.display()
		self.community_cards = []
		self.move_blinds()
		self.players_in_hand = self.players.copy()
		cards = self._cards.copy()
		random.shuffle(cards)
		self.call_amount = self.big_blind_amount
		self.pot_value = self.big_blind_amount + self.little_blind_amount

		# deal cards
		for player in self.players_in_hand:
			if player.is_big_blind:
				player.amount -= self.big_blind_amount
				player.put_in = self.big_blind_amount
				self._update_meta_player(player.name, player.amount)
			elif player.is_little_blind:
				player.amount -= self.little_blind_amount
				player.put_in = self.little_blind_amount
				self._update_meta_player(player.name, player.amount)
			player.hand.append(cards[0])
			del cards[0]
		for player in self.players_in_hand:
			player.hand.append(cards[0])
			del cards[0]

		first_to_go = self.big_blind_position + 2
		if first_to_go > len(self.players):
			first_to_go = 0

		self.display()
		# first round of betting // pre-flop
		self._bet(first_to_go)

		first_to_go -= 1
		if first_to_go < 0:
			first_to_go = 0

		# flop
		del cards[0]
		for i in range(3):
			self.community_cards.append(cards[i])
			del cards[i]

		self.turn = "Flop"
		self.display()

		# secound round of betting // post-flop
		self._bet(first_to_go)

		# turn
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.turn = "Turn"
		self.display()

		# fourth round of betting // post-turn
		self._bet(first_to_go)

		# river 
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.turn = "River"
		self.display()

		# fifth round of betting // post-river
		self._bet(first_to_go)

		self.display()
		self.calculate_winner() 
		self.reset_players()
		self.turn = "Pre-Flop"


	def update_odds(self):
		for player in self.players_in_hand:
			print(player.name, player.hand)
			player.odds = self.calc_odds(player)


	def _format_hand(self, hand):
		hand_str = ''
		for card in hand:
			if card.value[0] == 1:
				hand_str += 'T' + card.suit[0]
			else:
				hand_str += card.value[0] + card.suit[0]
		return Combo(hand_str)


	def _format_board(self, flop = False):
		if not flop:
			flop = self.community_cards
		board = []
		for card in flop:
			if card.value[0] == 1:
				board.append('T' + card.suit[0])
			else:
				board.append(card.value[0] + card.suit[0])
		return board


	def calc_odds(self, player):
		hand = self._format_board(player.hand)
		board = self._format_board()

		print(hand, board)

		odds = holdem_calc.calculate(board, True, 1, False, hand, True)
		print(odds[:-1])
		return odds[:-1]
		# return odds['win']




	def reset_players(self):
		for player in self.players:
			if player.amount < self.little_blind_amount: # player busted
				del self.players[self.players.index(player)]
			else:
				player.reset() 


	def play_again(self):
		new_players = []
		for player in self.players:
			play_again = player.play_again()
			if play_again:
				if play_again == 'a':
					self._play_all()
					return 
				new_players.append(player)
		self.players = new_players

	def _play_all(self):
		new_players = []
		for player in self.players:
			new_players.append(player)
		self.players = new_players

	def _bet(self, i: int):
		betting_list = self._resort_players(i)
		to_call = betting_list.copy()
		i = 0
		prev_raise = 0
		while len(to_call) > 0:
			player = to_call[0]
			print(to_call)
			self.display(player)
			decision = player.decision(self.call_amount)
			if decision[0] == 'raise':
				amount = decision[1]
				assert amount >= 2 * prev_raise
				self.pot_value += amount 
				self.call_amount = amount + player.put_in
				player.amount -= amount 
				player.put_in += amount
				self._update_meta_player(player.name, player.amount)
				to_call = self._resort_players(self._get_next_index(player.name, betting_list), betting_list)[:-1]
				prev_raise = amount
			elif decision[0] == 'call':
				self.pot_value += self.call_amount - player.put_in
				player.amount -= self.call_amount - player.put_in
				player.put_in += self.call_amount - player.put_in
				self._update_meta_player(player.name, player.amount)
				del to_call[0]
			else:
				del self.players_in_hand[self.players_in_hand.index(player)]
				del to_call[0]
				del betting_list[betting_list.index(player)]
			# next_player = to_call[self._get_next_index(player.name, betting_list)]
		self._reset_put_in()
		self.call_amount = 0


	def _get_next_index(self, name, array): 
		for i, player in enumerate(array):
			if player.name == name:
				if i == len(array) - 1:
					return 0
				else:
					return i + 1


	def _reset_put_in(self):
		for player in self.players_in_hand:
			player.put_in = 0


	def _update_meta_player(self, name, amount):
		for player in self.players:
			if player.name == name:
				player.amount = amount


	# def _remove_player(self, name):
	# 	for i in range(len(self.players_in_hand) - 1):
	# 		if self.players_in_hand[i].name == name:
	# 			del self.players_in_hand[i]


	def calculate_winner(self):
		calculator = WinnerCalculator(self.players_in_hand, self.community_cards)
		calculator.print_winners()
		for winner in calculator.winners:
			winner.amount += self.pot_value / len(calculator.winners)
			self._update_meta_player(winner.name, winner.amount)

	
	def _resort_players(self, i, players = None):
		if not players:
			return self.players_in_hand[i:] + self.players_in_hand[:i]
		else:
			return players[i:] + players[:i]


	def move_blinds(self):
		self.reset_blinds()

		if self.big_blind_position >= len(self.players) - 1:
			self.big_blind_position = 0
		else:
			self.big_blind_position += 1

		self.players[self.big_blind_position].is_big_blind = True

		if self.big_blind_position == len(self.players) - 1:
			self.players[0].is_little_blind = True
		else:
			self.players[self.big_blind_position + 1].is_little_blind = True


	def reset_blinds(self):
		for player in self.players:
			if player.is_big_blind:
				player.is_big_blind = False
			if player.is_little_blind:
				player.is_little_blind = False


	def _init_deck(self, deck):
		return deck.cards


	def display (self, cur_player = Player(""), odds = False):
		if odds:
			self.update_odds()
		os.system('cls' if os.name == 'nt' else 'clear')
		print(f"Pot value: {self.pot_value} ({self.turn})\n")
		for player in self.players_in_hand:
			if player.name == cur_player.name:
				print("●", player, "-", player.amount)
			else:
				print(player, "-", player.amount)
			for card in player.hand:
				print(card)
			print()
		print("Board: ", end = "")
		for card in self.community_cards:
			print(card, end = " ")
		print('\n')

