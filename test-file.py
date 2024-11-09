from training_data_utils import load_training_data, load_winner_history, get_last_game_id
import os
import sqlite3
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn as nn
from evaluation_network import EvaluationNet
from preprocessing import decode_hand, encode_tile, prepare_input
from gamestate import GameState
from tile import Tile


# Suppress warning regarding using `weights_only=False` in `torch.load`
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the database path
db_folder = "G:\\VS Code\\Mahjong_Data"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "mahjong_eval_net_training_data.db")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

game_id = get_last_game_id(conn)
print(f"Last game ID: {game_id}")

# data, targets = load_training_data(conn, decay=0.95)

# # Create data loader
# dataset = TensorDataset(data, targets)
# train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

# # Initialize model, optimizer, and loss function
# model_save_path = "G:\\VS Code\\Mahjong AI\\Evaluation_Network.pth"
# model = EvaluationNet()

# optimizer = optim.Adam(model.parameters(), lr=0.001)
# criterion = nn.MSELoss()

# # Check for GPU and set device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Move model to device
# model = model.to(device)

# if os.path.exists(model_save_path):
#     # Loading the model and optimizer state
#     checkpoint = torch.load(model_save_path)
#     model.load_state_dict(checkpoint['model_state_dict'])
#     optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
#     start_epoch = checkpoint['epoch'] + 1  # To continue from the last saved epoch
#     print(f"Evaluation Model loaded successfully.")
# else:
#     start_epoch = 0
#     print("No saved model found. Initializing new Evaluation Model.")

# # Set model to evaluation mode
# model.eval()

# # Generate a test hand
# player = 'player1'
# gamestate = GameState()

# manual_tiles = [
#     Tile('stick', 2),
#     Tile('stick', 2),
#     Tile('stick', 2),
#     Tile('circle', 1),
#     Tile('circle', 1),
#     Tile('circle', 1),
#     Tile('stick', 8),
#     Tile('stick', 8),
#     Tile('stick', 8),
#     Tile('stick', 9),
#     Tile('stick', 9),
#     Tile('stick', 9),
#     Tile('circle', 4),
#     Tile('circle', 4)
# ]

# for tile in manual_tiles:
#     gamestate.add_tile_to_hand(tile, player)

# gamestate_tensor = prepare_input(gamestate, player)
# player_hand = decode_hand(gamestate, gamestate_tensor)
# print(f"player_hand = \n{player_hand}")

# gamestate_tensor = gamestate_tensor.to(device)

# # Make prediction
# with torch.no_grad():
#     predicted_value = model(gamestate_tensor)

# predicted_hand_value = predicted_value.item() # convert from tensor to scalar value
# print(f"Predicted hand vlue: {predicted_hand_value:.2f}")