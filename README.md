# Mahjong AI

The purpose of this project is to create artificial intelligence that approaches optimal decision making in the game of Mahjong using reinforcement learning.

## The Game

While there are many different variations of Mahjong, the game in this project will be played as follows.

### Tiles

The game is made up of four tiles each of the following suits and ranks:

* "Circle" suit, 1-9 ranks
* "Stick" suit, 1-9 ranks
* "10k" suit, 1-9 ranks
* "Red" suit (no rank)
* "Green" suit (no rank)
* "White" suit (no rank)
* "East" suit (no rank)
* "South" suit (no rank)
* "West" suit (no rank)
* "North" suit (no rank)

Based on the above, there are 136 total tiles.

### Players

There are four players. Each player can see the tiles in their own hand, the discard pool, and any tiles played by other players.

### Game Setup

Each player draws four tiles from the draw pool until all players have 12 tiles. Then, each player draws a single tile from the draw pool. The player who goes first on any given round must begin their turn by drawing one additional tile from the draw pool.

Each player thus begins the game with 13 tiles.

### Cardinal Directions

The Mahjong game board is a square with four directions identical to the four directional tiles ("East", "South", "West", and "North"). Each player sits on one side of the board. The direction of the board that corresponds with the player sitting on that side is the local, player-specific direction. For example, during a given round, player 3 might be sitting on the North side of the board. This player's local direction is North. In addition to the local directions, there is also a global direction. At the start of the game, the global direction is always East. After one round, the board is rotated. During this rotation, the global direction remains the same, but the local direction changes in accordance with the board. After four rotations, when the board returns to its initial orientation, the global game state changes to South. After four more rounds, the global direction changes to West, and finally, North. The game ends after the North phase of the game is completed, and the player with the most points wins. Note that if the player who went first in any given round wins, the board does not rotate and the next round starts again as usual.

#### Win Conditions

A player wins the game when the tiles in their hand form a valid win condition. Players must draw their final winning tile from the draw pool, not from a tile discarded by another player. The only exception to this rule is in the case of the highest value winning hand. Most winning hands will be made up of 14 tiles. However, the total number of tiles increases by one for each set of four (more on this later). Usually, winning hands will be made up of four sets/runs and one double.

Note that a "set" is defined as three or four identical tiles, both in suit and rank (if applicable). For example, three or four tiles with suit "10k" and rank 3 form a set. A "run" is 3 tiles of the same suit with consecutive ranks. For example, three tiles with the "Circle" suit and ranks 7, 8, and 9, form a set. A "double" is any two identical tiles, both suit and rank (if applicable). For example, two "South" tiles form a double.

The lowest value winning hand is made up of a mix of four sets/runs and one double where all groups do not share the same suit. The value of this hand is 2 points. Additional points can be won by meeting some conditions:

* If all tiles in the hand are of the same suit, add 3 points to the score
* If all groups of tiles (excluding the double) are runs, add 1 point to the score
* If all groups of tiles (excluding the double) are sets, add 3 points to the score
* For each set that is a color (excluding the double), add 1 point to the score
* For each set that is a direction (excluding the double), add 1 point to the score if the direction matches up with the global game direction or the local player-specific direction
* If the double is made of tiles with a color ("Red", "Green", or "White") or a direction ("East", "South", "West", "North"), then the score is only 2, regardless of all other tiles in the winning hand

#### Player Turn Order

Game play proceeds in the same order (for example, 1, 2, 3, 4, 1, ...), though the player who goes first on a given round usually changes (refer to "Cardinal Directions" above for more detail). For the sake of this project, "player 1" will always be assumed to go first at the very beginning of the game.

#### Player Actions

The basic player actions involve drawing tiles, discarding tiles, and declaring victory.

* Tiles are drawn from the top of the draw pool
* Tiles are discarded into the discard pool
* Once a player declares victory, they are awarded three times the point value of their hand
  * Every player who did not win must give points to the winner of that round based on the value of the winning hand

#### Special Actions

There are several non-standard actions that players can make when drawing a tile.

* Pon
  * If a player has a double in their hand and another player discards the same tile, the player with the double may "Pon" the tile to form a set, even if it isn't their turn. The player must then reveal their double and discard a tile. The player turn order is then reset based on the player who Pon'd.
    * For example, if player 4 discards a tile and player 2 Pons it, player 3 goes next after player 2, skipping player 1. Play then continues in sequential player order as normal.

