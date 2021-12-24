# Texas No Limit Hold'em Poker CLI Interface

## Background
Poker has been a passion of mine since the start of Covid-19 and I decided to recreate this classic game as a fun project. If you are not familiar with poker rules, give [this](https://www.pokernews.com/poker-rules/texas-holdem.htm#:~:text=In%20a%20game%20of%20no-limit%20Texas%20hold%27em%2C%20the,raise%20is%20always%20exactly%20twice%20the%20big%20blind.) a quick read.

## Groundwork

 - In order to play poker, we first need a deck of cards. As with any card, the [card](https://github.com/cezar-r/poker/blob/main/src/cards.py) objects in this game have two main features: rank and suit. Later on, we will need to compare card values, so each card also has a integer representation of its value; every card that is 10 or lower is simply represented by their rank, and face cards recieve higher values (Jack: 11, Queen: 12, etc). These cards are then stored in a [deck](https://github.com/cezar-r/poker/blob/main/src/deck.py) object as a list.
 - The second step is to get some [players](https://github.com/cezar-r/poker/blob/main/src/player.py). There are two types of players in this game: real people and bots. Each player has two main attributes that we need to worry about: pot value and hand. They also each have a decision() method, in which they can call, fold or raise. When the player is a real player, the decision is made by getting input from the CLI interface. When it is a bot, the same method is called, however its decision-making is done internally, which will be discussed more in depth later on.
 - Next, we need a scoring system to calculate who wins at the end. To do this, a [calculator](https://github.com/cezar-r/poker/blob/main/src/winner_calculator.py) checks to see which of the 10 hands the player has at the end (Two pair, Three of a Kind, etc). This is done by giving each outcome a score between 16 and 140. A High Card score ranges from 16-27, where 27 represents an Ace High Card, 26 is King High Card, etc. (Realistically, the lowest possible High Card is a 7, so the lowest possible score is a 21). Pairs range from 27.01 - 40, with the following high card represented as a decimal. With these scores, we can now compare the hands at showdown and calculate who the winner is.
 - Lastly, we need the table. The [table](https://github.com/cezar-r/poker/blob/main/src/table.py) object contains the deck, list of players, pot value, and the current board (or community cards). For each turn on the board, there is a betting cycle that takes place under the bet() method. 
 
 ## Bot Logic
  - While there are Poker AI programs out there that are very intelligent and beat professionals, I did not take this route as I do not have enough exposure to game theory nor do I have the computational power to host such a powerful program. Instead, I implemented decision logic based on my experience from playing poker and what I believe is an optimal strategy. The key factors in the decision making is the attribute max_put_in, which represents the most amount of money the bot is willing to risk on any given hand.
 
 ### Pre-Flop
  - To play the pre-flop betting round, we analyze our hand and look for a pocket pair, suited cards, connectors, or suited connectors. These each return a score, the better the hand the better the score. For example, two Ace's will have a higher score than 8 9 suited. The max_put_in is then calculated from this score. In practice, we would hope to see a bot with 7 2 fold to a raise, for example.

### Flop, Turn, and River
 - To play the rest of the betting rounds, the bot calculates it's max_put_in based on a series of simulations. For example, if we are currently betting around on the flop, the bot will simulate every possible turn and river card. From there, it will calculate the average score it recieves from those simulations, which is then used to calculate the max_put_in. With this logic, the bot is able to play straight and flush draws, but will still fold if the bet is too big.
 - You may be thinking, "What determines a good score?". Using the simulation program, I was able to calculate winning hand score over a series of 10,000 games, and found that a score of 50-60 (Two Pair with one pair of face cards or low Three of a Kind) wins about 45% of the games. If the bot sees an average score of 55 in its simulations, it will have a very strong max_put_in. If the score is very high (Flush with face card or better), its max_put_in is adjusted to its entire stack. This means that the bot will not fold a very strong hand. 

### Slow Playing and Bluffing
 - To get the bots to play more like a real person, it needs to play with some randomness. If a bot has a very good hand, we already know its max_put_in is going to be very high. However, we do not want it to play super aggressive and scare everyone into folding, thus resulting in less money. To combat this, the bot will make small raises on the flop a majority of the time, with each bet increasing in size as there are more cards on the board. Even though it is taught to slow play, it will still call big raises since its max_put_in is already high. It will also randomly decide to not slow play and place a big bet, hoping someone bites.
 - The least mathematical part of poker is bluffing. Bluffing goes against all the logic explained above, which is why its important to implement it; we do not want the bot to be predictable. Therefore, the bot will randomly decide its going to bluff on any hand and will increase its max_put_in to half it's stack on the flop, 3/4 of the stack on the turn and everything on the river. 

## Display
 - Now that the entire game logic is implemented, it needs to be displayed on the command line. Below is an example of what a game would look like:
<img src = "https://github.com/cezar-r/poker/blob/main/cli_poker.png" width = 500 height = 400> 

## In Action
 - [Here](https://youtu.be/ra7i8MT12_c) is a video of the bots in action against each other. When a blank name is entered for the player, it creates a bot player, which allows us to see the bots play against each other. When there are no real players in the game, cards are visible at all times.
 - [Here]() is a video of me playing against the bots
 - [Here]() is a video of me playing heads up against somebody
