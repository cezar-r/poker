#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File containing the table object"""
import random
import os
import time

from deck import Deck
from player import Player
from winner_calculator import WinnerCalculator


class Table:
	"""
	A class representing the table
	
	Attributes
	----------
	players : list
		List of all players in game
	players_in_hand : list
		List of players in current game
	_cards : list
		List of cards representing the deck
	pot_value : int
		Amount of money in pot
	big_blind_position : int
		Position of big blind
	community_cards : list
		List of cards on board
	big_blind_amount : int
		Amount the big blind is
	little_blind_amount : int
		Amount the little blind is
	call_amount : int
		Amount players need to call
	turn : str
		Current turn of the game
	prev_player : Player()
		previous player in the turn
	prev_player_decision : list
		Represents the previous players decision ([Decision, Amount raised])
	games : int
		Number of games played
	"""

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
		"""Method that plays each turn"""
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
		"""Method that resets the table back to the initial state"""
		self.display(done = done)
		if done:
			self.calculate_winner() 
		else:
			self.calculate_winner(verbose = False)
		self._reset_players()
		self.turn = "Pre-Flop"
		self.prev_player = Player("doe")
		self.prev_player_decision = ["", ""]
		self.games += 1

	def _reset_players(self):
		"""Method that resets all players to their initial state"""
		for player in self.players:
			if player.amount < self.little_blind_amount: # player busted
				del self.players[self.players.index(player)]
			else:
				player.reset() 

	def play_again(self):
		"""Method that checks to see if all players want to play again"""
		if self._humanCount() == 0:
			# play_again = input(f"Play again? [Y][N]\n")
			play_again = 'y'
			time.sleep(10)
			if play_again =='y':
				return
			else:
				exit()
		new_players = []
		for player in self.players:
			play_again = player.play_again()
			if play_again:
				if play_again == 'a':
					return 
				new_players.append(player)
		self.players = new_players


	def _bet(self, i: int):
		"""
		Method that plays a round of betting
		
		Parameters
		----------
		i : int
			Represents the first player to go in the turn
		"""
		betting_list = self._resort_players(i)
		to_call = betting_list.copy()
		i = 0
		prev_raise = 0
		while len(to_call) > 0:
			player = to_call[0]
			player.cur_board = self.community_cards
			self.display(player)
			if player.amount == 0:
				del to_call[0]
			if player.amount > 10:
				decision = player.decision(self.call_amount)
				if decision[0] == 'raise':
					amount = decision[1]
					if player.amount < self.call_amount and amount < 2 * prev_raise:
						amount = player.amount
						self.pot_value += amount
						player.amount -= amount
						player.put_in += amount
					else:
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
					if self.call_amount > player.amount:
						self.pot_value += player.amount
						player.put_in += player.amount
						player.amount = 0
					else:
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
		"""
		Method that gets the index of the next player 
		
		Parameters
		----------
		name : str
			Name of current player
		array : list
			List of players to bet
		
		Returns
		-------
		int 
			i + 1 if player is not at the end of the table, otherwise 0
		"""
		for i, player in enumerate(array):
			if player.name == name:
				if i == len(array) - 1:
					return 0
				else:
					return i + 1

	def _reset_put_in(self):
		"""Method that resets the amount put in by each player"""
		for player in self.players_in_hand:
			player.put_in = 0

	def _update_meta_player(self, name, amount):
		"""
		Method pdates the amount in each player
		
		Parameters
		----------
		name : str
			Name of current player
		amount : int
			Amount of money to add to players balance
		"""
		for player in self.players:
			if player.name == name:
				player.amount = amount
			if player.amount < 10:
				del self.players[self.players.index(player)]

	def _remove_player(self, name):
		"""Method that removes a player from the table"""
		for i in range(len(self.players_in_hand) - 1):
			if self.players_in_hand[i].name == name:
				del self.players_in_hand[i]

	def calculate_winner(self, verbose = True):
		"""Method that calculates who the winner is and the winnings they recieve"""
		calculator = WinnerCalculator(self.players_in_hand, self.community_cards, verbose)
		for winner in calculator.winners:
			winner.amount += self.pot_value / len(calculator.winners)
			self._update_meta_player(winner.name, winner.amount)

	def _resort_players(self, i, players = None):
		"""
		Method that resorts the betting order of the players
		
		i : int
			index of current player
		players : list
			List of players in hand
		"""
		if not players:
			return self.players_in_hand[i:] + self.players_in_hand[:i]
		else:
			return players[i:] + players[:i]

	def move_blinds(self):
		"""Method that moves the blind positions"""
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
		"""Method that resets blind attributes for players"""
		for player in self.players:
			if player.is_big_blind:
				player.is_big_blind = False
			if player.is_little_blind:
				player.is_little_blind = False

	def _init_deck(self, deck):
		"""Method that initalizes the deck"""
		return deck.cards

	def _humanCount(self, arr = []):
		"""
		Method that counts how many real players are in the hand
		
		Parameters
		----------
		arr : list
			List of players in hand
		
		Returns
		-------
		int
			Number of real players in hand
		"""
		if arr == []:
			arr = self.players
		count = 0
		for player in arr:
			if not player.is_bot:
				count += 1
		return count

	def display(self, cur_player = Player("doe"), odds = False,  prev_player = [Player("doe"), ["", ""]], done = False):
		"""
		Method that displays the game
		
		Parameters
		----------
		cur_player : Player()
			Current player in turn
		odds : bool
			Whether or not to display odds
		prev_player : List
			List that contains previous player and previous decision
		done : bool
			Whether or not the hand got to showdown
		"""
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
		"""Method that tells a real player to look away from the screen when it is the other players turn"""
		os.system('cls' if os.name == 'nt' else 'clear')
		print(f"Everyone but {cur_player.name} look away")
		input("Press any key to continue")

