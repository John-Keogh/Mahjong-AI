import numpy as np
from tile import Tile
import torch
from gamestate import GameState

import logging
from logging.handlers import RotatingFileHandler
import os

# Logging
logger = logging.getLogger("preprocessing_logger")
logger.setLevel(logging.INFO)

log_file_path = "logs/preprocessing_logging.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

TILE_ENCODING_LEN = 19

def encode_tile(gamestate: GameState, tile: Tile) -> np.ndarray:
    '''
    Encode a tile with one-hot encoding

    Args:
    tile: object of Tile class with suit and rank

    Returns:
    tile_encoding: a numpy vector of 19 zeros/ones to represent the tile suit and rank
        10 suits: 'stick', 'circle', '10k', 'red', 'green', 'white', 'east', 'south', 'west', 'north'
        9 ranks: 1, 2, 3, 4, 5, 6, 7, 8, 9
    '''
    if tile.suit not in gamestate.suits:
        raise ValueError(f"Invalid tile suit: {tile.suit}")
    
    if tile.rank not in gamestate.ranks and tile.rank is not None:
        raise ValueError(f"Invalid tile rank: {tile.rank}")

    suit_vector = np.zeros(len(gamestate.suits))  # 10 total suits
    rank_vector = np.zeros(len(gamestate.ranks))   # 9 total ranks
    
    suit_vector[gamestate.suit_to_idx[tile.suit]] = 1

    if tile.rank is not None:
        rank_vector[gamestate.rank_to_idx[tile.rank]] = 1

    tile_encoding = np.concatenate([suit_vector, rank_vector])
    return tile_encoding

def encode_tile_batch(gamestate: GameState, tiles: list[Tile]):
    '''
    Encode a batch of tiles with one-hot encoding

    Args:
    tiles: list of Tile class objects

    Returns:
    tile_encodings_tensor: a PyTorch tensor where each row is the encoding of a tile
    '''
    tile_encodings = np.array([encode_tile(gamestate, tile) for tile in tiles])
    tile_encodings_tensor = torch.from_numpy(tile_encodings).float()
    tile_encodings_tensor = torch.flatten(tile_encodings_tensor)
    return tile_encodings_tensor

def encode_macro_direction(gamestate: GameState):
    '''
    Encode the macro game direction with one-hot encoding

    Args:
    gamestate: object of GameState class

    Returns:
    macro_direction_encoding: a PyTorch tensor of 4 zeros/ones to represent the macro game direction
    '''
    macro_direction_encoding = np.zeros(4)
    macro_direction = gamestate.macro_direction[0]

    macro_direction_encoding[gamestate.macro_direction_to_idx[macro_direction]] = 1
    macro_direction_tensor = torch.from_numpy(macro_direction_encoding).float()
    return macro_direction_tensor

def encode_micro_direction(gamestate: GameState):
    '''
    Encode the micro game direction with one-hot encoding

    Args:
    gamestate: object of GameState class

    Returns:
    macro_direction_encoding: a numpy vector of 4 zeros/ones to represent the micro game direction
    '''
    micro_direction_encoding = np.zeros(4)
    micro_direction = gamestate.micro_direction[0]

    micro_direction_encoding[gamestate.micro_direction_to_idx[micro_direction]] = 1
    micro_direction_tensor = torch.from_numpy(micro_direction_encoding).float()
    return micro_direction_tensor


def prepare_input(gamestate: GameState, player: str):
    '''
    Compiles the following information to prepare for network input:
    1) Tiles in player's hand
    2) Tiles in the discard pool
    3) Tiles in the draw pool
    4) Macro game direction
    5) Micro game direction

    Args:
    gamestate: object of GameState class
    player: 'player1', 'player2', etc.

    Returns:
    input_tensor: a PyTorch tensor with 2839 elements representing all information available to player
        Tiles in player's hand: 14*19 = 266
        Tiles in the draw/discard pool: (136 - 14 - 3*13)*19 = 1577
        Macro game direction: 4
        Micro game direction: 4
        266 + 1577 + 4 + 4 = 1851
    '''
    logger.debug(f"player: {player}")

    # 1) Tiles in player's hand
    tiles_in_hand_tensor = encode_tile_batch(gamestate, gamestate.players[player])
    logger.debug(f"tiles_in_hand_tensor = \n{tiles_in_hand_tensor}")
    logger.debug(f"size of tiles_in_hand_tensor: {tiles_in_hand_tensor.numel()}")

    # 2) Tiles in discard pool
    if len(gamestate.discard_pool) == 0:
        tiles_in_discard_pool_tensor = torch.empty(0)
    elif len(gamestate.discard_pool) == 1:
        tile_in_discard_pool_encoded = encode_tile(gamestate, gamestate.discard_pool[0])
        tiles_in_discard_pool_tensor = torch.from_numpy(tile_in_discard_pool_encoded).float()
    else:
        tiles_in_discard_pool_tensor = encode_tile_batch(gamestate, gamestate.discard_pool)
    logger.debug(f"tiles_in_discard_pool_tensor = \n{tiles_in_discard_pool_tensor}")
    logger.debug(f"size of tiles_in_discard_pool_tensor: {tiles_in_discard_pool_tensor.numel()}")

    # 3) Tiles in draw pool (one-hot encoding of all zeros)
    tiles_in_draw_pool_tensor = torch.zeros(len(gamestate.draw_pool) * TILE_ENCODING_LEN) # zeros because unrevealed
    logger.debug(f"tiles_in_draw_pool_tensor = \n{tiles_in_draw_pool_tensor}")
    logger.debug(f"size of tiles_in_draw_pool_tensor: {tiles_in_draw_pool_tensor.numel()}")

    # 4) Macro game direction
    macro_direction_tensor = encode_macro_direction(gamestate)
    logger.debug(f"macro_direction_tensor = \n{macro_direction_tensor}")
    logger.debug(f"size of macro_direction_tensor: {macro_direction_tensor.numel()}")

    # 5) Micro game direction
    micro_direction_tensor = encode_micro_direction(gamestate)
    logger.debug(f"micro_direction_tensor = \n{micro_direction_tensor}")
    logger.debug(f"size of micro_direction_tensor: {micro_direction_tensor.numel()}")


    input_tensor = torch.hstack((tiles_in_hand_tensor, tiles_in_discard_pool_tensor, tiles_in_draw_pool_tensor, macro_direction_tensor, micro_direction_tensor))
    logger.debug(f"size of input_tensor: {input_tensor.numel()}")

    return input_tensor

def decode_hand(gamestate: GameState, gamestate_tensor) -> list[Tile]:
    '''
    Decode a player's hand with one-hot decoding

    Args:
    gamestate_tensor: PyTorch Tensor that represents the entire state of the game
        Note that only the first 19 * 14 entries represent the player's hand

    Returns:
    player_hand: A list of objects of the Tile class
    '''
    player_hand = []
    for k in range(14):
        for i in range(0, 10):
            if gamestate_tensor[i + TILE_ENCODING_LEN*k] == 1:
                suit = gamestate.idx_to_suit[i]
        
        rank = None
        for j in range(10, TILE_ENCODING_LEN):
            if gamestate_tensor[j + TILE_ENCODING_LEN*k] == 1:
                rank = gamestate.idx_to_rank[j-10]
                
        tile = Tile(suit, rank)
        player_hand.append(tile)

    return player_hand