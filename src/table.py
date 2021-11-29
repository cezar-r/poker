import random
import os
import time

from deck import Deck
from player import Player
from winner_calculator import WinnerCalculator


class Table:

	def __init__(self, players, deck, buyin):
		self.players = players
		for player in self.players:
			player.buyin(buyin)
			player.players_in_hand = len(players)
		self.players_in_hand = players
		self._cards = self._init_deck(deck)
		self.pot_value = 0
		self.big_blind_position = 0
		self.community_cards = []
		self.big_blind_amount = buyin // 1000
		self.little_blind_amount = self.big_blind_amount // 2
		self.call_amount = self.big_blind_amount
		self.turn = "Pre-Flop"
		self.prev_player = Player("doe")
		self.prev_player_decision = ["", ""]
		self.games = 0

	def play(self):
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

		# first round of betting // pre-flop
		self._bet(first_to_go)
		if len(self.players_in_hand) == 1:
			self._reset_table()
			return

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
		if len(self.players_in_hand) == 1:
			self._reset_table()
			return

		# turn
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.turn = "Turn"
		self.display()

		# fourth round of betting // post-turn
		self._bet(first_to_go)
		if len(self.players_in_hand) == 1:
			self._reset_table()
			return

		# river 
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.turn = "River"
		self.display()

		# fifth round of betting // post-river
		self._bet(first_to_go)
		if len(self.players_in_hand) == 1:
			self._reset_table()
			return

		self._reset_table(done=True)
		self.games += 1

	def _reset_table(self, done = False):
		self.display(done = done)
		if done:
			self.calculate_winner() 
		else:
			self.calculate_winner(verbose = False)
		self.reset_players()
		self.turn = "Pre-Flop"
		self.prev_player = Player("doe")
		self.prev_player_decision = ["", ""]
		self.games += 1

	def reset_players(self):
		for player in self.players:
			if player.amount < self.little_blind_amount: # player busted
				del self.players[self.players.index(player)]
			else:
				player.reset() 

	def play_again(self):
		if self._humanCount() == 0:
			# play_again = input(f"Play again? [Y][N]\n")
			play_again = 'y'
			time.sleep(3)
			if play_again =='y':
				return
			else:
				exit()
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
			player.cur_board = self.community_cards
			self.display(player)
			if player.amount > 10:
				decision = player.decision(self.call_amount)
				if decision[0] == 'raise':
					amount = decision[1]
					if player.is_bot and amount < 2 * prev_raise:
						amount = 2 * prev_raise
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
				self.prev_player = player
				self.prev_player_decision = decision
				if len(self.players_in_hand) == 1:
						return

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
			if player.amount < 10:
				del self.players[self.players.index(player)]

	def _remove_player(self, name):
		for i in range(len(self.players_in_hand) - 1):
			if self.players_in_hand[i].name == name:
				del self.players_in_hand[i]

	def calculate_winner(self, verbose = True):
		calculator = WinnerCalculator(self.players_in_hand, self.community_cards, verbose)
		for winner in calculator.winners:
			winner.amount += self.pot_value / len(calculator.winners)
			self._update_meta_player(winner.name, winner.amount)

	def _resort_players(self, i, players = None):
		if not players:
			return self.players_in_hand[i:] + self.players_in_hand[:i]
		else:
			return players[i:] + players[:i]

	def move_blinds(self):
		self._reset_blinds()

		if self.big_blind_position >= len(self.players) - 1:
			self.big_blind_position = 0
		else:
			self.big_blind_position += 1

		self.players[self.big_blind_position].is_big_blind = True

		if self.big_blind_position == len(self.players) - 1:
			self.players[0].is_little_blind = True
		else:
			self.players[self.big_blind_position + 1].is_little_blind = True

	def _reset_blinds(self):
		for player in self.players:
			if player.is_big_blind:
				player.is_big_blind = False
			if player.is_little_blind:
				player.is_little_blind = False

	def _init_deck(self, deck):
		return deck.cards

	def _humanCount(self, arr = []):
		if arr == []:
			arr = self.players
		count = 0
		for player in arr:
			if not player.is_bot:
				count += 1
		return count

	def display(self, cur_player = Player("doe"), odds = False, arr = [], prev_player = [Player("doe"), ["", ""]], done = False):
		if not cur_player.is_bot and cur_player.name != "":
			if self._humanCount() > 1:
				self.look_away(cur_player)
		if odds:
			# self.update_odds() -> need new odds function
			pass

		os.system('cls' if os.name == 'nt' else 'clear')
		print("Game", self.games + 1)
		print(f"Pot value: {self.pot_value} ({self.turn})")
		if self.prev_player.name != "":
			print(self.prev_player.name, self.prev_player_decision[0] + "s", "$" + str(self.call_amount))
		else:
			print()
		print()
		for player in self.players_in_hand:
			if player.name == cur_player.name:
				print("●", player, "-", "$" + str(player.amount))
			else:
				print(player, "-", "$" + str(player.amount))
			if player.name == cur_player.name and not player.is_bot:
				for card in player.hand: 
					print(card)
			elif (self._humanCount(self.players_in_hand) == 0 and len(self.players_in_hand) > 1) or (len(self.players_in_hand) == 1 and player.play_bluff) or done:
				for card in player.hand: 
					print(card)
			else:
				print('** ********\n** ********')
			print()
		print("Board: ", end = "")
		for card in self.community_cards:
			print(card, end = " ")
		print('\n')
		if not done and len(self.players_in_hand) == 1:
			print("Winner:", self.players_in_hand[0].name, "\n")

	def look_away(self, cur_player):
		os.system('cls' if os.name == 'nt' else 'clear')
		print(f"Everyone but {cur_player.name} look away")
		input("Press any key to continue")

