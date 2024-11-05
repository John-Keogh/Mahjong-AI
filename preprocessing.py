import numpy as np
from tile import Tile
import torch
from gamestate import GameState

import logging
from logging.handlers import RotatingFileHandler

# Set up a dedicated logger for tile_utils
logger = logging.getLogger("preprocessing_logger")
logger.setLevel(logging.ERROR)  # Set logging level

# Define handler with rotation settings
handler = RotatingFileHandler('preprocessing_logging.log', maxBytes=10*1024*1024, backupCount=5)
handler.setLevel(logging.ERROR)  # Set logging level for this handler

# Set log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)

def encode_tile(gamestate: GameState, tile: Tile) -> np.ndarray:
    '''
    Encode a tile with one-hot encoding

    Args:
    tile: object of Tile class with suit and rank

    Returns:
    tile_encoding: a numpy vector of 19 zeros/ones to represent the tile suit and rank
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
    input_tensor: a PyTorch tensor representing all information available to player
    '''
    # 1) Tiles in player's hand
    tiles_in_hand_tensor = encode_tile_batch(gamestate, gamestate.players[player])
    logger.debug(f"tiles_in_hand_tensor = \n{tiles_in_hand_tensor}")

    # 2) Tiles in discard pool
    logger.debug(f"tiles in discard pool: {gamestate.discard_pool}")
    if len(gamestate.discard_pool) == 0:
        tiles_in_discard_pool_tensor = torch.empty(0)
    elif len(gamestate.discard_pool) == 1:
        tile_in_discard_pool_encoded = encode_tile(gamestate, gamestate.discard_pool[0])
        tiles_in_discard_pool_tensor = torch.from_numpy(tile_in_discard_pool_encoded).float()
    else:
        tiles_in_discard_pool_tensor = encode_tile_batch(gamestate, gamestate.discard_pool)
    logger.debug(f"tiles_in_discard_pool_tensor = \n{tiles_in_discard_pool_tensor}")

    # 3) Tiles in draw pool (one-hot encoding of all zeros)
    num_tiles_not_in_hand = 136 - 14 - 3*13 # 136 total tiles, 14 in player's hand, 13 in all other players' hands
    num_tiles_in_draw_pool = num_tiles_not_in_hand - len(gamestate.discard_pool)
    tiles_in_draw_pool_tensor = torch.zeros(num_tiles_in_draw_pool * 19) # 19 one-hot values per tile
    logger.debug(f"tiles_in_draw_pool_tensor = \n{tiles_in_draw_pool_tensor}")

    # 4) Macro game direction
    macro_direction_tensor = encode_macro_direction(gamestate)
    logger.debug(f"macro_direction_tensor = \n{macro_direction_tensor}")

    # 5) Micro game direction
    micro_direction_tensor = encode_micro_direction(gamestate)
    logger.debug(f"micro_direction_tensor = \n{micro_direction_tensor}")

    input_tensor = torch.hstack((tiles_in_hand_tensor, tiles_in_discard_pool_tensor, tiles_in_draw_pool_tensor, macro_direction_tensor, micro_direction_tensor))

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
            if gamestate_tensor[i + 19*k] == 1:
                suit = gamestate.idx_to_suit[i]
        
        rank = None
        for j in range(10, 19):
            if gamestate_tensor[j + 19*k] == 1:
                rank = gamestate.idx_to_rank[j-10]
                
        tile = Tile(suit, rank)
        player_hand.append(tile)

    return player_hand