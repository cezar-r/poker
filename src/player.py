

class Player():
	def __init__(self, name, buy_in):
		self.name = name
		self.amount = buy_in
		self.hand = []
		self.is_big_blind = False
		self.is_little_blind = False
		self.cur_bet = 0
		self.put_in = 0

	def __str__(self):
		return f'{self.name}'


	def __repr__(self):
		return f'{self.name}'

	def reset(self):
		self.hand = []
		self.cur_bet = 0
		self.put_in = 0


	def decision(self, amount):
		decision = input(f'\nTo call: {amount - self.put_in}\n{self.name}\nCall[1]\tFold[2]\tRaise[3]\n')
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
		play_again = input("Play again? [Y][N]")
		if play_again == 'y':
			return True
		return False



		
		