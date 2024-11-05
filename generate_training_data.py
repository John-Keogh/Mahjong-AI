import random
import torch
import os
import sqlite3
import time
import random

from tile_utils import compute_score
from gamestate import GameState
from preprocessing import prepare_input
from training_data_utils import get_last_game_id, save_winner_data

global_start_time = time.time()
global_elapsed_time = 0

# Define the database path
db_folder = "G:\\VS Code\\Mahjong_Data"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "mahjong_eval_net_training_data.db")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for storing winner history if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS winner_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        player TEXT,
        turn INTEGER,
        gamestate_tensor BLOB,
        final_score INTEGER
    )
''')
conn.commit()


num_rounds = 2
game_id = get_last_game_id(conn)
count = 0

micro_dict = {'player1': 0,
            'player2': 1,
            'player3': 2,
            'player4': 3}

start_time = time.time()

for i in range(num_rounds):
    if count % 250 == 0:
        print(f"Round: {count}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        # print(f"Batch time: {elapsed_time:.2f} s")
        start_time = time.time()

    # Initialize game
    gamestate = GameState()
    gamestate.randomize_macro_direction()
    gamestate.randomize_micro_direction()
    gamestate.initialize_draw_pool()
    gamestate.deal_tiles()

    # Initialize player hand histories (1851 is length of gamestate_tensor)
    player_history = torch.zeros((4, len(gamestate.draw_pool), 1851))

    # Initialize number of turns each player has taken
    turns = {
        'player1': 0,
        'player2': 0,
        'player3': 0,
        'player4': 0
    }

    players = ['player1',
            'player2',
            'player3',
            'player4']

    player = players[3]

    while len(gamestate.draw_pool) != 0:
        # Move to the next player's turn based on whose turn it was previously
        if player == player[0]:
            player = player[1]
        elif player == player[1]:
            player = player[2]
        elif player == player[2]:
            player = player[3]
        elif player == player[3]:
            player = player[0]
        
        turns[player] += 1

        # Calculate score of player's hand
        gamestate.add_tile_to_hand(gamestate.draw_pool[0], player)
        gamestate.remove_tile_from_draw_pool(gamestate.draw_pool[0])
        score = compute_score(gamestate, player)

        # Generate one-hot encoded tensor to represent the gamestate
        gamestate_tensor = prepare_input(gamestate, player)
        player_history[gamestate.players_to_int[player], turns[player]-1, :] = gamestate_tensor

        # Discard tile
        discard_idx = random.randint(0, len(gamestate.players[player])-1)
        discard_tile = gamestate.players[player][discard_idx]
        gamestate.add_tile_to_discard_pool(discard_tile)
        gamestate.remove_tile_from_hand(discard_tile, player)

        # Check to see if player won
        if score != 0:
            break
    
    if score != 0:
        winner_history = player_history[gamestate.players_to_int[player], 0:turns[player], :]
        save_winner_data(conn, game_id, winner_history, player, score)
        game_id += 1
        print(f"$$$ WINNER $$$")

    count += 1

global_end_time = time.time()
global_elapsed_time += global_end_time - global_start_time
print(f"Total elapsed time: {global_elapsed_time:.2f} s")

# Close database
conn.close()