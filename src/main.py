from table import Table 
from deck import Deck 
from player import Player 

BUYIN = 100
deck = Deck()

player1 = Player("Bob", BUYIN)
player2 = Player("Joe", BUYIN)
player3 = Player("Tod", BUYIN)
player4 = Player("Ron", BUYIN)

def main():
	table = Table([player1, player2, player3, player4], deck)
	while len(table.players) >= 2:
		table.play()
		table.play_again()


if __name__ == '__main__':
	main()

