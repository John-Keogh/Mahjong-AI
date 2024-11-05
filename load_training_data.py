from training_data_utils import load_winner_history, load_and_inspect_winner_data
from preprocessing import decode_hand
import os
import sqlite3
from gamestate import GameState

# Define the database path
db_folder = "G:\\VS Code\\Mahjong_Data"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "mahjong_eval_net_training_data.db")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

game_id = 2

load_and_inspect_winner_data(conn, game_id)

winner_history = load_winner_history(conn, game_id)
# print(winner_history[-1])
gamestate_tensor = winner_history[-1][3]
# print(gamestate_tensor)

gamestate = GameState()
player_hand = decode_hand(gamestate, gamestate_tensor)
print(f"player_hand = \n{player_hand}")

