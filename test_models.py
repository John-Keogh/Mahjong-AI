from tile_utils import compute_score
from gamestate import GameState
import time
import os

import logging
from logging.handlers import RotatingFileHandler

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor

from gamestate_env import MahjongEnv


# === Logging Setup ===
logger = logging.getLogger("test_models_logger")
logger.setLevel(logging.INFO)

log_file_path = "logs/test_models_logging.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

logger.info("=== Starting Model Test ===")

def load_model(model_name: str):
    model_path = f"models/{model_name}.zip"
    log_dir = f"logs/{model_name}"
    vec_monitor_path = os.path.join(log_dir, "vec_monitor.csv")  # optional

    # Rebuild environment
    env = DummyVecEnv([lambda: MahjongEnv()])
    env = VecMonitor(env, filename=vec_monitor_path)

    # Load model with environment
    model = PPO.load(model_path, env=env, device="cpu")
    return model, env

# Setup player models
# Player 1
player1_model_name = "discard_model_v1"
player1_model, player1_env = load_model(player1_model_name)

# Player 2
player2_model_name = "discard_model_v0"
player2_model, player2_env = load_model(player2_model_name)

# Player 3
player3_model_name = "discard_model_v0"
player3_model, player3_env = load_model(player3_model_name)

# Player 4
player4_model_name = "discard_model_v0"
player4_model, player4_env = load_model(player4_model_name)

# Initialize
num_games = 1_000
win_tracker = {'player1': 0,
               'player2': 0,
               'player3': 0,
               'player4': 0}

def player_turn(player: str):
        gamestate.add_tile_to_hand(gamestate.draw_pool[0], player)
        gamestate.remove_tile_from_draw_pool(gamestate.draw_pool[0])

for _ in range(num_games):
    gamestate = GameState()
    gamestate.initialize_draw_pool()
    gamestate.deal_tiles()

    