* Gon
  * Similar to Pon, this action can be taken at any time (even out of turn) by a player to form a set of 4, and the set of four must then be revealed to the rest of the players. Just like with Pon, player turn order is reset based on the player who Gon'd.
  * Unlike Pon, after revealing your set of four to the other players, the player who Gon'd must then draw an additional tile from the back of the draw pool prior to discarding.
    * For example, player 4 has a set of "North" tiles in their hand. If player 2 discards a "North" tile, player 4 may Gon it, taking the tile and revealing the rest of their set to all other players. Then, player 4 must draw the last tile in the draw pool before discarding. Finally, play continues with player 1 going next.

* Blind Gon
  * The mechanics of this action are identical to Gon, however, this can only occur if a player draws the fourth tile themselves. In this case, the player with the set of four tiles does not have to reveal what the set is to the other players. Drawing from the back of the discard pool, discarding, and resuming play order with the next sequential player happen as described above.

* Eat
  * If the player immediately before the player whose turn it is discards a tile that could be used to form a run for the player whose turn it is, the tile may be eaten to form run. The run must then be revealed to all other players.
    * For example, if player 1 discards a "Circle" 2, and player 2 has "Circle" 1 and "Circle" 3, player 2 may Eat the discarded "Circle" 2 and make a run. Note that if players 3 or 4 could have also used the "Circle" 2 to make a run, they are not allowed to Eat. Eating may only occur using the tile discarded by the player immediately before.
   
Pon and Gon have precidence over Eat. For example, if one player wants to Pon/Gon the tile that was just discarded, and a different player wants to Eat it, the player Poning/Goning has priority.

## The AI

The AI in this game will be responsible for making decisions regarding both drawing tiles and discarding tiles. At each step in the game (i.e. whenever a player discards), the AI will receive a snapshot of the game and execute one of the drawing actions. Each player will have the opportunity to Pon/Gon (which can happen out of order). If no player Pons/Gons, then the player whose turn it is can Eat the tile discarded by the player before them or draw from the draw pool. Once drawing is complete, the AI must decide which tile to discard. Drawing and discarding will each be handled by separate models.

The state of the game will be represented as a one-hot encoded vector, and it will represent the input to the model. This includes all tiles in the player's hand, all tiles in the discard pool, and any tiles that have been played by another player and are now visible to all (via pon/gon/eat). Each tile will is encoded by its suit and rank. Unknown tiles such as those still in the draw pool are represented by a zero vector. This ensures that the one-hot gamestate vector remains a consistent size.

The AI agents for this project are still under development (see below), but my initial plan is to simulate a large quantity of games assigning random actions for drawing and discarding. The data from these simulations will then be used to train two models: one for drawing and one for discarding. Later, I want to implement a reinforcement learning methodology to train a separate agent using little to no previous data, allowing the agent to improve during simulation. The models behind each agent will be a neural network. The structure of the hidden layers for each network is to be determined. The output node for the discarding agent will be one of the tiles in the player's hand, and the output for the drawing agent will correspond to where to draw a tile (if there are possible actions such as pon/gon/eat).

Ultimately, I want to have the different agents play against each other. There aren't any concrete plans to expand the environment to allow for real-time inputs, but if the AI seems promising, I may work towards being able to use it when playing against friends in real time.


## Current State of the Project

Currently, the environment (the game of Mahjong described above) is completely built. There are functions for each operation in the game such as initialization (shuffling the tiles and dealing 12 tiles to each player), removing tiles from the draw pool, adding tiles to the discard pool, adding and removing tiles from a player's hand, and more. There is a comprehensive scoring function and a suite of unit tests. Currently, I am still working on compiling data to train a model using supervised learning. This data is being stored in a SQLite database. I have started to train evaluation_network and discard_network using this data, but much more needs to be simulated to refine these models.

Continuing to improve the reinforcement learning models is the next step. After that, the reinforcement learning models will be created. Lastly, these models will be tested against each other.

Optionally, I will later update the environment to allow for real time inputs of an external game state that allow me to use the best models in a real game. The vision for this is that I'm playing a game with friends and I have my laptop with me. At every development of the game, I make an update on my computer. When applicable, I gather the best decision based on the trained models from this project.

