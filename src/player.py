import names
import random
from winner_calculator import OddsCalculator, WinnerCalculator
from deck import Deck
import time

class Player():
	def __init__(self, name = ""):
		if name == "":
			self.name = str(names.get_first_name())
			self.is_bot = True
		elif name == "doe":
			self.name = ""
			self.is_bot = True
		else:
			self.name = name.title()
			self.is_bot = False
		self.amount = 0
		self.hand = []
		self.is_big_blind = False
		self.is_little_blind = False
		self.cur_bet = 0
		self.put_in = 0
		self.odds = 0
		self.cur_board = []
		self.players_at_table = 0
		self.all_in = False
		self.willing_to_bet = 0
		self.play_bluff = False

	def __str__(self):
		string = self.name
		if self.is_big_blind:
			string += ' [BB]'
		elif self.is_little_blind:
			string += ' [SB]'
		return string

	def __repr__(self):
		string = self.name
		if self.is_big_blind:
			string += ' [BB]'
		elif self.is_little_blind:
			string += ' [SB]'
		return string

	def buyin(self, amount):
		self.amount = amount

	def reset(self):
		self.hand = []
		self.cur_bet = 0
		self.put_in = 0
		self.willing_to_bet = 0
		self.play_bluff = False

	def _raise(self, to_call_amount):
		raise_amount = int(input('Raise by how much?\n'))
		if raise_amount < 2* to_call_amount and self.amount > 2 * to_call_amount:
			print(f'Reraise must be at least double previous raise ({to_call_amount *2})\n')
			return self._raise(to_call_amount)
		elif raise_amount > self.amount:
			print('Cannot raise more than current balance')
			return self._raise(to_call_amount)
		return raise_amount

	def decision(self, to_call_amount):
		if self.is_bot:
			time.sleep(2)
			return self.play_hand(to_call_amount)
		decision = input(f'\n{self.name}\nTo call: {to_call_amount - self.put_in}\nCall[1]\tFold[2]\tRaise[3]\n')
		if decision == '3':
			raise_amount = self._raise(to_call_amount)
			self.cur_bet = raise_amount
			return ('raise', raise_amount)
		elif decision == '1':
			return ('call', 0)
		else:
			return ('fold', 0)

	def play_hand(self, to_call_amount):
			if len(self.cur_board) > 0:
				return self._calculate_odds(to_call_amount)
			else:
				return self._play_pre_flop(to_call_amount)

	def _calculate_odds(self, to_call_amount):
		comp = Computer(self, to_call_amount)
		score = comp.get_odds_of_winning()
		if len(self.cur_board) == 3:
			return self._play_flop(to_call_amount, score)
		elif len(self.cur_board) == 4:
			return self._play_turn(to_call_amount, score)
		else:
			return self._play_river(to_call_amount, score)

	def _normalize_score(self, score):
		return (score / 10 - 2) / 2

	def _play_flop(self, to_call_amount, score):
		hand_strength = self._normalize_score(score) 
		return self._play_hand(to_call_amount, hand_strength)

	def _play_turn(self, to_call_amount, score):
		hand_strength = self._normalize_score(score)
		return self._play_hand(to_call_amount, hand_strength)

	def _play_river(self, to_call_amount, score):
		hand_strength = self._normalize_score(score)
		return self._play_hand(to_call_amount, hand_strength)

	def _play_pre_flop(self, to_call_amount):
		hand_strength = self._cur_hand_score()
		return self._play_hand(to_call_amount, hand_strength)
	
	def _play_hand(self, to_call_amount, hand_strength):
		if not self.play_bluff:
			self.willing_to_bet = hand_strength / 10
		self._bluff()
		if self.amount > 2000:
			max_put_in = round(2000 * self.willing_to_bet, -1)
		else:
			max_put_in = round(self.amount * self.willing_to_bet *  (1000 /self.amount) , -1)
			if max_put_in > self.amount:
				max_put_in = self.amount

		# if hand is strong, play anything
		if self.willing_to_bet > .4: 
			max_put_in = self.amount
			self.all_in = True

		if to_call_amount == 0:

			# if they check on the river, raise
			if len(self.cur_board) == 5: 
				return ('raise', round(max_put_in // 6 + 50, -1))

			# if they check on the turn, raise
			elif len(self.cur_board) == 4: 
				return ('raise', round(max_put_in // 12, -1))

			# raise less
			return ('raise', round(max_put_in // 20 + 10, -1))

		if to_call_amount > max_put_in * 1.1:

			# if the bet is not too big and we have a decent hand on the preflop, call sometimes
			if to_call_amount / self.amount > .2 and self.willing_to_bet > .1 and random.randint(1,15) == 7 and len(self.cur_board) == 0:
				return ('call', 0)

			# if the bet is not too big and we have a decent hand on the flop, call sometimes
			elif to_call_amount / self.amount > .2 and self.willing_to_bet > .1 and random.randint(0,10) == 7 and len(self.cur_board) == 3:
				return ('call', 0)

			# if the bet is not too big and we have a decent hand on the river, call sometimes
			elif to_call_amount / self.amount > .2 and self.willing_to_bet > .1 and random.randint(0,5) == 2 and len(self.cur_board) == 5:
				return ('call', 0)

			# if the bet is very large and we have a decent hand before the turn, call sometimes
			elif to_call_amount / self.amount > .5 and self.willing_to_bet > .1 and random.randint(0,10) == 7 and len(self.cur_board) < 4:
				return ('call', 0)

			# if the bet is very large and we have a strong hand after the turn, call sometimes
			elif to_call_amount / self.amount > .5 and self.willing_to_bet > .2 and random.randint(0,10) == 7 and len(self.cur_board) >= 4:
				return ('call', 0)

			# otherwise fold
			return ('fold', 0)

		# if raise is more than half of our max bet, call
		if to_call_amount / max_put_in >= .5:
			return ('call', 0)

		if to_call_amount / max_put_in > .3:

			# if value raised on the river, raise
			if len(self.cur_board) == 5:
				small_value_raise = 20
				med_value_raise = 100
				high_value_raise = 200
				random.choices([small_value_raise, med_value_raise, high_value_raise,  round(max_put_in // 1.5 + 50, -1),  round(max_put_in // 3 + 50, -1), round(max_put_in // 5 + 50, -1)], weights = (10, 15, 20, 10, 15, 30), k = 1)[0]
				return ('raise', round(max_put_in // 1.5 + 50, -1))

			# if value raised pre-flop, randomly call or raise
			elif len(self.cur_board) == 0:
				raise_amount =  round(2 * to_call_amount, -1) + 10
				if raise_amount > 100 and to_call_amount > 50:
					return random.choices([('call', 0), ('raise', raise_amount), ('raise', round(raise_amount * 1.5, -1))], weights = (70, 20, 10), k = 1)[0]
				return ('raise', raise_amount)

			# otherwise, randomly call or raise
			else:
				if to_call_amount == 10 and self.willing_to_bet > .1:
					to_call_amount = 20
				raise_amount = round(2 * to_call_amount, -1)
				second_raise_amount = round(raise_amount * 1.5, -1)

				# if raise is relatively small, risk tripling the raise
				if to_call_amount / self.amount < .1:
					third_raise_amount = round(second_raise_amount * 1.5, -1)
				else:
					third_raise_amount = second_raise_amount

				raise_amount = random.choices([to_call_amount, raise_amount, second_raise_amount, third_raise_amount], weights = (45, 35, 15, 5), k = 1)[0]
				if raise_amount == to_call_amount:
					return ('call', 0)
				else:
					if raise_amount > self.amount:
						raise_amount = self.amount
					return ('raise', raise_amount)
		# otherwise, bet must be relatively small to what we want to put in
		else:
			raise_amount = round(2 * to_call_amount, -1)
			secound_raise_amount = round(raise_amount * 1.5, -1)
			raise_amount = random.choices([raise_amount, secound_raise_amount], weights = (70, 30), k = 1)[0]
			return ('raise', raise_amount)
		
	def _bluff(self):
		if not self.play_bluff:
			x = random.randint(0, random.randint(5, 25))
			if x == 17 and self.willing_to_bet < .1:
				self.play_bluff = True
		else:
			if len(self.cur_board) == 0:
				self.willing_to_bet = .15
			elif len(self.cur_board) == 3:
				self.willing_to_bet = .2
			elif len(self.cur_board) == 4:
				self.willing_to_bet = .3
			else:
				y = random.randint(0,20)
				if y <= 10:
					self.willing_to_bet = .4
				else:
					self.willing_to_bet = 1

	def _cur_hand_score(self):
		if self._have_pocket_pair():
			return self.hand[0].int_value / 3
		if self._have_suited() and self._have_connectors():
			return max([card.int_value for card in self.hand]) / 4
		if self._have_suited():
			return max([card.int_value for card in self.hand]) / 6
		if self._have_connectors():
			return max([card.int_value for card in self.hand]) / 7
		else:
			return sum([card.int_value for card in self.hand]) / 2 / 8

	def _have_pocket_pair(self):
		return self.hand[0].value == self.hand[1].value 

	def _have_suited(self):
		return self.hand[0].suit == self.hand[1].suit

	def _have_connectors(self):
		diff = abs(self.hand[0].int_value - self.hand[1].int_value)
		if diff == 12 or diff == 1: # ace-two
			return True
		return False

	def play_again(self):
		if self.is_bot:
			return 'y'
		play_again = input(f"{self.name} Play again? [Y][N]\n")
		if play_again == 'y':
			return True
		elif play_again == 'a':
			return 'a'
		else:
			return False


class Computer:

	def __init__(self, player, to_call_amount):
		self.player = player
		self.to_call_amount = to_call_amount

	def get_odds_of_winning(self):
		hand = self.player.hand
		board = self.player.cur_board
		deck = Deck()
		deck = self.init_deck(hand, board, deck.cards)
		calculator = OddsCalculator([self.player], board, deck)

		# get average score of remaining possible hands
		calculator.calculate_odds()
		return sum(list(calculator.scores.values())[0])/len(list(calculator.scores.values())[0])

	def init_deck(self, hand, board, cards):
		cards = self.shuffle_cards(cards)
		cards = self.remove_cards(hand, board, cards)
		return cards

	def shuffle_cards(self, cards):
		random.shuffle(cards)
		return cards

	def remove_cards(self, hand, board, cards):
		hand_board = hand + board
		for card in hand_board:
			suit = card.suit
			value = card.value
			for i, _card in enumerate(cards):
				if _card.suit == suit and _card.value == value:
					del cards[i]
		return cards



if __name__ == '__main__':
	p = Player()

