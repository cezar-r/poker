

class Player():
	def __init__(self, name):
		self.name = name
		self.amount = 0
		self.hand = []
		self.is_big_blind = False
		self.is_little_blind = False
		self.cur_bet = 0
		self.put_in = 0
		self.odds = 0

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


	def decision(self, amount):
		decision = input(f'\n{self.name}\nTo call: {amount - self.put_in}\nCall[1]\tFold[2]\tRaise[3]\n')
		if decision == '3':
			raise_amount = int(input('Raise by how much?\n'))
			assert raise_amount <= self.amount
			self.cur_bet = raise_amount
			return ('raise', raise_amount)
		elif decision == '1':
			return ('call', 0)
		else:
			return ('fold', 0)


	def play_again(self):
		play_again = input("Play again? [Y][N]\n")
		if play_again == 'y':
			return True
		elif play_again == 'a':
			return 'a'
		else:
			return False



		
		