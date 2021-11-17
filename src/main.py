from table import Table 
from deck import Deck 
from player import Player 

BUYIN = 1000
deck = Deck()

player1 = Player("Bob")
player2 = Player("Joe")
player3 = Player("Tod")
player4 = Player("Ron")


def main():
	table = Table([player1, player2, player3, player4], deck, BUYIN)
	while len(table.players) >= 2:
		table.play()
		table.play_again()


if __name__ == '__main__':
	main()

