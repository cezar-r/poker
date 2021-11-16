import random
import os

from deck import Deck
from player import Player
from winner_calculator import WinnerCalculator


BIG_BLIND_AMOUNT = 4
LITTLE_BLIND_AMOUNT = 2


class Table:

	def __init__(self, players, deck):
		self.players = players
		self.players_in_hand = players
		self._cards = self._init_deck(deck)
		self.pot_value = 0
		self.big_blind_position = 0
		self.community_cards = []
		self.call_amount = BIG_BLIND_AMOUNT

	def play(self):
		self.display()
		self.community_cards = []
		self.move_blinds()
		self.players_in_hand = self.players.copy()
		cards = self._cards.copy()
		random.shuffle(cards)
		self.pot_value = BIG_BLIND_AMOUNT + LITTLE_BLIND_AMOUNT

		# deal cards
		for player in self.players_in_hand:
			if player.is_big_blind:
				player.amount -= BIG_BLIND_AMOUNT
				player.put_in = BIG_BLIND_AMOUNT
				self._update_meta_player(player.name, player.amount)
			elif player.is_little_blind:
				player.amount -= LITTLE_BLIND_AMOUNT
				player.put_in = LITTLE_BLIND_AMOUNT
				self._update_meta_player(player.name, player.amount)
			player.hand.append(cards[0])
			del cards[0]
			# remove card from cards
		for player in self.players_in_hand:
			player.hand.append(cards[0])
			del cards[0]
			# remove card from cards

		# first round of betting // pre-flop
		first_to_go = self.big_blind_position + 2
		if first_to_go > len(self.players):
			first_to_go = 0

		self.display()
		self._bet(first_to_go)

		first_to_go -= 1
		if first_to_go < 0:
			first_to_go = 0

		# flop
		del cards[0]
		for i in range(3):
			self.community_cards.append(cards[i])
			del cards[i]
			# remove ith card

		self.display()

		# secound round of betting // post-flop
		self._bet(first_to_go)

		self.display()

		# turn
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.display()

		# fourth round of betting // post-turn
		self._bet(first_to_go)

		# river 
		del cards[0]
		self.community_cards.append(cards[0])
		del cards[0]

		self.display()

		# fifth round of betting // post-river
		self._bet(first_to_go)

		self.calculate_winner() 
		self.reset_players()


	def reset_players(self):
		for player in self.players:
			player.reset()


	def play_again(self):
		new_players = []
		for player in self.players:
			if player.play_again():
				new_players.append(player)
		self.players = new_players


	def _bet(self, i):
		betting_list = self._resort_players(i)
		to_call = betting_list.copy()
		i = 0
		prev_raise = 0
		while len(to_call) > 0:
			player = to_call[0]
			decision = player.decision(self.call_amount)
			if decision[0] == 'raise':
				amount = decision[1]
				assert amount >= 2 * prev_raise
				self.pot_value += amount 
				self.call_amount = amount + player.put_in
				player.amount -= amount 
				player.put_in += amount
				self._update_meta_player(player.name, player.amount)
				to_call = self._resort_players(self._get_index(player.name, betting_list), betting_list)[:-1]
				prev_raise = amount
			elif decision[0] == 'call':
				self.pot_value += self.call_amount - player.put_in
				player.amount -= self.call_amount - player.put_in
				player.put_in += self.call_amount - player.put_in
				self._update_meta_player(player.name, player.amount)
				del to_call[0]
			else:
				self._remove_player(player.name)
				del to_call[0]
			self.display()
		self._reset_put_in()
		self.call_amount = 0


	# def _continue_betting(self, betting_list):

	def _get_index(self, name, array):
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


	def _remove_player(self, name):
		for i in range(len(self.players_in_hand) - 1):
			if self.players_in_hand[i].name == name:
				del self.players_in_hand[i]


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


	def display (self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print()
		print(f"Pot value: {self.pot_value}")
		print()
		for player in self.players_in_hand:
			print(player, end = " ")
			for card in player.hand:
				print(card, end = " ")
			print()
			print(player.amount)
			print()
		print("Community: ", end = "")
		for card in self.community_cards:
			print(card.value + " " + card.suit + " ", end = "")
		print('\n')



if __name__ == '__main__':
	BUYIN = 100
	deck = Deck()

	player1 = Player("Bob", BUYIN)
	player2 = Player("Joe", BUYIN)
	player3 = Player("Tod", BUYIN)
	player4 = Player("Ron", BUYIN)

	table = Table([player1, player2, player3, player4], deck)

	while len(table.players) >= 2:
		table.play()
		table.play_again()