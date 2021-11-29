from cards import Card
from player import Player


def two_pair(player, board, high_score = 0):
	best_hand = _value_dict(player, board)
	has_two = False
	values = []
	for value in best_hand:
		if len(best_hand[value]) == 2:
			if has_two:
				high_score = score + round(value / 14, 2)
				break
			has_two = True
			score = 3 * 14 + value - 1
	if has_two:
		for value in best_hand:
			if len(best_hand[value]) == 1:
				high_score += (value - 1) / 1400
				return high_score



def one_pair(player, board, high_score = 0):
		best_hand = _value_dict(player, board)
		score = 0
		has_pair = False
		for value in best_hand:
			if len(best_hand[value]) == 2:
				high_score = 2 * 14 + value - 1
				has_pair = True
				break
		num_cards = 0
		if has_pair:
			for value in best_hand:
				if len(best_hand[value]) == 1 and num_cards <= 2:
					num_cards += 1
					high_score += (value-1) / 390
		return high_score



def _value_dict(player, board):
		suits = [card.suit for card in player.hand]
		values = [card.int_value for card in player.hand]
		best_hand = {}
		for suit, value in list(zip(suits, values)):
			if value in best_hand:
				best_hand[value].append(suit)
			else:
				best_hand[value] = [suit]
		for card in board:
			if card.int_value in best_hand:
				best_hand[card.int_value].append(card.suit)
			else:
				best_hand[card.int_value] = [card.suit]
		best_hand = dict(sorted(list(best_hand.items()), key = lambda x: x[0])[::-1])
		return best_hand



if __name__ == '__main__':
	ace = Card("clubs", "10")
	two = Card("spades", "10")

	three = Card("spades", "9")
	four = Card("hearts", "9")

	ten = Card("hearts", "K")
	ten2 = Card("spades", "5")
	queen = Card("clubs", "7")
	queen2 = Card("hearts", "8")
	three2 = Card("spades", "4")


	player1 = Player("Bob")
	player1.hand = [ace, two]

	player2 = Player("Jon")
	player2.hand = [three, four]

	cards = [ten, ten2, queen, queen2, three2]
	
	for player in [player1, player2]:
		print(player, one_pair(player, cards))


'''
TEST: 

cezar [BB] - $11055.0
10 clubs
2 clubs

Marquis [SB] - $8595.0
10 diamonds
J clubs

Board: K clubs 8 hearts J diamonds A diamonds 6 hearts

ingame: tie with high card
reality: marquis wins with jacks



Cez - $8890.0
10 clubs
10 spades

Lisa - $8890.0
9 spades
9 hearts

Board: K hearts 5 spades 7 clubs 4 spades 8 hearts

ingame: tie with high card
reality: cez wins w one pair
'''


