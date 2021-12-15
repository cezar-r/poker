import matplotlib.pyplot as plt 
import numpy as np
import random
from player import Player 
from deck import Deck
from winner_calculator import WinnerCalculator

deck = Deck()
plt.style.use("dark_background")


class Simulation:

	def __init__(self, iters = 1000, plot = True):
		self.iters = iters
		self.deck = deck.cards
		self.plot = plot


	def run_simulation(self):
		self.scores = {}
		for j in range(2, 7):
			j_scores = []
			for i in range(self.iters):
				self._shuffle()
				deck_copy = self.deck.copy()
				players = self._deal_cards(self._init_players(j), deck_copy)
				board = self._create_board(deck_copy)
				calculator = WinnerCalculator(players, board, verbose = False)
				winning_score = np.mean(calculator.scores)
				player = calculator.winners[0]
				hand = [player.hand[0], player.hand[1]]
				board = calculator.community
				winning_hand = calculator.winning_hand
				j_scores.append({'winning_score' : winning_score,
							'hand' : hand,
							'board' : board,
							'winning_hand' : winning_hand,
							'game_nmbr' : i + 1,
							'players' : j})
			self.scores[str(j)] = j_scores
		

		avg_score_dict = {}
		for player_count in self.scores:
			score_total = 0
			for game in self.scores[player_count]:
				score_total += game['winning_score']
			avg_score_dict[player_count] = score_total/len(self.scores[player_count])
		
		if self.plot:
			self._plot()


	def _plot(self):
		for player_count in self.scores:
			plt.figure(figsize=(14,7))
			x = []
			y = []
			for game in self.scores[player_count]:
				x.append(game['game_nmbr'])
				y.append(game['winning_hand'])
			plt.hist(y, bins = len(list(set([game['winning_hand'] for game in self.scores[player_count]]))))
			plt.title(f"Players: {game['players']}")
			plt.tight_layout()
			plt.show()



	def _shuffle(self):
		random.shuffle(self.deck)


	def _create_board(self, deck):
		board = []
		for i in range(5):
			board.append(deck[0])
			del deck[0]
		return board


	def _init_players(self, num_players = 6):
		players = []
		for i in range(num_players):
			player = Player()
			players.append(player)
		return players


	def _deal_cards(self, players, deck):
		for player in players:
			player.hand = [deck[0], deck[1]]
			del deck[0]
			del deck[0]
		return players



if __name__ == '__main__':
	sim = Simulation(10000)
	sim.run_simulation()

