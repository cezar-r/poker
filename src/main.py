#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main file that runs the game.
Has methods to get players and load the table up.
"""
from table import Table 
from deck import Deck 
from player import Player 
import os

BUYIN = 10000
deck = Deck()

def clear():
	"""
	Clears the screen
	"""
	os.system('cls' if os.name == 'nt' else 'clear')


def get_players(players = []):
	"""
	Recursive method to get players from command line input.
	Method is recursive to avoid invalid inputs
	
	Returns
	-------
	players : list
		List of player objects (real players)
	"""
	clear()
	name = input("Enter name\n")
	player = Player(name)
	players.append(player)

	add_more_input = input("Add more players? [Y][N]\nPress enter after selection\n")
	if add_more_input == 'n':
		return players
	elif add_more_input == 'y':
		players = get_players(players)
	else:
		return get_players()
	return players


def get_players_bots():
	"""
	Gets all real players and bots
	
	Returns
	-------
	players : list
		List of player objects (real players and bots)
	"""
	num_bots = int(input("How many opponents?\nPress enter after selection\n"))
	players = get_players()
	clear()
	for i in range(num_bots):
		player = Player()
		if player.name in [p.name for p in players]:
			player = Player()
		players.append(Player())
	return players


def collect_players():
	"""
	Start menu that allows player to decide to play against player or bot
	
	Returns
	-------
	players : list
		List of player objects (real players and/or bots)
	"""
	clear()
	inp = input("[person vs person][1]\t[person vs bots][2]\nPress enter after selection\n")
	if inp == '1':
		players = get_players()
	elif inp == '2':
		players = get_players_bots()
	else:
		return collect_players()
	return players


def start_screen():
	"""
	The home screen
	
	Returns
	-------
	players : list
		List of player objects (real players and/or bots)
	"""
	clear()
	input("cmdline poker\npress enter to continue")
	players = collect_players()
	return players


def main():
	players = start_screen()
	assert len(players) >= 2
	table = Table(players, deck, BUYIN)
	while len(table.players) >= 2:
		table.play()
		table.play_again()


if __name__ == '__main__':
	main()

