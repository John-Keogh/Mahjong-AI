## FOR DISCARDING TILES - ASSUMES PLAYER HAS 14 CARDS IN HAND ##

import gymnasium as gym
from gymnasium import spaces
import numpy as np
from gamestate import GameState
from preprocessing import prepare_input
from tile_utils import compute_score, is_winning_hand, is_set, is_run
import random
import copy
import itertools
from tile import Tile

import os
import logging
from logging.handlers import RotatingFileHandler

# Logging
logger = logging.getLogger("gamestate_env_logger")
logger.setLevel(logging.DEBUG)

log_file_path = "logs/gamestate_env_logger.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Clear the logs before each execution
open("logs/gamestate_env_logger.log", "w").close()

logger.info("Starting gamestate_env logging.")

class MahjongEnv(gym.Env):
    def __init__(self):
        super().__init__()  # run the standard Gym environment setup

        self.state = GameState()
        self.player = 'player1'
        self.max_turns = 200

        # each observation will be a fixed-length binary vector
        self.observation_space = spaces.MultiBinary(self._obs_length())

        # the agent can choose from a fixed number of discrete actions
        self.action_space = spaces.Discrete(self._num_actions())

    def reset(self, seed=None, options=None):
        logger.debug("="*40)
        logger.debug("NEW GAME - Executing function: 'reset'")
        logger.debug("="*40 + "\n")

        super().reset(seed=seed)

        self.state = GameState()
        self.state.initialize_draw_pool()
        self.state.deal_tiles()
        self.player = 'player1'
        self.turn_count = 0

        observation = self._get_obs()
        info = {}
        return observation, info
    
    def step(self, action):
        logger.debug(f"Executing function: 'step'")
        logger.debug(f"Turn count: {self.turn_count}.")
        logger.debug(f"{self.player}'s hand: {self.state.players[self.player]}")
        if len(self.state.players[self.player]) != 14:
            logger.error(f"Length of {self.player}'s hand is {len(self.state.players[self.player])}. Should be 14.")
        else:
            logger.debug(f"Action: discard tile in index {action} ({self.state.players[self.player][action]}).")

        info = {}

        # Set player to 'player1'
        player = self.player

        # Compute reward using action
        reward, info = self._compute_reward(action, player, info)
        observation = self._get_obs()

        # Apply action
        discarded_tile = self.state.players[player][action]
        self.state.remove_tile_from_hand(discarded_tile, player)
        self.state.add_tile_to_discard_pool(discarded_tile)

        # Determine if episode is finished
        terminated = False  # True if game is won
        truncated = False   # True if ended early by other rule/timer

        # Cycle over other players - draw from top of draw pool and discard randomly
        for player in ['player2', 'player3', 'player4']:
            if len(self.state.draw_pool) == 0:
                logger.debug(f"Draw pool is empty. Exiting player loop and setting 'terminated' to True.")
                terminated = True
                break            
            draw_tile = self.state.draw_pool[0]
            self.state.add_tile_to_hand(draw_tile, player)
            self.state.remove_tile_from_draw_pool(draw_tile)
            is_winning, _ = is_winning_hand(self.state, player)
            if is_winning:
                logger.debug(f"{player} won. Exiting player loop and setting 'terminated' to True.")
                terminated = True
                break
            random.shuffle(self.state.players[player])
            discard_tile = self.state.players[player][0]
            self.state.remove_tile_from_hand(discard_tile, player)
            self.state.add_tile_to_discard_pool(discard_tile)

        if len(self.state.draw_pool) == 0:
            logger.debug(f"Draw pool is empty.")
            terminated = True
        
        if not terminated:
            player = self.player
            draw_tile = self.state.draw_pool[0]
            self.state.add_tile_to_hand(draw_tile, player)
            self.state.remove_tile_from_draw_pool(draw_tile)
            is_winning, _ = is_winning_hand(self.state, player)
            if len(self.state.draw_pool) == 0:
                logger.debug(f"Draw pool is empty after {player} drew. Setting 'terminated' to True.")
                terminated = True
            elif is_winning:
                logger.debug(f"{player} won. Setting 'terminated' to True.")
                terminated = True

        self.turn_count += 1
        if self.turn_count >= self.max_turns:
            truncated = True
            terminated = True

        logger.debug(f"Reward: {reward}.")
        logger.debug(f"terminated: {terminated}.")
        logger.debug(f"truncated: {truncated}.\n")

        return observation, reward, terminated, truncated, info
    
    def render(self):
        temp_hand = copy.deepcopy(self.state.players[self.player])
        sorted_temp_hand = sorted(temp_hand, key=lambda tile: (tile.suit, tile.rank))
        print(f"\n--- {self.player}'s hand ---")
        # self.state.print_player_hand(self.player)
        for tile in sorted_temp_hand:
            tile.display()

    def close(self):
        pass        

    def _get_obs(self):
        # One-hot encode GameState into a fixed-size vector
        observation_tensor = prepare_input(self.state, self.player)
        observation = observation_tensor.numpy().astype(np.int8) # Convert to Numpy array from PyTorch tensor
        return observation
    
    def _obs_length(self):
        # Tiles in player's hand: 14*19 = 266
        # Tiles in the draw/discard pool: (136 - 14 - 3*13)*19 = 1577
        # Macro game direction: 4
        # Micro game direction: 4
        # 266 + 1577 + 4 + 4 = 1851
        return 1851
    
    def _num_actions(self):
        # 14 (tiles in player's hand to discard)
        return 14
    
    def _compute_reward(self, action, player, info):
        discard_tile = self.state.players[player][action]
        discard_suit = discard_tile.suit
        discard_rank = discard_tile.rank
        
        reward = 0.0

        hand_14 = copy.deepcopy(self.state.players[player])
        hand_13 = copy.deepcopy(hand_14)
        hand_13.pop(action)

        # count number of sets/runs before discarding
        groups = list(itertools.combinations(hand_14, 3))
        valid_sets_14 = 0
        valid_runs_14 = 0
        for group in groups:
            if is_set(group[0], group[1], group[2]):
                valid_sets_14 += 1
            elif is_run(group[0], group[1], group[2]):
                valid_runs_14 += 1

        # count number of sets/runs after discarding
        groups = list(itertools.combinations(hand_13, 3))
        valid_sets_13 = 0
        valid_runs_13 = 0
        for group in groups:
            if is_set(group[0], group[1], group[2]):
                valid_sets_13 += 1
            elif is_run(group[0], group[1], group[2]):
                valid_runs_13 += 1
        
        # penalize for breaking up a set/run
        if valid_sets_14 > valid_sets_13:
            reward -= 1.0
        elif valid_runs_14 > valid_runs_13:
            reward -= 1.0
        
        # colors - reward if unlikely/impossible to complete a color set
        color_1_count_reward = 0.5
        color_2plus_count_reward = 1.0

        if discard_suit == 'red':
            discard_count_red = sum(tile.suit == "red" for tile in self.state.discard_pool)
            if discard_count_red == 1:
                reward += color_1_count_reward
            elif discard_count_red >= 2:
                reward += color_2plus_count_reward
        elif discard_suit == 'green':
            discard_count_green = sum(tile.suit == "green" for tile in self.state.discard_pool)
            if discard_count_green == 1:
                reward += color_1_count_reward
            elif discard_count_green >= 2:
                reward += color_2plus_count_reward
        elif discard_suit == 'white':
            discard_count_white = sum(tile.suit == "white" for tile in self.state.discard_pool)
            if discard_count_white == 1:
                reward += color_1_count_reward
            elif discard_count_white >= 2:
                reward += color_2plus_count_reward

        # directions - reward if unlikely/impossible to complete a direction set
        macro_direction = self.state.macro_direction
        micro_direction = self.state.micro_direction

        macro_1_count_reward = 0.5
        macro_2plus_count_reward = 1.0

        micro_1_count_reward = 0.5
        micro_2plus_count_reward = 1.0

        if discard_suit == macro_direction:
            discard_count_macro_direction = sum(tile.suit == macro_direction for tile in self.state.discard_pool)
            if discard_count_macro_direction == 1:
                reward += macro_1_count_reward
            elif discard_count_macro_direction >= 2:
                reward += macro_2plus_count_reward
        elif discard_suit == micro_direction:
            discard_count_micro_direction = sum(tile.suit == micro_direction for tile in self.state.discard_pool)
            if discard_count_micro_direction == 1:
                reward += micro_1_count_reward
            elif discard_count_micro_direction >= 2:
                reward += micro_2plus_count_reward

        # potential sets: penalize for discarding if you already have another copy of the same tile
        same_tile_count = sum(tile.suit == discard_suit and tile.rank == discard_rank for tile in hand_13)
        if same_tile_count > 0:
            reward -= 0.5

        # boundary tiles: penalize 1 and 9 tiles since they're less flexible for making runs
        if discard_rank == 1 or discard_rank == 9:
            reward -= 0.1

        # potential runs: penalize for discarding if you have nearby tiles of the same rank

        info = {}
        return reward, info
