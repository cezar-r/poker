#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This file contains the Deck object
'''

from cards import SUITS, VALUES, Card
import random


class Deck:
	"""
	A class that represents a deck
	
	Attributes
	----------
	cards : list
		list of all cards
	"""
	def __init__(self):
		self.cards = self._init_cards()

	def _init_cards(self):
		"""
		Adds all the cards to the deck
		"""
		cards = []
		for suit in SUITS:
			for value in VALUES:
				cards.append(Card(suit, value))
		return cards

	def shuffle(self):
		"""
		Shuffles the list of cards
		"""
		random.shuffle(self.cards)


	def reset(self):
		"""
		Calls the _init_cards() method
		"""
		self.cards = self._init_cards()

