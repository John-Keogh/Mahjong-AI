import unittest
from tile_utils import is_set, is_run, is_winning_hand, compute_score, Tile, GameState
import time
import random
import numpy as np
import logging
import matplotlib.pyplot as plt
import copy
import itertools

num_wins = []
exec_time = []
scores = []

global_start_time = time.time()
global_elapsed_time = 0
round = 0
while round < 25000:
    if round % 250 == 0:
        print(f"Round: {round}")

    start_time = time.time()

    # Initialize game
    gamestate = GameState()
    gamestate.initialize_draw_pool()
    gamestate.deal_tiles()

    players = ['player1',
            'player2',
            'player3',
            'player4']

    player = players[3]

    def player_turn(player: str) -> int:
        '''
        Carries out a player's turn

        Args:
        player: 'player1', 'player2', etc.

        Returns
        score: integer representing the value of player's hand
        '''
        gamestate.add_tile_to_hand(gamestate.draw_pool[0], player)
        gamestate.remove_tile_from_draw_pool(gamestate.draw_pool[0])

        score = compute_score(gamestate, player)

        if score != 0:
            return score
        
        random.shuffle(gamestate.players[player])
        discard_tile = gamestate.players[player][0]
        gamestate.add_tile_to_discard_pool(discard_tile)
        gamestate.remove_tile_from_hand(discard_tile, player)
        return score
    

    turn = 0
    while len(gamestate.draw_pool) != 0 and turn<200:
        # Move to the next player's turn based on whose turn it was previously
        if player == player[0]:
            player = player[1]
        elif player == player[1]:
            player = player[2]
        elif player == player[2]:
            player = player[3]
        elif player == player[3]:
            player = player[0]
        
        score = player_turn(player)
        if score != 0:
            break
        turn += 1   # Delete after testing code
        # print(f"turn = {turn}")

    if score == 0:
        # print(f"Nobody won that round.")
        num_wins.append(0)
    else:
        # print(f"{player} has won the round with a score of {score}.")
        # gamestate.print_player_hand(player)
        num_wins.append(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time:.2f} seconds")
    exec_time.append(elapsed_time)
    round += 1
    global_elapsed_time += end_time - global_start_time
    scores.append(score)

print(f"Total rounds: {round}")
print(f"Average round time: {sum(exec_time) / len(exec_time):.2f}s")
print(f"Maximum round time: {max(exec_time):.2f}s")
print(f"Percentage of rounds with a winner: {(sum(num_wins) / len(num_wins))* 100:.2f}%")
print(f"Average score: {sum(scores) / len(scores)} points")

plt.plot(np.arange(len(exec_time)), exec_time, marker='o')
plt.xlabel('Round')
plt.ylabel('Execution Time (s)')
plt.title('Execution Time per Round')
plt.show()